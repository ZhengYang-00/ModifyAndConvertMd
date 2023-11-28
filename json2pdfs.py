import json
import markdown2
from weasyprint import HTML
import re
import os
from time import time
from tqdm import tqdm

import concurrent
from concurrent.futures import ProcessPoolExecutor
from itertools import islice
from multiprocessing import Process
import subprocess

from modify_markdown import ModifyMarkdown

import katex


def json2pdf(jsonline, output=None, theme=None, dpi=96):
    json_data = json.loads(jsonline)
    text = json_data['text']
    hexsha = json_data['meta']['hexsha']

    if output is not None:
        if not os.path.exists(output):
            raise Exception("No a valid output path")
        output = os.path.join(output, hexsha + '.pdf')
    else:
        BASE_DIR = os.path.abspath(os.path.dirname(__file__))
        output = os.path.join(BASE_DIR, 'pdf_files')
        if not os.path.exists(output):
            os.mkdir(output)
        output = os.path.join(output, hexsha + '.pdf')

    modify_md = ModifyMarkdown(text)
    text = modify_md.modify_markdown()
    if not text.replace('\n', ''):
        return
    if modify_md.has_latex_formula():
        md_file_path = 'md_files/{}.md'.format(hexsha)
        with open(md_file_path, 'w', encoding='utf-8') as f:
            f.write(text)
        subprocess.call(["pandoc", "-o", output, md_file_path, 
                         "--pdf-engine=xelatex", 
                         "-V", "CJKmainfont:SimSun", 
                         "-V", 'CJKmainfontoptions:BoldFont=simsun.ttc, ItalicFont=simsun.ttc, BoldItalicFont=simsun.ttc',
                         "--wrap=auto"
                        #  "-V","margin-top:0.5in",
                        #  "-V","margin-bottom:0.5in",
                        #  "-V","margin-left:0.5in",
                        #  "-V","margin-right:0.5in",
                        ])
        subprocess.call(['rm', md_file_path])
        return output
            

    html = markdown2.markdown(text, extras = ['fenced-code-blocks','tables'],)

    if theme is not None:
        if not os.path.exists(theme):
            raise Exception("No a valid css file path")
        css_file = theme
        HTML(string=html).write_pdf(output, stylesheets=[css_file], dpi=dpi)
    else:
        HTML(string=html).write_pdf(output, dpi=dpi)
    return output
    

def set_time4convert(jsonline, output=None, theme=None, dpi = 96, timeout = 20):
    p = Process(target=json2pdf, args=(jsonline, output, theme, dpi))
    p.start()
    p.join(timeout=timeout)
    if p.is_alive():
        p.terminate()
    p.join()


data_path = "/seaweedfs_mount_hdd/lts_data/vision/synth_dataset/corpus/markdown"
json_files = [os.path.join(data_path, file) for file in os.listdir(data_path)]

if __name__ == '__main__':
    start_time = time()
    for json_file in json_files:
        with open(json_file) as f:           
            sub_f = islice(f, 5000)
            with ProcessPoolExecutor(max_workers=64) as executor:
                futures = {executor.submit(set_time4convert, line, None, "themes/autowrap.css",  None, 15) for line in tqdm(sub_f)}
                concurrent.futures.wait(futures)
        print(time() - start_time)
        # break

        



