Running the Older Picamera / imutils Tests
==========================================

Prior to Raspberry Pi OS Bullseye, the original Picamera Python module was used.
The original **imageZMQ** test programs used the original PiCamera Python module
by using an ``imutils`` Python module. However, both Picamera and imutils are 
no longer working with the Raspberry Pi OS Bullseye or Bookworm or later versions. 
The Picamera2 module is now the standard way to access the Raspberry Pi camera 
module. All the **imageZMQ** test programs have been converted to the Picamera2
module. However, if you are using an older Raspberry Pi OS (Buster or older), 
the orignal Picamera / imutils test programs are in the old_tests folder.

As of July 2024, these older **imageZMQ** test programs are still 
working fine on several RPis we have running the older RPi OS versions. The older
programs are not being updated, since Picamera2 has become standard. But if you 
want to continue to use **imageZMQ** with the original Picamera module, you can
run the test programs in the ``old_tests`` folder. 

When running the tests, use multiple terminal windows on the computer that will
be displaying the images (I used a Mac for these examples; in my descriptions
I use the term "Mac" to refer to any Mac or Linux computer, including a
Raspbery Pi). One terminal window is used to launch the programs that run on the
Mac to receive the images. Another terminal window on the Mac is used to ssh
into the Raspberry Pi and run the image sending program. If sending from multiple
Raspberry Pis, ssh to each Raspberry Pi in a new terminal window. **imageZMQ**
and its dependencies must be installed on the Mac and on each Raspberry Pi that
will be sending images.

There are 3 tests. Each of the tests uses 2 programs in matched pairs. One
program sends images and the other program displays images. Because of the
REQ/REP pattern that is being used, it is important that the receiving program
be started before the sending program.

Test 1: Simple generated images sent and displayed on Mac
---------------------------------------------------------

**The first test** runs both the sending program and the receiving program on
the Mac. This confirms that all the software is installed correctly and that
``cv2.imshow()`` works on the Mac. No Raspberry Pi or camera is involved. The
sending program generates test images and sends them to the receiving program.
First, in one terminal window, activate your virtual environment, then change to
the tests directory and run the receiving program, which will receive and
display images::

    workon py3cv3  # use your virtual environment name
    cd imagezmq/tests
    python test_1_receive_images.py

Then, in a second terminal window on the same display computer (Mac), change to
the tests directory and run the sending program, which will generate and send
images::

    workon py3cv3  # use your virtual environment name
    cd imagezmq/tests
    python test_1_send_images.py

After a few seconds, a ``cv2.imshow()`` window should open and display a green
square on a black background. There will be a yellow number in the green square
that will increase (1, 2, ...) once per second until you stop both
programs by pressing Ctrl-C. It is normal to get a cascade of error messages
when stopping the program with Ctrl-C. This simple test program has no
try / except error trapping.

Test 2: Sending stream of OpenCV images from RPi(s) to Mac
----------------------------------------------------------

**The second test** runs the sending program on a Raspberry Pi, capturing
images from the PiCamera at up to 32 frames a second and sending them via
**imageZMQ** to the Mac. The receiving program on the Mac displays a continuous
video stream of the images captured by the Raspberry Pi. First, in one terminal
window, activate your virtual environment, change to the tests directory and
run the receiving program which will display the images::

    workon py3cv3  # use your virtual environment name
    cd imagezmq/tests
    python test_2_receive_images.py

Then, in a second terminal window on the Mac, ssh into the Raspberry Pi that
will be sending images. Activate your Python virtual environment, change to the
tests directory and **edit the test_2_send_images.py program to specify the tcp
address of your display computer.** There are 2 lines in the program that show
different ways of specifying the tcp address: by hostname or by tcp numeric address.
Pick one method, change the tcp address to that of your display computer and
comment out the method you are not using. Finally, run the program, which will
capture and send images::

    workon py3cv3  # use your virtual environment name
    cd imagezmq/tests
    python test_2_send_images.py

In about 5 seconds, a ``cv2.imshow()`` window will appear on the Mac and display
the video stream being sent by the Raspberry Pi.  You can repeat this step in
additional terminal windows, to ssh into additional Raspberry Pi computers and
start additional video streams. The receiving program can receive and display
images from multiple Raspberry Pis, with each Raspberry Pi's image stream
showing in a separate window. For this to work, each Raspberry Pi must have a
unique hostname because the images are sorted into different
``cv2.imshow()`` windows based on the hostname. The ``cv2.imshow()`` windows
for multiple Raspberry Pi streams will be stacked on top of each other until you
drag them and arrange them on your desktop. The example picture at the start of
this documentation shows 8 simultaneous video streams for 8 Raspberry Pi
computers with different hostnames. Each program must be stopped by pressing
Ctrl-C in its terminal window. It is normal to get a cascade of error messages
when stopping these programs with Ctrl-C. This simple test program has no try /
except error trapping.

