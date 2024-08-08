import os

HDEV_FOLDER = os.path.join("C:\\", "dev", "experiments", "test")

HDEV_FUNCTIONS = {
        'BinomialFilter': {
                'name': 'binomial_filter',
                'in': 'Image',
                'out': 'Image'
        },
        'FastThreshold': {
                'name': 'fast_threshold',
                'in': 'Image',
                'out': 'Region'
        }
}

HDEV_HEADER = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n" \
        "<hdevelop file_version=\"1.1\" halcon_version=\"13.0\">\n" \
        "<procedure name=\"main\">\n" \
        "<interface/>\n"\
        "<body>\n" \
        "<l>list_image_files('imgs', 'default', [], ImageFiles)</l>\n" \
        "<l>for Index := 1 to |ImageFiles| - 1 by 1</l>\n" \
        "<l>    read_image(Image, ImageFiles[Index])</l>\n" \
        "<l>    get_image_size(Image, Width, Height)</l>\n"\
        "<c>    * --------------</c>\n"\
        "<c>    * CGP Code Block</c>\n"\
        "<c>    * --------------    </c>\n"

HDEV_MIDDLE = "<l>    binomial_filter(Image, Image, 35, 29)</l>\n"\
        "<l>    fast_threshold(Image, Region, 155, 196, 22)\n"\
        "</l>\n"

HDEV_FOOTER = "<c>    * --------------</c>\n"\
        "<c>    * END Code Block</c>\n"\
        "<c>    * --------------</c>\n"\
        "<l>    gen_image_const(ImageResult, 'byte', Width, Height)</l>\n"\
        "<l>    paint_region(Region, ImageResult, ImageResult, 255, 'margin')</l>\n"\
        "<l>    out_img_path := 'out/' + Index</l>\n"\
        "<l>    *write_image(ImageResult, 'png', 0, out_img_path)</l>\n"\
        "<l>endfor</l>\n" \
        "<l>exit()</l>\n" \
        "</body>\n" \
        "<docu id=\"main\">\n" \
        "<parameters/>\n" \
        "</docu>\n" \
        "</procedure>\n" \
        "</hdevelop>"