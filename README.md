# ros2-pangolin-robot

## **Requirements**

- Python 3.10
- [ROS2 humble](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debians.html)

### RaspberryPI environment setup
- [GPIO root setup](https://forum.up-community.org/discussion/2141/solved-tutorial-gpio-i2c-spi-access-without-root-permissions)
```
$ mkdir pangolin_ws && cd pangolin_ws
```
```
$ git clone https://github.com/BruceLin90620/ros2-pangolin-robot.git
```
```
$ git checkout dev
```

- build: 
```
$ sudo apt install python3-pip
$ sudo pip3 install pigpio
$ sudo pip3 install RPi.GPIO
$ sudo pip3 install smbus2
```
```
$ pip3 install setuptools==58.2.0
```
```
$ colcon build --symlink-install
```
```
$ sudo apt install ros-humble-joy && sudo apt install ros-humble-teleop-twist-joy
``` 

- cd /home/user: 
```
$ git clone https://github.com/ROBOTIS-GIT/DynamixelSDK.git
```
- cd /DynamixlSDK/python: 
```
$ sudo python setup.py install
```


### Pangolin Start
```
$ ./start.sh
```
```
$ ros2 launch pangolin_bringup pangolin_bringup.launch.py
```

### test
```
$ ros2 run joy joy_node
$ ros2 topic echo /joy
```

### Control Button
* #### START: walk
* #### X: stance_mode
* #### A: reset
* #### B: get dowm & stand up
* #### Y: freedom_mode

### Record
* #### LB: start(first pressed) & stop(second pressed) record
* #### RB: repaly 

### Bug Fix

- [https://www.notion.so/ROS2-Joystick-Driver-Issue-ce55f7c88de34f2aa791ee9c2afc8dd5?pvs=4](https://www.notion.so/ROS2-Joystick-Driver-Issue-ce55f7c88de34f2aa791ee9c2afc8dd5?pvs=21)