"""
def detect(imagepath):
    return [
        {'object': 'person', 'proba': 0.98,
         'x0': 12, 'y0': 8, 'x1': 20, 'y1': 12},
        {'object': 'umbrella', 'proba': 0.8,
         'x0': 57, 'y0': 40, 'x1': 80, 'y1': 42},
    ]

def draw_boxes(imagepath, detections):
    return image

image = draw_boxes('myimage.png', detect('myimage.png'))


Convert to dictionary, how do the coord work, check openCV, how the function works
"""
import darknet

# Detection Function
def detect(net, meta, imagepath):
    r = darknet.detect(net, meta, imagepath)
    return r


def test_detect_data_structure(net, meta):
    result = detect(net, meta, "test_img/test_image1.jpg")
    assert isinstance(result, list)
    assert len(result) != 0
    for entry in result:
        print(entry)

        assert sorted(entry.keys()) == [
            'object',  # string such as 'umbrella'
            'proba',  # proba between 0 and 1
            'x0', 'y0',  # lower left corner
            'x1', 'y1'  # upper right corner
            ]
        assert isinstance(entry['object'], str)
        assert isinstance(entry['proba'], float)
        assert isinstance(entry['x0'], int)


def main():
    # Declare network
    darknet.set_gpu(0)
    net = darknet.load_net(b"cfg/yolov3.cfg", "weights/yolov3.weights", 0)
    meta = darknet.load_meta(b"cfg/coco.data")

    test_detect_data_structure(net, meta)


if __name__ == '__main__':
    main()
