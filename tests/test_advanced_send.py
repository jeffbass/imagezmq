import sys
import numpy as np
import time
import cv2
sys.path.insert(0, '../imagezmq')  # imagezmq.py is in ../imagezmq
import imagezmq

# Create an image sender in PUB/SUB (non-blocking) mode
sender = imagezmq.ImageSender(connect_to='tcp://localhost:5555')

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

