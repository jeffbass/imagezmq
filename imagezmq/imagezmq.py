""" imagezmq: Transport OpenCV images via ZMQ.

Classes that transport OpenCV images from one computer to another. For example,
OpenCV images gathered by a Raspberry Pi camera could be sent to another
computer for displaying the images using cv2.imshow() or for further image
processing. See API and Usage Examples for details.

Copyright (c) 2019 by Jeff Bass.
License: MIT, see LICENSE for more details.
"""

import zmq
import numpy as np
import cv2


class ImageSender():
    """Opens a zmq socket and sends images

    Opens a zmq (REQ or PUB) socket on the image sending computer, often a
    Raspberry Pi, that will be sending OpenCV images and
    related text messages to the hub computer. Provides methods to
    send images or send jpg compressed images.

    Two kinds of ZMQ message patterns are possible in imagezmq:
    REQ/REP: an image is sent and the sender waits for a reply ("blocking").
    PUB/SUB: an images is sent and no reply is sent or expected ("non-blocking").

    There are advantabes and disadvantages for each message pattern.
    See the documentation for a full description of REQ/REP and PUB/SUB.
    The default is REQ/REP for the ImageSender class and the ImageHub class.

    Arguments:
      connect_to: the tcp address:port of the hub computer.
      REQ_REP: (optional) if True (the default), a REQ socket will be created
                          if False, a PUB socket will be created
    """

    def __init__(self, connect_to='tcp://127.0.0.1:5555', REQ_REP = True):
        """Initializes zmq socket for sending images to the hub.

        Expects an appropriate ZMQ socket at the connect_to tcp:port address:
        If REQ_REP is True (the default), then a REQ socket is created. It
        must connect to a matching REP socket on the ImageHub().

        If REQ_REP = False, then a PUB socket is created. It must connect to
        a matching SUB socket on the ImageHub().
        """

        if REQ_REP == True:
             # REQ/REP mode, this is a blocking scenario
             self.init_reqrep(connect_to)
        else:
             #PUB/SUB mode, non-blocking scenario
             self.init_pubsub(connect_to)

    def init_reqrep(self, address):
        """ Creates and inits a socket in REQ/REP mode
        """

        socketType = zmq.REQ
        self.zmq_context = SerializingContext()
        self.zmq_socket = self.zmq_context.socket(socketType)
        self.zmq_socket.connect(address)

        # Assign corresponding send methods for REQ/REP mode
        self.send_image = self.send_image_reqrep
        self.send_jpg   = self.send_jpg_reqrep

    def init_pubsub(self, address):
        """Creates and inits a socket in PUB/SUB mode
        """

        socketType = zmq.PUB
        self.zmq_context = SerializingContext()
        self.zmq_socket = self.zmq_context.socket(socketType)
        self.zmq_socket.bind(address)

        # Assign corresponding send methods for PUB/SUB mode
        self.send_image = self.send_image_pubsub
        self.send_jpg   = self.send_jpg_pubsub

    def send_image(self, msg, image):
        """ This is a placeholder. This method will be set to either a REQ/REP
        or PUB/SUB sending method, depending on REQ_REP option value.

        Arguments:
          msg: text message or image name.
          image: OpenCV image to send to hub.

        Returns:
          A text reply from hub in REQ/REP mode or nothing in PUB/SUB mode.

        """
        pass

    def send_image_reqrep(self, msg, image):
        """Sends OpenCV image and msg to hub computer in REQ/REP mode

        Arguments:
          msg: text message or image name.
          image: OpenCV image to send to hub.

        Returns:
          A text reply from hub.
        """

        if image.flags['C_CONTIGUOUS']:
            # if image is already contiguous in memory just send it
            self.zmq_socket.send_array(image, msg, copy=False)
        else:
            # else make it contiguous before sending
            image = np.ascontiguousarray(image)
            self.zmq_socket.send_array(image, msg, copy=False)
        hub_reply = self.zmq_socket.recv()  # receive the reply message
        return hub_reply

    def send_image_pubsub(self, msg, image):
        """Sends OpenCV image and msg hub computer in PUB/SUB mode. If
        there is no hub computer subscribed to this socket, then image and msg
        are discarded.

        Arguments:
          msg: text message or image name.
          image: OpenCV image to send to hub.

        Returns:
          Nothing; there is no reply from hub computer in PUB/SUB mode
        """

        if image.flags['C_CONTIGUOUS']:
            # if image is already contiguous in memory just send it
            self.zmq_socket.send_array(image, msg, copy=False)
        else:
            # else make it contiguous before sending
            image = np.ascontiguousarray(image)
            self.zmq_socket.send_array(image, msg, copy=False)

    def send_jpg(self, msg, jpg_buffer):
        """This is a placeholder. This method will be set to either a REQ/REP
        or PUB/SUB sending method, depending on REQ_REP option value.

        Arguments:
          msg: image name or message text.
          jpg_buffer: bytestring containing the jpg image to send to hub.

        Returns:
          A text reply from hub in REQ/REP mode or nothing in PUB/SUB mode.
        """

    def send_jpg_reqrep(self, msg, jpg_buffer):
        """Sends msg text and jpg buffer to hub computer in REQ/REP mode.

        Arguments:
          msg: image name or message text.
          jpg_buffer: bytestring containing the jpg image to send to hub.

        Returns:
          A text reply from hub.
        """

        self.zmq_socket.send_jpg(msg, jpg_buffer, copy=False)
        hub_reply = self.zmq_socket.recv()  # receive the reply message
        return hub_reply

    def send_jpg_pubsub(self, msg, jpg_buffer):
        """Sends msg text and jpg buffer to hub computer in PUB/SUB mode. If
        there is no hub computer subscribed to this socket, then image and msg
        are discarded.

        Arguments:
          msg: image name or message text.
          jpg_buffer: bytestring containing the jpg image to send to hub.

        Returns:
          Nothing; there is no reply from the hub computer in PUB/SUB mode.
        """

        self.zmq_socket.send_jpg(msg, jpg_buffer, copy=False)


