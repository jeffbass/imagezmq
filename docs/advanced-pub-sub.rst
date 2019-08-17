=============================================================================
Advanced example of using both messageing patterns in a streaming application
=============================================================================

So far all examples were implying that we receive images on a regular computer
(with a monitor) so we can use functions like ``cv2.imshow()`` to immediately see
a result (the received stream).

However, this is not always an option. Consider the following scenario: multiple cameras send images to a headless server (computer that does not have a monitor and could be located somewhere in datacenter).

We want to be able to connect somehow to this server remotely (ideally using web browser) and check our video streams.

So we want to connect/disconnect to our video streams occasionaly and this should not affect processing of those streams (motion or object detection, recording etc).

Lets see how this can be implemented.

Raspberry code
==============

There will be nothing new on this side:

.. code-block:: python
    :number-lines:
    
    import socket
    import time
    from imutils.video import VideoStream
    import imagezmq

    sender = imagezmq.ImageSender(connect_to='tcp://192.168.0.100:5555')

    rpi_name = socket.gethostname() # send unique RPi hostname with each image
    picam = VideoStream(usePiCamera=True).start()
    time.sleep(2.0)  # allow camera sensor to warm up
    while True:  # send images as stream until Ctrl-C
        image = picam.read()
        sender.send_image(rpi_name, image)    

The script creates an image sender in a default REQ/REP mode that connects to
the server with IP address 192.168.0.100, port 5555 and starts an infinite loop
of reading images from the PI camera and sending them to the server.

Server code (receiving images from the cameras)
==============================================

This code is pretty similar to `test_1_receive_images.py`:

.. code-block:: python
    :number-lines:

    # run this program on the Mac to display image streams from multiple RPis
    import cv2
    import imagezmq

    def processImage(image):
        # Do something useful here, for example, run motion detection and record
        # a stream to a file if detected.
        pass

    # Create a hub for receiving images from cameras
    image_hub = imagezmq.ImageHub()

    # Create a PUB server to send images for monitoring purposes in a non-blocking mode
    stream_monitor = imagezmq.ImageSender(connect_to = 'tcp://*:5566', REQ_REP = False)

    # Start main loop
    while True:
        rpi_name, image = image_hub.recv_image()
        image_hub.send_reply(b'OK')
        processImage(image)
        stream_monitor.send_image(rpi_name, image)

Additional things in this script are lines 14 and 21.

Line 14 - here we create an `ImageSender` object in **PUB/SUB** mode (more about this you can read here_) This object will be used to publish images after they are processed for monitoring (this is done in Line 21).

.. _here: api-examples.rst#two-messaging-patterns-reqrep-and-pubsub

HTTP server code
================

This code handles HTTP requests and can serve video stream from the headless server to your browser.

We use a simple Python library that can handle incoming HTTP connetions to create a very simple HTTP server. Whenever there is an incoming request from the browser we start pulling images from the queue, encode them into a JPEG format and return to the browser as part of `multipart` data.

As a result, we will receive a stream of frames that will assemble into a live video in a browser.

.. code-block:: python
    :number-lines:
    
    import cv2
    import imagezmq
    from werkzeug.wrappers import Request, Response
    from werkzeug.serving import run_simple
    
    def sendImagesToWeb():
        # When we have incoming request, create a receiver and subscribe to a publisher
        receiver = imagezmq.ImageHub(open_port='tcp://localhost:5566', REQ_REP = False)
        while True:
            # Pull an image from the queue
            camName, frame = receiver.recv_image()
            # Using OpenCV library create a JPEG image from the frame we have received 
            jpg = cv2.imencode('.jpg', frame)[1]
            # Convert this JPEG image into a binary string that we can send to the browser via HTTP
            yeild b'--frame\r\nContent-Type:image/jpeg\r\n\r\n'+jpg.tostring()+b'\r\n'
   
    # Add `application` method to Request class and define this method here
    @Request.application
    def application(request):
        # What we do is we `sendImagesToWeb` as Iterator (generator) and create a Response object
        # based on its output.
        return Response(sendImagesToWeb(), mimetype='multipart/x-mixed-replace; boundary=frame')

    if __name__ == '__main__':
        # This code starts simple HTTP server that listens on interface with IP 192.168.0.114, port 4000
        run_simple('192.168.0.114', 4000, application)


