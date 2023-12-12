from DXL_motor_control import DXL_Conmunication
import time
import sys, tty, termios
import traceback
import json 
import threading
import log
from Pangolin_ActionGroups import action_dic

# main control command
DEVICE_NAME = "/dev/ttyUSB0"
B_RATE      = 57600
LED_ADDR_LEN = (65,1)
LED_ON = 1
LED_OFF = 0
x = 200
y = 300

class PangolinControl:
    def __init__(self, log_level="info", log_file_level="debug"):
        self.control_cmd = ControlCmd()

        self.log_level = log_level
        self.log_file_level = log_file_level
        self.log = log.LogHandler(self.__class__.__name__, __name__, self.log_level, self.log_file_level)

        self.motor_center_position = {"motor1":1423, "motor2":2672, "motor3": 1023, "motor4":2672, "motor5":1423}
        self.control_cmd.leg_motor_position_control(position = {"motor1":self.motor_center_position["motor1"]    ,"motor2":self.motor_center_position["motor2"]      , "motor3":self.motor_center_position["motor3"], "motor4":self.motor_center_position["motor4"]     , "motor5":self.motor_center_position["motor5"]     })
        
        self.init_fail = False
        self.is_walking = False
        self.servo_rate = [1.0, 1.0]

        self.is_led_blink = True
        self.is_recording = False
        self.record_path = '/home/ubuntu/pangolin_ws/ros2-pangolin-robot/pangolin_control/driver/output.txt'

    # Reset to the original state
    def reset_to_orginal(self):    
        self.control_cmd.leg_motor_position_control(position = {
            "motor1":self.motor_center_position["motor1"], 
            "motor2":self.motor_center_position["motor2"], 
            "motor3":self.motor_center_position["motor3"], 
            "motor4":self.motor_center_position["motor4"], 
            "motor5":self.motor_center_position["motor5"]
            }
        )

    # Pangolin move gait process
    def process_gait(self):
        while self.is_walking:
            self.control_cmd.leg_motor_position_control(position = {"motor1":int( x * self.servo_rate[0]+self.motor_center_position["motor1"]), "motor2":int( y * self.servo_rate[1]+self.motor_center_position["motor2"]) , "motor3":int(self.motor_center_position["motor3"]), "motor4":int(-y * self.servo_rate[0]+self.motor_center_position["motor4"]) , "motor5":int(-x * self.servo_rate[1]+self.motor_center_position["motor5"]) })
            self.control_cmd.leg_motor_position_control(position = {"motor1":int( x * self.servo_rate[0]+self.motor_center_position["motor1"]), "motor2":int(     self.servo_rate[1]+self.motor_center_position["motor2"]) , "motor3":int(self.motor_center_position["motor3"]), "motor4":int(     self.servo_rate[0]+self.motor_center_position["motor4"]) , "motor5":int(-x * self.servo_rate[1]+self.motor_center_position["motor5"]) })
            self.control_cmd.leg_motor_position_control(position = {"motor1":int(-y * self.servo_rate[0]+self.motor_center_position["motor1"]), "motor2":int(     self.servo_rate[1]+self.motor_center_position["motor2"]) , "motor3":int(self.motor_center_position["motor3"]), "motor4":int(     self.servo_rate[0]+self.motor_center_position["motor4"]) , "motor5":int( y * self.servo_rate[1]+self.motor_center_position["motor5"]) })
            self.control_cmd.leg_motor_position_control(position = {"motor1":int(-y * self.servo_rate[0]+self.motor_center_position["motor1"]), "motor2":int(-x * self.servo_rate[1]+self.motor_center_position["motor2"]) , "motor3":int(self.motor_center_position["motor3"]), "motor4":int( x * self.servo_rate[0]+self.motor_center_position["motor4"]) , "motor5":int( y * self.servo_rate[1]+self.motor_center_position["motor5"]) })
            self.control_cmd.leg_motor_position_control(position = {"motor1":int(     self.servo_rate[0]+self.motor_center_position["motor1"]), "motor2":int(-x * self.servo_rate[1]+self.motor_center_position["motor2"]) , "motor3":int(self.motor_center_position["motor3"]), "motor4":int( x * self.servo_rate[0]+self.motor_center_position["motor4"]) , "motor5":int(     self.servo_rate[1]+self.motor_center_position["motor5"]) })
            self.control_cmd.leg_motor_position_control(position = {"motor1":int(     self.servo_rate[0]+self.motor_center_position["motor1"]), "motor2":int( y * self.servo_rate[1]+self.motor_center_position["motor2"]) , "motor3":int(self.motor_center_position["motor3"]), "motor4":int(-y * self.servo_rate[0]+self.motor_center_position["motor4"]) , "motor5":int(     self.servo_rate[1]+self.motor_center_position["motor5"]) })

    # Start moving 
    def start_gait(self):
        self.is_walking = True
        self.walking_thread = threading.Thread(target=self.process_gait, args=(), daemon=True)
        self.walking_thread.start()

    # Stop moving 
    def stop_gait(self):
        self.is_walking = False
        self.reset_to_orginal()

    # Set the twist msg to left and right side of the motors
    def set_servo_rate(self, servo_rate=[1.0, 1.0]):
        self.servo_rate = servo_rate

    # The process of the recording function
    def process_record_action_points(self):
        self.control_cmd.disable_all_motor()
        print("disabling")
        self.control_cmd.dynamixel.rebootAllMotor()
        print("rebooting")
        self.control_cmd.motor_led_control(LED_ON)
        
        with open(self.record_path, 'w') as f:
            print("start record the action points....")
            while self.is_recording:
                all_servo_position = self.control_cmd.read_all_motor_data()
                print(f"recording: {all_servo_position}")
                f.write(json.dumps(all_servo_position)+'\n')
                time.sleep(0.01)
            self.control_cmd.motor_led_control(LED_OFF)
        print("finish recording!")

    # Start recording the motors position
    def start_record_action_points(self):
        self.is_recording = True
        self.recording_thread = threading.Thread(target=self.process_record_action_points, args=(), daemon=True)
        self.recording_thread.start()

    # Stop recording
    def stop_record_action_points(self):
        self.is_recording = False


    # Replay the recording file
    def replay_recorded_data(self):
        self.control_cmd.enable_all_motor()
        with open(self.record_path) as f: 
            one_action_point = f.readline()
            while one_action_point:
                one_action_point = json.loads(one_action_point) 
                print(one_action_point)

                self.control_cmd.leg_motor_position_control(position = {"motor1":one_action_point["motor1"], "motor2":one_action_point["motor2"], "motor3":one_action_point["motor3"], 
                                                                        "motor4":one_action_point["motor4"], "motor5":one_action_point["motor5"]})
                # time.sleep(0.1)
                one_action_point = f.readline()
    
    # Run the action in Pangolin_ActionGroups.py
    def run_action_curl(self, action_name = 'start_curl'):
        action = action_dic[action_name]
        for i in range(len(action)):
            self.control_cmd.leg_motor_position_control(position = {"motor1":action[i]["motor1"], "motor2":action[i]["motor2"], "motor3":action[i]["motor3"], "motor4":action[i]["motor4"], "motor5":action[i]["motor5"]})
            print(i)
            time.sleep(1)

    def run_action_get_down(self, action_name = 'get_down'):
        action = action_dic[action_name]
        for i in range(len(action)):
            self.control_cmd.leg_motor_position_control(position = {"motor1":action[i]["motor1"], "motor2":action[i]["motor2"], "motor3":action[i]["motor3"], "motor4":action[i]["motor4"], "motor5":action[i]["motor5"]})
            print(i)
            time.sleep(0.1)

    def run_action_stand_up(self, action_name = 'stand_up'):
        action = action_dic[action_name]
        for i in range(len(action)):
            self.control_cmd.leg_motor_position_control(position = {"motor1":action[i]["motor1"], "motor2":action[i]["motor2"], "motor3":action[i]["motor3"], "motor4":action[i]["motor4"], "motor5":action[i]["motor5"]})
            print(i)
            time.sleep(1)

    # def motor_led_blink(self):
    #     while self.is_led_blink:
    #         self.control_cmd.motor_led_control(LED_ON)
    #         time.sleep(0.2)
    #         self.control_cmd.motor_led_control(LED_OFF)
    #         time.sleep(0.2)
    
    # def start_led_blink(self):
    #     self.is_led_blink = True
    #     self.led_blinking_thread = threading.Thread(target=self.motor_led_blink, args=(), daemon=True)
    #     self.led_blinking_thread.start()

    # def stop_led_blink(self):
    #     self.is_led_blink = False


