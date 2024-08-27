HDEV_HEADER = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n" \
              "<hdevelop file_version=\"1.1\" halcon_version=\"13.0\">\n" \
              "<procedure name=\"main\">\n" \
              "<interface/>\n" \
              "<body>\n"

HDEV_TEMPLATE_CODE = "<l>dev_update_off()</l>\n"\
                     "<l>list_image_files(source_path, 'default', [], ImageFiles)</l>\n" \
                     "<c></c>\n" \
                     "<l>for Index := 0 to |ImageFiles| - 1 by 1</l>\n" \
                     "<l>    file_exists(output_path, dir_exists)</l>\n" \
                     "<l>    if(dir_exists == 0)</l>\n" \
                     "<l>        make_dir(output_path)</l>\n" \
                     "<l>    endif</l>\n" \
                     "<l>    out_img_path := output_path + Index + '.png'</l>\n" \
                     "<l>    file_exists(out_img_path, exists)</l>\n" \
                     "<l>    if(exists)</l>\n" \
                     "<l>        delete_file(out_img_path)</l>\n" \
                     "<l>    endif</l>\n" \
                     "<l>    read_image(Image, ImageFiles[Index])</l>\n" \
                     "<l>    get_image_size(Image, Width, Height)</l>\n" \
                     "<c>    * --------------</c>\n" \
                     "<c>    * CGP Code Block</c>\n" \
                     "<c>    * --------------</c>\n" \
                     "<l>    try</l>\n"

HDEV_MIDDLE = "<l>        binomial_filter(Image, Image, 35, 29)</l>\n" \
              "<l>        fast_threshold(Image, Region, 155, 196, 22)\n" \
              "</l>\n"

HDEV_FOOTER = "<l>    catch (Exception)</l>\n" \
              "<l>        gen_empty_region(Region)</l>\n" \
              "<l>    endtry        </l>\n" \
              "<c>    * --------------</c>\n" \
              "<c>    * END Code Block</c>\n" \
              "<c>    * --------------</c>\n" \
              "<l>    gen_image_const(ImageResult, 'byte', Width, Height)</l>\n" \
              "<l>    paint_region(Region, ImageResult, ImageResult, 255, 'fill')</l>\n" \
              "<l>    out_img_path := output_path + Index</l>\n" \
              "<l>    write_image(ImageResult, 'png', 0, out_img_path)</l>\n" \
              "<l>endfor</l>\n" \
              "<l>exit()</l>\n" \
              "</body>\n" \
              "<docu id=\"main\">\n" \
              "<parameters/>\n" \
              "</docu>\n" \
              "</procedure>\n" \
              "</hdevelop>"
