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

This is what the detection function returns:
(b'cup', 0.9995042681694031,
(350.91656494140625, 482.6078796386719, 197.35728454589844, 195.4808349609375))

Do the following:
Convert to dictionary, how does the coord system work -check openCV for how the function works

"""
import darknet

# Detection Function
def detect(net, meta, imagepath):
    r_dict_list = []
    r = darknet.detect(net, meta, imagepath.encode())
    for obj in r:
        r_dict = {} # tried to initialise it outside for loop but gave me an error too.
        r_dict["object"] = obj[0]
        r_dict["proba"] = obj[1]
        r_dict["x0"] = obj[2][0]
        r_dict["y0"] = obj[2][1]
        r_dict["x1"] = obj[2][2]
        r_dict["y1"] = obj[2][3]

        r_dict_list.append(r_dict)
    return r_dict_list
    #return r

def test_detect_data_structure(net, meta):
    result = detect(net, meta, "test_img/test_image1.jpg")

    for entry in result:
        print(entry)
        assert isinstance(result, list) # using list & tuple gives me error "no attr keys" How to ref. dictionary? have seached this.
        assert len(result) != 0

        print(sorted(entry.keys()))
        assert sorted(entry.keys()) == { # This is where it does not execute. changes to {} but this does not help either
            'object',  # string such as 'umbrella'
            'proba',  # proba between 0 and 1
            'x0', 'x1',  # lower left corner
            'y0', 'y1'}  # upper right corner
            }
        assert isinstance(entry[0], str)
        assert isinstance(entry[1], float)
        assert isinstance(entry[2][0], int)
        assert isinstance(entry[3][1], int)
        assert isinstance(entry[4][2], float)
        assert isinstance(entry[5][3], float)
        return entry


def main():
    # Declare network
    darknet.set_gpu(0)
    net = darknet.load_net(b"cfg/yolov3.cfg", "weights/yolov3.weights", 0)
    meta = darknet.load_meta(b"cfg/coco.data")

    test_detect_data_structure(net, meta)


if __name__ == '__main__':
    main()
