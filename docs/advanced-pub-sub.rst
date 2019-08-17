=============================================================================
Advanced example of using both messageing patterns in a streaming application
=============================================================================

So far all examples were implying that we receive images on a regular computer
(with a monitor) so we can use functions like cv2.imshow() to immediately see
a result (to see the received streem).

However, this is not always an option. Consider following scenario: multiple cameras
send images to a server, which is processing them (for example, performs motion
detection, objects analisys etc). The server is headless (ideally, on a remote 
facility). So you need a tool to check streams occasionaly. Lets see how we could
implement this.

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

Also, almost nothing new here:

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


