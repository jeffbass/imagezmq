"""faster_jpg_hub.py -- demonstrate the use of "simplejpeg" to improve
jpg conversion speed.

This script uses ImageHub via a "with" statement. To learn more check the 
"with_ImageHub.py" script in the examples folder.

Images are jpg compressed before being sent and we can speed up this part 
of the process.

"simplejpeg" has 2 useful functions that we can use:

encode_jpeg( image, quality=95, colorspace='BGR', fastdct=False)
decode_jpeg( jpg_buffer, colorspace='BGR', fastdct=False, fastupsample=False)

The performance improvement, compared to using OpenCV, increases with the 
size of the images.

What to keep in mind for the Hub:
    
    1. The function "encode_jpeg()" returns a jpg-byte-string.
      
    2. The function "decode_jpeg()" accepts a jpg-byte-string and 
       returns an image as numpy array.
    
    3. Don't forget to change the colorspace to 'BGR' to make OpenCV happy.
     
    4. If 'fastdct' and 'fastupsample' are set to True, the speed will improve
       slightly, for minor loss in quality. 
      (Speed improvement not really perceivable)

a. Run this program in its own terminal window on the server:
    ~$ python faster_jpg_hub.py

b. Run the image sending program on the client (RPi):
    ~$ python faster_jpg_send.py
"""

import sys
import time
import traceback
import numpy as np
import cv2
import imagezmq
import simplejpeg
from   imutils.video import FPS

try:
    with imagezmq.ImageHub() as image_hub:
        while True:                    # receive images until Ctrl-C is pressed
            sent_from, jpg_buffer = image_hub.recv_jpg()
            image                 = simplejpeg.decode_jpeg( jpg_buffer, 
                                                            colorspace='BGR')
            cv2.imshow(sent_from, image)  # display images 1 window per sent_from
            cv2.waitKey(1)
            image_hub.send_reply(b'OK')   # REP reply
except (KeyboardInterrupt, SystemExit):
    pass                                  # Ctrl-C was pressed to end program
except Exception as ex:
    print('Python error with no Exception handler:')
    print('Traceback error:', ex)
    traceback.print_exc()
finally:
    cv2.destroyAllWindows()         # closes the windows opened by cv2.imshow()
    sys.exit()
