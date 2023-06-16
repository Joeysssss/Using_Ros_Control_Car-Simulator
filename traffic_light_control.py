import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from time import sleep
import random
import Jetson.GPIO as GPIO

#Jetson Nano Pin
RED_LED_PIN = 18
YELLOW_LED_PIN = 23
GREEN_LED_PIN = 24

# Car speed
STOPPED_SPEED = 0.0
FORWARD_SPEED = 1.0
SLOW_SPEED = 0.5

def setup_leds():
    # Initialize GPIO pins
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RED_LED_PIN, GPIO.OUT)
    GPIO.setup(YELLOW_LED_PIN, GPIO.OUT)
    GPIO.setup(GREEN_LED_PIN, GPIO.OUT)
    GPIO.output(RED_LED_PIN, GPIO.LOW)
    GPIO.output(YELLOW_LED_PIN, GPIO.LOW)
    GPIO.output(GREEN_LED_PIN, GPIO.LOW)

def turn_on_led(led_pin):
    GPIO.output(led_pin, GPIO.HIGH)

def turn_off_led(led_pin):
    GPIO.output(led_pin, GPIO.LOW)

def traffic_light():
    # Initialize ROS node 
    rospy.init_node('traffic_light_node', anonymous=True)

    # Create Publisher for publish traffic_light
    light_pub = rospy.Publisher('/traffic_light', String, queue_size=10)

    # Create Publisher for publish Car Simulator
    cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

    lights = ['red', 'green', 'yellow']
    light_index = 0

    setup_leds()

    cmd_vel_msg = Twist()

    while not rospy.is_shutdown():
        light_pub.publish(lights[light_index])

        if lights[light_index] == 'red':
            rospy.loginfo('Red Light: Stop!')
            turn_on_led(RED_LED_PIN)  
            turn_off_led(YELLOW_LED_PIN)  
            turn_off_led(GREEN_LED_PIN)  
            cmd_vel_msg.linear.x = STOPPED_SPEED  
            cmd_vel_pub.publish(cmd_vel_msg)
            sleep(15)
        elif lights[light_index] == 'green':
            rospy.loginfo('Green Light: Go!')
            turn_off_led(RED_LED_PIN)  
            turn_off_led(YELLOW_LED_PIN)  
            turn_on_led(GREEN_LED_PIN) 
            start_time = rospy.Time.now()
            duration = rospy.Duration(20.0)     #Let Car keep running until the time is up
            while rospy.Time.now() - start_time < duration:
                cmd_vel_msg.linear.x = 0.3  
                cmd_vel_pub.publish(cmd_vel_msg)
                sleep(0.1)  
        elif lights[light_index] == 'yellow':
            rospy.loginfo('Yellow Light: Slow down!')
            turn_off_led(RED_LED_PIN)  
            turn_on_led(YELLOW_LED_PIN)  
            turn_off_led(GREEN_LED_PIN)  
            start_time = rospy.Time.now()
            duration = rospy.Duration(2.0)  
            while rospy.Time.now() - start_time < duration:
                cmd_vel_msg.linear.x = 0.1  
                cmd_vel_pub.publish(cmd_vel_msg)
                sleep(0.1)

        # Turn into a No_Light state with a probability of 0.01
        if random.random() < 0.01:
            rospy.loginfo('No Traffic Light: Slow down!')
            turn_on_led(YELLOW_LED_PIN)  
            turn_off_led(RED_LED_PIN)  
            turn_off_led(GREEN_LED_PIN)  
            light_pub.publish('none')
            cmd_vel_msg.linear.x = SLOW_SPEED  
            cmd_vel_pub.publish(cmd_vel_msg)
            sleep(1)
            light_index = (light_index + 1) % len(lights)
        else:
            light_index = (light_index + 1) % len(lights)

    GPIO.cleanup()

if __name__ == '__main__':
    try:
        traffic_light()
    except rospy.ROSInterruptException:
        pass
