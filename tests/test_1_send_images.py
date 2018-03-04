"""test_1_send_images.py -- basic send images test.

A simple test program that uses imagezmq to send images to a receiving program
that will display the images.

This program requires that the image receiving program to be running first.
Brief test instructions are in that program: test_1_receive_images.py.
"""

import sys
import time
import numpy as np
import cv2
sys.path.insert(0, '../imagezmq')  # imagezmq.py is in ../imagezmq
import imagezmq

# Create 2 different test images to send
# A green square on a black background
image1 = np.zeros((400, 400, 3), dtype='uint8')
green = (0, 255, 0)
cv2.rectangle(image1, (50, 50), (300, 300), green, 5)
# A red square on a black background
image2 = np.zeros((400, 400, 3), dtype='uint8')
red = (0, 0, 255)
cv2.rectangle(image2, (100, 100), (350, 350), red, 5)

sender = imagezmq.ImageSender()

image_window_name = 'From Sender'
while True:  # press Ctrl-C to stop image sending program
    sender.send_image(image_window_name, image1)
    time.sleep(1)
    sender.send_image(image_window_name, image2)
    time.sleep(1)
