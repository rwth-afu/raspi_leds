#!/usr/bin/python2
from __future__ import print_function
from RPi import GPIO
import time

# the high temperature LEDs pin
HIGH_TEMP_LED_PIN = 23 
# seconds between checking the temperature
WAIT_TIME = 5 
# OW temp sensor devince file path
OW_SENSOR_PATH = "/sys/bus/w1/devices/28-0213195eb3aa/w1_slave"
# threshold for turning the LED on in deg C
TEMP_HIGH_THRESHOLD = 45

def get_temperature():
    """ get the temperature from the OW sensor """
    with open(OW_SENSOR_PATH, 'r') as f:
        lines = f.readlines()
        retval = lines[0].split(' ')
        retval = int(retval[1], 16)<<8 | int(retval[0], 16)
        retval /= 16.
        return retval
    raise Exception("Could not open OW sensor file")

def set_led(state):
    GPIO.output(HIGH_TEMP_LED_PIN, (GPIO.HIGH if state else GPIO.LOW))
    
if __name__ == "__main__":
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(HIGH_TEMP_LED_PIN, GPIO.OUT, initial=GPIO.LOW)

    err_blink_state = False

    print("started up..")

    while True:
        # get the temperature
        try:
            temp = get_temperature()
        except e:
            print("failed to get temperature")
            print(e)

            # blink LED if the temperature sensor does not work
            err_blink_state = not err_blink_state
            set_led(err_blink_state)
        else:
            # set the LED state
            set_led(temp>TEMP_HIGH_THRESHOLD)

            # print warning if the temperature is too high
            if temp>TEMP_HIGH_THRESHOLD:
                print("Temperature is too high: ", temp, " C")

        # wait
        time.sleep(WAIT_TIME)
