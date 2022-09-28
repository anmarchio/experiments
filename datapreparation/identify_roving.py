import os
import sys

import cv2

"""
Hysteresis Threshold Values
* for filtering roving within histogram
* gray value range from LOW to HIGH
"""
DEFAULT_LOW = 92
DEFAULT_HIGH = 255

THRESHOLD_SLIDER_MAX = 255
WINDOW_TITLE = 'Show'

MAX_AREA_SIZE = 10000


def on_trackbar_value_change(*args):
    global trackbar_low_threshold
    trackbar_low_threshold = args[0]
    thresh_img, _ = threshold_image(gray_image, trackbar_low_threshold, DEFAULT_HIGH)
    cv2.imshow('img', resize_image(thresh_img))


def threshold_image(image, low_thresh, high_thresh):
    ret, image_thresh = cv2.threshold(image, low_thresh, high_thresh, cv2.THRESH_BINARY)
    # Get roving coordinates
    contours, _ = cv2.findContours(image_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    # Get contours
    rovings = {}
    selected_contours = []
    i = 0
    x_margin = 0
    for cnt in contours:
        x, y, w1, h1 = cv2.boundingRect(cnt)
        if (w1 * h1) >= MAX_AREA_SIZE:
            rovings[i] = (x + x_margin, w1 - x_margin)
            cv2.rectangle(image, (x, y), (x + w1, y + h1), (0, 0, 0), -1)
            selected_contours.append(cnt)
            i = i + 1
    return image, rovings


def resize_image(image):
    resized = image
    if image.shape[1] > 4096:
        scale_percent = 4096 / image.shape[1]  # percent of original size
        width = int(image.shape[1] * scale_percent)
        height = int(image.shape[0] * scale_percent)
        dim = (width, height)
        # resize image
        resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    return resized


def identify_roving(source, low_thresh, high_thresh):
    """
    --------
    IRRELEVANT
    --------
    (0) load image
    (1) find roving in image
    (2) render all outside areas BLACK
    """
    # yes_no = input(f"Using tresholds LOW: {low_thresh}, HIGH: {high_thresh}? (y/n)")
    # if yes_no == 'n':
    #   low_thresh = int(input("Set LOW  treshold: "))
    #   high_thresh = int(input("Set HIGH treshold: "))
    file_list = os.listdir(source)
    # for file in file_list:
    file = file_list[0]
    image = cv2.imread(os.path.join(source, file))
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    rovings = []


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

# print("Converting images to tiles ...")
path = ""
try:
    path = sys.argv[1]
    destination = sys.argv[2]
except Exception as e:
    print("Argument error: ", e.__class__)

"""
Define the best treshold
by visually checking
"""
file_list = os.listdir(path)
# for file in file_list:
file = file_list[0]
image = cv2.imread(os.path.join(path, file))
rovings = []
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

cv2.namedWindow(WINDOW_TITLE, cv2.WINDOW_NORMAL)
trackbar_name = 'low_threshold'
cv2.createTrackbar(trackbar_name, WINDOW_TITLE, DEFAULT_LOW, THRESHOLD_SLIDER_MAX, on_trackbar_value_change)

# call method to initialize first time
on_trackbar_value_change(DEFAULT_LOW)

while 1:
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    key = cv2.waitKey(1) & 0xFF
    # if the 'c' key is pressed, break from the loop
    if key == ord('c'):
        break

cv2.destroyAllWindows()

yes_no_quit = input("Continue (y) or quit (q)?: ")
# image_rovings, yes_no_quit = identify_roving(path, DEFAULT_LOW, DEFAULT_HIGH)

"""
Render all non-roving areas
BLACK in the images
"""
if yes_no_quit == 'q':
    pass
elif yes_no_quit == 'y':
    black_out_empty_areas(path, rovings, destination)
else:
    pass


if __name__ == "__main__":
    print("Converting images to tiles ...")