========================================================
Examples showing different techniques for using imageZMQ
========================================================

There are a wide variety of ways to use imageZMQ. Here are some
examples that illustrate different techniques. Studying these will help you
use imageZMQ in your own projects. Each of the examples has 2 programs
in the ``examples`` folder, one that sends images and one that receives images.

.. contents::

Fixing REQ/REP ImageSender hangs when ImageHub is restarted using ZMQ TimeOuts
==============================================================================

When using the REQ/REP pattern, the sender will hang when it does not receive a
timely REP back from the receiving hub. There are many reasons or this,
including network issues, a restarted or stalled hub, brief power glitches or
several other things. One way to deal with these ImageSender hangs is to
set the ZMQ Timeout options to an appropriate value and then restart either
the ImageSender or the entire program when the Exception occurs.
You can see an example of how to set the ZMQ TimeOut options and catch their
Exception in the example program ``timeout_req_ImageSender.py`` in the examples
folder in this repository. To demonstrate this example, run this program pair:

1. ``timeout_req_ImageSender.py`` runs on the RPi to send the images.
2. ``with_ImageHub.py`` should be run on the computer receiving the images.

You can start and stop the ``with_ImageHub.py`` image receiving program and
then restart it and the image stream will resume.
There is more to be said about REQ/REP ImageSender stalls when the ImageHub is
restarted or if the network hangs. See the REQ/REP question in the
`FAQ <FAQ.rst>`_.

Equivalent PUB/SUB code for the Multiple RPi video streaming example
====================================================================

The README.rst file for this imageZMQ GitHub repository starts with a picture of
a screen where 8 Raspberry Pi computers are sending images to a single Mac
computer. This can be accomplished using either the REQ/REP messaging pattern or
using the PUB/SUB messaging pattern. The programs ``test_2_rpi_send_images.py``
and ``test_2_mac_receive_images.py``, located in ``tests`` folder, were used
to create that display. Those 2 programs are an example of how use the REQ/REP
messaging pattern to send images from multiple RPis to a single Mac.
Sending images from multiple RPi's to display on a single Mac can also be done
using the PUB/SUB messaging pattern. There are 2 programs in the ``examples``
folder which are the same as the ``test_2_`` program pair, but use the PUB/SUB
messaging pattern:

1. ``t2_send_images_via_pub.py`` is equivalent to ``test_2_rpi_send_images.py``.
2. ``t2_recv_images_via_sub.py`` is equivalent to ``test_2_mac_receive_images.py``.

Running this program pair will allow multiple RPi's to send to and display on
a single Mac or Linux computer, but will do it using the PUB/SUB messaging
pattern. To learn about how these examples work and how the two messaging
patterns differ, read:
`More details about the multiple RPi video streaming example <more-details.rst>`_.

Advanced example using both messaging patterns in an HTTP streaming application
===============================================================================

This example illustrates how images can be sent from an RPi to a hub computer using
REQ/REP and then relayed to an HTTP server using PUB/SUB so the images can be
viewed in a browser. This example shows how a single program can use two
different imageZMQ instances using different ports. The 3 example programs are:

1. ``advanced_send.py`` runs on the RPi to send the images.
2. ``advanced_pub.py`` runs on the hub computer to send the images to the HTTP server.
3. ``advanced_http.py`` also runs on the hub computer and serves the images for
   display in a browser.

The instructions for this example are in:
`Advanced example using both messaging patterns in an HTTP streaming application <advanced-pub-sub.rst>`_.
(Thanks to Maksym, @bigdaddymax for this example code and documentation.)

PUB/SUB Multithreaded Fast Subscribers for Realtime Processing
==============================================================

This example illustrates a method to allow a "slower" SUBscriber receiving
images to keep up with a faster PUBlisher of images. This allows a subscriber
that is doing image processing to receive images at full speed from a publisher.
It is a way to deal with the ZMQ "slow subscriber" issue (you can see some
discussion of this in imageZMQ issue #27). It also demonstrates a great way to
use threading with the imageZMQ PUB/SUB message pattern.

The example programs are:

1. ``pub_sub_broadcast.py`` runs on the computer sending the images.
2. ``pub_sub_receive.py`` runs on the computer receiving the images.

Note that the example broadcast program has code for a RPi PiCamera or a Webcam.
Be sure to comment out the one you don't need. The receive program has a
"limit_to_2_fps" function to simulate the heaving processing of a "slow
subscriber". It is commented out for full speed, but you can remove the # and
easily simulate a "slow subscriber".

The instructions for this example are in:
`Advanced PUB/SUB example with multithreaded fast subscribers for realtime processing <fast-pub-sub.rst>`_.
(Thanks to Philipp Schmidt, @philipp-schmidt for this example code and documentation.)

Example of using imageZMQ in a context manager "with" statement
===============================================================

This example illustrates how to use a ``with`` statement to instantiate and
close both an ImageSender and an ImageHub. The example programs are:

1. ``with_ImageSender.py`` runs on the computer sending the images.
2. ``with_ImageHub.py`` runs on the computer receiving the images.

Using a ``with`` statement as a content manager can simplify programs
and make sure that the ZMQ sockets and contexts are properly closed without
expressly calling the imageZMQ ``close`` methods.

A simple example program pair is also in the test folder
========================================================

The programs ``timing_send_images.py`` and ``timing_receive_images.py`` provide
examples of how to use the **imageZMQ** API to send and receive OpenCV
images.  Both of these programs are in the `tests` folder.
The programs show a simple, but complete **imageZMQ** use case.
Additional image processing in the sending program would typically be placed
between the ``picam.read()`` and the ``sender.send_image()`` lines. Such processing
would be done with calls to methods for image rotation, resizing,
dilation, etc.  The program that is receiving images would do other processing
and save the images to disk using the text portion of the image message to
categorize or label each image file received. See the comments in these programs
for more details on where these processing statements would be placed.

Full imagenode and imagehub Project Examples
============================================

I wrote imageZMQ to send images from multiple RPi's to multiple Mac and Linux
hub computers as part of my own project to automate my small permaculture farm.
So the most complete example of an ImageSender sending images is my own
`imagenode project on GitHub <https://github.com/jeffbass/imagenode>`_. And the
most complete example of an ImageHub that receives and store images and event
messages is my own `imagehub project on GitHub <https://github.com/jeffbass/imagehub>`_.
The "meta project" describing how imagenode, imagehub and imageZMQ are used
together to manage the farm is this
`Yin Yang Ranch project overview on GitHub <https://github.com/jeffbass/yin-yang-ranch>`_.
I gave a talk about it as part of **PyCon 2020:**

**Jeff Bass - Yin Yang Ranch: Building a Distributed Computer
Vision Pipeline using Python, OpenCV and ZMQ**

`PyCon 2020 Talk Video about the project  <https://youtu.be/76GGZGneJZ4?t=2>`_

`PyCon 2020 Talk Presentation slides  <https://speakerdeck.com/jeffbass/yin-yang-ranch-building-a-distributed-computer-vision-pipeline-using-python-opencv-and-zmq-17024000-4389-4bae-9e4d-16302d20a5b6>`_

Other Contributed imageZMQ Examples are Welcome!
================================================

If you have an example program that uses imageZMQ and you think it would be
helpful to other imageZMQ users, feel free to open an issue and describe it. We can
work together to get your example and a short description listed here so other
imageZMQ users can learn from it. Or, if you have forked imageZMQ and made some
changes you would like to share with others, perhaps we could list it in the
"Helpful Forks of imageZMQ" section of the README.rst. Open an issue to start
the discussion. Thanks!


`Return to main documentation page README.rst <../README.rst>`_
