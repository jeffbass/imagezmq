# run this program on the Mac to display image streams from multiple RPis
import sys
sys.path.insert(0, '../imagezmq')  # imagezmq.py is in ../imagezmq
import cv2
import imagezmq

def processImage(image):
    # Do something useful here, for example, run motion detection and record
    # a stream to a file if detected.
    pass

# Create a hub for receiving images from cameras
image_hub = imagezmq.ImageHub()

# Create a PUB server to send images for monitoring purposes in a non-blocking mode
stream_monitor = imagezmq.ImageSender(connect_to = 'tcp://*:5566', REQ_REP = False)

# Start main loop
while True:
    rpi_name, image = image_hub.recv_image()
    image_hub.send_reply(b'OK')
    processImage(image)
    stream_monitor.send_image(rpi_name, image)

