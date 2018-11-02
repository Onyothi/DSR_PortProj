
#Original code: https://stackoverflow.com/questions/22003441/streaming-m3u8-file-with-opencv
import cv2
import subprocess as sp
import numpy as np
VIDEO_URL = "https://videos3.earthcam.com/fecnetwork/9974.flv/chunklist_w917803974.m3u8"

cv2.namedWindow("Streetcam",cv2.WINDOW_AUTOSIZE)
FFMPEG_BIN = "/anaconda3/bin/ffmpeg"
command = [FFMPEG_BIN,"-i", VIDEO_URL,
           "-loglevel", "quiet", # no text output
           "-an",   # disable audio
           "-f", "image2pipe",
           "-pix_fmt", "bgr24",
           "-vcodec", "rawvideo", "-"
            ]
pipe = sp.Popen(command, stdin = sp.PIPE, bufsize=10**8)
pipe
stdin = sp.PIPE, stdout = sp.PIPE)
while True:
    raw_image = pipe.stdout.read(1280*720*3) # read 432*240*3 bytes (= 1 frame)
    image =  np.fromstring(raw_image, dtype='uint8').reshape((720,1280,3))
    cv2.imshow("GoPro",image)
    if cv2.waitKey(5) == 27:
        break
cv2.destroyAllWindows()