class ImageHub():
    """Opens a zmq socket and receives images

    Opens a zmq (REP or SUB) socket on the hub computer, for example,
    a Mac, that will be receiving and displaying or processing OpenCV images
    and related text messages. Provides methods to receive images or receive
    jpg compressed images.

    Two kinds of ZMQ message patterns are possible in imagezmq:
    REQ/REP: an image is sent and the sender waits for a reply ("blocking").
    PUB/SUB: an images is sent and no reply is sent or expected ("non-blocking").

    There are advantabes and disadvantages for each message pattern.
    See the documentation for a full description of REQ/REP and PUB/SUB.
    The default is REQ/REP for the ImageSender class and the ImageHub class.

    Arguments:
      open_port: (optional) the socket to open for receiving REQ requests or
                 socket to connect to for SUB requests.
      REQ_REP: (optional) if True (the default), a REP socket will be created
                          if False, a SUB socket will be created
    """

    def __init__(self, open_port='tcp://*:5555', REQ_REP = True):
        """Initializes zmq socket to receive images and text.

        Expects an appropriate ZMQ socket at the senders tcp:port address:
        If REQ_REP is True (the default), then a REP socket is created. It
        must connect to a matching REQ socket on the ImageSender().

        If REQ_REP = False, then a SUB socket is created. It must connect to
        a matching PUB socket on the ImageSender().

        """
        self.REQ_REP = REQ_REP
        if REQ_REP ==True:
            #Init REP socket for blocking mode
            self.init_reqrep(open_port)
        else:
            #Connect to PUB socket for non-blocking mode
            self.init_pubsub(open_port)

    def init_reqrep(self, address):
        """ Initializes Hub in REQ/REP mode
        """
        socketType = zmq.REP
        self.zmq_context = SerializingContext()
        self.zmq_socket = self.zmq_context.socket(socketType)
        self.zmq_socket.bind(address)

    def init_pubsub(self, address):
       """ Initialize Hub in PUB/SUB mode
       """
       socketType = zmq.SUB
       self.zmq_context = SerializingContext()
       self.zmq_socket = self.zmq_context.socket(socketType)
       self.zmq_socket.setsockopt(zmq.SUBSCRIBE, b'')
       self.zmq_socket.connect(address)

    def connect(self, open_port):
        """In PUB/SUB mode, the hub can connect to multiple senders at the same
        time.
        Use this method to connect (and subscribe) to additional senders.

        Arguments:
             open_port: the PUB socket to connect to.
        """

        if self.REQ_REP == False:
            #This makes sense only in PUB/SUB mode
            self.zmq_socket.setsockopt(zmq.SUBSCRIBE, b'')
            self.zmq_socket.connect(open_port)
            self.zmq_socket.subscribe(b'')
        return

    def recv_image(self, copy=False):
        """Receives OpenCV image and text msg.

        Arguments:
          copy: (optional) zmq copy flag.

        Returns:
          msg: text msg, often the image name.
          image: OpenCV image.
        """

        msg, image = self.zmq_socket.recv_array(copy=False)
        return msg, image

    def recv_jpg(self, copy=False):
        """Receives text msg, jpg buffer.

        Arguments:
          copy: (optional) zmq copy flag
        Returns:
          msg: text message, often image name
          jpg_buffer: bytestring jpg compressed image
        """

        msg, jpg_buffer = self.zmq_socket.recv_jpg(copy=False)
        return msg, jpg_buffer

    def send_reply(self, reply_message=b'OK'):
        """Sends the zmq REP reply message.

        Arguments:
          reply_message: reply message text, often just string 'OK'
        """
        self.zmq_socket.send(reply_message)


