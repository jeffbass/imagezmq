====================================
imageZMQ: Transporting OpenCV images
====================================

Introduction
============

**imageZMQ** is a set of Python classes that transport OpenCV images from one
computer to another using PyZMQ messaging. For example, here is a screen on a
Mac computer showing simultaneous image streams from 8 Raspberry Pi cameras:

.. image:: docs/images/screenshottest.png

Using **imageZMQ**, this is possible with 11 lines of Python on each Raspberry
Pi and with 8 lines of Python on the Mac.

First, run this receiver program on the Mac (or other display computer):

.. code-block:: python

    # run this program on the Mac to display image streams from multiple RPis
    import cv2
    import imagezmq
    image_hub = imagezmq.ImageHub()
    while True:  # show streamed images until Ctrl-C
        rpi_name, image = image_hub.recv_image()
        cv2.imshow(rpi_name, image) # 1 window for each RPi
        cv2.waitKey(1)
        image_hub.send_reply(b'OK')


Then, on each Raspberry Pi, run this sender program:

.. code-block:: python

    # run this program on each RPi to send a labelled image stream
    # you can run it on multiple RPi's; 8 RPi's running in above example
    import socket
    import time
    from picamera2 import Picamera2
    import imagezmq

    sender = imagezmq.ImageSender(connect_to='tcp://jeff-macbook:5555')

    rpi_name = socket.gethostname() # send RPi hostname with each image
    picam = Picamera2()
    picam.start()
    time.sleep(2)  # allow camera sensor to warm up
    while True:  # send images as stream until Ctrl-C
        image = picam.capture_array()
        sender.send_image(rpi_name, image)


Wow! A video surveillance system with 8 (or more!) Raspberry Pi cameras in
19 lines of Python.

See `About the multiple RPi video streaming examples <docs/more-details.rst>`_
for more details about this example.

.. contents::

Why use imageZMQ?
=================

**imageZMQ** is an easy to use image transport mechanism for a distributed image
processing network. For example, a network of a dozen Raspberry Pis with cameras
can send images to a more powerful central computer. The Raspberry Pis perform
image capture and simple image processing like flipping, blurring and motion
detection. Then the images are passed via **imageZMQ** to the central computer for
more complex image processing like image tagging, text extraction, feature
recognition, etc. An example of using **imageZMQ** can be found
at `Using imageZMQ in distributed computer vision projects <docs/imagezmq-uses.rst>`_.
Each **imageZMQ** message is a ``(text_message, image)`` tuple. The text 
portion of the tuple identifies the source and other info about the image. In 
the example above, the ``text_message`` portion identifies which RPi is sending the
the image so that the receiver can put each unique RPi image stream into a
specific window. More details about the **imageZMQ** tuples in the above exampe
are `here <docs/more-details.rst>`_.

Features
========

- Sends OpenCV images from one computer to another using ZMQ.
- Can send jpeg compressed OpenCV images, to lighten network loads.
- Uses the powerful ZMQ messaging library through PyZMQ bindings.
- Allows a choice of 2 different ZMQ messaging patterns (REQ/REP or PUB/SUB).
- Enables the image hub to receive and process images from multiple image senders
  simultaneously. 

Why ZMQ? Why not some other messaging protocol?
===============================================

There are a number of high quality and well maintained messaging protocols for
passing messages between computers. I looked at MQTT, RabbitMQ, AMQP and ROS as
alternatives. I chose ZMQ and its Python PyZMQ bindings for several reasons:

- ZMQ does not require a message broker. It is a peer to peer protocol that does
  not need to pass an image first to a message broker and then to the imagehub.
  This means fewer running processes and less “double handling” of images.
  OpenCV images are large compared to simple text messages, so the absence of a
  message broker is important.
- ZMQ is very fast for passing OpenCV images. It enables high throughput between
  image senders and image hubs.
- ZMQ and its PyZMQ bindings are easy to install.

**imageZMQ** has been transporting images from a dozen Raspberry Pi computers
scattered around my farm to 2 linux image hub servers for over 5
years. The RPi's capture and send dozens to thousands of frames frames a day.
**imageZMQ** has worked very reliably and is very fast. You can learn more about
my "science experiment urban permaculture farm" project at
`Yin Yang Ranch project overview. <https://github.com/jeffbass/yin-yang-ranch>`_


Messaging Patterns: REQ/REP versus PUB/SUB
==========================================

ZMQ allows many different messaging patterns. Two are implemented in **imageZMQ**:

