"""test_sub_receive_num_images.py -- basic receive images test in PUB/SUB mode.

A simple test program that uses imagezmq to receive images from a program that
is sending images. This test pair uses the PUB/SUB messaging pattern.
"""

import cv2
import imagezmq

# use either of the formats below to specifiy address of display computer
# sender = imagezmq.ImageSender(open_port='tcp://rpi32:5555',REQ_REP=False)
image_hub = imagezmq.ImageHub(open_port='tcp://192.168.86.33:5555', REQ_REP=False)

# additional rpi publisher / ImageSenders can be added using the .connect() method
# image_hub.connect('tcp://192.168.86.38:5555')    # second publisher address
# image_hub.connect('tcp://rpi38:5555')            # third publisher address
# image_hub.connect('tcp://rpi41:5555')  # must specify address for every sender
while True:  # press Ctrl-C to stop image display program
    image_name, image = image_hub.recv_image()
    cv2.imshow(image_name, image)
    cv2.waitKey(10)  # wait until a key is pressed
