"""test_send_picam2_images.py -- send PiCamera image stream.

A Raspberry Pi test program that uses imagezmq to send image frames from the
PiCamera continuously to a receiving program on a Mac that will display the
images as a video stream.

This program requires that the image receiving program be running first.
"""

import socket
import time
from picamera2 import Picamera2
import imagezmq

# use either of the formats below to specifiy address of display computer
# sender = imagezmq.ImageSender(connect_to='tcp://jeff-macbook:5555')
sender = imagezmq.ImageSender(connect_to='tcp://192.168.86.35:5555')

rpi_name = socket.gethostname()  # send RPi hostname with each image
picam = Picamera2()
picam.start()
time.sleep(2.0)  # allow camera sensor to warm up
while True:  # send images as stream until Ctrl-C
    image = picam.capture_array()
    sender.send_image(rpi_name, image)
