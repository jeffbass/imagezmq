"""pub_sub_broadcast.py -- broadcast OpenCV stream using PUB SUB."""

import sys

import socket
import traceback
import cv2
from imutils.video import VideoStream
import imagezmq

if __name__ == "__main__":
    # Publish on port
    port = 5555
    sender = imagezmq.ImageSender("tcp://*:{}".format(port), REQ_REP=False)

    # Open input stream; comment out one of these capture = VideoStream() lines!
    # *** You mus use only one of Webcam OR PiCamera
    # Webcam source for broadcast images
    capture = VideoStream()  # Webcam
    # PiCamera source for broadcast images (Raspberry Pi only)
    # capture = VideoStream(usePiCamera=True)  # PiCamera

    capture.start()
    print("Input stream opened")

    # JPEG quality, 0 - 100
    jpeg_quality = 95

    # Send RPi hostname with each image
    # This might be unnecessary in this pub sub mode, as the receiver will
    #    already need to know our address and can therefore distinguish streams
    # Keeping it anyway in case you wanna send a meaningful tag or something
    #    (or have a many to many setup)
    rpi_name = socket.gethostname()

    try:
        counter = 0
        while True:
            frame = capture.read()
            ret_code, jpg_buffer = cv2.imencode(
                ".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality])
            sender.send_jpg(rpi_name, jpg_buffer)
            print("Sent frame {}".format(counter))
            counter = counter + 1
    except (KeyboardInterrupt, SystemExit):
        print('Exit due to keyboard interrupt')
    except Exception as ex:
        print('Python error with no Exception handler:')
        print('Traceback error:', ex)
        traceback.print_exc()
    finally:
        capture.stop()
        sys.exit()
