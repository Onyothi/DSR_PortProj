#Original code: https://stackoverflow.com/questions/22003441/streaming-m3u8-file-with-opencv
import cv2
import subprocess as sp
import numpy as np
VIDEO_URL = "https://videos3.earthcam.com/fecnetwork/9974.flv/chunklist_w917803974.m3u8"
VIDEO_URL
cv2.namedWindow("Streetcam",cv2.WINDOW_NORMAL)
FFMPEG_BIN = "/anaconda3/bin/ffmpeg"
#command = [FFMPEG_BIN,"-i", VIDEO_URL,
#           "-loglevel", "quiet", # no text output
#           "-an",   # disable audio
#           "-f", "image2pipe",
#           "-pix_fmt", "bgr24",
#           "-vcodec", "rawvideo", "-"
#            ]
command = [ FFMPEG_BIN,"-i", VIDEO_URL,
        "-y", # (optional) overwrite output file if it exists
        "-f", "rawvideo",
        "-vcodec","rawvideo",
        "-s", "420x360", # size of one frame
        "-pix_fmt", "rgb24",
        "-r", "24", # frames per second
        "-", # The imput comes from a pipe
        "-an", # Tells FFMPEG not to expect any audio
        "-vcodec", "mpeg",
        "my_output_videofile.mp4" ]
command
pipe = sp.Popen(command, stdin=sp.PIPE, stdout=sp.PIPE)
pipe
while True:
    raw_image = pipe.stdout.read(1280*720*3) # read 432*240*3 bytes (= 1 frame)
    image =  np.fromstring(raw_image, dtype='uint8').reshape((720,1280,3))
    cv2.imshow("Streetcam",image)
    if cv2.waitKey(5) == 27:
        break
cv2.destroyAllWindows()
