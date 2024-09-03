from param_tuning.hdev.hdev_templates import HDEV_HEADER, HDEV_TEMPLATE_CODE, HDEV_FOOTER
from param_tuning.utils import get_evias_experimts_path_for_hdev


def scale_to_gray():
    scale_to_gray = "<c>        * Scale To Gray</c>\n" + \
                    "<l>        gen_empty_obj(ScaledImage)</l>\n" + \
                    "<l>        min_max_gray(Image, Image, 0, MinGrayVal, MaxGrayVal, GrayRange)</l>\n" + \
                    "<l>        if(not(MinGrayVal <= 255 and MaxGrayVal >= 0))</l>\n" + \
                    "<l>            if(MaxGrayVal - MinGrayVal > 0)</l>\n" + \
                    "<l>                Mult := 255.0 / (MaxGrayVal - MinGrayVal)</l>\n" + \
                    "<l>            else</l>\n" + \
                    "<l>                Mult := 255.0</l>\n" + \
                    "<l>            endif</l>\n" + \
                    "<l>            Add := - Mult * MinGrayVal</l>\n" + \
                    "<l>            scale_image(Image, ImageScaled, Mult, Add)</l>\n" + \
                    "<l>        else</l>\n" + \
                    "<l>            scale_image(Image, ImageScaled, Mult, Add)    </l>\n" + \
                    "<l>       endif</l>\n"
    return scale_to_gray


def scale_to_gray_img2():
    scale_to_gray_img2 = "<c>        * Scale To Gray</c>\n" + \
                         "<l>        gen_empty_obj(ScaledImage)</l>\n" + \
                         "<l>        min_max_gray(Image2, Image2, 0, MinGrayVal, MaxGrayVal, GrayRange)</l>\n" + \
                         "<l>        if(not(MinGrayVal <= 255 and MaxGrayVal >= 0))</l>\n" + \
                         "<l>            if(MaxGrayVal - MinGrayVal > 0)</l>\n" + \
                         "<l>                Mult := 255.0 / (MaxGrayVal - MinGrayVal)</l>\n" + \
                         "<l>            else</l>\n" + \
                         "<l>                Mult := 255.0</l>\n" + \
                         "<l>            endif</l>\n" + \
                         "<l>            Add := - Mult * MinGrayVal</l>\n" + \
                         "<l>            scale_image(Image2, ImageScaled, Mult, Add)</l>\n" + \
                         "<l>        else</l>\n" + \
                         "<l>            scale_image(Image2, ImageScaled, Mult, Add)    </l>\n" + \
                         "<l>       endif</l>\n"
    return scale_to_gray_img2


def get_var_threshold_code():
    var_threshold_code = "<c>        * VarThreshold</c>\n" + \
                         "<l>        get_image_type(Image, Type)  </l>\n" + \
                         "<l>        if(Type != 'byte' and Type != 'int2' and Type != 'int4' and Type != 'uint2' and " \
                         "Type != 'real')</l>\n" + \
                         scale_to_gray() + \
                         "<l>            convert_image_type(ScaledImage, Image, 'byte')</l>\n" + \
                         "<l>            var_threshold(Image, Region, MaskWidth, MaskHeight, StdDevScale, " \
                         "AbsThreshold, LightDark)</l>\n" + \
                         "<l>        else</l>\n" + \
                         "<l>            var_threshold(Image, Region, MaskWidth, MaskHeight, StdDevScale, " \
                         "AbsThreshold, LightDark)</l>\n" + \
                         "<l>        endif</l>\n" + \
                         "<c></c>\n"
    return var_threshold_code


def get_ellipse_struct_code(A, B, phi):
    if phi is None:
        phi = 0.0
    ellipse_struct_code = f"<l>        * StructElementType Ellipse</l>\n" + \
                          f"<l>        * using A, B and C as shape_params</l>\n" + \
                          f"<l>        tuple_max2({A}, {B}, max_rad)</l>\n" + \
                          f"<l>        longer := {A}</l>\n" + \
                          f"<l>        shorter := {B}</l>\n" + \
                          f"<l>        if (shorter &gt; longer)</l>\n" + \
                          f"<l>            tmp := shorter</l>\n" + \
                          f"<l>            shorter := longer</l>\n" + \
                          f"<l>            longer := tmp</l>\n" + \
                          f"<l>        endif</l>\n" + \
                          f"<l>        phi := {phi}</l>\n" + \
                          f"<l>        tuple_ceil({A} + 1, max_rad_ceil)</l>\n" + \
                          f"<l>        gen_ellipse(StructElement, max_rad_ceil, max_rad_ceil, phi, longer, " \
                          f"shorter)</l>\n" + \
                          f"<l>        * Apply StructElement Ellipse</l>\n"
    return ellipse_struct_code


