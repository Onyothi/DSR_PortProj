# Original code: https://stackoverflow.com/questions/22003441/streaming-m3u8-file-with-opencv
#This code, skips some frames. Use code where raw image = take 420*360*3 , image = reshape 360,420,3
#This script captures images, per second, and saves them with a timestampself.
#Each JPEG image is 340KB ~0.34MB in size

import cv2
import time
import datetime
import glob
import subprocess as sp
import numpy as np
import pandas as pd
#import opencv-python as cv

VIDEO_URL = "https://videos3.earthcam.com/fecnetwork/9974.flv/chunklist_w917803974.m3u8"
VIDEO_URL
# Use if you have multiple images in the same folder
files_new = set()
files_wr = set()

filename= "/Users/ndapewaonyothi/Documents/DataScienceRetreat/DSR-2018/DSR_Project/cam_data/{0}"
print(filename)

cv2.namedWindow("Streetcam", cv2.WINDOW_NORMAL)
FFMPEG_BIN = "/anaconda3/bin/ffmpeg"
command = [FFMPEG_BIN, "-i", VIDEO_URL,
           "-loglevel", "quiet",  # no text output
           "-an",   # disable audio
           "-f", "image2pipe",
           "-pix_fmt", "bgr24",
           "-vcodec", "rawvideo", "-"
           ]
pipe = sp.Popen(command, stdin = sp.PIPE, stdout = sp.PIPE)

files = glob.glob("/Users/ndapewaonyothi/Documents/DataScienceRetreat/DSR-2018/DSR_Project/cam_data/*.jpg")
print(files)

# -------- sorting paths in the txt file using the union
with open('cam_images.txt', 'w') as f:
    for item in sorted(files):
        f.write("%s\n" % item)

files_wr = files_wr.union(set(files))
print(files_wr)
print(type(files_wr))

while True:
    # Run below code in while loop for actual normal frames || 16:44
    # raw_image = pipe.stdout.read(420*360*3) # read 432*240*3 bytes (= 1 frame)
    # image =  np.fromstring(raw_image, dtype='uint8').reshape((360,420,3))

    raw_image = pipe.stdout.read(1280*720*3) # read 432*240*3 bytes (= 1 frame)
    image = np.fromstring(raw_image, dtype='uint8').reshape((720,1280,3))
    cv2.imshow("Streetcam",image)
    #sckit for img processing. s3 fs to plug it into cv2 for img writing.
    #Srcript Credit Pascal Schambach - Helped rewrite this
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('_%Y%m%d_%H%M%S')
    new_filename = 'captured' + st + '.jpg' #jpg smaller than >png (transparent)
    print(new_filename)
    #---write files to file destination
    cv2.imwrite(filename.format(new_filename), image) #write to a filepath, by timestamp
    files = glob.glob("cam_data/*.jpg")
    new_files = set(files) - files_wr
    # -------- sorting paths in the txt file using the union
    with open('cam_images.txt', 'a+') as f:
        for item in sorted(new_files):
            f.write("%s\n" % item)
    files_wr = files_wr.union(new_files)


    #What is happening here. I get these glitched frames, must resolve
    #What is the standard for the waitkey?
    if cv2.waitKey(1) == 2:
        break
cv2.destroyAllWindows()

#find dist file system with python to write imgs to.
