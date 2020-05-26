========================================================
Examples showing different techniques for using imageZMQ
========================================================

There are a wide variety of ways to use imageZMQ. We are providing a number of
examples that illustrate different techniques. Hopefully these will help you
with using imageZMQ in your own projects. Each of the examples has 2 programs
in the ``examples`` folder, one that sends images and one that receives images.

.. contents::

Example PUB/SUB code for the multiple RPi video streaming example
=================================================================

The README.rst file for this repository starts with a picture of a screen
where 8 Raspberry Pi computers are sending images to a single Mac computer.
This can be accomplished using either the REQ/REP messaging pattern or using the
PUB/SUB messaging pattern. The pair of programs ``test_2_rpi_send_images.py``
and ``test_2_mac_receive_images.py``, located in ``tests`` folder, was used
to create that display. Those programs use the REQ/REP messaging pattern.
Simultaneously sending images from multiple RPi's to a Mac can also be done
using the PUB/SUB messaging pattern. There are 2 programs in the ``examples``
folder which are the same as the ``test_2_`` program pair, but use the PUB/SUB
messaging pattern.

1. ``t2_send_images_via_pub.py`` is equivalent to ``test_2_rpi_send_images.py``.
2. ``t2_recv_images_via_sub.py`` is equivalent to ``test_2_mac_receive_images.py``.

Running this program pair will allow multiple RPi's to send to and display on
a single Mac or Linux computer, but will do it using the PUB/SUB messaging
pattern. To read more details about how these examples
work and how the two messaging patterns differ, read:
`More details about the multiple RPi video streaming example <docs/more-details.rst>`_

Advanced example using both messaging patterns in an HTTP streaming application
===============================================================================

This example illustrates how images can be sent from an RPi to a hub computer using
REQ/REP and then relayed to an HTTP server using PUB/SUB so the images can be
viewed in a browser. The example programs are:

1. ``advanced_send.py`` runs on the RPi to send the images.
2. ``advanced_pub.py`` runs on the hub computer to send the images to the HTTP server.
3. ``advanced_http.py`` also runs on the hub computer and serves the images for
   display in a browser.

The instructions for this example are in:
`Advanced example using both messaging patterns in an HTTP streaming application <docs/advanced-pub-sub.rst>`_
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
`Advanced PUB/SUB example with multithreaded fast subscribers for realtime processing <docs/fast-pub-sub.rst>`_ 
(Thanks to Philipp Schmidt, @philipp-schmidt for this example code and documentation.)


Example of using imageZMQ in a context manager "with" statement
===============================================================

This example illustrates how to use a ``with`` statement to instantiate and
close both an ImageSender and an ImageHub.


Tiny imagenode sending to Tiny imagehub
=======================================

This example illustrates how to use imageZMQ to send images from an imagenode
that captures images to an imagehub that saves the images to disk storage. The
programs are called ``tiny_imagenode`` and ``tiny_imagehub`` because they are
small versions on the imagenode and imagehub projects that were the reason that
I developed imageZMQ.









`Return to main documentation page README.rst <../README.rst>`_