def get_crop_rectangle_code():
    crop_rectangle_code = "<c></c>\n" \
                          "<c>        * CropRectangle  </c>\n" \
                          "<l>        tuple_real(MinRatio, MinRatio)</l>\n" \
                          "<l>        gen_empty_region(Region)</l>\n" \
                          "<c></c>\n" \
                          "<l>        count_channels(Image, NumChannels)</l>\n" \
                          "<l>        if(NumChannels > 1)</l>\n" \
                          "<l>            access_channel(Image, Image, 1)</l>\n" \
                          "<l>        endif</l>\n" \
                          "<c></c>\n" \
                          "<l>        get_image_type(Image, Type)</l>\n" \
                          "<l>        if(Type != 'byte' and Type != 'uint2' and Type != 'direction' and Type != 'cyclic' and " \
                          "Type != 'real')</l>\n" + \
                          scale_to_gray() + \
                          "<l>            convert_image_type(ScaledImage, Image, 'byte')</l>\n" \
                          "<l>        endif</l>\n" \
                          "<c></c>\n" \
                          "<l>        fast_threshold(Image, Region, 45, 255, 80)</l>\n" \
                          "<l>        fill_up(Region, Rectangle)</l>\n" \
                          "<c></c>\n" \
                          "<l>        gen_empty_obj(FaultyRegion)</l>\n" \
                          "<l>        gen_empty_obj(NewImgReduced)</l>\n" \
                          "<l>        gen_empty_obj(ImgPart)</l>\n" \
                          "<l>        gen_empty_obj(RelativeRegion)</l>\n" \
                          "<c></c>\n" \
                          "<l>        smallest_rectangle1(Rectangle, Row1, Col1, Row2, Col2)</l>\n" \
                          "<l>        reduce_domain(Image, Rectangle, NewImageReduced)</l>\n" \
                          "<l>        region_features(Rectangle, 'width', RegWidth)</l>\n" \
                          "<l>        region_features(Rectangle, 'height', RegHeight)</l>\n" \
                          "<c></c>\n" \
                          "<l>        WStep := RegWidth / MaskWidth</l>\n" \
                          "<l>        HStep := RegHeight / MaskHeight</l>\n" \
                          "<c></c>\n" \
                          "<l>        EndW := (Col2 - (WStep / 1.5)) - 20</l>\n" \
                          "<l>        StepW := WStep / 2</l>\n" \
                          "<c></c>\n" \
                          "<l>        for ImgWidth := Col1 + 20 to EndW by StepW</l>\n" \
                          "<l>            EndH := Row2 - (HStep / 1.5)    </l>\n" \
                          "<l>            StepH := HStep / 2</l>\n" \
                          "<c></c>\n" \
                          "<l>            if(StepW == 0.0)</l>\n" \
                          "<l>                break</l>\n" \
                          "<l>            endif</l>\n" \
                          "<c></c>\n" \
                          "<l>            for ImgHeight := Row1 + 3 to EndH by StepH</l>\n" \
                          "<l>                if(StepH == 0.0)</l>\n" \
                          "<l>                    break</l>\n" \
                          "<l>                endif</l>\n" \
                          "<c></c>\n" \
                          "<l>                gen_empty_obj(ImagePart)</l>\n" \
                          "<l>                crop_rectangle1(NewImageReduced, ImgPart, ImgHeight, ImgWidth, ImgHeight + HStep, ImgWidth + WStep)</l>\n" \
                          "<c></c>\n" \
                          "<l>                gray_histo_range(ImgPart, ImgPart, 0, 255, 2, Histo, BinSize)</l>\n" \
                          "<c></c>\n" \
                          "<l>                PixelCount := Histo[0] + Histo[1]</l>\n" \
                          "<c></c>\n" \
                          "<l>                tuple_real(PixelCount, PixelCount)</l>\n" \
                          "<c></c>\n" \
                          "<l>                if(PixelCount &lt;= 0.6 * WStep * HStep)</l>\n" \
                          "<l>                    continue</l>\n" \
                          "<l>                endif</l>\n" \
                          "<l>                Ratio := (Histo[1] * 1.0) / (PixelCount * 1.0)</l>\n" \
                          "<c></c>\n" \
                          "<l>                if(Ratio &lt;= MinRatio)</l>\n" \
                          "<l>                    gen_rectangle1(FaultyRegion, ImgHeight, ImgWidth, ImgHeight + HStep, " \
                          "ImgWidth + WStep)</l>\n" \
                          "<l>                    concat_obj(FaultyRegion, RelativeRegion, FaultyRegion)</l>\n" \
                          "<l>                    union1(FaultyRegion, RelativeRegion)</l>\n" \
                          "<l>                endif</l>\n" \
                          "<l>            endfor</l>\n" \
                          "<l>        endfor</l>\n" \
                          "<c></c>\n" \
                          "<l>        count_obj(RelativeRegion, Number)</l>\n" \
                          "<l>        if(Number == 0)</l>\n" \
                          "<l>            gen_empty_region(Region)</l>\n" \
                          "<l>        else</l>\n" \
                          "<l>            Region := RelativeRegion</l>\n" \
                          "<l>        endif</l>\n" \
                          "<c></c>\n"
    return crop_rectangle_code


