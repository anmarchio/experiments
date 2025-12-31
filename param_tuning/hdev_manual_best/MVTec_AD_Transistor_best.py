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

    # Parameters
    param_lines = (
            "<c>        * Parameters</c>\n"
            "<l>        Sigma := " + str(params[0]) + "</l>\n"
            "<l>        Rho := " + str(params[1]) + "</l>\n"
            "<l>        Theta := " + str(params[2]) + "</l>\n"
            "<l>        IterationsCoh := " + str(params[3]) + "</l>\n"
            "<c></c>\n"
            "<l>        FilterType := '" + str(params[4]) + "'</l>\n"
            "<l>        MaskSize := " + str(params[5]) + "</l>\n"
            "<c></c>\n"
            "<l>        Method := '" + str(params[6]) + "'</l>\n"
            "<l>        LightDark := '" + str(params[7]) + "'</l>\n"
            "<l>        MaskSizeThresh := " + str(params[8]) + "</l>\n"
            "<l>        Scale := " + str(params[9]) + "</l>\n"
            "<c></c>\n"
            "<l>        IterationsErosion := " + str(params[10]) + "</l>\n"
            "<l>        A := " + str(params[11]) + "</l>\n"
            "<l>        B := " + str(params[12]) + "</l>\n"
            "<c></c>\n"
            "<l>        A2 := " + str(params[13]) + "</l>\n"
            "<l>        B2 := " + str(params[14]) + "</l>\n"
            "<l>        GrayValueMax2 := " + str(params[15]) + "</l>\n"
            "<c></c>\n"
            "<l>        MinGray := " + str(params[16]) + "</l>\n"
            "<l>        MaxGray := " + str(params[17]) + "</l>\n"
            "<l>        MinSize := " + str(params[18]) + "</l>\n"
            "<l>        MaxSize := " + str(params[19]) + "</l>\n"
            "<l>        WindowWidth := " + str(params[20]) + "</l>\n"
            "<l>        WindowHeight := " + str(params[21]) + "</l>\n"
    )

    # Core pipeline
    core_code = (
            "<c>* Pipeline</c>\n"        
            "<c></c>\n"
            "<c>* Branch 1: CoherenceEnhancing -> SobelAmp</c>\n"
            "<l>        coherence_enhancing_diff(Image, ImageCED, Sigma, Rho, Theta, IterationsCoh)</l>\n"   
            "<c></c>\n"        
            "<c>* SobelAmp</c>\n"
            "<l>        convert_image_type(ImageCED, ImageCED, 'byte')</l>\n"
            "<l>        sobel_amp(ImageCED, ImageAmp, FilterType, MaskSize)</l>\n"   
            "<c></c>\n"                
            "<c>* LocalThreshold</c>\n"
            "<c></c>\n"
            "<l>        access_channel(ImageAmp, ImageAmp, 1)</l>\n" 
            "<l>        convert_image_type(ImageAmp, ImageAmp, 'byte')</l>\n" 
            "<l>        local_threshold(ImageAmp, RegionErosion, Method, LightDark, ['mask_size','scale'], [MaskSizeThresh, Scale])</l>\n" 
            "<c></c>\n"                
            "<c>* Erosion1 (Ellipse SE)</c>\n"
            "<l>        tuple_max2(A, B, max_rad)</l>\n" 
            "<l>        phi := 0</l>\n" 
            "<l>        longer := A</l>\n" 
            "<l>        shorter := B</l>\n" 
            "<l>        if (shorter > longer)</l>\n" 
            "<l>            tmp := shorter</l>\n" 
            "<l>            shorter := longer</l>\n" 
            "<l>            longer := tmp</l>\n" 
            "<l>        endif</l>\n" 
            "<l>        phi := 0.0</l>\n" 
            "<l>        tuple_ceil(max_rad + 1, max_rad_ceil)</l>\n" 
            "<l>        gen_ellipse(StructElement, max_rad_ceil, max_rad_ceil, phi, longer, shorter)</l>\n" 
            "<l>        *erosion1(RegionThresh, StructElement, RegionErosion, 1)</l>\n" 
            "<c></c>\n"
            "<c>* Branch 2: GrayClosing -> AreaSizeThresh</c>\n"
            "<c></c>\n"
            "<c>* GrayClosing</c>\n"
            "<l>        get_image_type(Image, Type)</l>\n" 
            "<l>        gen_disc_se(SE, Type, A2, B2, GrayValueMax2)</l>\n" 
            "<l>        gray_closing(Image, SE, Image2)</l>\n" 
            "<c></c>\n"
            "<c>* AreaSizeThreshold</c>\n"
            "<l>        abs_image(Image, Image2)</l>\n" 
            "<c></c>\n"
            "<l>        gen_empty_region(FaultyRegion)</l>\n" 
            "<l>        gen_empty_region(TempRegion)</l>\n" 
            "<c></c>\n"
            "<l>        get_image_size(Image2, Width, Height)</l>\n" 
            "<c></c>\n"
            "<l>        I_W := Width / WindowWidth</l>\n" 
            "<l>        I_H := Height / WindowHeight</l>\n" 
            "<c></c>\n"
            "<l>        for i := 0 to I_W by 1</l>\n" 
            "<l>            for j := 0 to I_H by 1</l>\n" 
            "<l>                Row1 := j * WindowHeight</l>\n" 
            "<l>                Col1 := i * WindowHeight</l>\n" 
            "<l>                Row2 := j * WindowHeight + WindowHeight</l>\n" 
            "<l>                Col2 := i * WindowHeight + WindowHeight</l>\n" 
            "<c></c>\n"               
            "<l>                if(Row2 > Height)</l>\n" 
            "<l>                    Row2 := Height</l>\n" 
            "<l>                endif</l>\n" 
            "<c></c>\n"      
            "<l>                if(Col2 > Width)</l>\n" 
            "<l>                    Col2 := Width</l>\n" 
            "<l>                endif</l>\n" 
            "<c></c>\n"      
            "<l>                if(Row1 > Height)</l>\n" 
            "<l>                    Row1 := Height - 1</l>\n" 
            "<l>               endif</l>\n" 
            "<c></c>\n"
            "<l>                if(Col1 > Width)</l>\n" 
            "<l>                    Col1 := Width - 1</l>\n" 
            "<l>                endif</l>\n" 
            "<c></c>\n"        
            "<l>                crop_rectangle1(Image2, ImagePart, Row1, Col1, Row2, Col2)</l>\n" 
            "<l>                threshold(ImagePart, Threads, 40, 255)</l>\n" 
            "<l>                area_center(Threads, AreaSize, Row, Col)</l>\n" 
            "<c></c>\n"        
            "<l>                if(AreaSize &lt; MaxSize and AreaSize &gt; MinSize)</l>\n" 
            "<l>                    gen_rectangle1(TempRegion, Row, Col, Row, Col)</l>\n" 
            "<l>                    union2(TempRegion, FaultyRegion, FaultyRegion)</l>\n" 
            "<l>                endif</l>\n" 
            "<c></c>\n"        
            "<l>                smallest_rectangle1(FaultyRegion, Row1, Col1, Row2, Col2)</l>\n" 
            "<l>                region_features(FaultyRegion, 'area', Value)        </l>\n" 
            "<l>            endfor</l>\n" 
            "<l>        endfor</l>\n" 
            "<c></c>\n"
            "<l>        count_obj(FaultyRegion, Number)</l>\n" 
            "<l>        if(Number > 0)</l>\n" 
            "<l>            Region2 := FaultyRegion</l>\n" 
            "<l>        else</l>\n" 
            "<l>            gen_empty_region(Region2)</l>\n" 
            "<l>        endif</l>\n" 
            "<c></c>\n"
            "<c>* Merge: Union2</c>\n"
            "<l>        union2(RegionErosion, Region2, Region)</l>\n"
    )

    return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


MVTec_AD_Transistor_best_pipeline_initial_params = [
    0.1,  # Sigma
    28,  # Rho
    0.3,  # Theta
    1,  # IterationsCoh (shortened)
    #312,  # IterationsCoh
    'x',  # FilterType
    3,  # MaskSize
    'adapted_std_deviation',  # Method
    'light',  # LightDark
    15,  # MaskSizeThresh
    0.2,  # Scale
    40, # IterationsErosion
    24, # A
    4,  # B
    14, # A2
    5, # B2
    1, # GrayValueMax2
    17, # MinGray
    240, # MaxGray
    10000, # MinSize
    21000, # MaxSize
    210, # WindowWidth
    300  # WindowHeight
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
