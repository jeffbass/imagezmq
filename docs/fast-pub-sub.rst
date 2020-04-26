===============================================================================
PUB/SUB Multithreaded Fast Subscribers for Realtime Processing
===============================================================================

When using the PUB/SUB pattern, the receiver of the frames will always receive
all frames of the publisher. This works as long as the receiver can keep up
with the incoming data. If the receiver needs to do some processing work on the
frames (motion detection, edge detection, maybe even object detection using CNNs)
it can fall behind and will not process the most recent frames from the publisher,
but whatever is still in the receive queue of the zmq socket.

To make sure such a receiver always processes the most recent frames from the
publisher, one could connect, receive a frame and disconnect immediately, to
ensure its the most recent frame. However, this might neither be viable nor
elegant, as every connect will introduce an additional delay (e.g. TCP handshake
round-trip-time).

A better approach (if network bandwidth is not most concerning) is to keep the
socket open, receive every frame in a dedicated IO thread, but only process the
most recent one in a processing thread. This is possible with this helper class:

Fast Pub Sub Subscriber Helper Class
====================================

.. code-block:: python
    :number-lines:

    class VideoStreamSubscriber:

        def __init__(self, hostname, port):
            self.hostname = hostname
            self.port = port
            self._stop = False
            self._data_ready = threading.Event()
            self._thread = threading.Thread(target=self._run, args=())
            self._thread.daemon = True
            self._thread.start()

        def receive(self, timeout=15.0):
            flag = self._data_ready.wait(timeout=timeout)
            if not flag:
                raise TimeoutError(
                    f"Timeout while reading from subscriber tcp://{self.hostname}:{self.port}")
            self._data_ready.clear()
            return self._data

        def _run(self):
            receiver = imagezmq.ImageHub(f"tcp://{self.hostname}:{self.port}", REQ_REP=False)
            while not self._stop:
                self._data = receiver.recv_jpg()
                self._data_ready.set()
            # Close socket here, not implemented in ImageHub :(
            # zmq_socket.close()

        def close(self):
            self._stop = True

This helper class creates a sub socket in a dedicated IO thread and signals new
data via an event. The main thread can read the most recent frame by calling
receive().

A timeout can be configured, after which the connection must be considered down.
Keep in mind that in line with the ZMQ socket behavior, there is no way of
checking whether the connection was established successfully. If the first call
to receive creates a timeout, the connection might not have been established
or the publisher is not sending frames (...fast enough?).

The event synchronization in this class makes sure a single frame will never be
read twice.

Please note that this class is not thread-safe, as there is only a single event
for new data.

For a full example see `pub_sub_receive.py <../examples/pub_sub_receive.py>`_ and `pub_sub_broadcast.py <../examples/pub_sub_broadcast.py>`_

`Return to main documentation page README.rst <../README.rst>`_
