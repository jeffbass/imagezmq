README_Unit_Tests.rst -- Explain this directory and my Unit Tesing method.

As new features and significant changes are added to imageZMQ, they will need
to be tested. I will put the test programs (in pairs, one sending and one
receiving). I am using a slightly different kind of "unit testing" since any
change to imageZMQ will need a modification to imageZMQ and 2 test programs.

The first test program pair is made up of test_receive_with_close.py and
test_send_with_close.py.

Test programs in this directory so far:

1. test_receive_with_close.py and test_send_with_close.py: This pair tests the
   new .close() method added to both imageZMQ classes in version 1.1.0.

The below instructions are the ones for test_receive_with_close.py:

**Instructions for running BOTH test programs for a complete Unit Test:**

To make sure your testing the latest development version of imagezmq.py:


1. Copy imagezmq.py from its directory into this one, changing its name:
   cp ../../imagezmq/imagezmq.py imagezmqtest.py
2. Edit imagezmqtest.py to add a print("test version") statement it to be
   sure it is importing correctly. Add it right after the import numpy
   statement:
   print('Test: importing imagezmqtest.py')
3. Be sure to be in your appropriate virtualenv:
   workon py3cv3  # this is my testing one for these tests

Then run the tests. These test programs expect imagezmqtest.py to be available
in this same directory and will produce an import error if it is not.

1. Run this program in its own terminal window:
python test_receive_with_close.py

This "receive and display images" program MUST be running before starting the
image sending program.

2. Wait until the first 3 test steps show 3 OK messages (or note if an
error occurs). If an error occurs, it must be fixed before the remaining steps.

3. Run the image sending program in a different terminal window:
python test_send_with_close.py

After the 3 "OK" test messages appear:
A cv2.imshow() window will appear showing the tramsmitted image. The sending
program sends a series of images with an incrementing couner value.

To end the programs, press Ctrl-C in the terminal window of the sending program
first. Then press Ctrl-C in the terminal window of the receiving proram. You
get various error messages when you press Ctrl-C. That's normal; there is no
error or exception trapping in these simple test programs.
