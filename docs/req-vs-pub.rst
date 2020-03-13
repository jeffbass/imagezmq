=========================================
REQ/REP versus PUB/SUB Messaging Patterns
=========================================

ImageSender/ImageHub can work in either of two modes: REQ/REP or PUB/SUB.
The mode is selected when ImageSender and ImageHub are instantiated by setting
the REQ_REP parameter in the constructor to *True* or *False*. REQ/REP mode is
the default.

Two messaging patterns: REQ/REP and PUB/SUB
===========================================

These two modes (or to be more precise,  messaging patterns) are similar.
Both are used to send images from sender to receiver. But the behavior of the
sender and receiver is significantly different for the two messaging patterns.

The **REQ/REP** pattern guarantees image delivery from sender to recipient: the
sender receives confirmation from recipient before the next image is sent. This
makes the code "blocking". This means that if a recipient for some reason does
not reply, then the sender will stop execution until it does receive a reply
(it will be blocked).

When using the REQ/REP pattern, one recipient can receive
images from many senders, however one sender can only send images to a single
recipient (many image senders send images to a single image hub). This feature
is helpful in an situation where you know address of the hub (the computer where
ImageHub runs), but the addresses of senders (computers on which ImageSender
runs) can change often (for example, you use DHCP and the sending computers
reboot from time to time).

**PUB/SUB**, in contrast, is a non-blocking pattern with non-guaranteed delivery.
The sender does not expect confirmation from recipient. The sender will continue
sending images even if there are no recipients at all.

The PUB/SUB pattern easily supports many-to-many relations. One sender can send
to many recipients and each recipient can receive images from many senders.

From a configuration point of view, the PUB/SUB pattern requires more planning:
each sender is an image server and the ImageHub must explicitly subscribe to
each one of them. In the PUB/SUB pattern, the recipient must know the addresses
of all senders.

The REQ/REP pattern was the first pattern implemented in **imagezmq** because it
works well for the original **imagezmq** application: many Raspberry Pi (RPi)
computers sending images to a single image hub computer receiving the images. The
RPi's only need to know the address of a single hub computer. The hub computer
does not need to know how many RPi's there will be or what their addresses are.

Advantages of the REQ/REP pattern
=================================

- Receipt of each sent image is verified (by the sender receiving a "REP").
- Receiving hub computer does not need to know the addresses of senders.
- Receiving hub computer can receive from one or many senders.
- Receiving hub computer can receive and process images from multiple image
  senders simultaneously.
- Starting and stopping any of the senders does not affect the hub (or any of
  the other senders).

Disadvantages of the REQ/REP pattern
====================================

- Each sender is "blocked" from sending the next image until it gets a reply
  from the hub computer.
- If the hub computer restarts, the senders must restart.
- Hub needs to be reliable and not restart often (since all the senders have to
  restart if the hub restarts).

Advantages of the PUB/SUB pattern
=================================

- It is a non-blocking pattern; senders keep sending images without waiting for
  a reply.
- Senders do not need to restart if the receiving hub restarts.
- PUB/SUB can easily implement a many to many pattern with many senders and many
  hubs.

Disadvantages of the PUB/SUB pattern
====================================

- Receiving hub computer must know each senders address in advance.
- Receiving hub must explicitly subscribe to each sender.
- If the receiving hub computer fails or does not receive an image, the sender
  will not know (since there is no REP sent).
- If one (or more) of the receiving programs is much slower than the sender,
  then the slow subscriber can start to build up a ZMQ queue that slows down and
  can even cause the program to fail. This has been an issue for some
  **imagezmq** users. See issue #27, [PUB/SUB] Subscriber slow motion video
  (queue keeps growing). See also the ZMQ documentation about slow subscribers:
  `ZMQ Slow Subscriber Detection (Suicidal Snail Pattern). <http://zguide.zeromq.org/php:chapter5#toc4>`_
  If you use the PUB/SUB pattern and encounter this Slow Subscriber problem,
  read Issue #27 and comment there if you come up with a good solution!

Further reading on messaging patterns
=====================================

A full discussion of the two different messaging patterns is in the ZMQ
documentation:
`ZeroMQ Messaging Patterns <https://zeromq.org/socket-api/#messaging-patterns/>`_.

Demonstrating the Difference between REQ/REP and PUB/SUB
========================================================

To demonstrate the difference between two messaging patterns you can run two
examples from tests folder: ``test_1_send_image.py``/``test_1_receive_image.py``
for a REQ/REP pattern and ``test_1_pub.py``/``test_1_sub.py`` for a
PUB/SUB pattern.

If you run ``test_1_send_image.py`` and ``test_1_receive_image.py`` scripts in
separate console windows you should see incremental output on the sender window::

   Sending 1
   Sending 2
   ...


The receiver will open a window and display an incrementing number that will
correspond to whatever number you see on the sender screen.

If you stop receiver (using Ctrl-C) you should notice that sender will stop
printing "Sending XX". The sender will block until recipient is started again.
This demonstrates that the REQ/REP pattern is "blocking".
The recipient window should continue from the moment where it was stopped.

Next, run the ``test_1_pub.py`` and ``test_1_sub.py`` pair. You should see the
same "Sending XX" printed on the sender window and see the corresponding number
incrementing on recipient window.

However, if you close the recipient script the sender will continue printing and
incrementing the value.

And if you start the recipient again it will just pick from the current sending
number. This demonstrates that the PUB/SUB pattern is "non-blocking".

`Return to main documentation page README.rst <../README.rst>`_
