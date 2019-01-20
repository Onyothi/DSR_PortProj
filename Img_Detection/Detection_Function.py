
import os
import cv2
import darknet
import json
import joblib
from pathlib import Path

# Seems to work only on txt documents - try on images
img_folder = Path("Data_Collection/")
file_to_open = img_folder / "capture_20181126_181828.jpg"
f = open(file_to_open)
print(f)

# Declare network
darknet.set_gpu(0)
net = darknet.load_net(b"cfg/yolov3.cfg", b"weights/yolov3.weights", 0)
meta = darknet.load_meta(b"cfg/coco.data")

# Detection Function
def detect(imagefile):
    #filehandle = open(imagefile)
    #print(filehandle.read())
    #filehandle.close()
    r = darknet.detect(net, meta, imagefile.encode())
    return r
    #print("image is:" + file + ".")
    #print("path is:" + file + ".")

# Calling detect function from the main method

def main():
    #detect(capture_20181126_181828.jpg)
    #fileDir = os.path.dirname(os.path.realpath('__file__'))
    #print(fileDir)
    imagefile = "capture_20181126_181828.jpg"
    detect(imagefile)
    result_list.append(r)
    print(r)
