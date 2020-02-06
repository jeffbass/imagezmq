======================
API and Usage Examples
======================

The API for **imagezmq** consists of 2 classes with 2 methods each. The
ImageSender class has 2 methods: one for sending an OpenCV image and one for
sending a jpg compressed OpenCV image. The ImageHub class has 2 methods: one for
receiving an OpenCV image and one for receiving a jpg compressed OpenCV image.

Each ImageSender/ImageHub pair can work in one of following modes: REQ/REP or PUB/SUB.
The mode is selected when ImageSender and ImageHub are instantiated by setting
REQ_REP parameter in constructor to *True* or *False*.
**REQ/REP mode is the default**.
There are advantages and disadvantages for each pattern. For further details,
see: `REQ/REP versus PUB/SUB Messaging Patterns <docs/req-vs-pub.rst>`_.


imagezmq API
============

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
      Opens a zmq socket on the hub computer (REP type if REQ_REP = True,
      SUB type otherwise), for example, a Mac, that will be receiving and
      displaying or processing OpenCV images and related text messages.
      Provides methods to receive images or receive jpg compressed images.

      Arguments:
        open_port: (optional) the socket to open for receiving REQ requests.
        REQ_REP: (optional) whether to use REQ/REP messaging pattern or not.
        Example: REQ_REP = True (default) The Hub will be
                 use a REQ/REP pattern.
                 REQ_REP = False The Hub will use a PUB/SUB
                 pattern


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

The simple test and example programs mentioned below show how to use the API.
The programs are found in the tests folder.

The programs ``timing_send_images.py`` and ``timing_receive_images.py`` provide
examples of how to use the **imagezmq** API to send and receive OpenCV
images.  The programs show a simple **imagezmq** use case.
Additional image processing in the sending program would typically be placed
between the ``picam.read()`` and the ``sender.send_image()`` lines. Such processing
would be done with calls to methods for image rotation, resizing,
dilation, etc. from an application specific image processing class.

The programs ``timing_send_jpg_buf`` and ``timing_receive_jpg_buf`` show how
**imagezmq** would be used to send jpg compressed OpenCV images to reduce
network load. The current API requires that the conversion from OpenCV image
format to a jpg bytestring be done by the application program. This may
change in the future. The 2 example programs show how to
perform the conversion using OpenCV's ``cv2.imencode()`` and ``cv2.imdecode()``
methods.

=====================================================================
Using both messaging patterns together in a web streaming application
=====================================================================

It is possible to use both the REQ/REP and PUB/SUB patters in the same
application. That way, part of the application can be tightly coupled (and
therefore blocking) using REQ/REP while another part can be a non-blocking
web stream using PUB/SUB. Example programs are included in the tests folder.
There is a detailed explanation of these web streaming example programs
`here <advanced-pub-sub.rst>`_.


`Return to main documentation page README.rst <../README.rst>`_
