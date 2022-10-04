import os
import cv2
import sys
import numpy as np
from matplotlib import pyplot as plt
from pycocotools.coco import COCO

NROFTILES = 1

def convert_json(source):
    file_list = os.listdir(source)
    for file in file_list:
        coco = COCO(os.path.join(source, file))
        for tile_id in range(NROFTILES):
            cat_ids = coco.getCatIds()
            anns_ids = coco.getAnnIds(imgIds=tile_id + 1, catIds=cat_ids, iscrowd=None)
            anns = coco.loadAnns(anns_ids)
            mask = coco.annToMask(anns[0])
            for i in range(len(anns)):
                mask += coco.annToMask(anns[i])
            cv2.imshow("mask", mask)
            cv2.waitKey(0)



if __name__ == "__main__":
    print("Converting json to binary image ...")
    path = ""
    try:
        path = sys.argv[1]
    except Exception as e:
        print("Argument error: ", e.__class__)

    convert_json(path)