"""test_1_sub.py -- basic receive images test in PUB/SUB mode.

A simple test program that uses imagezmq to receive images from a program that
is sending images. This test pair uses the PUB/SUB messaging pattern.

1. Run this program in its own terminal window:
python test_1_sub.py

There is no particular order in which sending and receiving scripts should be
run.

2.Run the image sending program in a different terminal window:
python test_1_pub.py

A cv2.imshow() window will appear showing the tramsmitted image. The sending
program sends images with an incrementing counter so you can see what is sent
and what is received.

If you terminate receiving script pay attention to the fact that sending script
will continue to increment and send images.

If you start receiving script again it will start picking images from the
current position.

To end the programs, press Ctrl-C in the terminal window of the sending program
first. Then press Ctrl-C in the terminal window of the receiving proram. You
may have to press Ctrl-C in the display window as well.
"""

import sys
import cv2
sys.path.insert(0, '../imagezmq')  # imagezmq.py is in ../imagezmq
import imagezmq

image_hub = imagezmq.ImageHub(open_port='tcp://127.0.0.1:5555', REQ_REP=False)
while True:  # press Ctrl-C to stop image display program
    image_name, image = image_hub.recv_image()
    cv2.imshow(image_name, image)
    cv2.waitKey(1)  # wait until a key is pressed
