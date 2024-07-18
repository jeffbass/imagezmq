# run this program on the Mac to display jpg compressed image streams
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