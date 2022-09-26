import os
import cv2
import sys
import numpy as np

# "C:\\dev\\experiments\\test"
TILE_HEIGHT = 1024
TILE_WIDTH = 1024

"""
    prefilter using image-browser =>
    (...)
    get_data.py -> convert.yp -> filter.py -> (plotly)
"""


def convert_tiles(source):
    file_list = os.listdir(source)
    for file in file_list:
        log = open(path + '/crop_tile_log_' + file + '.csv', 'a')
        line = f'src_file; tile; tow; src_width; src_height; tile_width; tile_height; x_pos; y_pos \n'
        log.write(line)

        image = cv2.imread(os.path.join(source, file))
        # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        height, width, channels = image.shape

        """
        CROP IMAGE
        """
        number_of_tiles_height = int(height / TILE_HEIGHT)
        if height % TILE_HEIGHT > 0:
            number_of_tiles_height = number_of_tiles_height + 1

        number_of_tiles_width = int(width / TILE_WIDTH)
        if width % TILE_WIDTH > 0:
            number_of_tiles_width = number_of_tiles_width + 1

        for col in range(number_of_tiles_width):

            for row in range(number_of_tiles_height):
                y = row * TILE_HEIGHT
                x = col * TILE_WIDTH

                h = TILE_HEIGHT
                w = TILE_WIDTH

                if y < height < y + h:
                    crop_img = np.zeros((h, w, 3), np.uint8)
                    tile_img = image[y:height, x:x + w]
                    crop_img[0:tile_img.shape[0], 0:tile_img.shape[1]] = tile_img
                elif w < width < x + w:
                    crop_img = np.zeros((h, w, 3), np.uint8)
                    tile_img = image[y:y + h, x:width]
                    crop_img[0:tile_img.shape[0], 0:tile_img.shape[1]] = tile_img
                else:
                    crop_img = image[y:y + h, x:x + w]


                tile_name = str(col * number_of_tiles_height + row) + ".jpg"

                # Show tile if necessary
                # cv2.imshow("cropped", crop_img)
                # cv2.waitKey(0)

                # write metadata to log
                line = f'{file}; {tile_name}; 0; {width}; {height}; {TILE_WIDTH}; {TILE_HEIGHT}; {x}; {y} \n'
                log.write(line)

                # create dir using the original filename
                dir_name = os.path.join(source, "t_" + file)
                if not os.path.isdir(dir_name):
                    os.mkdir(dir_name, mode=0o777)

                #if cv2.countNonZero(crop_img) > 0:
                    # only store image if it is NOT entirely black
                cv2.imwrite(os.path.join(dir_name, tile_name), crop_img)
        log.close()


if __name__ == "__main__":
    print("Converting images to tiles ...")
    path = ""
    try:
        path = sys.argv[1]
    except Exception as e:
        print("Argument error: ", e.__class__)

    convert_tiles(path)
