import os
import sys

import cv2

"""
Hysteresis Threshold Values
* for filtering roving within histogram
* gray value range from LOW to HIGH
"""
LOW = 92  # 0.55 * 255
HIGH = 255  # 0.73 * 255


def identify_roving(source, low_thresh, high_thresh):
    """
    (0) load image
    (1) find roving in image
    (2) render all outside areas BLACK
    """
    image_rovings = {}
    file_list = os.listdir(source)
    for file in file_list:
        image = cv2.imread(os.path.join(source, file))
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        ret, image_thresh = cv2.threshold(gray_image, low_thresh, high_thresh, cv2.THRESH_BINARY)

        # Get roving coordinates
        contours, _ = cv2.findContours(image_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        rovings = {}
        selected_contours = []
        i = 0
        x_margin = 0
        for cnt in contours:
            x, y, w1, h1 = cv2.boundingRect(cnt)
            if (w1 * h1) >= 10000:
                rovings[i] = (x + x_margin, w1 - x_margin)
                cv2.rectangle(gray_image, (x, y), (x + w1, y + h1), (0, 0, 0), -1)
                selected_contours.append(cnt)
                i = i + 1
        image_rovings[file] = rovings
    while True:
        cv2.imshow('image', gray_image)
        key = cv2.waitKey(1) & 0xFF
        # if the 'c' key is pressed, break from the loop
        if key == ord('c'):
            break

    yes_no = input("Continue? (y/n): ")

    return image_rovings, yes_no


def black_out_empty_areas(source, image_rovings, destination):
    file_list = os.listdir(source)
    for file in file_list:
        image = cv2.imread(os.path.join(source, file))
        rovings = image_rovings[file]
        for i in range(len(rovings)):
            x = rovings[i][0]
            w1 = rovings[i][1]
            y = 0
            h1 = image.shape[0]
            cv2.rectangle(image, (x, y), (x + w1, y + h1), (0, 0, 0), -1)
        file_name = file + "_black.jpg"
        cv2.imwrite(os.path.join(destination, file_name), image)


if __name__ == "__main__":
    print("Converting images to tiles ...")
    path = ""
    try:
        path = sys.argv[1]
        destination = sys.argv[2]
    except Exception as e:
        print("Argument error: ", e.__class__)

    image_rovings, yes_no = identify_roving(path, LOW, HIGH)

    if yes_no == 'y':
        black_out_empty_areas(path, image_rovings, destination)
