#！usr/bin python3

import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy

import os, sys, math
import numpy as np

import threading


sys.path.append('/home/ubuntu/pangolin_ws/ros2-pangolin-robot/pangolin_control/driver')
# sys.path.append('/home/puppypi/puppypi_ws/src/puppy_control/driver')
from Pangolin_ControlCmd_1 import Pangolincontrol_old
from Pangolin_ControlCmd import PangolinControl


class Pangolin(Node):
    def __init__(self):
        super().__init__('pangolin_control')
        self.control_cmd_old = Pangolincontrol_old()
        self.control_cmd = PangolinControl()

        self.joy_subscriber_ = self.create_subscription(Joy, 'joy', self.joy_callback, 0)
        self.cmd_vel_subscriber_ = self.create_subscription(Twist, 'cmd_vel', self.cmd_vel_callback, 1)

        self.is_first_time = True
        self.is_disalbe_motor = True
        self.last_joy_msgs_buttons = []

# destroy ros    
    def destroy(self):
        self.cmd_vel_subscriber_.destroy()
        super().destroy_node()
    

    def joy_callback(self, msg):
        # last_joy_msgs_buttons = []
        if self.is_first_time == True:
            self.last_joy_msgs_buttons = msg.buttons
            self.is_first_time = False
        # print(last_joy_msgs_buttons)
        # self.get_logger().info('last_joy_msgs_buttons: %s' % self.last_joy_msgs_buttons)
        if msg.buttons[0] != self.last_joy_msgs_buttons[0]:
            
            # self.control_cmd_old.startCurl() #for test
            self.control_cmd.run_action_curl()

        if msg.buttons[1] != self.last_joy_msgs_buttons[1]:
            self.control_cmd.reset_to_orginal()

        # self.get_logger().info(f'button3: {msg.buttons[3]}, last_button: {self.last_joy_msgs_buttons[3]}')

        if msg.buttons[2] != self.last_joy_msgs_buttons[2]:
            self.control_cmd.run_action_get_down()

        if msg.buttons[3] != self.last_joy_msgs_buttons[3]:
            self.control_cmd.run_action_stand_up()
            


            # if self.control_cmd.is_recording == False:
            #     self.control_cmd.start_record_action_points()
            # else:
            #     self.control_cmd.stop_record_action_points()


        if msg.buttons[4] != self.last_joy_msgs_buttons[4]:
            self.control_cmd.controlcmd.start_recording()

        if msg.buttons[5] != self.last_joy_msgs_buttons[5]:
            self.control_cmd.controlcmd.stop_record_action_points()
            self.get_logger().info('last_joy_msgs_buttons: %s' % self.last_joy_msgs_buttons)

        if msg.buttons[8] != self.last_joy_msgs_buttons[8]:
            if self.is_disalbe_motor == True:
                self.control_cmd_old.openPort()
                self.control_cmd_old.enableMotor()
                self.is_disalbe_motor = False
            
            else:
                self.control_cmd_old.disableMotor()
                self.is_disalbe_motor = True

        # self.control_cmd.control_cmd.leg_motor_position_control(position = {"motor1":int(msg.axes[0]*1000 + 1423), "motor2":int(msg.axes[1]*1000 + 2672), "motor3":0, 
        #                                                                     "motor4":int(msg.axes[2]*1000 + 2672), "motor5":int(msg.axes[3]*1000 + 1423)})
        
        # if msg.buttons[0] == 1 and self.control_cmd.is_curling == False:
        #     self.control_cmd.is_curling = True
        #     self.control_cmd.startCurl()
        # else:
        #     self.control_cmd.is_curling = False
            
        # if msg.buttons[1] == 1:
        #     self.control_cmd.is_curling = False
        # self.get_logger().info('vel callback: %s' % round(msg.linear.x, 0))
        # else:
        #     self.control_cmd.startGait()

        self.last_joy_msgs_buttons = msg.buttons

# puppy cmd vel callback
    def cmd_vel_callback(self, msg):

        self.get_logger().info(f'linear.x: {msg.linear.x} angular.z: {msg.angular.z}')

        self.control_cmd.set_servo_rate([msg.linear.x - msg.angular.z, msg.linear.x + msg.angular.z])

        if round(msg.linear.x, 0) != 0 or round(msg.angular.z, 0) != 0:
            if self.control_cmd.is_walking == False:
                self.control_cmd.start_gait()

        else:
            if self.control_cmd.is_walking == True:
                self.control_cmd.stop_gait()


def main(args=None):
    rclpy.init(args=args)
    PangolinControl = Pangolin()

    rclpy.spin(PangolinControl)
    
    PangolinControl.destroy()
    rclpy.shutdown()


if __name__ == '__main__':
    main()