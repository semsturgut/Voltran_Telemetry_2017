import RPi.GPIO as GPIO
import time

delay = 5000
buzzer_pin = 17
GPIO.setmode(GPIO.BCM)  # Use the Broadcom method for naming the GPIO pins
GPIO.setup(buzzer_pin, GPIO.OUT)  # Set pin 17 as an output pin

try:
    while True:
        GPIO.output(buzzer_pin, True)  # set pin 18 to high
except KeyboardInterrupt:
    GPIO.output(buzzer_pin, False)
