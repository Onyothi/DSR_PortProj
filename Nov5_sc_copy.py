#Original code: https://stackoverflow.com/questions/22003441/streaming-m3u8-file-with-opencv
#This code, skips some frames. Use code where raw image = take 420*360*3 , image = reshape 360,420,3
#This script captures images, per second, and saves them with a timestampself.
#Each JPEG image is 340KB ~0.34MB in size

import cv2
import time
import subprocess as sp
import numpy as np
!pwd
#import opencv-python as cv
VIDEO_URL = "https://videos3.earthcam.com/fecnetwork/9974.flv/chunklist_w917803974.m3u8"
VIDEO_URL
filename= "/Users/ndapewaonyothi/Documents/DataScienceRetreat/DSR-2018/DSR_Project/cam_data/Day1_17.30{}.jpg"
cv2.namedWindow("Streetcam",cv2.WINDOW_NORMAL)
FFMPEG_BIN = "/anaconda3/bin/ffmpeg"
command = [FFMPEG_BIN,"-i", VIDEO_URL,
           "-loglevel", "quiet", # no text output
           "-an",   # disable audio
           "-f", "image2pipe",
           "-pix_fmt", "bgr24",
           "-vcodec", "rawvideo", "-"
            ]
pipe = sp.Popen(command, stdin = sp.PIPE, stdout = sp.PIPE)
while True:
    #Run below code in while loop for actual normal frames || 16:44
    #raw_image = pipe.stdout.read(420*360*3) # read 432*240*3 bytes (= 1 frame)
    #image =  np.fromstring(raw_image, dtype='uint8').reshape((360,420,3))

    raw_image = pipe.stdout.read(1280*720*3) # read 432*240*3 bytes (= 1 frame)
    image =  np.fromstring(raw_image, dtype='uint8').reshape((720,1280,3))
    cv2.imshow("Streetcam",image)
    cv2.imwrite(filename.format(time.time()), image) #write to a filepath, by timestamp
    if cv2.waitKey(5) == 27:
        break
cv2.destroyAllWindows()
