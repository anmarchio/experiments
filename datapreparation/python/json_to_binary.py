import os
import cv2
import sys
import json
import string
import numpy as np
from imgann import Convertor


def convert_json(source, destination):
    # Iterate through json files and generate the binary images of the annotations of each image
    for file in file_list:
        with open(os.path.join(source, file), 'r') as json_file:
            anns = json.load(json_file)
            dir_path = os.path.join(destination, anns['info']['description'])
            if not os.path.exists(dir_path):
                os.mkdir(dir_path)
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
                path = os.path.join(dir_path, img['file_name'][:-4] + '.png')
                cv2.imwrite(path, bin_img)


def convert_xml(source, destination):
    # convert xml to json
    (head, tail) = os.path.split(source)
    data_dir = os.path.join(head, 'images')
    json_dir = os.path.join(head, 'ann_json')
    if not os.path.exists(json_dir):
        os.mkdir(json_dir)
    file = os.path.join(json_dir, 'ann_json.json')
    Convertor.voc2coco(dataset_dir=data_dir, voc_ann_dir=source, save_dir=file)

    # draw binary images of the annotations of each image
    with open(os.path.join(source, file), 'r') as json_file:
        anns = json.load(json_file)
        for img in anns['images']:
            bin_img = np.zeros((img['width'], img['height']))
            img_id = img['id']
            bboxes = []
            for a in anns['annotations']:
                if a['image_id'] == img_id:
                    bboxes.append(a['bbox'])
            for bbox in bboxes:
                pt1 = (bbox[0], bbox[1])
                pt2 = (bbox[2], bbox[3])
                cv2.rectangle(bin_img, pt1, pt2, (255, 255, 255), -1)
            path = os.path.join(destination, img['file_name'][:-4] + '.png')
            cv2.imwrite(path, bin_img)


def print_help():
    print("HELP")
    print("-" * 4)
    print("python json_to_binary.py <SOURCE> <DESTINATION>\n")
    print("Sample call:\n")
    print("\t python json_to_binary.py <MY_DIR>\experiments\test\json\ <MY_DIR>\experiments\out\json")


if __name__ == "__main__":
    print("Converting to binary image ...")
    path = ""
    destination = ""
    try:
        if sys.argv[1] == "help":
            print_help()
        else:
            path = sys.argv[1]
            destination = sys.argv[2]
            file_list = os.listdir(path)

            if file_list[0].endswith('.xml'):
                convert_xml(path, destination)
            else:
                convert_json(file_list, destination)



    except Exception as e:
        print("Argument error: ", e.__class__)
