"""
=======================================
MVTec_AD_Pultrusion_Window_best_pipeline
=======================================
"""
import os

from param_tuning.hdev_manual_mean.hdev_manual_utils import get_custom_hdev_pipeline_code, convert_margin_to_int, \
    sobel_check_filter_type, area_size_threshold
from settings import EVIAS_SRC_PATH


def get_Pultrusion_Window_best_pipeline(params, dataset_path=None):
    pipeline_name = "Pultrusion_Window_best_pipeline"

    if dataset_path is None:
        dataset_path = "/Pultrusion/window_cgp/train/images"

    # Parameters
    param_lines = (
                "<l>        MinGray := " + str(params[0]) + "</l>\n"
                                                            "<l>        MaxGray := " + str(params[1]) + "</l>\n"
                                                                                                        "<c></c>\n"
                                                                                                        "<l>        FilterType := '" + str(
            params[2]) + "'</l>\n"
                         "<l>        MaskSize := " + str(params[3]) + "</l>\n"
                                                                      "<c></c>\n"
                                                                      "<l>        MinRatio := " + str(
            params[4]) + "</l>\n"
                         "<l>        MaskHeight := " + str(params[5]) + "</l>\n"
                                                                        "<l>        MaskWidth := " + str(
            params[6]) + "</l>\n"
                         "<c></c>\n"
    )

    # Core pipeline
    core_code = (
            "<c>* CropSmallestRectangle</c>\n"
            "<l>        threshold(Image, Region, MinGray, MaxGray)</l>\n"
            "<l>        smallest_rectangle1(Region, Row1, Column1, Row2, Column2)</l>\n"
            "<l>        crop_rectangle1(Image, Image2, Row1, Column1, Row2, Column2)</l>\n"
            "<c></c>\n"
            "<c>* SobelAmp with scaling/conversion</c>\n"
            "<l>        get_image_type(Image2, Type)</l>\n"
            "<l>        if (FilterType == 'x_binomial' or FilterType == 'y_binomial')</l>\n"
            "<l>            if (Type != 'byte' and Type != 'int2' and Type != 'real')</l>\n"
            "<l>                gen_empty_obj(ScaledImage)</l>\n"
            "<l>                min_max_gray(Image2, Image2, 0, MinGrayVal, MaxGrayVal, GrayRange)</l>\n"
            "<l>                if (not(MinGrayVal &lt;= 255 and MaxGrayVal &gt;= 0))</l>\n"
            "<l>                    if (MaxGrayVal - MinGrayVal &gt; 0)</l>\n"
            "<l>                        Mult := 255.0 / (MaxGrayVal - MinGrayVal)</l>\n"
            "<l>                    else</l>\n"
            "<l>                        Mult := 255.0</l>\n"
            "<l>                    endif</l>\n"
            "<l>                    Add := - Mult * MinGrayVal</l>\n"
            "<l>                    scale_image(Image2, ImageScaled, Mult, Add)</l>\n"
            "<l>                else</l>\n"
            "<l>                    scale_image(Image2, ImageScaled, Mult, Add)</l>\n"
            "<l>                endif</l>\n"
            "<l>                convert_image_type(ScaledImage, Image2, 'byte')</l>\n"
            "<l>            endif</l>\n"
            "<l>        elseif (Type != 'byte' and Type != 'int2' and Type != 'uint2' and Type != 'real')</l>\n"
            "<l>            gen_empty_obj(ScaledImage)</l>\n"
            "<l>            min_max_gray(Image2, Image2, 0, MinGrayVal, MaxGrayVal, GrayRange)</l>\n"
            "<l>            if (not(MinGrayVal &lt;= 255 and MaxGrayVal &gt;= 0))</l>\n"
            "<l>                if (MaxGrayVal - MinGrayVal &gt; 0)</l>\n"
            "<l>                    Mult := 255.0 / (MaxGrayVal - MinGrayVal)</l>\n"
            "<l>                else</l>\n"
            "<l>                    Mult := 255.0</l>\n"
            "<l>                endif</l>\n"
            "<l>                Add := - Mult * MinGrayVal</l>\n"
            "<l>                scale_image(Image2, ImageScaled, Mult, Add)</l>\n"
            "<l>            else</l>\n"
            "<l>                scale_image(Image2, ImageScaled, Mult, Add)</l>\n"
            "<l>            endif</l>\n"
            "<l>            convert_image_type(Image2, Image2, 'byte')</l>\n"
            "<l>        endif</l>\n"
            "<l>        sobel_amp(Image2, Image2, FilterType, MaskSize)</l>\n"
            "<c></c>\n"
            "<c>* CropRectangle (Relative Threshold)</c>\n"
            "<l>        gen_empty_obj(RelativeRegion)</l>\n"
            "<l>        count_channels(Image, NumChannels)</l>\n"
            "<l>        if (NumChannels &gt; 1)</l>\n"
            "<l>            access_channel(Image, Image, 1)</l>\n"
            "<l>        endif</l>\n"
            "<l>        get_image_type(Image, ImgType)</l>\n"
            "<l>        if (ImgType != 'byte' and ImgType != 'uint2' and ImgType != 'direction' and ImgType != 'cyclic' and ImgType != 'real')</l>\n"
            "<l>            convert_image_type(Image, Image, 'byte')</l>\n"
            "<l>        endif</l>\n"
            "<l>        fast_threshold(Image, Region, 45, 255, 80)</l>\n"
            "<l>        fill_up(Region, Rectangle)</l>\n"
            "<l>        smallest_rectangle1(Rectangle, Row1, Col1, Row2, Col2)</l>\n"
            "<l>        reduce_domain(Image, Rectangle, NewImgReduced)</l>\n"
            "<l>        region_features(Rectangle, 'width', Width)</l>\n"
            "<l>        region_features(Rectangle, 'height', Height)</l>\n"
            "<l>        WStep := Width / MaskWidth</l>\n"
            "<l>        HStep := Height / MaskHeight</l>\n"
            "<l>        EndW := (Col2 - (WStep / 1.5)) - 20</l>\n"
            "<l>        StepW := WStep / 2</l>\n"
            "<l>        for ImgWidth := Col1 + 20 to EndW by StepW</l>\n"
            "<l>            EndH := Row2 - (HStep / 1.5)</l>\n"
            "<l>            StepH := HStep / 2</l>\n"
            "<l>            for ImgHeight := Row1 + 3 to EndH by StepH</l>\n"
            "<l>                crop_rectangle1(NewImgReduced, ImgPart, ImgHeight, ImgWidth, ImgHeight + HStep, ImgWidth + WStep)</l>\n"
            "<l>                gray_histo_range(ImgPart, ImgPart, 0, 255, 2, Histo, BinSize)</l>\n"
            "<l>                PixelCount := Histo[0] + Histo[1]</l>\n"
            "<l>                if (PixelCount &gt; 0.6 * WStep * HStep)</l>\n"
            "<l>                    Ratio := Histo[1] / PixelCount</l>\n"
            "<l>                    if (Ratio &lt; MinRatio)</l>\n"
            "<l>                        gen_rectangle1(FaultyRegion, ImgHeight, ImgWidth, ImgHeight + HStep, ImgWidth + WStep)</l>\n"
            "<l>                        union2(RelativeRegion, FaultyRegion, RelativeRegion)</l>\n"
            "<l>                    endif</l>\n"
            "<l>                endif</l>\n"
            "<l>            endfor</l>\n"
            "<l>        endfor</l>\n"
            "<l>        Region := RelativeRegion</l>\n"
            "<c></c>\n"
            "<c>* AreaToRectangle</c>\n"
            "<l>        area_center(Region, Area, Row, Column)</l>\n"
            "<l>        gen_rectangle1(RectangleRegion, Row - Area/2, Column - Area/2, Row + Area/2, Column + Area/2)</l>\n"
            "<l>        union2(Region, RectangleRegion, Region)</l>\n"
    )

    return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)

Pultrusion_Window_best_pipeline_initial_params = [
    21,  # MinGray
    255,  # MaxGray
    'y',  # FilterType
    3,  # MaskSize
    0.04,  # MinRatio
    27,  # MaskHeight
    29  # MaskWidt
]

Pultrusion_Window_best_pipeline_bounds = [
    [v for v in range(0, 256)],  # MinGray
    [v for v in range(0, 256)],  # MaxGray
    ['x', 'y', 'x_binomial', 'y_binomial'],  # FilterType
    [3, 5, 7, 9, 11],  # MaskSize
    [round(0.01 * v, 3) for v in range(0, 101)],  # MinRatio
    [v for v in range(1, 100)],  # MaskHeight
    [v for v in range(1, 100)]  # MaskWidth
]

Pultrusion_Window_training_source_path = os.path.join(EVIAS_SRC_PATH,
                                                      "Pultrusion", "window_cgp", "train")