def get_crop_rectangle_img2_code():
    crop_rectangle_img2_code = "<c></c>\n" \
                               "<c>        * CropRectangle  </c>\n" \
                               "<l>        tuple_real(MinRatio, MinRatio)</l>\n" \
                               "<l>        gen_empty_region(Region2)</l>\n" \
                               "<c></c>\n" \
                               "<l>        count_channels(Image2, NumChannels)</l>\n" \
                               "<l>        if(NumChannels > 1)</l>\n" \
                               "<l>            access_channel(Image2, Image2, 1)</l>\n" \
                               "<l>        endif</l>\n" \
                               "<c></c>\n" \
                               "<l>        get_image_type(Image2, Type)</l>\n" \
                               "<l>        if(Type != 'byte' and Type != 'uint2' and Type != 'direction' and Type != 'cyclic' and " \
                               "Type != 'real')</l>\n" + \
                               scale_to_gray_img2() + \
                               "<l>            convert_image_type(ScaledImage, Image2, 'byte')</l>\n" \
                               "<l>        endif</l>\n" \
                               "<c></c>\n" \
                               "<l>        fast_threshold(Image2, Region2, 45, 255, 80)</l>\n" \
                               "<l>        fill_up(Region2, Rectangle)</l>\n" \
                               "<c></c>\n" \
                               "<l>        gen_empty_obj(FaultyRegion)</l>\n" \
                               "<l>        gen_empty_obj(NewImgReduced)</l>\n" \
                               "<l>        gen_empty_obj(ImgPart)</l>\n" \
                               "<l>        gen_empty_obj(RelativeRegion)</l>\n" \
                               "<c></c>\n" \
                               "<l>        smallest_rectangle1(Rectangle, Row1, Col1, Row2, Col2)</l>\n" \
                               "<l>        reduce_domain(Image2, Rectangle, NewImageReduced)</l>\n" \
                               "<l>        region_features(Rectangle, 'width', RegWidth)</l>\n" \
                               "<l>        region_features(Rectangle, 'height', RegHeight)</l>\n" \
                               "<c></c>\n" \
                               "<l>        WStep := RegWidth / MaskWidth</l>\n" \
                               "<l>        HStep := RegHeight / MaskHeight</l>\n" \
                               "<c></c>\n" \
                               "<l>        EndW := (Col2 - (WStep / 1.5)) - 20</l>\n" \
                               "<l>        StepW := WStep / 2</l>\n" \
                               "<c></c>\n" \
                               "<l>        for ImgWidth := Col1 + 20 to EndW by StepW</l>\n" \
                               "<l>            EndH := Row2 - (HStep / 1.5)    </l>\n" \
                               "<l>            StepH := HStep / 2</l>\n" \
                               "<c></c>\n" \
                               "<l>            if(StepW == 0.0)</l>\n" \
                               "<l>                break</l>\n" \
                               "<l>            endif</l>\n" \
                               "<c></c>\n" \
                               "<l>            for ImgHeight := Row1 + 3 to EndH by StepH</l>\n" \
                               "<l>                if(StepH == 0.0)</l>\n" \
                               "<l>                    break</l>\n" \
                               "<l>                endif</l>\n" \
                               "<c></c>\n" \
                               "<l>                gen_empty_obj(ImagePart)</l>\n" \
                               "<l>                crop_rectangle1(NewImageReduced, ImgPart, ImgHeight, ImgWidth, ImgHeight + HStep, ImgWidth + WStep)</l>\n" \
                               "<c></c>\n" \
                               "<l>                gray_histo_range(ImgPart, ImgPart, 0, 255, 2, Histo, BinSize)</l>\n" \
                               "<c></c>\n" \
                               "<l>                PixelCount := Histo[0] + Histo[1]</l>\n" \
                               "<c></c>\n" \
                               "<l>                tuple_real(PixelCount, PixelCount)</l>\n" \
                               "<c></c>\n" \
                               "<l>                if(PixelCount &lt;= 0.6 * WStep * HStep)</l>\n" \
                               "<l>                    continue</l>\n" \
                               "<l>                endif</l>\n" \
                               "<l>                Ratio := (Histo[1] * 1.0) / (PixelCount * 1.0)</l>\n" \
                               "<c></c>\n" \
                               "<l>                if(Ratio &lt;= MinRatio)</l>\n" \
                               "<l>                    gen_rectangle1(FaultyRegion, ImgHeight, ImgWidth, ImgHeight + HStep, " \
                               "ImgWidth + WStep)</l>\n" \
                               "<l>                    concat_obj(FaultyRegion, RelativeRegion, FaultyRegion)</l>\n" \
                               "<l>                    union1(FaultyRegion, RelativeRegion)</l>\n" \
                               "<l>                endif</l>\n" \
                               "<l>            endfor</l>\n" \
                               "<l>        endfor</l>\n" \
                               "<c></c>\n" \
                               "<l>        count_obj(RelativeRegion, Number)</l>\n" \
                               "<l>        if(Number == 0)</l>\n" \
                               "<l>            gen_empty_region(Region2)</l>\n" \
                               "<l>        else</l>\n" \
                               "<l>            Region2 := RelativeRegion</l>\n" \
                               "<l>        endif</l>\n" \
                               "<c></c>\n"
    return crop_rectangle_img2_code


