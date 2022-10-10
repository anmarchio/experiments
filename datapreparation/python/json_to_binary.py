import os
import cv2
import sys
import json
import numpy as np
from matplotlib import pyplot as plt

NROFTILES = 1

def convert_json(source):
    file_list = os.listdir(source)
    for file in file_list:
        with open(os.path.join(source, file), 'r') as json_file:
            anns = json.load(json_file)
            img_list = anns.items()
            print(img_list)
        #for tile_id in range(NROFTILES):
            #img_width = anns['images']['width']
            #img_height = anns
            #an_area = anns

            #bin_img = np.zeros((img_width, img_height))
            #bin_img = cv2.fillPoly(bin_img, an_area, (255, 255, 255))

            # cv2.imshow("Binary Image", bin_img)
            # cv2.waitKey(0)



if __name__ == "__main__":
    print("Converting json to binary image ...")
    path = ""
    try:
        path = sys.argv[1]
    except Exception as e:
        print("Argument error: ", e.__class__)

    convert_json(path)