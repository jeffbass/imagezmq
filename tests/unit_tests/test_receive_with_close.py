"""test_receive_with_close.py -- test close() method.
This test program tests the new .close() method added in v1.1.0.

This program is the RECEIVE part of a program pair. The SEND part is
test_send_with_close.py.

*** RUN this RECEIVE program of this pair first, then leave it running while
you run the sending program. Instructions for running the complete test of both
programs are below.

This program is a Unit Test (on both sender and receiver) of .close() method.

The total test of both programs in the pair has 3 stages:
1. Instantiate an ImageHub, the use hub.close() and then reinstantiate
   an ImageHub. Then await images. Thats THIS program.
2. Instantiate an ImageSender, then use sender.close() and then reinstantiate
   the ImageSender. Then start sending images. That's the OTHER program in this
   program test pair.
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
python test_receive_with_close.py

This "receive and display images" program MUST be running before starting the
image sending program.

2. Wait until the first 3 test steps show 3 OK messages (or note if an
error occurs). If an error occurs, it must be fixed before the remaining steps.

3. Run the image sending program in a different terminal window:
python test_send_with_close.py

After the 3 "OK" test messages appear:
A cv2.imshow() window will appear showing the tramsmitted image. The sending
program sends a series of images with an incrementing couner value.

To end the programs, press Ctrl-C in the terminal window of the sending program
first. Then press Ctrl-C in the terminal window of the receiving proram. You
get various error messages when you press Ctrl-C. That's normal; there is no
error or exception trapping in these simple test programs.

"""

import sys
import cv2
import imagezmqtest

image_hub = imagezmqtest.ImageHub()
print('Opened ImageHub OK.')
image_hub.close()
print('Closed ImageHub OK.')
image_hub = imagezmqtest.ImageHub()
print('Reopened ImageHub OK after first close. Starting receive & show loop.')
while True:  # press Ctrl-C to stop image display program
    image_name, image = image_hub.recv_image()
    cv2.imshow(image_name, image)
    cv2.waitKey(1)  # wait until a key is pressed
    image_hub.send_reply(b'OK')