def get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code):
    hdev_code = HDEV_HEADER

    # Dataset name and path
    hdev_code += "<l>dataset_name := '" + pipeline_name + "'</l>\n" + \
                 "<l>source_path := '" + get_evias_experimts_path_for_hdev() + dataset_path + "'</l>\n" + \
                 "<l>output_path := dataset_name + '/'</l>\n" + \
                 "<c></c>\n"

    hdev_code += HDEV_TEMPLATE_CODE

    for line in param_lines:
        hdev_code += line

    hdev_code += core_code

    hdev_code += HDEV_FOOTER

    return hdev_code


def get_area_to_rectangle():
    area_to_rectangle_code = "<c>        * AreaToRectangle</c>\n" + \
                             "<l>        area_center(Region, Area, Row, Column)</l>\n" + \
                             "<l>        Num:= | Area |</l>\n" + \
                             "<l>        gen_empty_region(Rectangles)</l>\n" + \
                             "<l>        for Index1 := 1 to Num by 1</l>\n" + \
                             "<l>            select_obj(Region, obj, Index1)</l>\n" + \
                             "<l>            smallest_rectangle1(obj, Row11, Column11, Row21, Column21)</l>\n" + \
                             "<l>            gen_rectangle1(Rectangle, Row11, Column11, Row21, Column21)</l>\n" + \
                             "<l>            union2(Rectangles, Rectangle, Rectangles)</l>\n" + \
                             "<l>        endfor</l>\n"
    return area_to_rectangle_code


def convert_margin_to_int():
    margin_to_int = "<l>        if(Margin == 'Zero')</l>\n" \
                    "<l>            Margin := 0</l>\n" \
                    "<l>        elseif(Margin == 'Thirty')</l>\n" \
                    "<l>            Margin := 30</l>\n" \
                    "<l>        elseif(Margin == 'Sixty')</l>\n" \
                    "<l>            Margin := 60</l>\n" \
                    "<l>        elseif(Margin == 'Ninety')</l>\n" \
                    "<l>            Margin := 90</l>\n" \
                    "<l>        elseif(Margin == 'OneTwenty')</l>\n" \
                    "<l>            Margin := 120</l>\n" \
                    "<l>        elseif(Margin == 'OneFifty')</l>\n" \
                    "<l>            Margin := 150</l>\n" \
                    "<l>        elseif(Margin == 'OneEighty')</l>\n" \
                    "<l>            Margin := 180</l>\n" \
                    "<l>        elseif(Margin == 'TwoTen')</l>\n" \
                    "<l>            Margin := 210</l>\n" \
                    "<l>        elseif(Margin == 'TwoForty')</l>\n" \
                    "<l>            Margin := 240</l>\n" \
                    "<l>        elseif(Margin == 'TwoFiftyFive')</l>\n" \
                    "<l>            Margin := 255</l>\n" \
                    "<l>        endif</l>\n" \
                    "<c>        </c>\n"
    return margin_to_int


