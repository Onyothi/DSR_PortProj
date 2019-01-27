# Original code: https://stackoverflow.com/questions/22003441/streaming-m3u8-file-with-opencv
#This code, skips some frames. Use code where raw image = take 420*360*3 , image = reshape 360,420,3
#This script captures images, per second, and saves them with a timestampself.
#Each JPEG image is 340KB ~0.34MB in size

import cv2
from datetime import datetime
import numpy as np
import subprocess as sp
from time import time
from time import sleep
# import glob
# import pandas as pd

#from IPython.core.display import display, HTML
#display(HTML("<style>.container { width:100% !important; }</style>"))

#import opencv-python as cv
VIDEO_URL = "https://videos3.earthcam.com/fecnetwork/9974.flv/chunklist_w917803974.m3u8"
VIDEO_URL
# Use if you have multiple images in the same folder
files_new = set()
files_wr = set()

filepath = "/Users/ndapewaonyothi/Documents/DataScienceRetreat/DSR-2018/DSR_Project/cam_data/{0}"

cv2.namedWindow("Streetcam", cv2.WINDOW_NORMAL)
FFMPEG_BIN = "/anaconda3/bin/ffmpeg"
command = [FFMPEG_BIN, "-i", VIDEO_URL,
           "-loglevel", "quiet",  # no text output
           "-an",   # disable audio
           "-f", "image2pipe",
           "-pix_fmt", "bgr24",
           "-vcodec", "rawvideo", "-"
           ]
pipe = sp.Popen(command, stdin=sp.PIPE, stdout=sp.PIPE)

# files = glob.glob("/Users/ndapewaonyothi/Documents/DataScienceRetreat/DSR-2018/DSR_Project/cam_data/*.jpg")
# print(len(files), sorted(files))

# -------- sorting paths in the txt file using the union
# with open('cam_images.txt', 'w') as f:
#     for item in sorted(files):
#        f.write("%s\n" % item)

# files_wr = files_wr.union(set(files))
# print(files_wr)
# print(type(files_wr))

def print_time(comment):
    ts = time()
    st = datetime.fromtimestamp(ts).strftime("%H:%M:%S.%f")[:-3]
    print(comment, st)

counter = 0
last_time = 0
last_raw_image = None

# Would like write all print outs to a log file - How :( ?
while True:
    # Run below code in while loop for actual normal frames || 16:44
    # raw_image = pipe.stdout.read(420*360*3) # read 432*240*3 bytes (= 1 frame)
    # image =  np.fromstring(raw_image, dtype='uint8').reshape((360,420,3))
#    print("")
#    print("Number "+str(counter))
#    print_time("Beginning")
    raw_image = pipe.stdout.read(1280*720*3) # read 432*240*3 bytes (= 1 frame)
    # Check if raw image has the same bytes as the previous image.
    # To avoid taking duplicates should the stream freeze at some point.
    if raw_image == last_raw_image:
        continue
    last_raw_image = raw_image

#    print_time("reading image")
#    print(raw_image is None)

#    print_time("")
    #sckit for img processing. s3 fs to plug it into cv2 for img writing.
    #Srcript Credit Pascal Schambach - Helped rewrite this

    # Capture images every 10 seconds
    current_time = time()
    if current_time - last_time >= 10:
        image = np.fromstring(raw_image, dtype='uint8').reshape((720,1280,3))
        #    print_time("showing image")
        cv2.imshow("Streetcam", image)
        last_time = current_time
        st = datetime \
            .fromtimestamp(current_time) \
            .strftime('_%Y%m%d_%H%M%S')
        new_filename = 'capture' + st + '.jpg' # jpg smaller than >png (transparent)
        print("writing file ", counter, ": ", new_filename)

        # print_time("write to path")
        image_path = filepath.format(new_filename)
        cv2.imwrite(image_path, image) # write to a filepath, by timestamp
        # files = glob.glob("cam_data/*.jpg")
        # new_files = set(files) - files_wr
        # sorting paths in the txt file using the union
        # print_time("Soting images")
        with open('cam_images.txt', 'a+') as f:
            # for item in sorted(new_files):
            f.write("%s\n" % image_path)

        counter += 1

        # files_wr = files_wr.union(new_files)

    #
    # Use ESC to kill windhow.
    if cv2.waitKey(int(1000/24)) == 27:
        break


# This does not seem to work.
cv2.destroyAllWindows()
