"""faster_jpg_send.py -- demonstrate the use of "simplejpeg" to improve
jpg conversion speed.

This script uses ImageSender via a "with" statement. To learn more, check the 
"with_ImageSender.py" script in the examples folder.

Images are jpg compressed before being sent and we can speed up this part 
of the process.

"simplejpeg" has 2 useful functions that we can use:

encode_jpeg( image, quality=95, colorspace='BGR', fastdct=False)
decode_jpeg( jpg_buffer, colorspace='BGR', fastdct=False, fastupsample=False)

The performance improvement, compared to using OpenCV, increases with the 
size of the images.

What to keep in mind for the Sender:
    
    1. The function "encode_jpeg()" returns a jpg-byte-string.
    
       This can be seen as equivalent to: 
    
           ret_code, jpg_buffer = cv2.imencode(
                ".jpg", image, [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality])
           
           jpg_buffer = jpg_buffer.tobytes()

    2. Don't forget to change the colorspace to 'BGR'.

"""

import sys
import socket
import time
import traceback
import cv2
import imagezmq
import simplejpeg
from   imutils.video import VideoStream

rpi_name     = socket.gethostname() # send RPi hostname with each image
picam        = VideoStream(usePiCamera=True).start()
time.sleep(2.0)                     # allow camera sensor to warm up
jpeg_quality = 95                   # 0 to 100, higher is better quality

try:
    with imagezmq.ImageSender(connect_to='tcp://192.168.86.34:5555') as sender:
        while True:                 # send images as a stream until Ctrl-C
            image          = picam.read()
            jpg_buffer     = simplejpeg.encode_jpeg(image, quality=jpeg_quality, 
                                                    colorspace='BGR')
            reply_from_mac = sender.send_jpg(rpi_name, jpg_buffer)
            
except (KeyboardInterrupt, SystemExit):
    pass                            # Ctrl-C was pressed to end program
except Exception as ex:
    print('Python error with no Exception handler:')
    print('Traceback error:', ex)
    traceback.print_exc()
finally:
    picam.stop()                    # stop the camera thread
    sys.exit()
