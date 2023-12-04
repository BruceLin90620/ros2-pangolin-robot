#！usr/bin python3

import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy

import os, sys, math
import numpy as np

import threading


sys.path.append('/home/ubuntu/pangolin_robot_ws/ros2-pangolin-robot/pangolin_control/driver')
# sys.path.append('/home/puppypi/puppypi_ws/src/puppy_control/driver')
from Pangolin_ControlCmd import PangolinControl


class Pangolin(Node):
    def __init__(self):
        super().__init__('pangolin_control')
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
            
            self.control_cmd.startCurl()

        if msg.buttons[8] != self.last_joy_msgs_buttons[8]:
            if self.is_disalbe_motor == True:
                self.control_cmd.openPort()
                self.control_cmd.enableMotor()
                self.is_disalbe_motor = False
            
            else:
                self.control_cmd.disableMotor()
                self.is_disalbe_motor = True

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

        self.get_logger().info('vel callback: %s' % msg.angular.z)
        self.control_cmd.set_servo_rate([round(msg.linear.x), round(msg.angular.z)])

        if abs(msg.linear.x) >= abs(msg.angular.z):

            # self.get_logger().info('vel callback: %s' % round(msg.linear.x, 0))
            
            

            if np.sign(round(msg.linear.x, 0)) > 0:
                if self.control_cmd.is_walking == False:
                    self.control_cmd.startGait()
            elif np.sign(round(msg.linear.x, 0)) < 0:
                if self.control_cmd.is_walking == False:
                    self.control_cmd.startGait()
            else:
                if self.control_cmd.is_walking == True:
                    self.control_cmd.stopWalking()
        else:
            if np.sign(round(msg.angular.z, 0)) > 0:
                if self.control_cmd.is_walking == False:
                    self.control_cmd.startGait()
            elif np.sign(round(msg.angular.z, 0)) < 0:
                if self.control_cmd.is_walking == False:
                    self.control_cmd.startGait()
            else:
                if self.control_cmd.is_walking == True:
                    self.control_cmd.stopWalking()

        # self.control_cmd.startGait()

def main(args=None):
    rclpy.init(args=args)
    PangolinControl = Pangolin()

    rclpy.spin(PangolinControl)
    
    PangolinControl.destroy()
    rclpy.shutdown()


if __name__ == '__main__':
    main()