import os
import cv2
import sys
import json
import numpy as np


def convert_json(source, destination):
    file_list = os.listdir(source)
    for file in file_list:
        with open(os.path.join(source, file), 'r') as json_file:
            anns = json.load(json_file)
            for img in anns['images']:
                bin_img = np.zeros((img['width'], img['height']))
                img_id = img['id']
                polygons = []
                for a in anns['annotations']:
                    if a['image_id'] == img_id:
                        polygons.append(a['segmentation'])
                for poly in polygons:
                    temp_img = np.zeros((img['width'], img['height']))
                    i = 1
                    coord = []
                    while i < len(poly[0]) + 1:
                        coord.append((poly[0][i - 1], poly[0][i]))
                        i += 2
                    temp_img = cv2.fillPoly(img=temp_img, pts=np.array([coord], dtype=np.int32), color=(255, 255, 255))
                    bin_img = np.maximum(bin_img, temp_img)
                path = os.path.join(destination, anns['info']['description'] + '_' + img['file_name'] + '_bin.jpg')
                cv2.imwrite(path, bin_img)


def print_help():
    print("HELP")
    print("-" * 4)
    print("python json_to_binary.py <SOURCE> <DESTINATION>\n")
    print("Sample call:\n")
    print("\t python json_to_binary.py <MY_DIR>\experiments\test\json\ <MY_DIR>\experiments\out\json")


if __name__ == "__main__":
    print("Converting json to binary image ...")
    path = ""
    destination = ""
    try:
        if sys.argv[1] == "help":
            print_help()
        else:
            path = sys.argv[1]
            destination = sys.argv[2]
            convert_json(path, destination)

    except Exception as e:
        print("Argument error: ", e.__class__)