class ControlCmd:
    def __init__(self):

        #Record path
        self.record_path = 'output.txt'

        #Coummunicate the dynamixel motors
        self.dynamixel = DXL_Conmunication(DEVICE_NAME, B_RATE)
        self.dynamixel.activateDXLConnection()

        #Create the dynamixel motors
        motor1 = self.dynamixel.createMotor('motor1', motor_number=1)
        motor2 = self.dynamixel.createMotor('motor2', motor_number=2)
        motor3 = self.dynamixel.createMotor('motor3', motor_number=3)
        motor4 = self.dynamixel.createMotor('motor4', motor_number=4)
        motor5 = self.dynamixel.createMotor('motor5', motor_number=5)

        #Create the leg motor list
        self.leg_motor_list = [motor1, motor2, motor4, motor5]

        #Create the curl motor
        self.curl_motor = motor3

        self.motor_position = {"motor1":0, "motor2":0, "motor3":0, "motor4":0, "motor5":0}
        
        #Reboot and update the state
        self.dynamixel.rebootAllMotor()
        self.dynamixel.updateMotorData()

        #Enalbe the motor torque
        self.enable_all_motor()

        #define the walk frequency
        self.walking_freq = 10

        #check list
        self.is_recording = False

        
    def enable_all_motor(self):
        for motor in self.leg_motor_list:
            motor.enableMotor()
        self.curl_motor.enableMotor()
        self.curl_motor.directWriteData(50, 112, 4)
            

    def disable_all_motor(self):
        for motor in self.leg_motor_list:
            motor.disableMotor()
        self.curl_motor.disableMotor()
        # self.dynamixel.closeHandler()
    
    # Read all the motors data
    def read_all_motor_data(self):
        self.dynamixel.updateMotorData()
        for motor in self.leg_motor_list:
            self.motor_position[motor.name] = motor.PRESENT_POSITION_value
        self.motor_position['motor3'] = self.curl_motor.PRESENT_POSITION_value

        print("motor_position", self.motor_position)
        return self.motor_position

    # Control led lights of all motors
    def motor_led_control(self, state = LED_ON):
        for motor in self.leg_motor_list:
            led_on = motor.directWriteData(state, *LED_ADDR_LEN)
        self.curl_motor.directWriteData(state, *LED_ADDR_LEN)
            
        return led_on
    
    
    # Control position of all motors
    def leg_motor_position_control(self, position = {"motor1":2000, "motor2":2000, "motor3":1025, "motor4":2000, "motor5":2000}):
        for motor in self.leg_motor_list:
            motor.writePosition(position[motor.name])
        self.curl_motor.writePosition(position["motor3"])
        self.dynamixel.sentAllCmd()
        time.sleep(1 / self.walking_freq)




if __name__ == "__main__":
    pangolin_control = PangolinControl()

    command_dict = {
        "enable":pangolin_control.control_cmd.enable_all_motor,
        "record":pangolin_control.start_record_action_points,
        "stop":pangolin_control.stop_record_action_points,
        "replay":pangolin_control.replay_recorded_data,
        "disable":pangolin_control.control_cmd.disable_all_motor,
        "read":pangolin_control.control_cmd.read_all_motor_data,
        "pos":pangolin_control.control_cmd.leg_motor_position_control,
        # "led":pangolin_control.start_led_blink,
        "run":pangolin_control.run_action_curl,
        "run1":pangolin_control.run_action_get_down,
        "run2":pangolin_control.run_action_stand_up,
        "reset":pangolin_control.reset_to_orginal,
    }


    while True:
        try:
            cmd = input("CMD : ")
            if cmd in command_dict:
                command_dict[cmd]()
            elif cmd == "exit":
                break
        except Exception as e:
            traceback.print_exc()
            break