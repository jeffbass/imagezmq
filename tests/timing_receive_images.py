"""timing_receive_images.py -- receive and display images, then print FPS stats

A timing program that uses imagezmq to receive and display an image stream
from one or more Raspberry Pi computers and print timing and FPS statistics.

A cv2.imshow() window will appear on the Mac showing the tramsmitted images
as a video stream. You can repeat Step 2 and start the timing_send_images.py
on multiple RPis and each one will cause a new cv2.imshow() window to open.

To end the programs, press Ctrl-C in the terminal window of the receiving
program first, so that FPS and timing statistics will be accurate. Then, press
Ctrl-C in each terminal window running a Rasperry Pi image sending program.
"""

import sys

import time
import traceback
import cv2
from collections import defaultdict
from imutils.video import FPS
import imagezmq

# instantiate image_hub
image_hub = imagezmq.ImageHub()

image_count = 0
sender_image_counts = defaultdict(int)  # dict for counts by sender
first_image = True

try:
    while True:  # receive images until Ctrl-C is pressed
        sent_from, image = image_hub.recv_image()
        if first_image:
            fps = FPS().start()  # start FPS timer after first image is received
            first_image = False
        fps.update()
        image_count += 1  # global count of all images received
        sender_image_counts[sent_from] += 1  # count images for each RPi name
        cv2.imshow(sent_from, image)  # display images 1 window per sent_from
        cv2.waitKey(1)
        # other image processing code, such as saving the image, would go here.
        # often the text in "sent_from" will have additional information about
        # the image that will be used in processing the image.
        image_hub.send_reply(b"OK")  # REP reply
except (KeyboardInterrupt, SystemExit):
    pass  # Ctrl-C was pressed to end program; FPS stats computed below
except Exception as ex:
    print('Python error with no Exception handler:')
    print('Traceback error:', ex)
    traceback.print_exc()
finally:
    # stop the timer and display FPS information
    print()
    print('Test Program: ', __file__)
    print('Total Number of Images received: {:,g}'.format(image_count))
    if first_image:  # never got images from any RPi
        sys.exit()
    fps.stop()
    print('Number of Images received from each RPi:')
    for RPi in sender_image_counts:
        print('    ', RPi, ': {:,g}'.format(sender_image_counts[RPi]))
    image_size = image.shape
    print('Size of last image received: ', image_size)
    uncompressed_size = image_size[0] * image_size[1] * image_size[2]
    print('    = {:,g} bytes'.format(uncompressed_size))
    print('Elasped time: {:,.2f} seconds'.format(fps.elapsed()))
    print('Approximate FPS: {:.2f}'.format(fps.fps()))
    cv2.destroyAllWindows()  # closes the windows opened by cv2.imshow()
    image_hub.close()  # closes ZMQ socket and context
    sys.exit()
