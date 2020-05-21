"""test_receive_with_stmt.py -- test ImageHub in with statement.
This test program tests the __enter__ and __exit__ methods for ImageHub.

This program is the RECEIVE part of a program pair. The SEND part is
test_send_with_stmt.py.

*** RUN this RECEIVE program of this pair first, then leave it running while
you run the sending program. Instructions for running the complete test of both
programs are below.

This program is a Unit Test (on both sender and receiver) of of the __enter__
and __exit__ methods.

The program in the pair tests the use of ImageHub in a with context:
1. Uses ImageHub in 1st with statement to receive images.
2. Receives 25 images in the first with statement. That is enough to have the
   sender program enter its 2nd context.
3. Exits the 1st with statement, thus closing the first ImageHub.
4. Uses ImageHub in a 2nd with statement to receive images, but this will stall
   the sender, since it is using REQ/REP. That is expected.
3. A cv2.imshow() window appears showing the 2 programs are working OK together.

*** Instructions for running BOTH programs for a complete Unit Test:
To make sure you are testing the latest development version of imagezmq.py:
1. Copy imagezmq.py from its directory into this one, changing its name:
   cp ../../imagezmq/imagezmq.py imagezmqtest.py
2. Be sure to be in your appropriate virtualenv:
   workon py3cv3  # this is my testing one for these tests

Then run the tests. These test programs expect imagezmqtest.py to be available
in this same directory and will produce an import error if it is not.

1. Run this program in its own terminal window:
python test_receive_with_stmt.py

This "receive and display images" program MUST be running before starting the
image sending program.

2. Run the image sending program in a different terminal window:
python test_send_with_stmt.py

A cv2.imshow() window will appear showing the tramsmitted image. The sending
program sends a series of images with an incrementing couner value.

To end the programs, press Ctrl-C in the terminal window of the sending program
first. Then press Ctrl-C in the terminal window of the receiving proram. You
get various error messages when you press Ctrl-C. That's normal; there is no
error or exception trapping in these simple test programs.

"""

import sys
import cv2
from imagezmqtest import ImageHub

print('Entering 1st with statement.')
with ImageHub() as image_hub:
    for i in range(0,25):  # receive 25 images, then exit ImageHub() context
        image_name, image = image_hub.recv_image()
        cv2.imshow(image_name, image)
        cv2.waitKey(1)  # wait until a key is pressed
        image_hub.send_reply(b'OK')

print('Entering 2nd with statement.')
with ImageHub() as image_hub:  # open ImageHub again
    print('Successfully entered 2nd with statement. Press Ctrl-C to end.')
    for i in range(0,50):
        image_name, image = image_hub.recv_image()
        cv2.imshow(image_name, image)
        cv2.waitKey(1)  # wait until a key is pressed
        image_hub.send_reply(b'OK')
