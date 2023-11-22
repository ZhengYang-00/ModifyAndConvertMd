#!/bin/bash

md_path="./md_files"
pdf_path="./pdf_files"

pdf_engine="xelatex" 
# "weasyprint" "pdflatex" "lualatex" "xelatex" "tectonic" "context" "wkhtmltopdf"

start_time=$(date +%s)
for md_file in "$md_path"/*; do
    IFS='/' read -ra parts <<< "$md_file"
    filename="${parts[-1]}"
    IFS='.' read -ra parts <<< "$filename"
    filename="${parts[0]}"
    # pandoc $md_file -o $pdf_path/$filename$".pdf" --pdf-engine=$pdf_engine
    # md2pdf $md_file --output $pdf_path/$filename$".pdf" --theme=github
    # mdpdf -o $pdf_path/$filename$".pdf" $md_file
    pandoc $md_file -o $pdf_path/$filename$".pdf" --pdf-engine=$pdf_engine \
        -V mainfont:SimSun \
        -V margin-top:0.5in \
        -V margin-bottom:0.5in \
        -V margin-left:0.5in \
        -V margin-right:0.5in
done

end_time=$(date +%s)
elapsed_time=$((end_time - start_time))
echo "${pdf_engine} took ${elapsed_time} seconds to run."