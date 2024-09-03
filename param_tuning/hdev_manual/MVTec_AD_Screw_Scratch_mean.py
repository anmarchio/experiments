"""
=======================================
MVTec_AD_Screw_Scratch_mean_pipeline
=======================================
"""
import os

from param_tuning.hdev_manual.hdev_manual_utils import get_custom_hdev_pipeline_code, convert_margin_to_int, \
    get_ellipse_struct_code, get_crop_rectangle_img2_code, get_crop_rectangle_code
from settings import EVIAS_SRC_PATH


def get_MVTec_AD_Screw_Scratch_mean_pipeline(params):
    pipeline_name = "MVTec_AD_Screw_Scratch_mean_pipeline"
    dataset_path = "/MVTecAnomalyDetection/screw_scratch_neck_train/images"

    # Parameters
    param_lines = "<l>        MaskType := '" + str(params[0]) + "'</l>\n" + \
                  "<l>        Radius := " + str(params[1]) + "</l>\n" + \
                  "<l>        ModePercent := " + str(params[2]) + "</l>\n" + \
                  "<l>        Margin := '" + str(params[3]) + "'</l>\n" + \
                  "<l>        MinRatio := " + str(params[4]) + "</l>\n" + \
                  "<l>        MaskHeight := " + str(params[5]) + "</l>\n" + \
                  "<l>        MaskWidth := " + str(params[6]) + "</l>\n" + \
                  "<l>        MinGray := " + str(params[7]) + "</l>\n" + \
                  "<l>        MaxGray := " + str(params[8]) + "</l>\n" + \
                  "<l>        MinSize := " + str(params[9]) + "</l>\n" + \
                  "<l>        MaxSize := " + str(params[10]) + "</l>\n" + \
                  "<l>        WindowWidth := " + str(params[11]) + "</l>\n" + \
                  "<l>        WindowHeight := " + str(params[12]) + "</l>\n" + \
                  "<l>        A := " + str(params[13]) + "</l>\n" + \
                  "<l>        B := " + str(params[14]) + "</l>\n" + \
                  "<c></c>\n"

    # Core Pipeline Code
    core_code = "<c>        * PATH 1</c>\n" \
                "<c>        * ------</c>\n" \
                "<c>        * DualRank</c>\n" + \
                convert_margin_to_int() + \
                "<c>        </c>\n" \
                "<l>        dual_rank(Image, Image1, MaskType, Radius, ModePercent, Margin)</l>\n" \
                "<c>        </c>\n" + \
                get_crop_rectangle_code() + \
                "<c>        </c>\n" \
                "<c>        * PATH 2</c>\n" \
                "<c>        * ------</c>\n" \
                "<c>        </c>\n" \
                "<l>        abs_image(Image, Image2)</l>\n" \
                "<c>        </c>\n" \
                "<l>        gen_empty_region(FaultyRegion)</l>\n" \
                "<l>        gen_empty_region(TempRegion)</l>\n" \
                "<c>        </c>\n" \
                "<l>        get_image_size(Image2, Width, Height)</l>\n" \
                "<c>        </c>\n" \
                "<l>        I_W := Width / WindowWidth</l>\n" \
                "<l>        I_H := Height / WindowHeight</l>\n" \
                "<c>        </c>\n" \
                "<l>        for i := 0 to I_W by 1</l>\n" \
                "<l>            for j := 0 to I_H by 1</l>\n" \
                "<l>                Row1 := j * WindowHeight</l>\n" \
                "<l>                Col1 := i * WindowHeight</l>\n" \
                "<l>                Row2 := j * WindowHeight + WindowHeight</l>\n" \
                "<l>                Col2 := i * WindowHeight + WindowHeight</l>\n" \
                "<c>        </c>\n" \
                "<l>                if(Row2 > Height)</l>\n" \
                "<l>                    Row2 := Height</l>\n" \
                "<l>                endif</l>\n" \
                "<c>        </c>\n" \
                "<l>                if(Col2 > Width)</l>\n" \
                "<l>                    Col2 := Width</l>\n" \
                "<l>                endif</l>\n" \
                "<c>        </c>\n" \
                "<l>                if(Row1 > Height)</l>\n" \
                "<l>                    Row1 := Height - 1</l>\n" \
                "<l>                endif</l>\n" \
                "<c>        </c>\n" \
                "<l>                if(Col1 > Width)</l>\n" \
                "<l>                   Col1 := Width - 1</l>\n" \
                "<l>                endif</l>\n" \
                "<c>        </c>\n" \
                "<l>                crop_rectangle1(Image2, ImagePart, Row1, Col1, Row2, Col2)</l>\n" \
                "<l>                threshold(ImagePart, Threads, 40, 255)</l>\n" \
                "<l>                area_center(Threads, AreaSize, Row, Col)</l>\n" \
                "<c>        </c>\n" \
                "<l>                if(AreaSize < MaxSize and AreaSize > MinSize)</l>\n" \
                "<l>                    gen_rectangle1(TempRegion, Row, Col, Row, Col)</l>\n" \
                "<l>                    union2(TempRegion, FaultyRegion, FaultyRegion)</l>\n" \
                "<l>                endif</l>\n" \
                "<l>                smallest_rectangle1(FaultyRegion, Row1, Col1, Row2, Col2)</l>\n" \
                "<l>                region_features(FaultyRegion, 'area', Value)       </l>\n" \
                "<l>            endfor</l>\n" \
                "<l>        endfor</l>\n" \
                "<c>        </c>\n" \
                "<l>        count_obj(FaultyRegion, Number)</l>\n" \
                "<l>        if(Number > 0)</l>\n" \
                "<l>            Region2 := FaultyRegion</l>\n" \
                "<l>        else</l>\n" \
                "<l>            gen_empty_region(Region2)</l>\n" \
                "<l>        endif</l>\n" \
                "<c>        </c>\n" \
                "<c>        * Opening</c>\n" \
                "<c>        </c>\n" \
                "<c>        * with struct element circle</c>\n" \
                "<c>        * using A, B and C as shape_params</c>\n" \
                "<l>        tuple_max2(A, B, max_rad)</l>\n" \
                "<l>        longer := A</l>\n" \
                "<l>        shorter := B</l>\n" \
                "<l>        if (shorter > longer)</l>\n" \
                "<l>            tmp := shorter</l>\n" \
                "<l>            shorter := longer</l>\n" \
                "<l>            longer := tmp</l>\n" \
                "<l>        endif</l>\n" \
                "<l>        phi := 0.0  </l>\n" \
                "<l>        tuple_ceil(max_rad + 1, max_rad_ceil)</l>\n" \
                "<l>        gen_ellipse(StructElement, max_rad_ceil, max_rad_ceil, phi, longer, shorter)</l>\n" \
                "<c>        </c>\n" \
                "<l>        union2(Region1, Region2, Region)</l>\n" \
                "<l>        opening(Region, StructElement, Region)</l>\n" \
                "<c>        </c>\n"

    return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


