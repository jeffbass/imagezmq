"""test_send_webcam_images.py -- send OpenCV webcam image stream.

A Raspberry Pi test program that uses imagezmq to send image frames from the
PiCamera continuously to a receiving program on a Mac that will display the
images as a video stream.

This program requires that the image receiving program be running first.
"""

import time
from cv2 import VideoCapture
import imagezmq

# use either of the formats below to specifiy address of display computer
# sender = imagezmq.ImageSender(connect_to='tcp://jeff-macbook:5555')
sender = imagezmq.ImageSender(connect_to='tcp://192.168.86.35:5555')

sender_name = "From Webcam" # name will at top of receiver window
webcam = VideoCapture(0) # 0 is typical source; try 1 or 2 as needed
# picam.start()
time.sleep(2.0)  # allow camera sensor to warm up
while True:  # send images as stream until Ctrl-C
    ret_code, image = webcam.read()
    sender.send_image(sender_name, image)
