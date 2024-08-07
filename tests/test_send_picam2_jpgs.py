"""test_send_picam2_jpg.py -- send PiCamera jpg stream.

A Raspberry Pi test program that uses imagezmq to send image frames from the
PiCamera continuously to a receiving program on a Mac that will display the
images as a video stream. Images are converted to jpg format before sending.

This program requires that the image receiving program be running first.
"""

import sys

import socket
import time
import cv2
from picamera2 import Picamera2
import imagezmq

# use either of the formats below to specifiy address of display computer
# sender = imagezmq.ImageSender(connect_to='tcp://jeff-macbook:5555')
sender = imagezmq.ImageSender(connect_to='tcp://192.168.86.35:5555')

rpi_name = socket.gethostname()  # send RPi hostname with each image
picam = Picamera2()
picam.start()
time.sleep(2.0)  # allow camera sensor to warm up
jpeg_quality = 95  # 0 to 100, higher is better quality, 95 is cv2 default
while True:  # send images as stream until Ctrl-C
    image = picam.capture_array()
    ret_code, jpg_buffer = cv2.imencode(
        ".jpg", image, [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality])
    sender.send_jpg(rpi_name, jpg_buffer)
