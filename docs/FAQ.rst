==============================================
FAQ: Frequently Asked Questions about imageZMQ
==============================================

**imageZMQ** users have raised a number of questions in multiple forums (GitHub
issues, emails, pull requests and responses to my PyCon 2020 presentation).
Here are some Frequently Asked Questions and answers. If you have a question
that is not listed here, I suggest you start a new issue. You will likely get an
answer from me or another imageZMQ user in a few days.

.. contents::

Does imageZMQ work with Windows OS?
===================================

I don't use Windows, but a number of imageZMQ users have reported that imageZMQ
does indeed work on Windows. See the discussion on this open issue#20. Making
it work involves opening the right port and opening the firewall to Python
programs. See issue #20.

Is it possible to send images to multiple receivers?
====================================================

Yes, but only with PUB/SUB messaging pattern. The REQ/REP messaging pattern
allows multiple senders but only one receiver (one ImageHub). The PUB/SUB
messaging pattern allows multiple senders and multiple ImageHubs. You need to be
careful with "connect_to" addresses. Take a look at this description:
`More details about the multiple RPi video streaming example. <more-details.rst>`_

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
compression example in the test program ``timing_send_jpg_buf.py``. I do not find
the 320 x 240 image size limiting because I have to use smaller sizes with most
deep machine learning techniques downstream anyway. But if you need larger
images sizes, network bandwidth and network load will be the dominant issues.
If you are using PUB/SUB and have a Slow Subscriber, see the Slow Subscriber
question below.

Is it possible to send images from 2 cameras on a single Raspberry Pi?
======================================================================

Yes. It is possible to send 2 image streams from the same RPi by using a
PiCamera and a USB Webcam attached to the same RPi.

The existing imagezmq test programs show how to send a single stream of images
from a single PiCamera. If you want to send a 2nd video stream of images from
the same RPi, you would have to use a USB Webcam plugged into one of the USB
ports on the RPi. I have one RPi set up with 1 PiCamera and 1 USB WebCam (a
Logitech C920 Webcam). To test the 2 camera RPi setup I  modified
``test_2_rpi_send_images.py``. Running 2 cameras on the same RPi requires 2 unique
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

In REQ/REP pattern, what should be done when the ImageSender hangs?
===================================================================

When using the REQ/REP pattern, the sender will hang when it does not receive a
timely REP back from the receiving hub. There are many reasons or this,
including network issues, a restarted or stalled hub, brief power glitches or
several other things. If the image sender does not receive a REP back from the
hub, the sender loop hangs waiting for the REP. This is by design; the REQ/REP
is meant to be a tightly coupled messaging pattern. Every sent image requires a
REP before sending another image. This allows a careful and continuous
monitoring of image communication. There is no REP in the PUB/SUB pattern, so
network issues can pass unnoticed.

In my system with many RPi's sending to each hub, I find that "stalls" in the
network or the RPi happen fairly frequently due brief power glitches. There are
multiple solutions, but the 2 primary ones I have used are:

1. Set the ZMQ Timeout options to an appropriate value and then restart either
   the ImageSender or the entire program when the Exception occurs.
2. Get a timestamp just before sending and a timestamp just after sending each
   image message. Check the amount of time between them in a timed loop running
   in a separate thread. If the amount of time between the timestamps is longer
   than desired, then close / restart the ImageSender() or the entire program.

You can see an example of how #1 above can be implemented in the example program
``timeout_req_ImageSender.py`` in the examples folder in this repository. The
example is discussed in the `Examples documentation. <examples.rst>`_

You can see an example of #2 above in the most recent version of imagenode.
I use a method of saving a timestamp before and after each call to
``sender.send_jpg(text, jpg_buffer)`` in lines 326-347 of
`imagenode. <https://github.com/jeffbass/imagenode/blob/master/imagenode/tools/imaging.py>`_
I then check for an excessive amount of time between the timestamps in
the method ``REP_watcher()`` in the same block of code.  ``REP_watcher()`` is
started in a separate thread with a timing loop.

