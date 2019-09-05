# raspi_leds
Driving LEDs to indicate temperature and system status. Built for the DB0SDA APRS relay.

## direwolf_led.py

Will turn on an LED if the direwolf systemd service is running.

## temperature_led.py

Turns on an LED if the DS18B20 OW temperature sensor reaches a temperature threshold.

## systemd

The systemd files run the scripts as the ```pi``` user. They expect the python scripts to be located ```/lib/led_scripts```.
