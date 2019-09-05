#!/usr/bin/python2
from __future__ import print_function
from RPi import GPIO
import time, subprocess

# the high temperature LEDs pin
SW_RUNNING_LED_PIN = 24 
# seconds between checking the temperature
WAIT_TIME = 5 
# monitored service file
TARGET_SERVICE = "direwolf"

def get_service_state():
    """ check whether the targeted service is active """
    cmd = ["systemctl", "is-active", "--quiet", TARGET_SERVICE]
    ret = subprocess.call(cmd) == 0 # return code is 0 if it is active
    #print('service is-active ret:', ret)
    return ret

def set_led(state):
    """ turn the LED on/off """
    GPIO.output(SW_RUNNING_LED_PIN, (GPIO.HIGH if state else GPIO.LOW))
    
if __name__ == "__main__":
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SW_RUNNING_LED_PIN, GPIO.OUT, initial=GPIO.LOW)

    err_blink_state = False

    print("started up..")

    last_state = None
    while True:
        # get the temperature
        try:
            is_running = get_service_state()
        except Exception as e:
            print("failed to get direwolf state")
            print(e)

            # blink LED if the temperature sensor does not work
            err_blink_state = not err_blink_state
            set_led(err_blink_state)
        else:
            # set the LED state
            set_led(is_running)

            # print notification if the state changes
            if is_running != last_state:
                print('New state: ', is_running)
                last_state = is_running

        # wait
        time.sleep(WAIT_TIME)
