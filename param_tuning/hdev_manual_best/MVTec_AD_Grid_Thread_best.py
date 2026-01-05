"""
=======================================
MVTec_AD_Grid_best_pipeline
=======================================
"""
import os

from param_tuning.hdev_manual_mean.hdev_manual_utils import get_custom_hdev_pipeline_code, get_ellipse_struct_code, \
    get_crop_rectangle_code
from settings import EVIAS_SRC_PATH


def get_MVTec_AD_Grid_Thread_best_pipeline(params, dataset_path=None):
    pipeline_name = "MVTec_AD_Grid_best_pipeline"

    if dataset_path is None:
        dataset_path = "/MVTecAnomalyDetection/grid_thread_train/images"

    # Parameters
    param_lines = "<l>        MaskHeightBinomial := " + str(params[0]) + "</l>\n" + \
                      "<l>        MaskWidthBinomial := " + str(params[1]) + "</l>\n" + \
                      "<c></c>\n" + \
                      "<l>        MinRatio := " + str(params[2]) + "</l>\n" + \
                      "<l>        MaskHeightCrop := " + str(params[3]) + "</l>\n" + \
                      "<l>        MaskWidthCrop := " + str(params[4]) + "</l>\n" + \
                      "<c></c>\n"

    # Core pipeline
    core_code = (
            "<l>        binomial_filter(Image, ImageBinomial, MaskWidthBinomial, MaskHeightBinomial)</l>\n"
            "<c></c>\n"
            "<c>        * CropRectangle (Relative Threshold)</c>\n"
            "<l>        gen_empty_obj (RelativeRegion)</l>\n"
            "<l>        count_channels (ImageBinomial, NumChannels)</l>\n"
            "<l>        if (NumChannels > 1)</l>\n"
            "<l>            access_channel (ImageBinomial, ImageBinomial, 1)</l>\n"
            "<l>        endif</l>\n"
            "<l>        get_image_type (ImageBinomial, ImgType)</l>\n"
            "<l>        if (ImgType != 'byte' and ImgType != 'uint2' and ImgType != 'direction' and ImgType != 'cyclic' and ImgType != 'real')</l>\n"
            "<l>            convert_image_type (ImageBinomial, ImageBinomial, 'byte')</l>\n"
            "<l>        endif</l>\n"
            "<l>        fast_threshold (ImageBinomial, Region, 45, 255, 80)</l>\n"
            "<l>        fill_up (Region, Rectangle)</l>\n"
            "<l>        smallest_rectangle1 (Rectangle, Row1, Col1, Row2, Col2)</l>\n"
            "<l>        reduce_domain (ImageBinomial, Rectangle, NewImgReduced)</l>\n"
            "<l>        region_features (Rectangle, 'width', Width)</l>\n"
            "<l>        region_features (Rectangle, 'height', Height)</l>\n"
            "<l>        WStep := Width / MaskWidthCrop</l>\n"
            "<l>        HStep := Height / MaskHeightCrop</l>\n"
            "<l>        EndW := (Col2 - (WStep / 1.5)) - 20</l>\n"
            "<l>        StepW := WStep / 2</l>\n"
            "<l>        for ImgWidth := Col1 + 20 to EndW by StepW</l>\n"
            "<l>            EndH := Row2 - (HStep / 1.5)</l>\n"
            "<l>            StepH := HStep / 2</l>\n"
            "<l>            for ImgHeight := Row1 + 3 to EndH by StepH</l>\n"
            "<l>                crop_rectangle1 (NewImgReduced, ImgPart, ImgHeight, ImgWidth, ImgHeight + HStep, ImgWidth + WStep)</l>\n"
            "<l>                gray_histo_range (ImgPart, ImgPart, 0, 255, 2, Histo, BinSize)</l>\n"
            "<l>                PixelCount := Histo[0] + Histo[1]</l>\n"
            "<l>                if (PixelCount > 0.6 * WStep * HStep)</l>\n"
            "<l>                    Ratio := Histo[1] / PixelCount</l>\n"
            "<l>                    if (Ratio &lt; MinRatio)</l>\n"
            "<l>                        gen_rectangle1 (FaultyRegion, ImgHeight, ImgWidth, ImgHeight + HStep, ImgWidth + WStep)</l>\n"
            "<l>                        union2 (RelativeRegion, FaultyRegion, RelativeRegion)</l>\n"
            "<l>                    endif</l>\n"
            "<l>                endif</l>\n"
            "<l>            endfor</l>\n"
            "<l>        endfor</l>\n"
            "<l>        Region := RelativeRegion</l>\n"
    )

    return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)

MVTec_AD_Grid_Thread_best_pipeline_initial_params = [
    27,  # MaskHeightBinomial
    31,  # MaskWidthBinomial
    0.055,  # MinRatio
    9,  # MaskHeightCrop
    21  # MaskWidthCrop
]

MVTec_AD_Grid_Thread_best_pipeline_bounds = [
    [v for v in range(3, 100, 2)],  # MaskHeightBinomial
    [v for v in range(3, 100, 2)],  # MaskWidthBinomial
    [round(0.01 * v, 2) for v in range(0, 20)],  # MinRatio
    [v for v in range(1, 100)],  # MaskHeightCrop
    [v for v in range(1, 200)]  # MaskWidthCrop
]

MVTec_AD_Grid_Thread_training_source_path = os.path.join(EVIAS_SRC_PATH,
                                                         "MVTecAnomalyDetection", "grid_thread_train")
