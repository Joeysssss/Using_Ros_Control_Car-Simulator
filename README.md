# Using_Ros_Control_Car-Simulator
**Device:** [Jetson Nano Developer Tool Kit 2GB](https://developer.nvidia.com/embedded/jetson-nano-developer-kit) <br>
## Launch Car simulator
```
roslaunch robot_description base_gazebo_control_xacro.launch
```
## Using code to  control Car & Traffic Light
**Code:** [traffic_light_control.py](https://github.com/Joeysssss/Using_Ros_Control_Car-Simulator/blob/main/traffic_light_control.py) <br>
1. Car Simulator
```
cmd_vel_msg.linear.x = FORWARD_SPEED   
cmd_vel_pub.publish(cmd_vel_msg)
```
2. Traffic light <br>
using GPIO to control traffic light <br>
```
import Jetson.GPIO as GPIO
```
```
def turn_on_led(led_pin):              # e.g.turn_on_led(RED_LED_PIN)
    GPIO.output(led_pin, GPIO.HIGH)
    
def turn_off_led(led_pin):             # e.g.turn_off_led(RED_LED_PIN)
    GPIO.output(led_pin, GPIO.LOW)
```
