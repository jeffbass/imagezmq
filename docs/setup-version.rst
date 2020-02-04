======================================================
Installing imagezmq: setup.py and __version__.py Files
======================================================

The installation

setup.py does and __version__.py

TwSubtitle
==========================================

These two modes (or to be more precise,  messaging patterns) are very similar:
to  parts.

.. code-block:: python
  :number-lines:

  class ImageSender(connect_to='tcp://127.0.0.1:5555', REQ_REP = True):
      Opens a zmq socket (REQ type if REQ_REP == True, PUB type if REQ_REP == False)
      on the image sending computer, typically a Raspberry Pi, that will be sending
      OpenCV images and related text messages to the hub computer. Provides methods
      to send images or send jpg compressed images.

      Arguments:
        connect_to: the tcp address and port of the hub computer
             Example format: connect_to='tcp://192.168.1.17:5555'
             Example format: connect_to='tcp://jeff-macbook:5555'
        REQ_REP: whether to use REQ/REP messaging pattern or not.
             Example: REQ_REP = True (default) The sender will be
                      use a REQ/REP pattern.
                      REQ_REP = False The sender will use a PUB/SUB
                      pattern

      send_image(self, msg, image):
          Sends OpenCV image and msg to hub computer.

          Arguments:
            msg: text message or image name.
            image: OpenCV image to send to hub.
          Returns:
            A text reply from hub.

      send_jpg(self, msg, jpg_buffer):
          Sends msg text and jpg buffer to hub computer.

          Arguments:
            msg: image name or message text.
            jpg_buffer: bytestring containing the jpg image to send to hub.
          Returns:
            A text reply from hub.

  class ImageHub(open_port='tcp://:5555', REQ_REP = True):
      Opens a zmq socket on the hub computer (REP type is REQ_REP = True,
      SUB type otherwise), for example, a Mac, that will be receiving and
      displaying or processing OpenCV images and related text messages.
      Provides methods to receive images or receive jpg compressed images.

      Arguments:
        open_port: (optional) the socket to open for receiving REQ requests.
        REQ_REP: (optional) whether to use REQ/REP messaging pattern or not.

      recv_image(self, copy=False):
          Receives OpenCV image and text msg.

          Arguments:
            copy: (optional) zmq copy flag.
          Returns:
            msg: text msg, often the image name.
            image: OpenCV image.

      recv_jpg(self, copy=False):
          Receives text msg, jpg buffer.

          Arguments:
            copy: (optional) zmq copy flag
          Returns:
            msg: text message, often image name
            jpg_buffer: bytestring jpg compressed image

      send_reply(self, reply_message=b'OK'):
          Sends the zmq REP reply message.

          Arguments:
            reply_message: reply message text, often just the string 'OK'

Usage Examples
==============

While additional programs using **imagezmq** are being developed, the programs
mentioned bample programs show how to
perform the conversion using OpenCV's ``cv2.imencode()`` and ``cv2.imdecode()``
methods.

Difference between REQ/REP and PUB/SUB
=====================================

To demonstrate the difference between two messaging patterns you can run two
examples fro it was stoped.

Now use the ``test_1_pub.py`` and ``test_1_sub.py`` pair. You should see the same
"Sending XX" printed on the sender window and corresponding number incrementing on
recipient window.

However, now if you close the recipient script the sender will continue printing and
incrementing the value.

And if you start the recipient again it will just pick from the current position.

`Return to main documentation page README.rst <../README.rst>`_
