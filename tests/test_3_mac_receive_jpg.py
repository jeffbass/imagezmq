"""test_3_mac_receive_jpg.py -- receive & display jpg stream.

A simple test program that uses imagezmq to receive an image jpg stream from a
Raspberry Pi and display it as a video steam.

1. Run this program in its own terminal window on the mac:
python test_3_mac_receive_jpg.py

This "receive and display images" program must be running before starting the
RPi sending program.

2. Run the jpg sending program on the RPi:
python test_3_rpi_send_jpg.py

A cv2.imshow() window will appear on the Mac showing the tramsmitted images as
a video stream. You can repeat Step 2 and start the test_3_rpi_send_jpg.py on
multiple RPis and each one will cause a new cv2.imshow() window to open.

To end the programs, press Ctrl-C in the terminal window of the RPi  first.
Then press Ctrl-C in the terminal window of the receiving proram. You may
have to press Ctrl-C in the display window as well.
"""
# import imagezmq from parent directory
import sys
sys.path.insert(0, '../imagezmq')  # imagezmq.py is in ../imagezmq

import numpy as np
import cv2
import imagezmq

image_hub = imagezmq.ImageHub()
while True:  # show streamed images until Ctrl-C
    rpi_name, jpg_buffer = image_hub.recv_jpg()
    image = cv2.imdecode(np.frombuffer(jpg_buffer, dtype='uint8'), -1)
    # see opencv docs for info on -1 parameter
    cv2.imshow(rpi_name, image)  # 1 window for each RPi
    cv2.waitKey(1)
    image_hub.send_reply(b'OK')
