"""test_receive_with_close.py -- test close() and __enter__ and __exit__.
This test program tests three new capabilities added in v1.1.0.

This program is the RECEIVE part of a program pair. The SEND part is
test_send_with_close.py.

*** RUN this RECEIVE program of this pair first, then leave it running while
you run the sending program. Instructions for running the complete test of both
programs are below.

This program is a Unit Test (on both sender and receiver) of sender.close() and
    sender.__enter__() and sender.__exit__ (using "with" context manager).

The total test of both programs in the pair has 4 parts:
1. Instantiate an ImageHub, the use hub.close() and then reinstantiate
   an ImageHub. Then send 3 images.
2. Use ImageHub context invocation to send 3 images. This should
   exit without errors.
3. Use "with ImageSender" context invocation to send 3 more images. This
   should both start and end without errors.
4. Run other program in pair -- test_send_with_close.py -- so that the above 3
   tests are also run on the receiving program and the imageZMQ link transmitting
   images between them is running OK.

*** Instructions for using BOTH programs for a complete Unit Test:
To make sure your testing the latest development version if imagezmq.py:
1. Copy imagezmq.py from its directory into this one, changing its name:
   cp ../../imagezmq/imagezmq.py imagezmqtest.py
2. Edit imagezmqtest.py to add a print("test version") statement it to be
   sure it is importing correctly. Add it right after the import numpy
   statement:
   print('Test: importing imagezmqtest.py')

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
# TODO: Jeff! Finish this and its paired program ASAP!

import sys
import cv2
import imagezmqtest

image_hub = imagezmq.ImageHub()
print('Opened ImageHub OK.')
image_hub.close()
print('Closed ImageHUB OK.')
image_hub = imagezmq.ImageHub()
while True:  # press Ctrl-C to stop image display program
    image_name, image = image_hub.recv_image()
    cv2.imshow(image_name, image)
    cv2.waitKey(1)  # wait until a key is pressed
    image_hub.send_reply(b'OK')
