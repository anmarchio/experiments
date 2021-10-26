import os
from datetime import datetime


def create_list(path):
    html = "<ul>\n"
    for dirname in os.listdir(path):
        html = html + \
               "<li>" \
               + dirname + \
               "</li>\n"
    html = html + "</ul>\n"
    return html


def create_table_of_contents(path):
    html = "<table class=\"table\">\n"
    html = html + "<thead class=\"thead-dark\">\n<tr>\n" \
                  "<th scope=\"col\">#</th>\n"
    html = html + "<th scope=\"col\">Run</th>\n"
    html = html + "<th scope=\"col\">Highest</th>\n"
    html = html + "<th scope=\"col\">Lowest</th>\n"
    html = html + "</tr>\n</thead>\n<tbody>\n"
    i = 1
    for dirname in os.listdir(path):
        html = html + "<tr><th scope=\"row\">" + str(i) + "</th>\n"
        html = html + "<td><a href=\"#anchor" \
               + dirname + "\">" \
               + dirname + \
               "</a></td>"
        html = html + "<td>0</td>\n"
        html = html + "<td>0</td>\n"
        html = html + "</tr>"
        i = i + 1
    html = html + "\n</tbody>\n</table>"
    return html


def create_html_report_details(path):
    html = ""
    for dirname in os.listdir(path):
        html = html + "<h2 id=anchor" + dirname + ">Report " + dirname + "</h2>\n"
        html = html + "<p>\n" + \
               "<button class=\"btn btn-primary\" type=\"button\" data-toggle=\"collapse\" data-target=\"#" + \
               dirname + \
               "\" aria-expanded=\"false\" aria-controls=\"" + dirname + "\">" + \
               "Show" + \
               "</button>\n" + \
               "<a class=\"btn btn-primary\" data-toggle=\"contents\" href=\"#contents\" " \
               "role=\"button\" aria-expanded=\"false\" aria-controls=\"contents\">" \
               "To Contents" + \
               "</a>\n</p>\n" + \
               "<div class=\"collapse\" id=\"" + \
               dirname + \
               "\">\n<div class=\"card card-body\">\n"
        html = html + "<h3>Analyzer</h3>\n"
        analyzer_path = os.path.join(path, dirname, "Analyzer")
        if os.path.exists(analyzer_path):
            html = html + create_list(analyzer_path)
        else:
            html = html + "<p>Empty</p>\n"

        html = html + "<h3>Config</h3>\n"
        # config_path = os.path.join(path, dirname, "Grid")
        # if os.path.exists(config_path):
        # else:
        html = html + "<p>Empty</p>\n"

        html = html + "<h3>Grid</h3>\n"
        grid_path = os.path.join(path, dirname, "Grid")
        if os.path.exists(grid_path):
            html = html + create_list(grid_path)
        else:
            html = html + "<p>Empty</p>\n"

        html = html + "<h3>Images</h3>\n"
        images_path = os.path.join(path, dirname, "Images")
        if os.path.exists(images_path):
            html = html + create_list(images_path)
        else:
            html = html + "<p>Empty</p>\n"

        html = html + "<h3>Log</h3>\n"
        log_path = os.path.join(path, dirname, "Log", "date.txt")
        if os.path.exists(log_path):
            f = open(log_path, "r")
            html = html + "<p>" + f.read() + "</p>\n"
        else:
            html = html + "<p>Empty</p>\n"

        html = html + "<a href=\"#contents\">Up</a>\n"
        html = html + "</div></div>"
        html = html + "<hr />\n"

    return html


def generate_html(source_path, target_path):
    title = "PyCGP-SP Report " + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    html_code = ""
    html_code = html_code + \
                "<!doctype html>\n" + \
                "<html lang=\"en\">\n" + \
                "<head>\n" + \
                "<meta charset=\"utf-8\">\n" + \
                "<title>" + title + "</title>\n" + \
                "<meta name=\"description\" content=\"Generated PyCGP Report\">" + \
                "<meta name =\"author\" content=\"PyCGP\">" + \
                "</head>\n" + \
                "<!-- Latest compiled and minified CSS -->\n" + \
                "<link rel=\"stylesheet\" href=\"https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css\">\n" + \
                "<!-- jQuery library -->" + \
                "<script src=\"https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js\"></script>\n" + \
                "<!-- Latest compiled JavaScript -->\n" + \
                "<script src=\"https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js\"></script>\n" + \
                "<body>\n" + \
                "<div class=\"container\">\n" + \
                "<h1 class=\"display-1\">" + title + "</h1>\n" + \
                "<h2 id=\"contents\">Table of Contents</h2>\n"
    """
    Insert Table of Contents
    """
    html_code = html_code + create_table_of_contents(source_path)
    html_code = html_code + "<hr />\n"
    """
    Loop through Folders and Create Report details
    """
    html_code = html_code + create_html_report_details(source_path)
    html_code = html_code + "</div>\n</body>\n</html>"
    f = open(os.path.join(target_path, "index.html"), "w")
    f.write(html_code)
    f.close()


def create_tex_list(path):
    tex = "\\begin{itemize}\n"
    for dirname in os.listdir(path):
        tex = tex + "\item " + dirname + "\n"
    tex = tex + "\end{itemize}\n"
    return tex


def create_tex_report_details(path):
    tex = ""
    for dirname in os.listdir(path):
        tex = tex + "\subsection*{Report " + dirname + "}\n\n"
        tex = tex + "\paragraph{Analyzer}\n"
        analyzer_path = os.path.join(path, dirname, "Analyzer")
        if os.path.exists(analyzer_path):
            tex = tex + create_tex_list(analyzer_path) + "\n\n"
        else:
            tex = tex + "\\textbf{Empty}\n\n"

        tex = tex + "\paragraph{Config}\n"
        # config_path = os.path.join(path, dirname, "Grid")
        # if os.path.exists(config_path):
        # else:
        tex = tex + "\\textbf{Empty}\n"

        tex = tex + "\paragraph{Grid}\n"
        grid_path = os.path.join(path, dirname, "Grid")
        if os.path.exists(grid_path):
            tex = tex + create_tex_list(grid_path) + "\n\n"
        else:
            tex = tex + "\\textbf{Empty}\n\n"

        tex = tex + "\paragraph{Images}\n"
        images_path = os.path.join(path, dirname, "Images")
        if os.path.exists(images_path):
            tex = tex + create_tex_list(images_path) + "\n\n"
        else:
            tex = tex + "\\textbf{Empty}\n\n"

        tex = tex + "\paragraph{Log}\n"
        log_path = os.path.join(path, dirname, "Log", "date.txt")
        if os.path.exists(log_path):
            f = open(log_path, "r")
            tex = tex + "\\textbf{" + f.read() + "}\n\n"
        else:
            tex = tex + "\\textbf{Empty}\n\n"

    return tex


def generate_tex(source_path, target_path):
    tex_code = "\section*{PyCGP-SP Report " + datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "}"
    """
    Loop through Folders and Create Report details
    """
    tex_code = tex_code + create_tex_report_details(source_path)
    f = open(os.path.join(target_path, "report.tex"), "w")
    f.write(tex_code)
    f.close()


def create_report():
    results_path = os.path.join(os.path.curdir, "results")
    report_path = os.path.join(os.path.curdir, "report")
    if not os.path.exists(report_path):
        os.makedirs(report_path, mode=777)
    # Creates HTML file report/index.html
    generate_html(results_path, report_path)
    # Creates HTML file report/report.tex
    generate_tex(results_path, report_path)


create_report()
