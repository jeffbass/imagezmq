"""timing_send_images.py -- send PiCamera image stream.

A Raspberry Pi test program that uses imagezmq to send image frames from the
PiCamera continuously to a receiving program on a Mac that will display the
images as a video stream.

This program requires that the image receiving program be running first. Brief
test instructions are in that program: timing_receive_images.py.

This program can turn an LED on and off if needed; assumes BCM pin 18. This
can help with lighting the subject area in front of the PiCamera.
"""

# import imagezmq from parent directory
import sys
sys.path.insert(0, '../imagezmq')  # imagezmq.py is in ../imagezmq

import socket
import time
import traceback
import cv2
from imutils.video import VideoStream
import imagezmq
import RPi.GPIO as GPIO

# use either of the formats below to specifiy address of display computer
# sender = imagezmq.ImageSender(connect_to='tcp://jeff-macbook:5555')
sender = imagezmq.ImageSender(connect_to='tcp://192.168.1.190:5555')

# optionally, turn on the LED area lighting
use_led = False  # set to True or False as needed

if use_led:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)
    GPIO.output(18, True)

rpi_name = socket.gethostname()  # send RPi hostname with each image
picam = VideoStream(usePiCamera=True).start()
time.sleep(2.0)  # allow camera sensor to warm up
try:
    while True:  # send images as stream until Ctrl-C
        image = picam.read()
        sender.send_image(rpi_name, image)
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
    picam.stop()
    sys.exit()
