"""test_send_with_close.py -- test close() method.
This test program tests three new capabilities added in v1.1.0.

This program is the SEND part of a program pair. The RECEIVE part is
test_receive_with_close.py. Instructions for running the complete test of both
programs are in the RECEIVE program of this pair.

*** RUN the RECEIVE program of this pair first, then leave that running while
you run this one.

This program is a Unit Test (on both sender and receiver) of .close() method.

The test has 3 parts:
1. Tests instantiating an ImageSender and prints an OK message.
2. Closes the sender using sender.close() and re-Instantiates it.
2. Starts forever sending loop.

"""

import sys
import time
import numpy as np
import cv2
import imagezmq

import imagezmqtest

sender = imagezmqtest.ImageSender()
print('Opened ImageSender OK.')
sender.close()
print('Closed ImageSender OK.')
sender = imagezmqtest.ImageSender()
print('Reopened ImageSender OK after first close. Starting receive & show loop.')

# Create 2 different test images to send
# A green square on a black background
# A red square on a black background

i = 0
image_window_name = 'From Sender'
while True:  # press Ctrl-C to stop image sending program
    # Increment a counter and print it's value to console
    i = i + 1
    print('Sending ' + str(i))

    # Create a simple image
    image = np.zeros((400, 400, 3), dtype='uint8')
    green = (0, 255, 0)
    cv2.rectangle(image, (50, 50), (300, 300), green, 5)

    # Add counter value to the image and send it to the queue
    cv2.putText(image, str(i), (100, 150), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 4)
    sender.send_image(image_window_name, image)
    time.sleep(1)
