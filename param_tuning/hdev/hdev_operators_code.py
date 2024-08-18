"""
HDEV Operators Code
    contains public variables for each hdev function used in CGP optimization
    that returns the main code of a function using the default variables
"""
AREA_SIZE_THRESHOLD_HDEV = "<procedure name='area_size_threshold'>\n" \
                                "<interface>\n" \
                                "<io>\n" \
                                "<par name='Image' base_type='iconic' dimension='0'/>\n" \
                                "</io>\n" \
                                "<oo>\n" \
                                "<par name='Region' base_type='iconic' dimension='0'/>\n" \
                                "</oo>\n" \
                                "<ic>\n" \
                                "<par name='minGray' base_type='ctrl' dimension='0'/>\n" \
                                "<par name='maxGray' base_type='ctrl' dimension='0'/>\n" \
                                "<par name='minSize' base_type='ctrl' dimension='0'/>\n" \
                                "<par name='maxSize' base_type='ctrl' dimension='0'/>\n" \
                                "<par name='W_Size' base_type='ctrl' dimension='0'/>\n" \
                                "<par name='H_Size' base_type='ctrl' dimension='0'/>\n" \
                                "</ic>\n" \
                                "</interface>\n" \
                                "<body>\n" \
                                "<l>gen_empty_region(Region)</l>\n" \
                                "<l>gen_empty_region(TempRegion)</l>\n" \
                                "<c>        </c>\n" \
                                "<l>get_image_size(Image, Width, Height)</l>\n" \
                                "<c>        </c>\n" \
                                "<l>I_W := Width / W_Size</l>\n" \
                                "<l>I_H := Height / H_Size</l>\n" \
                                "<c>        </c>\n" \
                                "<l>for I := 0 to I_W by 1</l>\n" \
                                "<l>    for J := 0 to I_H by 1</l>\n" \
                                "<l>        row1 := J * H_Size</l>\n" \
                                "<l>        column1 := I * W_Size</l>\n" \
                                "<l>        row2 := J * H_Size + H_Size</l>\n" \
                                "<l>        column2 := I * W_Size + W_Size</l>\n" \
                                "<c>               </c>\n" \
                                "<l>        if (row2 &gt; Height)</l>\n" \
                                "<l>            row2 := Height</l>\n" \
                                "<l>        endif         </l>\n" \
                                "<l>        if (column2 &gt; Width)                   </l>\n" \
                                "<l>            column2 := Width</l>\n" \
                                "<l>        endif</l>\n" \
                                "<l>        if (row1 &gt; Height)</l>\n" \
                                "<l>            row1 := Height - 1</l>\n" \
                                "<l>        endif</l>\n" \
                                "<l>        if (column1 &gt; Width)</l>\n" \
                                "<l>            column1 := Width - 1</l>\n" \
                                "<l>        endif</l>\n" \
                                "<c>               </c>\n" \
                                "<l>        crop_rectangle1(Image, ImagePart, row1, column1, row2, column2)</l>\n" \
                                "<l>        threshold(ImagePart, threads, 40, 255)</l>\n" \
                                "<c>               </c>\n" \
                                "<l>        area_center(threads, area_size, row, col)</l>\n" \
                                "<c>                              </c>\n" \
                                "<l>        if (area_size &lt; maxSize and area_size &gt; minSize)</l>\n" \
                                "<l>            gen_rectangle1(Rectangle, row1, column1, row2, column2)</l>\n" \
                                "<l>            union2(TempRegion, Region, Region)</l>\n" \
                                "<l>        endif</l>\n" \
                                "<l>    endfor</l>\n" \
                                "<l>endfor</l>\n" \
                                "<c>        </c>\n" \
                                "<l>smallest_rectangle1(Region, row1, column1, row2, column2)</l>\n" \
                                "<l>region_features(Region, 'area', Value)</l>\n" \
                                "</body>\n" \
                                "<docu id='area_size_threshold'>\n" \
                                "<parameters>\n" \
                                "<parameter id='H_Size'/>\n" \
                                "<parameter id='Image'/>\n" \
                                "<parameter id='Region'/>\n" \
                                "<parameter id='W_Size'/>\n" \
                                "<parameter id='maxGray'/>\n" \
                                "<parameter id='maxSize'/>\n" \
                                "<parameter id='minGray'/>\n" \
                                "<parameter id='minSize'/>\n" \
                                "</parameters>\n" \
                                "</docu>\n" \
                                "</procedure>"

AUTO_THRESHOLD_HDEV = ""

BINOMIAL_FILTER_HDEV = ""

FAST_THRESHOLD_HDEV = ""

GRAY_CLOSING_HDEV = ""

SOBEL_AMP_HDEV = ""