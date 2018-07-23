======================
API and Usage Examples
======================

The API for **imagezmq** consists of 2 classes with 2 methods each. The
ImageSender class has 2 methods: one for sending an OpenCV image and one for
sending a jpg compressed OpenCV image. The ImageHub class has 2 methods: one for
receiving an OpenCV image and one for receiving a jpg compressed OpenCV image.
**imagezmq** is in early development as part of a larger system. There are
currently separate methods for sending and receiving images vs. jpg compressed
images. Further development will refactor these into single methods for sending
and receiving.

.. code-block:: python
  :number-lines:

  class ImageSender(connect_to='tcp://127.0.0.1:5555'):
      Opens a zmq REQ socket on the image sending computer, typically a
      Raspberry Pi, that will be sending OpenCV images and
      related text messages to the hub computer. Provides methods to
      send images or send jpg compressed images.

      Arguments:
        connect_to: the tcp address and port of the hub computer
             Example format: connect_to='tcp://192.168.1.17:5555'
             Example format: connect_to='tcp://jeff-macbook:5555'

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

  class ImageHub(open_port='tcp://:5555'):
      Opens a zmq REP socket on the hub computer, for example,
      a Mac, that will be receiving and displaying or processing OpenCV images
      and related text messages. Provides methods to receive images or receive
      jpg compressed images.

      Arguments:
        open_port: (optional) the socket to open for receiving REQ requests.

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
mentioned below show how to use the API. The programs are found in the tests
folder.

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
format to a jpg bytestring be done by the application program. This will likely
change in the future. The 2 example programs show how to
perform the conversion using OpenCV's ``cv2.imencode()`` and ``cv2.imdecode()``
methods.

`Return to main documentation page README.rst <../README.rst>`_
