"""
=======================================
MAIPreform2_Spule0-0315_Upside_best_pipeline.py
=======================================
"""
import os

from param_tuning.hdev_manual_mean.hdev_manual_utils import get_custom_hdev_pipeline_code, get_crop_rectangle_code
from settings import EVIAS_SRC_PATH


def get_MAIPreform2_Spule0_0816_Upside_best_pipeline(params, dataset_path=None):
    pipeline_name = "MAIPreform2_Spule0_0816_Upside_best_pipeline"

    if dataset_path is None:
        dataset_path = "/MAIPreform2.0/20170502_Compositence/Spule2-0816_Upside/undone/durchlauf1/training/images"

    # Parameters
    param_lines = "<l>        Sigma := " + str(params[0]) + "</l>\n" + \
                      "<l>        Rho := " + str(params[1]) + "</l>\n" + \
                      "<l>        Theta := " + str(params[2]) + "</l>\n" + \
                      "<l>        Iterations := " + str(params[3]) + "</l>\n" + \
                      "<c></c>\n" + \
                      "<l>        MinRatio := " + str(params[4]) + "</l>\n" + \
                      "<l>        MaskHeight := " + str(params[5]) + "</l>\n" + \
                      "<l>        MaskWidth := " + str(params[6]) + "</l>\n" + \
                      "<c></c>\n"

    # Core pipeline (updated with corrected HDevelop code)
    core_code = (
            "<c>* Coherence Enhancing Diffusion</c>\n"
            "<l>        coherence_enhancing_diff(Image, Image, Sigma, Rho, Theta, Iterations)</l>\n"
            "<c></c>\n"
            "<c>* CropRectangle (Relative Threshold)</c>\n"
            "<l>        gen_empty_obj(RelativeRegion)</l>\n"
            "<c></c>\n"
            "<c>* Ensure single channel</c>\n"
            "<l>        count_channels(Image, NumChannels)</l>\n"
            "<l>        if (NumChannels &gt; 1)</l>\n"
            "<l>            access_channel(Image, Image, 1)</l>\n"
            "<l>        endif</l>\n"
            "<c></c>\n"
            "<c>* Ensure valid type</c>\n"
            "<l>        get_image_type(Image, ImgType)</l>\n"
            "<l>        if (ImgType != 'byte' and ImgType != 'uint2' and ImgType != 'direction' and ImgType != 'cyclic' and ImgType != 'real')</l>\n"
            "<l>            convert_image_type(Image, Image, 'byte')</l>\n"
            "<l>        endif</l>\n"
            "<c></c>\n"
            "<c>* Fast threshold + fill</c>\n"
            "<l>        fast_threshold(Image, Region, 45, 255, 80)</l>\n"
            "<l>        fill_up(Region, Rectangle)</l>\n"
            "<c></c>\n"
            "<c>* Smallest enclosing rectangle</c>\n"
            "<l>        smallest_rectangle1(Rectangle, Row1, Col1, Row2, Col2)</l>\n"
            "<l>        reduce_domain(Image, Rectangle, NewImgReduced)</l>\n"
            "<c></c>\n"
            "<l>        region_features(Rectangle, 'width', Width)</l>\n"
            "<l>        region_features(Rectangle, 'height', Height)</l>\n"
            "<l>        WStep := Width / MaskWidth</l>\n"
            "<l>        HStep := Height / MaskHeight</l>\n"
            "<c></c>\n"
            "<l>        EndW := (Col2 - (WStep / 1.5)) - 20</l>\n"
            "<l>        StepW := WStep / 2</l>\n"
            "<c></c>\n"
            "<l>        for ImgWidth := Col1 + 20 to EndW by StepW</l>\n"
            "<l>            EndH := Row2 - (HStep / 1.5)</l>\n"
            "<l>            StepH := HStep / 2</l>\n"
            "<c></c>\n"
            "<l>            for ImgHeight := Row1 + 3 to EndH by StepH</l>\n"
            "<l>                crop_rectangle1(NewImgReduced, ImgPart, ImgHeight, ImgWidth, ImgHeight + HStep, ImgWidth + WStep)</l>\n"
            "<c></c>\n"
            "<c>* Compute histogram</c>\n"
            "<l>                gray_histo_range(ImgPart, ImgPart, 0, 255, 2, Histo, BinSize)</l>\n"
            "<l>                PixelCount := Histo[0] + Histo[1]</l>\n"
            "<c></c>\n"
            "<l>                if (PixelCount &gt; 0.6 * WStep * HStep)</l>\n"
            "<l>                    Ratio := Histo[1] / PixelCount</l>\n"
            "<c></c>\n"
            "<l>                    if (Ratio &lt; MinRatio)</l>\n"
            "<l>                        gen_rectangle1(FaultyRegion, ImgHeight, ImgWidth, ImgHeight + HStep, ImgWidth + WStep)</l>\n"
            "<l>                        union2(RelativeRegion, FaultyRegion, RelativeRegion)</l>\n"
            "<l>                    endif</l>\n"
            "<l>                endif</l>\n"
            "<l>            endfor</l>\n"
            "<l>        endfor</l>\n"
            "<l>        Region := RelativeRegion</l>\n"
        )

    return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


MAIPreform2_Spule0_0816_Upside_best_pipeline_initial_params = [
    0.8,   # Sigma
    19,    # Rho
    0.2,   # Theta
    100,   # Iterations
    0.06,  # MinRatio
    7,     # MaskHeight
    9      # MaskWidth
]

MAIPreform2_Spule0_0816_Upside_best_pipeline_bounds = [
    [0.1 * v for v in range(1, 50)],  # Sigma
    [v for v in range(1, 50)],        # Rho
    [0.1 * v for v in range(1, 40)],  # Theta
    [v for v in range(1, 500)],       # Iterations
    [round(0.01 * v, 2) for v in range(0, 21)],  # MinRatio (0.0 - 0.2)
    [v for v in range(1, 100)],       # MaskHeight
    [v for v in range(1, 200)]        # MaskWidth
]

MAIPreform2_Spule0_0816_Upside_training_source_path = os.path.join(EVIAS_SRC_PATH,
                                                                   "MAIPreform2.0",
                                                                   "20170502_Compositence",
                                                                   "Spule2-0816_Upside",
                                                                   "undone",
                                                                   "durchlauf1",
                                                                   "training")
