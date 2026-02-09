"""
=======================================
MVTec_AD_Pill_Crack_best_pipeline
=======================================
"""
import os

from param_tuning.hdev_manual_mean.hdev_manual_utils import get_custom_hdev_pipeline_code, get_crop_rectangle_code
from settings import EVIAS_SRC_PATH


def get_MVTec_AD_Pill_Crack_best_pipeline(params, dataset_path=None):
    pipeline_name = "MVTec_AD_Pill_Crack_best_pipeline"

    if dataset_path is None:
        dataset_path = "/MVTecAnomalyDetection/pill_crack_train/images"

    # Parameters
    param_lines = "<l>        A1 := " + str(params[0]) + "</l>\n" + \
                      "<l>        B1 := " + str(params[1]) + "</l>\n" + \
                      "<l>        GrayValueMax := " + str(params[2]) + "</l>\n" + \
                      "<c></c>\n" + \
                      "<l>        MinRatio := " + str(params[3]) + "</l>\n" + \
                      "<l>        MaskHeightCrop := " + str(params[4]) + "</l>\n" + \
                      "<l>        MaskWidthCrop := " + str(params[5]) + "</l>\n" + \
                      "<c></c>\n" + \
                      "<l>        A2 := " + str(params[6]) + "</l>\n" + \
                      "<l>        B2 := " + str(params[7]) + "</l>\n" + \
                      "<l>        C := 0.392699</l>\n" + \
                      "<c></c>\n"

    # Core pipeline
    core_code = (
            "<c>* GrayErosion</c>\n"
            "<l>        get_image_type(Image, Type)</l>\n"
            "<l>        gen_disc_se(SE1, Type, A1, B1, GrayValueMax)</l>\n"
            "<l>        gray_erosion(Image, SE1, ImageEroded)</l>\n"
            "<c></c>\n"
            "<c>* CropRectangle (Relative Threshold)</c>\n"
            "<l>        tuple_real(MinRatio, MinRatio)</l>\n"
            "<l>        gen_empty_obj (RelativeRegion)</l>\n"
            "<l>        count_channels (ImageEroded, NumChannels)</l>\n"
            "<l>        if (NumChannels > 1)</l>\n"
            "<l>            access_channel (ImageEroded, ImageEroded, 1)</l>\n"
            "<l>        endif</l>\n"
            "<l>        get_image_type (ImageEroded, ImgType)</l>\n"
            "<l>        if (ImgType != 'byte' and ImgType != 'uint2' and ImgType != 'direction' and ImgType != 'cyclic' and ImgType != 'real')</l>\n"
            "<l>            convert_image_type (ImageEroded, ImageEroded, 'byte')</l>\n"
            "<l>        endif</l>\n"
            "<l>        fast_threshold (ImageEroded, Region, 45, 255, 80)</l>\n"
            "<l>        fill_up (Region, Rectangle)</l>\n"
            "<l>        smallest_rectangle1 (Rectangle, Row1, Col1, Row2, Col2)</l>\n"
            "<l>        reduce_domain (ImageEroded, Rectangle, NewImgReduced)</l>\n"
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
            "<l>        RegionCrop := RelativeRegion</l>\n"
            "<c></c>\n"
            "<c>        * Closing</c>\n"
            "<l>        get_image_type(Image, Type)</l>"
            "<l>        gen_disc_se(StructElement, Type, A2, B2, 0)</l>"        
            "<l>        closing(RegionCrop, StructElement, Region)</l>"
    )

    return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


MVTec_AD_Pill_Crack_best_pipeline_initial_params = [
        12,  # A1
        11,  # B1
        0,  # GrayValueMax
        0.105,  # MinRatio
        27,  # MaskHeightCrop
        29,  # MaskWidthCrop
        16,  # A2
        15  # B2
]

MVTec_AD_Pill_Crack_best_pipeline_bounds = [
        [v for v in range(1, 50)],  # A1
        [v for v in range(1, 50)],  # B1
        [v for v in range(0, 255)],  # GrayValueMax
        [round(0.01 * v, 3) for v in range(0, 20)],  # MinRatio
        [v for v in range(1, 100)],  # MaskHeightCrop
        [v for v in range(1, 100)],  # MaskWidthCrop
        [v for v in range(1, 50)],  # A2
        [v for v in range(1, 50)]  # B2
]

MVTec_AD_Pill_Crack_training_source_path = os.path.join(EVIAS_SRC_PATH,
                                                        "MVTecAnomalyDetection", "pill_crack_train")