- REQ/REP: Each RPi sends an image and waits for a REPLY from the central image
  hub. The RPi sends a new image only when the REPLY is received. In the REQ/REP
  messaging pattern, each image sender must await a REPLY before continuing. It is a
  "blocking" pattern for the sender.
- PUB/SUB: Each RPi sends an image, but does not expect a REPLY from the central
  image hub. It can continue sending images without awaiting any acknowledgement
  from the image hub. The image hub provides no REPLY. It is a "non-blocking"
  pattern for the sender.

There are advantages and disadvantages for each pattern. For further details,
see: `REQ/REP versus PUB/SUB Messaging Patterns <docs/req-vs-pub.rst>`_.
**REQ/REP is the default.**


Dependencies and Installation
=============================

+--------------+--------+---------------+-----------+-------+
| |pyversions| | |pypi| | |releasedate| | |license| | |doi| |
+--------------+--------+---------------+-----------+-------+

.. |pyversions| image:: /docs/images/python_versions.svg
   :target: https://pypi.org/project/imagezmq/

.. |pypi| image:: /docs/images/pypi_version.svg
   :target: https://pypi.org/project/imagezmq/

.. |releasedate| image:: /docs/images/release_date.svg
   :target: https://github.com/jeffbass/imagezmq/releases/tag/v1.1.1

.. |license| image::  /docs/images/license.svg
   :target: LICENSE.txt

.. |doi| image::  /docs/images/doi.svg
   :target: https://doi.org/10.5281/zenodo.3840855

**imageZMQ** has been tested with:

- Python 3.5, 3.6, 3.7, 3.8, 3.9, 3.10 and 3.11
- PyZMQ 16.0, 17.1, 19.0 and 26.0
- Numpy 1.13, 1.16, 1.18 and 1.24
- OpenCV 3.3, 4.0, 4.1 and 4.6
- Raspberry Pi OS Bookworm and Bullseye using PiCamera2
- Raspbian OS Buster, Stretch and Raspbian Jessie using legacy PiCamera

OpenCV can be challenging to install. There are many example tutorials on the web. 
For Raspberry Pi computers with current Raspberry Pi OS versions, the Picamera2 
documentation recommends installing OpenCV using apt. 

Be sure to install OpenCV, including Numpy, into a Python Virtual Environment.
Be sure to install **imageZMQ** into the **same** virtual environment. For
example, on a Raspberry Pi running Raspberry Pi OS Bookworm, my virtual
environment is named **py311cv4**.

Install **imageZMQ** using pip:

.. code-block:: bash

    workon py311cv4  # use your virtual environment name
    pip install imagezmq

**imageZMQ** has a directory of tests organized into sender and receiver pairs.
You will get the "tests" directory containing all the test programs by
cloning the GitHub repository:

.. code-block:: bash

    git clone https://github.com/jeffbass/imagezmq.git

Once you have cloned the imagezmq directory to a directory on your local machine,
you can run the tests per the instructions below. You can use imageZMQ in your
own code by importing it (``import imagezmq``).

**imageZMQ** and all of the software dependencies must be installed on the
display computer that will be receiving the images AND it must all be installed
on every Raspberry Pi that will be sending images. If you will be using multiple
Raspberry Pis to capture and send images it is may be helpful to install the
software on a single Raspberry Pi and test it using the tests below. Once all
the tests have run successfully, clone the SD card as needed to use the software
on multiple Raspberry Pis.

Running the Tests to verify **imageZMQ** is working
===================================================

After you have installed **imageZMQ** you will want to verify that it installed
correctly. The best way to do this is to run some of the test programs that are 
in the ``tests`` folder. The most basic test is a matched pair of sending and
receiving programs. The sender program creates a series of OpenCV numbered
images and sends them via **imageZMQ**. The receiving program displays the
numbered images. You can run both of these programs on the same computer first, 
then run them on 2 different computers on the same network. This will confirm
that **imageZMQ** installed correctly and that you are able to specify and open 
ports for transferring OpenCV images between computers. 

There are also test programs that send images from cameras:
1. Raspberry Pi camera module using the PiCamera2 library with Raspberry Pi OS
2. Webcam or USB camera using OpenCV's cv2.VideoCapture to capture images

The Picamera2 library requires Raspberry Pi OS Bullseye or later. There are also
some test programs that use the original Picamera library for older Raspberry Pi
OS versions (Buster and older).

Further details are in `Running the Test Programs <docs/running-tests.rst>`_.