Test 3: Sending stream of jpgs from RPi(s) to Mac
-------------------------------------------------

**The third test** runs a different pair of sending / receiving programs. The
program on the Raspberry Pi captures images from the PiCamera at up to 32
frames a second and **compresses them to jpeg form** before sending them via
**imageZMQ** to the Mac. The receiving program on the Mac converts the jpg
compressed frames back to OpenCV images and displays them as a continuous video
stream. This jpeg compression can greatly reduce the network load of sending many
images from multiple sources.

The programs that send and receive the images using jpg compression are run in
the same way as the above pair of programs that send uncompressed images. Use
the instructions above as a guide. The programs for Test 3 are::

    test_3_receive_jpg.py  # run on the Mac to receive & decompress images
    test_3_send_jpg.py     # ron on each Raspberry Pi to compress & send images

As with the previous Test 2 program pair, you will need to edit the "connect_to"
address in the sending program to the tcp address of your Mac (or other display
computer).  You will also need to remember to start the *receive* program on the
Mac before you start the sending program on the Raspberry Pi. As before, each
program must be stopped by pressing Ctrl-C in its terminal window. It is normal
to get a cascade of error messages when stopping these programs with Ctrl-C.
This simple test program has no try / except error trapping. Be sure to activate
your virtual environment as you did for Test 2 (see above) before running these
tests.

Test 4: Using PUB/SUB to send simple generated images and display them on Mac
-----------------------------------------------------------------------------

**The fourth test** is a repeat of Test 1, but uses the PUB/SUB messaging
pattern instead of the REQ/REP messaging pattern. It shows the differences
in running PUB/SUB versus REQ/REP in the simplest possible test program.

Test 4 runs both the sending program and the receiving program on
the Mac. No Raspberry Pi or camera is involved. This test shows the start / stop
flexibility of the PUB/SUB pattern. All 3 of the above REQ/REP tests require
that the receiving program be started first, then the sending program. And they
require that the sending program be restarted if the receiving program is
restarted. This is standard behavior for the REQ/REP messaging pattern. But
this test shows that either PUB/SUB program can be started first and that
message sending will resume if either program is restarted. That is a feature
of the PUB/SUB messaging pattern. See other documentation listed below for
further differences, advantages and disadvantages of the REQ/REP versus PUB/SUB
messaging patterns.

The sending program generates test images and sends them to the receiving program.
First, in one terminal window, activate your virtual environment, then change to
the tests directory and run the receiving program, which will receive and
display images::

    workon py3cv3  # use your virtual environment name
    cd imagezmq/tests
    python test_4_pub.py

Then, in a second terminal window on the same display computer (Mac), change to
the tests directory and run the sending program, which will generate and send
images::

    workon py3cv3  # use your virtual environment name
    cd imagezmq/tests
    python test_4_sub.py

After a few seconds, a ``cv2.imshow()`` window should open and display a green
square on a black background. There will be a yellow number in the green square
that will increase (1, 2, ...) once per second. Now you can stop either
program and restart it and see that the sending of numbers continues and picks
up where it left off (though some transmitted images may have been skipped
during restart). It is normal to get a cascade of error messages
when starting and stopping the program with Ctrl-C. These simple test program
have no try / except error trapping, since their only purpose is this simple
demonstration.

Timing tests: Complete imageZMQ usage examples
==============================================

The test programs above are short and simple. They test that the software and
dependencies are installed correctly and that images transfer successfully between
a Raspberry Pi computer and a display computer such as a Mac.  The tests
directory contains 2 more send / receive program pairs that provide a more
complete example of imageZMQ usage. Each of these programs includes
try / except blocks that enable ending the programs by typing Ctrl-C
without starting a cascade of error messages. They also perform frames per
second (FPS) timing tests that measure the speeds of image transfer using the
compressed versus the non-compressed transfer methods. They also show how to
capture the hub response in the sending program, which wasn't needed in the
simple tests.

One pair of programs transmits and receives **OpenCV images** and measures FPS::

    timing_receive_images.py  # run on Mac to display images
    timing_send_images.py     # run on Raspberry Pi to send images

Another pair of programs transmits and receives **jpg compressed images** and
measures FPS::

    timing_send_jpg_buf.py     # run on Raspberry Pi to send images
    timing_receive_jpg_buf.py  # run on Mac to display images

As with the other test program pairs, you will need to edit the "connect_to"
address in the sending program to the tcp address of your Mac (or other display
computer).  You will also need to remember to start the *receive* program on the
Mac before you start the sending program on the Raspberry Pi. With these programs,
the try / except blocks will end the programs cleanly with no errors when you
press Ctrl-C. Be sure to activate your virtual environment before running these
tests.