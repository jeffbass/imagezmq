"""test_pub_send_num_images.py -- basic send images test using PUB/SUB message pattern.

A simple test program that uses imagezmq to send images to a receiving program
that will display the images.

"""

import time
import numpy as np
import cv2
import imagezmq

# Create an image sender in PUB/SUB (non-blocking) mode
# same address 'tcp://*:555' is used by all senders
# addresses of each sender are specified in test_sub_receive_num_images.py 
sender = imagezmq.ImageSender(connect_to='tcp://*:5555', REQ_REP=False)

image_window_name = 'From Sender'
i = 0
while True:  # press Ctrl-C to stop image sending program
    # Increment a counter and print it's current state to console
    i = i + 1
    print('Sending ' + str(i))

    # Create a simple image
    image = np.zeros((400, 400, 3), dtype='uint8')
    green = (0, 255, 0)
    cv2.rectangle(image, (50, 50), (300, 300), green, 5)

    # Add an incrementing counter to the image
    cv2.putText(image, str(i), (100, 150), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 4)

    # Send an image to the queue
    sender.send_image(image_window_name, image)
    time.sleep(1)
