"""t2_recv_images_via_sub.py --  receive images using PUB/SUB messaging pattern.

This example program uses imagezmq to receive images from a matching program
that is sending images. This test pair uses the PUB/SUB messaging pattern.

1. Run this program in its own terminal window on the receving computer:
python t2_recv_images_via_sub.py

There is no particular order in which sending and receiving scripts should be
run.

2.Run the image sending program in a different terminal window that is running
on the sending computer:
python t2_send_images_via_pub.py

A cv2.imshow() window will appear showing the received images. If you start
additional image sending programs using step 2, then a new cv2.imshow() window
will open for each sending computer; this happens because each sending computer
is using its hostname as a unique label for its images.

If you terminate receiving script, the image sending program will continue to
send images (but they will not be displayed).

If you start receiving script again it will start displaying images from the
current image being sent by the image sending program.

To end the programs, press Ctrl-C in the terminal window of each program. It is
normal to get error messages when pressing Ctrl-C. There is no error trapping in
this simple example program.
"""

import cv2
import imagezmq

# Instantiate and provide the first publisher address
image_hub = imagezmq.ImageHub(open_port='tcp://192.168.86.39:5555', REQ_REP=False)
image_hub.connect('tcp://192.168.86.38:5555')    # second publisher address
# image_hub.connect('tcp://192.168.0.102:5555')  # third publisher address
# image_hub.connect('tcp://192.168.0.103:5555')  # must specify address for every sender
# repeat hub.connect() statements as needed for all senders.

while True:  # show received images
    rpi_name, image = image_hub.recv_image()
    cv2.imshow(rpi_name, image)  # 1 window for each unique RPi name
    cv2.waitKey(1)
