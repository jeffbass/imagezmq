"""test_1_receive_images.py -- basic receive images test.

A simple test program that uses imagezmq to receive images from a program that
is sending images.

1. Run this program in its own terminal window:
python test_1_receive_images.py

This "receive and display images" program must be running before starting the
image sending program.

2.Run the image sending program in a different terminal window:
python test_1_send_images.py

A cv2.imshow() window will appear showing the tramsmitted image. The sending
program sends 2 alternating images. One is a green square on a black background
and the other is a red square on a black background. They will alternate once
per second.

To end the programs, press Ctrl-C in the terminal window of the sending program
first. Then press Ctrl-C in the terminal window of the receiving proram. You
may have to press Ctrl-C in the display window as well.
"""

import sys
import cv2
sys.path.insert(0, '../imagezmq')  # imagezmq.py is in ../imagezmq
import imagezmq

image_hub = imagezmq.ImageHub()
while True:  # press Ctrl-C to stop image display program
    image_name, image = image_hub.recv_image()
    cv2.imshow(image_name, image)
    cv2.waitKey(1)  # wait until a key is pressed
    image_hub.send_reply(b'OK')