MVTec_AD_Screw_Scratch_mean_pipeline_initial_params = [
    'circle',
    47,
    17,
    'TwoFiftyFive',
    0.0249999985098839,
    13,
    19,
    20,
    254,
    900,
    18000,
    320,
    260,
    19,
    18
]

MVTec_AD_Screw_Scratch_mean_pipeline_bounds = [
    ['circle', 'square'],  # MaskType
    [1, 101],  # Radius
    [1, 100],  # ModePercent
    ['cyclic', 'continued', 'Zero', 'Thirty', 'Sixty', 'Ninety', 'OneTwenty', 'OneFifty', 'OneEighty', 'TwoTen',
     'TwoForty', 'TwoFifityFive'],  # Margin
    [float(v) * 0.005 for v in range(2, 22, 1)],  # MinRatio
    [3, 5, 7, 9, 13, 15, 17, 19, 21, 23, 27, 29],  # Width
    [3, 5, 7, 9, 13, 15, 17, 19, 21, 23, 27, 29],  # Height
    [v for v in range(15, 29, 1)],
    [v for v in range(230, 255, 1)],
    [v for v in range(9000, 10999, 1000)],
    [v for v in range(18000, 21999, 1000)],
    [v for v in range(160, 320, 10)],
    [v for v in range(1160, 320, 10)],
    [v for v in range(1, 30, 1)],
    [v for v in range(1, 30, 1)]
]

MVTec_AD_Screw_Scratch_training_source_path = os.path.join(EVIAS_SRC_PATH,
                                                           "MVTecAnomalyDetection", "screw_scratch_neck_train")
