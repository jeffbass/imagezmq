===============================================================================
Advanced example showcasing fast pub sub and heavy processing load
===============================================================================

When using the pub sub pattern, the receiver of the frames will always receive
all frames of the publisher. This works as long as the receiver can keep up
with the incoming data. If the receiver needs to do some processing work on the
frames (motion detection, edge detection, maybe even object detection using CNNs)
it can fall behind and will not process the most recent frames from the publisher,
but whatever is still in the receive queue of the zmq socket.

To make sure such a receiver always processes the most recent frames from the publisher,
one could connect, receive a frame and disconnect immediately, to ensure its the most recent frame.
However, this might not be viable, as every connect will introduce an additional delay (e.g. TCP handshake roundtriptime).

A better approach (if network bandwidth is not most concerning) is to keep a connection open,
receive every frame in a dedicated IO thread, but only process the most recent one in a processing thread.

Fast Pub Sub Subscriber
=======================

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

This helper class creates a sub socket in a dedicated IO thread and signals new data via an event.
The main thread can now read the most recent frame by calling receive().

For a full example see `pub_sub_receive.py <../examples/pub_sub_receive.py`_ and `pub_sub_broadcast.py <../examples/pub_sub_broadcast.py`_

`Return to main documentation page README.rst <../README.rst>`_
