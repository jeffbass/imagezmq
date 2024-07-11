"""test_send_num_images.py -- send generated numbers images

Tests sending class of imagezmq to send generated images to a receiving program
that will display the images. Receiver program can be localhost on this computer
OR another computer (if an address is provided)

The sent images are a sequence of numbers 1, 2, 3 ...
The numbers are Yellow and appear in a Green Rectangle
OpenCV cv2.rectangle and cv2.putText are used to create the images

This sending program uses the default REQ/REP message pattern 

Image receiving program must be running first before starting this program.
"""
import time
import numpy as np
import cv2
import imagezmq

# image will be green square on a black background
green = (0, 255, 0)

# ascending yellow number will be written in the green square using cv2.putText
yellow = (0, 255, 255)

# uncomment only ONE ImageSender statement for each test; comment out the others
sender = imagezmq.ImageSender()  # will send to localhost on THIS computer

# 2 different ways to specify a different computer that will receive images
# sender = imagezmq.ImageSender(connect_to='tcp://192.168.1.190:5555')
# sender = imagezmq.ImageSender(connect_to='tcp://jeff-macbook:5555')

i = 0
image_window_name = 'Images from Sender'
while True:  # press Ctrl-C to stop image sending program
    # Increment a counter and print it's value in terminal window
    i = i + 1
    print('Sending ' + str(i))
    
    # create an image with a black background with a green rectangle
    image = np.zeros((400, 400, 3), dtype='uint8')
    cv2.rectangle(image, (50, 50), (300, 300), green, 5)

    # put the counter value number into the image 
    cv2.putText(image, str(i), (100, 150), cv2.FONT_HERSHEY_SIMPLEX, 2, yellow, 4)
    sender.send_image(image_window_name, image)
    time.sleep(1)