Additional Documentation and Examples
=====================================
- `API and Two Simple Example Programs <docs/api-examples.rst>`_
- `More details about the multiple RPi video streaming example <docs/more-details.rst>`_
- `Running the Test Programs <docs/running-tests.rst>`_
- `REQ/REP versus PUB/SUB Messaging Patterns <docs/req-vs-pub.rst>`_
- `Examples showing different techniques for using imageZMQ <docs/examples.rst>`_
- `Using imageZMQ in distributed computer vision projects <docs/imagezmq-uses.rst>`_
- `FAQ: Frequently Asked Questions <docs/FAQ.rst>`_
- How **imageZMQ** is used in my own projects connecting multiple
  Raspberry Pi **imagenodes** to an **imagehub**:

  - My Yin Yang Ranch project to manage a small urban permaculture farm:
    `Yin Yang Ranch project overview <https://github.com/jeffbass/yin-yang-ranch>`_
  - `imagenode: Capture and Send Images and Sensor Data <https://github.com/jeffbass/imagenode>`_
  - `imagehub: Receive and Store Images and Event Logs <https://github.com/jeffbass/imagehub>`_


I gave a talk about imageZMQ and its use in my Yin Yang Ranch project at
PyCon 2020:
**Jeff Bass - Yin Yang Ranch: Building a Distributed Computer
Vision Pipeline using Python, OpenCV and ZMQ**

`PyCon 2020 Talk Video about the project  <https://youtu.be/76GGZGneJZ4?t=2>`_

`PyCon 2020 Talk Presentation slides  <https://speakerdeck.com/jeffbass/yin-yang-ranch-building-a-distributed-computer-vision-pipeline-using-python-opencv-and-zmq-17024000-4389-4bae-9e4d-16302d20a5b6>`_

Contributing
============
**imageZMQ** is still in active development. I welcome open issues and
pull requests, but because the programs are still evolving, it is best to
open an issue for some discussion before submitting pull requests. We can
exchange ideas about your potential pull request and open a development branch
where you can develop your code and get feedback and testing help from myself
and others. **imageZMQ** is used in my own long running projects and the
projects of others, so backwards compatibility with the existing API is
important.

Contributors
============
Thanks for all contributions big and small. Some significant ones:

+------------------------+-----------------+----------------------------------------------------------+
| **Contribution**       | **Name**        | **GitHub**                                               |
+------------------------+-----------------+----------------------------------------------------------+
| Initial code & docs    | Jeff Bass       | `@jeffbass <https://github.com/jeffbass>`_               |
+------------------------+-----------------+----------------------------------------------------------+
| Added PUB / SUB option | Maksym Bodnar   | `@bigdaddymax <https://github.com/bigdaddymax>`_         |
+------------------------+-----------------+----------------------------------------------------------+
| HTTP Streaming example | Maksym Bodnar   | `@bigdaddymax <https://github.com/bigdaddymax>`_         |
+------------------------+-----------------+----------------------------------------------------------+
| Fast PUB / SUB example | Philipp Schmidt | `@philipp-schmidt <https://github.com/philipp-schmidt>`_ |
+------------------------+-----------------+----------------------------------------------------------+

Helpful Forks of imageZMQ
=========================
Some users have come up with Forks of **imageZMQ** that I think will be helpful
to others, either by using their code or reading their changed code. If
you have developed a fork of **imageZMQ** that demonstrates a concept that
would be helpful to others, please open an issue describing your fork so we
can have a discussion first rather than opening a pull request. Thanks!

+----------------------------+------------+----------------------------------------------------------------------+
| **Helpful Fork**           | **Name**   | **GitHub repository of fork**                                        |
+----------------------------+------------+----------------------------------------------------------------------+
| Add timeouts to image      | Pat Ryan   | `@youngsoul <https://github.com/youngsoul/imagezmq>`_ See CHANGES.md |
| sender to fix restarts or  |            |                                                                      |
| non-response of ImageHub   |            |                                                                      |
+----------------------------+------------+----------------------------------------------------------------------+

Acknowledgements and Thank Yous
===============================
- **ZeroMQ** is a great messaging library with great documentation
  at `ZeroMQ.org <http://zeromq.org/>`_.
- **PyZMQ** serialization examples provided a starting point for **imageZMQ**. See the
  `PyZMQ documentation <https://pyzmq.readthedocs.io/en/latest/index.html>`_.
- **OpenCV** and its Python bindings provide great scaffolding for computer
  vision projects large or small: `OpenCV.org <https://opencv.org/>`_.
- **Picamera2** is a well documented library for accessing the features and
  settings of the PiCamera modules for various Raspberry Pi single board
  computers. 