class SerializingSocket(zmq.Socket):
    """Numpy array serialization methods.

    Modelled on PyZMQ serialization examples.

    Used for sending / receiving OpenCV images, which are Numpy arrays.
    Also used for sending / receiving jpg compressed OpenCV images.
    """

    def send_array(self, A, msg='NoName', flags=0, copy=True, track=False):
        """Sends a numpy array with metadata and text message.

        Sends a numpy array with the metadata necessary for reconstructing
        the array (dtype,shape). Also sends a text msg, often the array or
        image name.

        Arguments:
          A: numpy array or OpenCV image.
          msg: (optional) array name, image name or text message.
          flags: (optional) zmq flags.
          copy: (optional) zmq copy flag.
          track: (optional) zmq track flag.
        """

        md = dict(
            msg=msg,
            dtype=str(A.dtype),
            shape=A.shape,
        )
        self.send_json(md, flags | zmq.SNDMORE)
        return self.send(A, flags, copy=copy, track=track)

    def send_jpg(self,
                 msg='NoName',
                 jpg_buffer=b'00',
                 flags=0,
                 copy=True,
                 track=False):
        """Send a jpg buffer with a text message.

        Sends a jpg bytestring of an OpenCV image.
        Also sends text msg, often the image name.

        Arguments:
          msg: image name or text message.
          jpg_buffer: jpg buffer of compressed image to be sent.
          flags: (optional) zmq flags.
          copy: (optional) zmq copy flag.
          track: (optional) zmq track flag.
        """

        md = dict(msg=msg, )
        self.send_json(md, flags | zmq.SNDMORE)
        return self.send(jpg_buffer, flags, copy=copy, track=track)

    def recv_array(self, flags=0, copy=True, track=False):
        """Receives a numpy array with metadata and text message.

        Receives a numpy array with the metadata necessary
        for reconstructing the array (dtype,shape).
        Returns the array and a text msg, often the array or image name.

        Arguments:
          flags: (optional) zmq flags.
          copy: (optional) zmq copy flag.
          track: (optional) zmq track flag.

        Returns:
          msg: image name or text message.
          A: numpy array or OpenCV image reconstructed with dtype and shape.
        """

        md = self.recv_json(flags=flags)
        msg = self.recv(flags=flags, copy=copy, track=track)
        A = np.frombuffer(msg, dtype=md['dtype'])
        return (md['msg'], A.reshape(md['shape']))

    def recv_jpg(self, flags=0, copy=True, track=False):
        """Receives a jpg buffer and a text msg.

        Receives a jpg bytestring of an OpenCV image.
        Also receives a text msg, often the image name.

        Arguments:
          flags: (optional) zmq flags.
          copy: (optional) zmq copy flag.
          track: (optional) zmq track flag.

        Returns:
          msg: image name or text message.
          jpg_buffer: bytestring, containing jpg image.
        """

        md = self.recv_json(flags=flags)  # metadata text
        jpg_buffer = self.recv(flags=flags, copy=copy, track=track)
        return (md['msg'], jpg_buffer)


class SerializingContext(zmq.Context):
    _socket_class = SerializingSocket
