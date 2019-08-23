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

ImageSender/ImageHub pair can work in one of following modes: REQ/REP or PUB/SUB.
The mode is selected when ImageSender and ImageHub are instantiated by setting
REQ_REP parameter in constructor to *True* or *False*. REQ/REP mode is a default one.

Two messaging patterns: REQ/REP and PUB/SUB
========================================== 

These two modes (or to be more precise,  messaging patterns) are very similar: 
both are used to send images from sender to receiver. But the behaviour of the 
sender and receiver is pretty different.

**REQ/REP** pattern guarantees image delivery from sender to recipient: sender
reception confirmation from recipient before next image is sent. This feature
makes the code blocking. This means that if a recipient for some reason does not
reply sender will stop execution (it will be blocked).

Another interesting moment about REQ/REP pattern is that one recipient can receive
images from many senders, however one sender can send images only to single 
recipient (one-to-many relation). This feature helps a lot in dynamic environment
when you know address of the hub (computer where ImageHub runs), but addresses of 
senders (computers or RPIs on which ImageSender runs) can change dynamically (for
example, you use DHCP and RPIs tend to reboot time to time). 

**PUB/SUB** in contrast is a non-blocking pattern with a not guaranteed delivery.
Sender does not expect confirmation from recipient, even more, sender will continue
sending images event if there is no recipients at all (images will be discaded 
right away by underlying library, so you should not worry about memory leaks).

Also, PUB/SUB pattern support a many-to-many relations. One sender can send to many 
recipients and each recipient can receive images from many senders. 

However, from configuration point of view this pattern requires more planning: 
each sender is an image server and ImageHub should explicitly subscribe to them
so you have to know addresses of all senders (no dynamic discoveries).

Taking described differences into account you can chose appropriate pattern for
your application: use REQ/REP pattern for images delivery from cameras to central 
hub; use PUB/SUB pattern to detach some processing code from sensitive or time
critical parts.

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

Difference between REQ/REP and PUB/SUB
=====================================

To demonstrate the difference between two messaging patterns you can run two 
examples from tests folder: ``test_1_send_image.py``/``test_1_receive_image.py``
for a REQ/REP pattern and ``test_1_pub.py``/``test_1_sub.py`` for a PUB/SUB pattern.

If you run ``test_1_send_image.py`` and ``test_1_receive_image.py`` scripts in a
separate console windows you should see incremental output on the sender window::

   Sending 1
   Sending 2
   ...
etc

And the receiver should open a window and display an incrementing number that should
correspond to whatever you see on the sender screen.

Now if you stop receiver you should notice that sender will stop printing "Sending XX".
The sender will block until recipient is started again. And recipient window should 
continue from the moment where it was stoped.

Now use the ``test_1_pub.py`` and ``test_1_sub.py`` pair. You should see the same 
"Sending XX" printed on the sender window and corresponding number incrementing on
recipient window.

However, now if you close the recipient script the sender will continue printing and
incrementing the value.

And if you start the recipient again it will just pick from the current position.

`Return to main documentation page README.rst <../README.rst>`_
