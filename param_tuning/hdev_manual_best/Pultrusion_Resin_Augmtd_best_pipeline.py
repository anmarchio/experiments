"""
=======================================
MVTec_AD_Pultrusion_Resin_Augmtd_best_pipeline
=======================================
"""
import os

from param_tuning.hdev_manual_mean.hdev_manual_utils import get_custom_hdev_pipeline_code
from settings import EVIAS_SRC_PATH


def get_Pultrusion_Resin_Augmtd_best_pipeline(params, dataset_path=None):
    pipeline_name = "Pultrusion_Resin_Augmtd_best_pipeline"

    if dataset_path is None:
        dataset_path = "/Pultrusion/resin_cgp_augmntd/train/images"

    def get_sigma_sobel_binthresh_opening_selectshape_pipeline(params, dataset_path=None):
        pipeline_name = "Sigma_Sobel_BinaryThreshold_Opening_SelectShape_pipeline"

        if dataset_path is None:
            dataset_path = "/your/dataset/path"

        # Parameters
        param_lines = (
                "<l>        MaskHeight := " + str(params[0]) + "</l>\n"
                                                               "<l>        MaskWidth := " + str(params[1]) + "</l>\n"
                                                                                                             "<l>        Sigma := " + str(
            params[2]) + "</l>\n"
                         "<c></c>\n"
                         "<l>        FilterType := '" + str(params[3]) + "'</l>\n"
                                                                         "<l>        MaskSizeSobel := " + str(
            params[4]) + "</l>\n"
                         "<c></c>\n"
                         "<l>        Method1 := '" + str(params[5]) + "'</l>\n"
                                                                      "<l>        LightDark1 := '" + str(
            params[6]) + "'</l>\n"
                         "<l>        Method2 := '" + str(params[7]) + "'</l>\n"
                                                                      "<l>        LightDark2 := '" + str(
            params[8]) + "'</l>\n"
                         "<c></c>\n"
                         "<l>        A := " + str(params[9]) + "</l>\n"
                                                               "<l>        B := " + str(params[10]) + "</l>\n"
                                                                                                      "<c></c>\n"
                                                                                                      "<l>        Min := " + str(
            params[11]) + "</l>\n"
                          "<l>        Max := " + str(params[12]) + "</l>\n"
                                                                   "<l>        Features := '" + str(
            params[13]) + "'</l>\n"
                          "<c></c>\n"
        )

        # Core pipeline
        core_code = (
            "<c>* Branch 1: SigmaImage -> BinaryThreshold</c>\n"
            "<l>        sigma_image(Image, ImageSigma, MaskHeight, MaskWidth, Sigma)</l>\n"
            "<l>        binary_threshold(ImageSigma, Region1, Method1, LightDark1, UsedThreshold)</l>\n"
            "<c></c>\n"
            "<c>* Branch 2: EquHistoImage -> SobelAmp -> BinaryThreshold</c>\n"
            "<l>        equ_histo_image(Image, ImageEqu)</l>\n"
            "<l>        sobel_amp(ImageEqu, ImageAmp, FilterType, MaskSizeSobel)</l>\n"
            "<l>        get_image_type(ImageAmp, Type)</l>\n"
            "<l>        convert_image_type(ImageAmp, ImageConverted, 'byte')</l>\n"
            "<l>        binary_threshold(ImageConverted, Region2, Method2, LightDark2, UsedThreshold)</l>\n"
            "<c></c>\n"
            "<c>* Merge</c>\n"
            "<l>        union2(Region1, Region2, RegionUnion)</l>\n"
            "<c></c>\n"
            "<c>* Opening (Rectangle SE)</c>\n"
            "<l>        opening_rectangle1(RegionUnion, RegionOpened, A, B)</l>\n"
            "<c></c>\n"
            "<c>* SelectShape</c>\n"
            "<l>        select_shape(RegionOpened, Region, Features, 'and', Min, Max)</l>\n"
        )

        return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


Pultrusion_Resin_Augmtd_best_pipeline_initial_params = [
    19,  # MaskHeight
    5,  # MaskWidth
    145,  # Sigma
    'x_binomial',  # FilterType
    3,  # MaskSizeSobel
    'max_separability',  # Method1
    'light',  # LightDark1
    'smooth_histo',  # Method2
    'light',  # LightDark2
    24,  # A
    26,  # B
    35,  # Min
    99999,  # Max
    'ra'  # Features
]

Pultrusion_Resin_Augmtd_best_pipeline_bounds = [
    [v for v in range(1, 50)],  # MaskHeight
    [v for v in range(1, 50)],  # MaskWidth
    [v for v in range(1, 200)],  # Sigma
    ['x', 'y', 'sum_abs', 'sum_sqrt', 'x_binomial', 'y_binomial'],  # FilterType
    [3, 5, 7, 9, 11],  # MaskSizeSobel
    ['max_separability', 'entropy', 'otsu'],  # Method1
    ['dark', 'light'],  # LightDark1
    ['smooth_histo', 'max_separability', 'entropy'],  # Method2
    ['dark', 'light'],  # LightDark2
    [v for v in range(1, 50)],  # A
    [v for v in range(1, 50)],  # B
    [v for v in range(1, 500)],  # Min
    [v for v in range(500, 200000, 1000)],  # Max
    ['ra', 'roundness', 'rectangularity', 'compactness']  # Features
]

Pultrusion_Resin_Augmtd_training_source_path = os.path.join(EVIAS_SRC_PATH,
                                                            "Pultrusion", "resin_cgp_augmntd", "train")
