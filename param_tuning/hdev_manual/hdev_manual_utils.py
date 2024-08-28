from param_tuning.hdev.hdev_templates import HDEV_HEADER, HDEV_TEMPLATE_CODE, HDEV_FOOTER
from param_tuning.utils import get_evias_experimts_path_for_hdev


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
                          "Type != 'real')</l>\n" \
                          "<l>            convert_image_type(Image, Image, 'byte')</l>\n" \
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
                          "<l>            for ImgHeight := Row1 + 3 to EndH by StepH</l>\n" \
                          "<l>                gen_empty_obj(ImagePart)</l>\n" \
                          "<l>                crop_rectangle1(NewImageReduced, ImgPart, ImgHeight, ImgWidth, ImgHeight + HStep, ImgWidth + WStep)</l>\n" \
                          "<c></c>\n" \
                          "<l>                gray_histo_range(ImgPart, ImgPart, 0, 255, 2, Histo, BinSize)</l>\n" \
                          "<c></c>\n" \
                          "<l>                PixelCount := Histo[0] + Histo[1]</l>\n" \
                          "<c></c>\n" \
                          "<l>                tuple_real(PixelCount, PixelCount)</l>\n" \
                          "<c></c>\n" \
                          "<l>                if(PixelCount <= 0.6 * WStep * HStep)</l>\n" \
                          "<l>                    continue</l>\n" \
                          "<l>                endif</l>\n" \
                          "<l>                Ratio := (Histo[1] * 1.0) / (PixelCount * 1.0)</l>\n" \
                          "<c></c>\n" \
                          "<l>                if(Ratio < MinRatio)</l>\n" \
                          "<l>                    gen_rectangle1(FaultyRegion, ImgHeight, ImgWidth, ImgHeight + HStep, " \
                          "ImgWidth + WStep)</l>\n" \
                          "<l>                    concat_obj(FaultyRegion, RelativeRegion, FaultyRegion)endif</l>\n" \
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
