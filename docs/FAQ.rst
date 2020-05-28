==============================================
FAQ: Frequently Asked Questions about imageZMQ
==============================================

**imageZMQ** users have raised a number of questions in multiple forums (GitHub
issues, emails, pull requests and responses to my PyCon 2020 presentation).
(right now, this FAQ is a prototype / template that I will be adding actual
content to in the next few weeks).

.. contents::

Does imageZMQ work with Windows OS?
===================================

I don't use Windows, but a number of imageZMQ users have reported that imageZMQ
does indeed work on Windows. See the discussion on this open issue#20. Making
it work involves opening the right port and opening the firewall to Python
programs.

Is it possible to send images to multiple receivers?
====================================================

Yes, but only with PUB/SUB messaging pattern. The REQ/REP messaging pattern
allows multiple senders but only one receiver (one ImageHub). The PUB/SUB
messaging pattern allows multiple senders and multiple ImageHubs. You need to be
careful with "connect_to" addresses. Take a look at this description:
`More details about the multiple RPi video streaming example <docs/more-details.rst>`_

Why am I getting a slow Frames Per Second (FPS) throughput with imageZMQ?
=========================================================================

ZMQ and imageZMQ are very fast. But image files are large and low FPS can is
normal depending on your application. There are a number of reasons for a slow
FPS in a image sender ==> imageZMQ ==> image hub pipeline:

1. Image size
2. Image compression
3. Network loading; especially the number of RPi's transmitting images
   simultaneously WiFi versus ethernet

The image size / compression factors have been the rate limiting items for me,
but I always check all 4 of the above. I use relatively small images sizes
(320 x 240 is my most common size when transmitting from Raspberry Pi). I also
use jpeg compression (which cuts image size by 60-90%). You can see the jpeg
compression example in the test program ``timing_send_jpg_buf``. I do not find
the 320 x 240 image size limiting because I have to use smaller sizes with most
deep machine learning techniques downstream anyway. But if you need larger
images sizes, network bandwidth and network load will be the dominant issues.

Is it possible to send images from 2 cameras on a single Raspberry Pi?
======================================================================

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

In REQ/REP pattern, what should be done when ImageSender hangs?
===============================================================

When using the REQ/REP pattern, the sender will hang when it does not receive a
timely REP back from the receiving hub. There are many reasons or this,
including network issues, a stalled hub, brief power glitches or
several other things. If the image sender does not receive a REP back from the
hub, the sender loop hangs waiting for the REP. This is by design; the REQ/REP
is meant to be a tightly coupled messaging pattern. Every sent image requires a
REP before sending another image. This allows a careful and continuous
monitoring of image communication. There is no REP in the PUB/SUB pattern, so
network issues can pass unnoticed.

In my system with many RPi's sending to each hub, I find that "stalls" in the
network or the RPi happen fairly frequently due brief power glitches. There are
multiple solutions, but 2 primary ones I have used:
1. Set a SIGNAL timer for each image send that raises an exception in the
   sending program if there is not a REP received after some interval of time.
2. Use ZMQ polling or the ZMQ "Lazy Pirate" message protocol in the sending
   program.

I use the first one in my imagenode programs. It looks like this:

    code goes Here

Wrap up text goes here.

Why does image sender need to restart when the image hub program restarts?
==========================================================================

This need to restart the image sending program when an image receiving program
restarts is an expected behavior in the REQ/REP messaging pattern, but does not
happen in the PUB/SUB messaging pattern. This is actually a design choice made
by the ZMQ team for the simplest REQ / REP pattern (which is the one my own
projects use). Quoting from the ZMQ docs:

    If you kill the server (Ctrl-C) and restart it, the client won't recover
    properly. Recovering from crashing processes isn't quite that easy. Making
    a reliable request-reply flow is complex enough that we won't cover it until
    Chapter 4 - Reliable Request-Reply Patterns.

I restart my RPi image sending programs by raising an exception whenever the RPi
experiences a delay in receiving a reply from the image hub receiving program.
see the "What to do when the ImageServer hangs?" question above. Restarting the
image receiving hub causes a delayed or missing REP in the image sending program
and an exception is raised. I typically set the "Patience" exception to a low
value (5 seconds) for quick timeouts. I use the systemd / systemctl service
setup with "restart" set, so imagenode clients restart themselves if the server
is down. There is an example imagenode.service file in the imagenode repository.
In production, I have multiple imagehubs with 8-10 Pi's on each and this system
is very reliable. Pi imagenodes restart quickly after power outages or other
issues and imagehub servers restart very, very seldom (but the Pi's restart
quickly when they do), such as when I update the server software.

In the ZMQ "simplest" REQ / REP pattern, clients can restart all they want to
and things keep running. But, if the server restarts, clients need to restart.
With my systemd service setup on imagenodes this works very reliably for me.

The imagehubs (imageZMQ servers) in my farm system are laptops (which have
built-in laptop battery backup), so they run for months without failing, even
through brief power outages. So I have chosen not to use one of ZMQ's
recommended "more reliable, but more complex" REQ / REP patterns.

One imageZMQ user, @youngsoul forked imageZMQ and developed a helpful method to
add timeouts to image sender to fix restarts or non-response of ImageHub. A
link to his "Helpful Fork of imageZMQ" is in the README.rst file.

How can I fix the PUB/SUB "slow subscriber" when image processing slows down?
=============================================================================

Describe PUB/SUB slow subscriber issue. A number of imageZMQ users raised this
in issue#27

Describe @philipp-shmidt's solution and link to his example programs / docs.


How does the current version of imageZMQ differ from your PyCon 2020 presentation?
==================================================================================

This version of imageZMQ is the same as the one in the PyCon 2020 presentation
with 2 minor additions:

1. Added the capability to use the ImageSender and ImageHub classes in a "with"
   statement context manager.
2. Added a HISTORY.md file that serves as a project ChangeLog.
3. Added multiple imageZMQ example programs and documentation for them.
