"""timing_receive_jpg_buf.py -- receive and display images, then print FPS stats

A timing program that uses imagezmq to receive and display an image stream
from one or more Raspberry Pi computers and print timing and FPS statistics.
These jpg versions of the 2 timing programs perform jpg
compression / decompression before and after sending.

1. Run this program in its own terminal window on the mac:
python timing_receive_jpg_buf.py

This 'receive and display images' program must be running before starting
the RPi image sending program.

2. Run the image sending program on the RPi:
python timing_send_jpg_buf.py

A cv2.imshow() window will appear on the Mac showing the tramsmitted images
as a video stream. You can repeat Step 2 and start the timing_send_jpg_buf.py
on multiple RPis and each one will cause a new cv2.imshow() window to open.

To end the programs, press Ctrl-C in the terminal window of the receiving
program first, so that FPS and timing statistics will be accurate. Then, press
Ctrl-C in each terminal window running a Rasperry Pi image sending program.
"""

import sys
sys.path.insert(0, '../imagezmq')  # imagezmq.py is in ../imagezmq

import time
import traceback
import numpy as np
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
        sent_from, jpg_buffer = image_hub.recv_jpg()
        if first_image:
            fps = FPS().start()  # start FPS timer after first image is received
            first_image = False
        image = cv2.imdecode(np.frombuffer(jpg_buffer, dtype='uint8'), -1)
        # see opencv docs for info on -1 parameter
        fps.update()
        image_count += 1  # global count of all images received
        sender_image_counts[sent_from] += 1  # count images for each RPi name
        cv2.imshow(sent_from, image)  # display images 1 window per sent_from
        cv2.waitKey(1)
        image_hub.send_reply(b'OK')  # REP reply
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
    compressed_size = len(jpg_buffer)
    print('Size of last jpg buffer received: {:,g} bytes'.format(compressed_size))
    image_size = image.shape
    print('Size of last image received: ', image_size)
    uncompressed_size = 1
    for dimension in image_size:
        uncompressed_size *= dimension
    print('    = {:,g} bytes'.format(uncompressed_size))
    print('Compression ratio: {:.2f}'.format(compressed_size / uncompressed_size))
    print('Elasped time: {:,.2f} seconds'.format(fps.elapsed()))
    print('Approximate FPS: {:.2f}'.format(fps.fps()))
    cv2.destroyAllWindows()
    sys.exit()
