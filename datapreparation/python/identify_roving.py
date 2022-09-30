import os
import sys

import cv2

"""
Hysteresis Threshold Values
* for filtering roving within histogram
* gray value range from LOW to HIGH
"""
DEFAULT_LOW = 140
DEFAULT_HIGH = 255

THRESHOLD_SLIDER_MAX = 255
WINDOW_TITLE = 'Show'

MAX_AREA_SIZE = 10000

EXIT_NOTIFICATION_TEXT = "Press c to close window"

def on_trackbar_value_change(*args):
    global trackbar_low_threshold
    trackbar_low_threshold = args[0]
    thresh_img, _ = threshold_image(gray_image, trackbar_low_threshold, DEFAULT_HIGH)
    text = EXIT_NOTIFICATION_TEXT + "\n Threshold: " + str(trackbar_low_threshold)
    coordinates = (20, 20)
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 0.5
    color = (255, 255, 255)
    thickness = 1
    image = cv2.putText(thresh_img, text, coordinates, font, fontScale, color, thickness, cv2.LINE_AA)
    cv2.imshow('Image', gray_image)


def threshold_image(image, low_thresh, high_thresh):
    ret, image_thresh = cv2.threshold(image, low_thresh, high_thresh, cv2.THRESH_BINARY)
    # Get roving coordinates
    contours, _ = cv2.findContours(image_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    # Find contours, filter for (dark colored) rovings
    # and save as x coods in a list rovings
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
    """
    resizes image to a screen width of 1920
    to keep performance high
    """
    resized = image
    if image.shape[1] > 1920:
        scale_percent = 1920 / image.shape[1]  # percent of original size
        width = int(image.shape[1] * scale_percent)
        height = int(image.shape[0] * scale_percent)
        dim = (width, height)
        # resize image
        resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    return resized


def black_out_empty_areas(source, rovings, destination):
    file_list = os.listdir(source)
    for file in file_list:
        print("Processing " + file + " ...")
        image = cv2.imread(os.path.join(source, file))
        for i in range(len(rovings)):
            x = rovings[i][0]
            w1 = rovings[i][1]
            y = 0
            h1 = image.shape[0]
            cv2.rectangle(image, (x, y), (x + w1, y + h1), (0, 0, 0), -1)
        filename, file_extension = os.path.splitext(file)
        cv2.imwrite(os.path.join(destination, filename + ".jpg"), image)


"""
IDENTIFY ROVINGS IN IMAGE
-------------------------

    * starts by reading command line arguments as source and output path

def on_trackbar_value_change(*args)

    * open a window and manually find the best threshold
    * save roving coordinates and black out all background areas

black_out_empty_areas(path, rovings, destination)

    * store the modified images with black areas as new files: 
"""
print("Converting images to tiles ...")
path = ""
try:
    path = sys.argv[1]
    destination = sys.argv[2]
    DEFAULT_LOW = sys.argv[3]
except Exception as e:
    print("Argument error: ", e.__class__)

# Pick only the first file from list
file_list = os.listdir(path)
file = file_list[0]
# Load the image from path
image = cv2.imread(os.path.join(path, file))
# Resize image to fit into screen
resized_gray_image = resize_image(image)
gray_image = cv2.cvtColor(resized_gray_image, cv2.COLOR_BGR2GRAY)

"""
Find the best threshold
using a trackbar and 
checking the visual result
"""
cv2.namedWindow(WINDOW_TITLE)
cv2.resizeWindow(WINDOW_TITLE, 1024, 50)
trackbar_name = 'Threshold'
cv2.createTrackbar(trackbar_name, WINDOW_TITLE, DEFAULT_LOW, THRESHOLD_SLIDER_MAX, on_trackbar_value_change)
# Call method to initialize trackbar
on_trackbar_value_change(DEFAULT_LOW)

# Start loop to keep window open
# Exit when c is pressed
while 1:
    gray_image = cv2.cvtColor(resized_gray_image, cv2.COLOR_BGR2GRAY)
    key = cv2.waitKey(1) & 0xFF
    # if the 'c' key is pressed, break from the loop
    if key == ord('c'):
        break
cv2.destroyAllWindows()

# Ask to continue
yes_no_quit = input("Continue (y) or quit (q)?: ")
print("Filter real sized image using threshold value: " + str(trackbar_low_threshold))
full_sized_gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
_, rovings = threshold_image(full_sized_gray_image, trackbar_low_threshold, DEFAULT_HIGH)
"""
Paint all areas BLACK
that do not contain a roving
"""
if yes_no_quit == 'q':
    pass
elif yes_no_quit == 'y':
    print("Painting non-roving areas black ...")
    black_out_empty_areas(path, rovings, destination)
else:
    pass
print("Exiting")

# if __name__ == "__main__":
#    # Entry point