One imageZMQ user @youngsoul forked imageZMQ and modified the ImageSender
class to raise a ZMQ exception for a timeout on sending or receiving. You can
see his code
`here. <https://github.com/youngsoul/imagezmq/blob/master/imagezmq/imagezmq.py>`_

I mention @youngsoul's code in the Helpful Forks section of
the imageZMQ README.

If you use @youngsoul's code, you would need to include a try / except
block in your own code that checks for the exception being raised. You can see
an example of how @youngsoul did that
`here. <https://github.com/youngsoul/imagezmq/blob/master/CHANGES.md>`_

Why does image sender need to restart when the image hub program restarts?
==========================================================================

The need to restart the image sending program when an image receiving program
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

The "hanging" of the REQ client when the REP server restarts is a known ZMQ
"feature" and is there by design (so that a dropped REQ won't go unnoticed by
the sender). I use this ZMQ feature as a part of my own yin-yang-ranch project
design -- I want the RPi's to know if they need to deal with a non-responsive
imagehub.

One imageZMQ user, @youngsoul forked imageZMQ and developed a helpful method to
add timeouts to image sender to fix restarts or non-response of ImageHub. A
link to his "Helpful Fork of imageZMQ" is in the README.rst file.

It is also possible to set ZMQ TimeOut Socket options so that at Try / Except
block can catch a stalled ImageHub. See the question about REQ / REP ImageSender
hangs above. It also points to an example program in the ``Examples`` folder.

Is it possible to have two ImageHub servers running on the same computer?
=========================================================================

Yes. You can have multiple image receiving servers on the same computer, and
even in the same image receiving program. You
will have to run each server using a different port (I use 5555, 5556, 5557, but
any unused port numbers will do). The image sending client that is sending to
each server must have its port number changed to match the port number of the
server that it is sending to. You can, as always, have multiple clients sending
to the same server, but all the clients must have the same port number as the
server they are sending to. I have run as many as 3 servers on the same
computer, receiving images from 8 clients each.

How can I fix the PUB/SUB "slow subscriber" when image processing slows down?
=============================================================================

Some users of the PUB/SUB messaging pattern find have found that when the
receiver (SUB) does processing that makes it slower than the image sender (PUB)
frame transmission rate, the ZMQ queue can build and cause the image loop on the
subscriber to get extremely slow. This "slow subscriber" issue is mentioned in
the ZMQ documentation, with a recommendation of killing and restarting a slow
subscriber. (the ZMQ documentation calls it the "Suicidal Snail" problem). A
number of imageZMQ users have discussed this in issue #27.

Philipp Schmidt @philipp-shmidt contributed a solution to the slow subscriber
problem. It is an elegant use of Threading. I tested it with significant
subscriber delays and it worked perfectly. I merged his code and documentation
into the imageZMQ examples folder.  You can find his description of his solution
`here. <fast-pub-sub.rst>`_

Have you given a talk about imageZMQ? Is there a video explaining it?
=====================================================================

I gave a talk about my full **imagenode** ==> **imageZMQ** ==> **imagehub**
project at PyCon 2020:

**Jeff Bass - Yin Yang Ranch: Building a Distributed Computer
Vision Pipeline using Python, OpenCV and ZMQ**

`PyCon 2020 Talk Video about the project  <https://youtu.be/76GGZGneJZ4?t=2>`_

`PyCon 2020 Talk Presentation slides  <https://speakerdeck.com/jeffbass/yin-yang-ranch-building-a-distributed-computer-vision-pipeline-using-python-opencv-and-zmq-17024000-4389-4bae-9e4d-16302d20a5b6>`_

How does the current version of imageZMQ differ from your PyCon 2020 presentation?
==================================================================================

This version of imageZMQ is the same as the one in the PyCon 2020 presentation
with 4 minor additions:

1. Added the capability to use the ImageSender and ImageHub classes in a "with"
   statement context manager.
2. Added a HISTORY.md file that serves as a project ChangeLog.
3. Added multiple imageZMQ example programs and documentation for them.
4. Added this FAQ file.

`Return to main documentation page README.rst <../README.rst>`_
