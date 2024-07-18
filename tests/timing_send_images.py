"""timing_send_images.py -- send PiCamera2 image stream.

A Raspberry Pi test program that uses imagezmq to send image frames from the
PiCamera continuously to a receiving program on a Mac that will display the
images as a video stream.

This program requires that the image receiving program be running first.

This program can turn an LED on and off if needed; assumes BCM pin 18. This
can help with lighting the subject area in front of the PiCamera.
"""

import sys

import socket
import time
import traceback
import cv2
from picamera2 import Picamera2
import imagezmq
import RPi.GPIO as GPIO

# use either of the formats below to specifiy address of display computer
# sender = imagezmq.ImageSender(connect_to='tcp://jeff-macbook:5555')
sender = imagezmq.ImageSender(connect_to='tcp://192.168.86.35:5555')

# optionally, turn on the LED area lighting
use_led = False  # set to True or False as needed

if use_led:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)
    GPIO.output(18, True)

rpi_name = socket.gethostname()  # send RPi hostname with each image
picam = Picamera2()
picam.start()
time.sleep(2.0)  # allow camera sensor to warm up
try:
    while True:  # send images as stream until Ctrl-C
        image = picam.capture_array()
        # processing of image before sending would go here.
        # for example, rotation, ROI selection, conversion to grayscale, etc.
        reply_from_hub = sender.send_image(rpi_name, image)
        # above line shows how to capture REP reply text from Hub
except (KeyboardInterrupt, SystemExit):
    pass  # Ctrl-C was pressed to end program
except Exception as ex:
    print('Python error with no Exception handler:')
    print('Traceback error:', ex)
    traceback.print_exc()
finally:
    if use_led:
        GPIO.output(18, False)  # turn off LEDs
        GPIO.cleanup()  # close GPIO channel and release it
    picam.close()   # close Picamera
    sender.close()  # close the ZMQ socket and context
    sys.exit()
