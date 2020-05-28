==============================================
FAQ: Frequently Asked Questions about imageZMQ
==============================================

**imageZMQ** users have raised a number of questions in multiple forums (GitHub
issues, emails, pull requests and responses to my PyCon 2020 presentation).
(right now, this FAQ is a prototype / template that I will be adding actual
content to in the next few weeks).

.. contents::

Why does image sender need to restart when the image hub program restarts?
==========================================================================

This one needs a longer response. (Note to self: Use the responses to 1st closed
pull request and from issue #1 and some parts of PUB/SUB slow subscribers issue.)

Is it possible to send images to multiple receivers?
====================================================

Yes, but only with PUB/SUB messaging pattern. The REQ/REP messaging pattern
allows multiple senders but only one receiver (one ImageHub). The PUB/SUB
messaging pattern allows multiple senders and multiple ImageHubs. You need to be
careful with "connect_to" addresses. Take a look at this description:
`More details about the multiple RPi video streaming example <docs/more-details.rst>`_

Is it possible to send images from 2 cameras on a single Raspberry Pi?
===============================================================

Yes. It is possible to send 2 image streams from the same RPi by using a
PiCamera and a USB Webcam attached to the same RPi.

The existing imagezmq test programs show how to send a single stream of images
from a single PiCamera. If you want to send a 2nd video stream of images from
the same RPi, you would have to use a USB Webcam plugged into one of the USB
ports on the RPi. I have one RPi set up with 1 PiCamera and 1 USB WebCam (a
Logitech C920 Webcam). To test the 2 camera RPi setup I  modified
test_2_rpi_send_images.py. Running 2 cameras on the same RPi requires 2 unique
names for the 2 streams, and requires 2 camera instantiations from VideoStream
and 2 image reads and 2 image sends. Here are the changes I made to
``test_2_rpi_send.py``:

.. code-block:: python
  :number-lines:

    rpi_name = socket.gethostname()  # send RPi hostname with each image
    picam_name = rpi_name + " PiCamera"  # this name will show on PiCamera images
    webcam_name = rpi_name + " WebCam"  # this name will show on WebCam images
    picam = VideoStream(usePiCamera=True).start()
    webcam = VideoStream(usePiCamera=False).start()
    time.sleep(2.0)  # allow camera sensor to warm up
    while True:  # send images as stream until Ctrl-C
        image = picam.read()
        sender.send_image(picam_name, image)
        image = webcam.read()
        sender.send_image(webcam_name, image)


The test_2_mac_receive_images.py program did not need any changes. The sent
images appear in 2 different windows, one for each camera stream.

How does the current version of imageZMQ differ your PyCon 2020 presentation?
=============================================================================

This version of imageZMQ is the same as the one in the PyCon 2020 presentation
with 2 minor additions:

1. Added the capability to use the ImageSender and ImageHub classes in a "with"
   statement context manager.
2. Added a HISTORY.md file that serves as a project ChangeLog.
3. Added multiple imageZMQ example programs and documentation for them.
