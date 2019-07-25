""" imagezmq: Transport OpenCV images via ZMQ.

Classes that transport OpenCV images from one computer to another. For example,
OpenCV images gathered by a Raspberry Pi camera could be sent to another
computer for displaying the images using cv2.imshow() or for further image
processing. See API and Usage Examples for details.

Copyright (c) 2017 by Jeff Bass.
License: MIT, see LICENSE for more details.
"""

import zmq
import numpy as np
import cv2


class ImageSender():
    """In blocking mode (block = True, default setting) opens zmq REQ socket
       and sends images.

    Opens a zmq REQ socket on the image sending computer, often a
    Raspberry Pi, that will be sending OpenCV images and
    related text messages to the hub computer. Provides methods to
    send images or send jpg compressed images.

    In a non-blocking mode (block = False) creates a PUB socket 

    Arguments:
      connect_to: the tcp address:port of the hub computer.
      block:      defines if the sender is intialized in blocking or 
                  non-blocking mode
    """

    def __init__(self, connect_to='tcp://127.0.0.1:5555', block = True):
        """Initializes zmq socket for sending images to the hub.

        Expects an open socket at the connect_to tcp address; it will
        connect to that remote socket after setting up the REQ
        socket on this computer.

        By default, creates sender for REQ/REP (blocking mode) 
        
        If block = False, creates a publisher (PUB socket).
        """
        self.block = block
        if block == True:
             # REQ/REP mode, this is a blocking scenario
             socketType = zmq.REQ
             self.zmq_context = SerializingContext()
             self.zmq_socket = self.zmq_context.socket(socketType)
             self.zmq_socket.connect(connect_to)
        else:
             #PUB/SUB mode, non-blocking scenario
             socketType = zmq.PUB
             self.zmq_context = SerializingContext()
             self.zmq_socket = self.zmq_context.socket(socketType)
             self.zmq_socket.bind(connect_to)

    def send_image(self, msg, image):
        """Sends OpenCV image and msg to hub computer (REQ/REP mode)
        or publishes image and msg to PUB socket in PUB/SUB mode. If
        there is no subscriptions to this socket image and msg are
        discarded.

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
        if self.block == False:
            #In case of PUB/SUB mode just return, we do not expect anything from a subscriber
            return
        hub_reply = self.zmq_socket.recv()  # receive the reply message
        return hub_reply

    def send_jpg(self, msg, jpg_buffer):
        """Sends msg text and jpg buffer to hub computer.

        Arguments:
          msg: image name or message text.
          jpg_buffer: bytestring containing the jpg image to send to hub.
        Returns:
          A text reply from hub.
        """

        self.zmq_socket.send_jpg(msg, jpg_buffer, copy=False)
        if self.block == False:
            #In PUB/SUB mode just return, we do not expext anything from a subscriber
            return
        hub_reply = self.zmq_socket.recv()  # receive the reply message
        return hub_reply


class ImageHub():
    """If created in blocking mode, opens zmq REP socket and receives images.
    If created in non-blocking mode, tries to subscribe to a PUB socket.

    Opens a zmq REP socket on the hub compuer, for example,
    a Mac, that will be receiving and displaying or processing OpenCV images
    and related text messages. Provides methods to receive images or receive
    jpg compressed images.

    Arguments:
      open_port: (optional) the socket to open for receiving REQ requests or 
                 socket to connect to for SUB requests.
      block:     if set to True (default) the hub will connect to REP socket, 
                 will wait for messages and will send acknowlegements upon
                 successful message reception.
                 If set to False the hub will try to subscribe to PUB socket
                 and will wait for images. No acknowlegements will be sent 
                 back to sender upon successful reception.
    """

    def __init__(self, open_port='tcp://*:5555', block = True):
        """Initializes zmq REP or connects to PUB  socket to receive images and text.
        """
        self.block = block
        if block ==True:
            #Init REP socket for blocking mode
            socketType = zmq.REP
            self.zmq_context = SerializingContext()
            self.zmq_socket = self.zmq_context.socket(socketType)
            self.zmq_socket.bind(open_port)
        else:
            #Connect to PUB socket for non-blocking mode
            socketType = zmq.SUB
            self.zmq_context = SerializingContext()
            self.zmq_socket = self.zmq_context.socket(socketType)
            self.zmq_socket.setsockopt(zmq.SUBSCRIBE, b'')
            r = self.zmq_socket.connect(open_port)

    """In PUB/SUB mode one hub can connect to multiple senders at the same time
       Use this method to connect (and subscribe) to senders
      
       Arguments:
         open_port: the PUB socket to connect to.
    """
    def connect(self, open_port):
        """Connect to another PUB socket to receive images (one subscriver
           can connect/subsribe to multiple publishers) 
        """
        if self.block == False:
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
