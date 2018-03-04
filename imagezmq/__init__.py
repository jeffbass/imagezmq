"""
imagezmq: transport OpenCV images via ZMQ.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A pair of Python classes that transport OpenCV images from one
computer to another. For example, OpenCV images gathered by
a Raspberry Pi camera could be sent to another computer
for displaying the images using cv2.imshow() or for further image processing.

Copyright (c) 2017 by Jeff Bass.
License: MIT, see LICENSE for more details.
"""
# populate fields for >>>help(imagezmq)
from .__version__ import __title__, __description__, __url__, __version__
from .__version__ import __author__, __author_email__, __license__
from .__version__ import __copyright__
