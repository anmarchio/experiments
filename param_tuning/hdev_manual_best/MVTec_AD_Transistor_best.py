"""
=======================================
Transistor_best_pipeline
=======================================
"""
import os

from param_tuning.hdev_manual_mean.hdev_manual_utils import get_custom_hdev_pipeline_code, get_crop_rectangle_code
from settings import EVIAS_SRC_PATH


def get_MVTec_AD_Transistor_best_pipeline(params, dataset_path = None):
    pipeline_name = "MVTec_AD_Transistor_best_pipeline"

    if dataset_path is None:
        dataset_path = "/MVTecAnomalyDetection/transistor_damaged_case_train/images"

    # -------------------------
    # Parameters
    # -------------------------
    param_lines = (
        "<c>        * Parameters</c>\n"
        "<c>        </c>\n"
        "<c>        * EdgesImage</c>\n"
        "<l>        Filter := '" + str(params[0]) + "'</l>\n"
        "<l>        Alpha := " + str(params[1]) + "</l>\n"
        "<l>        Low := " + str(params[2]) + "</l>\n"
        "<l>        High := " + str(params[3]) + "</l>\n"
        "<l>        NonMaximumSuppression := '" + str(params[4]) + "'</l>\n"
        "<c>        </c>\n"
        "<c>        * HistoToThresh</c>\n"
        "<l>        Sigma := " + str(params[5]) + "</l>\n"
        "<c>        </c>\n"
        "<c>        * Connection</c>\n"
        "<l>        Neighborhood := 4</l>\n"
        "<c>        </c>\n"
        "<c>        * RegionGrowing</c>\n"
        "<l>        RasterHeight := " + str(params[6]) + "</l>\n"
        "<l>        RasterWidth := " + str(params[7]) + "</l>\n"
        "<l>        Tolerance := " + str(params[8]) + "</l>\n"
        "<l>        MinRegionSize := " + str(params[9]) + "</l>\n"
        "<c></c>\n"
        "<c>        * CropSmallestRectangle</c>\n"
        "<l>        MinGray := " + str(params[10]) + "</l>\n"
        "<l>        MaxGray := " + str(params[11]) + "</l>\n"
        "<c>        </c>\n"
        "<c>        * Closing</c>\n"
        "<l>        A := " + str(params[12]) + "</l>\n"
        "<l>        B := " + str(params[13]) + "</l>\n"
        "<l>        Phi := " + str(params[14]) + "</l>\n"
        "<l>        StructElementType := 'rectangle'</l>\n"
        "<c>        </c>\n"
        "<c>        * SelectShape</c>\n"
        "<l>        Features := '" + str(params[15]) + "'</l>\n"
        "<l>        MinWidth := " + str(params[16]) + "</l>\n"
        "<l>        MaxWidth := " + str(params[17]) + "</l>\n"
    )

    # -------------------------
    # Core pipeline
    # -------------------------
    core_code = (
        "<c>* Pipeline</c>\n"
        "<c>        </c>\n"
        "<c>* Branch A: EdgesImage (Canny)</c>\n"
        "<l>        edges_image(Image, ImageEdges, ImaDir, Filter, Alpha, NonMaximumSuppression, Low, High)</l>\n"
        "<c>        </c>\n"
        "<c>* Branch B: HistoToThresh -> Connection -> CropSmallestRectangle</c>\n"
        "<c>        </c>\n"
        "<c>* CropSmallestRectangle</c>\n"
        "<l>        threshold(Image, Region, MinGray, MaxGray)</l>\n"
        "<l>        smallest_rectangle1(Region, Row1, Column1, Row2, Column2)</l>\n"
        "<l>        crop_rectangle1(Image, Image2, Row1, Column1, Row2, Column2)</l>\n"
        "<c>        </c>\n"
        "<c>* Connection</c>\n"
        "<l>        connection(Region, ConnectedRegions)</l>\n"
        "<c>        </c>\n"
        "<c>* HistoToThresh</c>\n"
        "<l>        Image := ImageEdges</l>\n"
        "<l>        get_image_type(Image, Img_type)</l>\n"
        "<l>        if ((Img_type # 'byte') and (Img_type # 'uint2') and (Img_type # 'int4'))</l>\n"
        "<l>            convert_image_type(Image, Conv_out, 'byte')</l>\n"
        "<l>            Image := Conv_out</l>\n"
        "<l>        endif</l>\n"
        "<l>        union1(Image, RegionUnion)</l>\n"
        "<l>        gray_histo(RegionUnion, Image, AbsoluteHisto, RelativeHisto)</l>\n"
        "<l>        if (|AbsoluteHisto| &lt;= 0)</l>\n"
        "<l>            OutputVariableName := RegionUnion</l>\n"
        "<l>        endif</l>\n"
        "<l>        histo_to_thresh(AbsoluteHisto, Sigma, MinThresh, MaxThresh)</l>\n"
        "<l>        threshold(Image, Region, MinThresh, MaxThresh)</l>\n"
        "<c>        </c>\n"
        "<c>* Merge</c>\n"
        "<l>        union2(Image, ConnectedRegions, RegionUnion)</l>\n"
        "<c>        </c>\n"
        "<c>* Post: Closing -> SelectShape</c>\n"
        "<l>        gen_rectangle2(StructElement, 0, 0, Phi, A, B)</l>\n"
        "<l>        closing(Region, StructElement, RegionClosed)</l>\n"
        "<c>        </c>\n"
        "<c>* SelectShape</c>\n"
        "<l>        select_shape(RegionClosed, Region, Features, 'and', MinWidth, MaxWidth)</l>\n"
    )

    return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)

MVTec_AD_Transistor_best_pipeline_initial_params = [
        'canny',  # Filter
        1.1,  # Alpha
        5,  # Low
        10,  # High
        'nms',  # NonMaximumSuppression
        4,  # Sigma
        21,  # RasterHeight
        19,  # RasterWidth
        7,  # Tolerance
        1,  # MinRegionSize
        18,  # MinGray
        255,  # MaxGray
        16,  # A
        18,  # B
        0.392699,  # Phi
        'width',  # Features
        87,  # MinWidth
        99999  # MaxWidth
]

MVTec_AD_Transistor_best_pipeline_bounds = [
    [0.1],
    [28],
    [0.3],
    [v for v in range(1, 321)],  # IterationsCoh,
    ['x', 'y', 'sum_abs', 'sum_sqrt', 'x_binomial', 'y_binomial'],  # FilterType
    [3, 5, 7, 9, 11],  # MaskSize
    ['adapted_std_deviation', 'mean', 'max'],  # Method
    ['dark', 'light'],  # LightDark
    [v for v in range(3, 100, 2)],  # MaskSizeThresh
    [round(0.1 * v, 1) for v in range(1, 20)],  # Scale
    [v for v in range(1, 300)],  # IterationsErosion
    [v for v in range(1, 50)],  # A
    [v for v in range(1, 50)],  # B
    [v for v in range(1, 50)],  # A2
    [v for v in range(1, 50)],  # B2
    [1, 2, 3, 4, 5],  # GrayValueMax2
    [v for v in range(1, 255)],  # MinGray
    [v for v in range(1, 255)],  # MaxGray
    [v for v in range(1, 100000)],  # MinSize
    [v for v in range(1000, 100000)],  # MaxSize
    [v for v in range(1, 500)],  # WindowWidth
    [v for v in range(1, 500)]  # WindowHeight
]

MVTec_AD_Transistor_training_source_path = os.path.join(EVIAS_SRC_PATH,
                                                        "MVTecAnomalyDetection", "transistor_damaged_case_train")
