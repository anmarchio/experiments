import os
import sys

import cv2


def identify_roving(source):
    """
    (0) load image
    (1) find roving in image
    (2) render all outside areas BLACK
    """
    file_list = os.listdir(source)
    for file in file_list:
        image = cv2.imread(os.path.join(source, file))
        # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        height, width, channels = image.shape

        """
        CROP IMAGE
        """
    return 0


if __name__ == "__main__":
    print("Converting images to tiles ...")
    path = ""
    try:
        path = sys.argv[1]
    except Exception as e:
        print("Argument error: ", e.__class__)

    identify_roving(path)
