"""test_send_with_stmt.py -- test ImageSender in with statement.
This test program tests the __enter__ and __exit__ methods for ImageSender.

This program is the SEND part of a program pair. The RECEIVE part is
test_receive_with_stmt.py. Instructions for running the complete test of both
programs are in the RECEIVE program of this pair.

*** RUN the RECEIVE program of this pair first, then leave that running while
you run this one.

This program is a Unit Test (on both sender and receiver) of the __enter__
and __exit__ methods.

The test has 2 parts:
1. Uses ImageSender in a with context statement to send 10 images.
2. Uses ImageSender in a 2nd with statement to continue to send images until
   Ctrl-C is pressed.

"with ImageSender()" is done twice to test that the context correctly closes
upon exiting the with statement block, and that a 2nd "with ImageSender()"
statement works correctly.

"""

import sys
import time
import numpy as np
import cv2
import imagezmq

from imagezmqtest import ImageSender

i = 0
image_window_name = 'From Sender'
print('Entering 1st with statment.')
with ImageSender() as sender:
    while i < 11:
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

print('Completed 1st with statement; Entering 2nd with statment.')
with ImageSender() as sender:
    while True:  # this time keep sending until Ctrl-C
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