def sobel_check_filter_type():
    check_filter_code = "<l>        get_image_type(Image, Type)</l>\n" \
                        "<l>        if(FilterType == 'x_binomial' or FilterType == 'y_binomial')    </l>\n" \
                        "<l>            if(Type != 'byte' and Type != 'int2' and Type != 'real')</l>\n" + \
                        scale_to_gray() + \
                        "<l>                convert_image_type(Image, Image, 'byte')</l>\n" \
                        "<l>            endif</l>\n" \
                        "<l>        elseif(Type != 'byte' and Type != 'int2' and Type != 'uint2' and Type != 'real')</l>\n" + \
                        scale_to_gray() + \
                        "<l>            convert_image_type(Image, Image, 'byte')</l>\n" \
                        "<l>        endif</l>\n"
    return check_filter_code


def area_size_threshold():
    ares_size_threshold_code = "<c>        * AreaSizeThreshold</c>\n" + \
                               "<l>        abs_image(Image, Image)</l>\n" + \
                               "<c>        </c>\n" + \
                               "<c>        * MinGray := 20</c>\n" + \
                               "<c>        * MaxGray := 255</c>\n" + \
                               "<l>        gen_empty_region(FaultyRegion)</l>\n" + \
                               "<l>        gen_empty_region(TempRegion)</l>\n" + \
                               "<l>        get_image_size(Image, Width, Height)</l>\n" + \
                               "<c>        </c>\n" + \
                               "<l>        I_W := Width / WindowWidth</l>\n" + \
                               "<l>        I_H := Height / WindowHeight</l>\n" + \
                               "<c>        </c>\n" + \
                               "<l>        for i := 0 to I_W by 1</l>\n" + \
                               "<l>            for j := 0 to I_H by 1</l>\n" + \
                               "<l>                Row1 := j * WindowHeight</l>\n" + \
                               "<l>                Col1 := i * WindowHeight</l>\n" + \
                               "<l>                Row2 := j * WindowHeight + WindowHeight</l>\n" + \
                               "<l>                Col2 := i * WindowHeight + WindowHeight</l>\n" + \
                               "<c>        </c>\n" + \
                               "<l>                if(Row2 &gt; Height)</l>\n" + \
                               "<l>                    Row2 := Height</l>\n" + \
                               "<l>                endif</l>\n" + \
                               "<c>        </c>\n" + \
                               "<l>                if(Col2	&gt; Width)</l>\n" + \
                               "<l>                    Col2 := Width</l>\n" + \
                               "<l>                endif</l>\n" + \
                               "<c>        </c>\n" + \
                               "<l>                if(Row1 &gt; Height)</l>\n" + \
                               "<l>                    Row1 := Height - 1</l>\n" + \
                               "<l>                endif</l>\n" + \
                               "<l>                if(Col1 &gt; Width)</l>\n" + \
                               "<l>                    Col1 := Width - 1</l>\n" + \
                               "<l>                endif</l>\n" + \
                               "<c>        </c>\n" + \
                               "<l>                crop_rectangle1(Image, ImagePart, Row1, Col1, Row2, Col2)</l>\n" + \
                               "<l>                threshold(ImagePart, Threads, 40, 255)</l>\n" + \
                               "<l>                area_center(Threads, AreaSize, Row, Col)</l>\n" + \
                               "<c>        </c>\n" + \
                               "<l>                if(AreaSize &lt; MaxSize and AreaSize &gt; MinSize)</l>\n" + \
                               "<l>                    gen_rectangle1(TempRegion, Row1, Col1, Row2, Col2)</l>\n" + \
                               "<l>                    union2(TempRegion, FaultyRegion, FaultyRegion)</l>\n" + \
                               "<l>                endif</l>\n" + \
                               "<c>        </c>\n" + \
                               "<l>                smallest_rectangle1(FaultyRegion, Row1, Col1, Row2, Col2)</l>\n" + \
                               "<l>                region_features(FaultyRegion, 'area', Value)</l>\n" + \
                               "<l>            endfor</l>\n" + \
                               "<l>        endfor</l>\n" + \
                               "<c>        </c>\n" + \
                               "<l>        count_obj(FaultyRegion, Number)</l>\n" + \
                               "<l>        if(Number > 0)</l>\n" + \
                               "<l>            Region := FaultyRegion</l>\n" + \
                               "<l>        else</l>\n" + \
                               "<l>            gen_empty_region(Region)</l>\n" + \
                               "<l>        endif</l>\n" + \
                               "<c>        </c>\n"
    return ares_size_threshold_code
