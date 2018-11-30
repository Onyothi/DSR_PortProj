#!/usr/bin/env python3

import os
import cv2
import darknet

darknet.set_gpu(0)
net = darknet.load_net(b"cfg/yolov3.cfg", b"weights/yolov3.weights", 0)
meta = darknet.load_meta(b"cfg/coco.data")

cwd = os.getcwd()
print(cwd)
print("Running ", __file__, " in ", cwd, ".")

prediction_data_path = "predictions.txt"

# Stack overflow 3964681, 678236
# iterate over files from a specific poin
for root, dirs, files in os.walk(cwd + "/data/tdata/"):

    # Look at each individual file
    for file in files:

        # Only consider files that end with *.jpg
        if file.endswith(".jpg"):

            # Basename of the image file without the extension
            basename = os.path.splitext(file)[0]

            # Image file
            imagefile = os.path.join(root, file)

            # output text file
            # outfile = basename + "_out.txt"

            # output image name
            outimage = basename + "_out.png"

            # Compose the command to be executed - revise later
            #command = "./darknet detect cfg/yolov3.cfg ./yolov3.weights " + \
            #          imagefile + " >> " + prediction_data_path

            # Make an external command
            #os.system(command)
            print(imagefile)
            r = darknet.detect(net, meta, imagefile.encode())
            print(r)

            img = cv2.imread(imagefile)
            #for (cls_name, likelihood, (x, y, w, h)) in r:
                # cv2.putText(
                #     img,
                #     cls_name,
                #     (int(x + w/2), int(y + h/2)),
                #     cv2.FONT_HERSHEY_SIMPLEX,
                #     1,
                #     (255, 255, 255)
                # )
                # cv2.rectangle(
                #     img,
                #     (int(x), int(y)),
                #     (int(x + w), int(y + h)),
                #     (255, 255, 255)
                # )

            # cv2.imwrite(outimage, img)
            cv2.imshow(imagefile, img)

            #tmp_img_path = os.path.join(cwd, "predictions.png")
            #out_img_path = os.path.join(cwd, "predictions", outimage)

            # No idea what the output image is called but this
            # is where you would do something like
            #os.rename(tmp_img_path, out_img_path)

# You will clearly have to make changes - e.g. change "./Download...
