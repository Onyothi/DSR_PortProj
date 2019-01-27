
"""
Output of r returns two objects as below:
[(b'cup', 0.9995042681694031, (350.91656494140625, 482.6078796386719, 197.35728454589844, 195.4808349609375)),
(b'vase', 0.9675477743148804, (444.6388244628906, 264.5071105957031, 59.50741958618164, 238.81195068359375))]

coordinats from darknet: cx,cy,w,h
translation to rectangle (cx,cy,w,h) -> (cx-w/2, cy-h/2),(cx+w/2,cy+h/2)

What to do: Draw bounding boxes on all detected objets returned.

"""
import darknet
import cv2

darknet.set_gpu(0)
net = darknet.load_net(b"cfg/yolov3.cfg", b"weights/yolov3.weights", 0)
meta = darknet.load_meta(b"cfg/coco.data")
imagefile = "test_img/test_image1.jpg"

# Read in image
img = cv2.imread(imagefile)
print(img.shape)

# Call the detection algorithm on the image
r = darknet.detect(net, meta, imagefile.encode())
print(r)

# select one of the objects detected 'cup', to draw the bounding boxes on
first_entry = r[0]
print(first_entry)
# Tip: Rewrite out as a formula
cv2.rectangle(img,(250,382),(450,582),(0,255,0),3)
# Show Image
cv2.imshow('result', img)
cv2.waitKey(int(1000/24)) == 27
cv2.destroyAllWindows()
