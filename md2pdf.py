import subprocess
import os 
from time import time
from modify_markdown import ModifyMarkdown
from tqdm import tqdm
from itertools import islice
import json


data_path = "/seaweedfs_mount_hdd/lts_data/vision/synth_dataset/corpus/markdown"
json_files = [os.path.join(data_path, file) for file in os.listdir(data_path)]

md_path = './md_files'
output_path = './pdf_files'

pdf_engine = "tectonic"

if __name__ == "__main__":
    start_time = time()
    for json_file in json_files:
        with open(json_file) as f:
            f = islice(f, 100)
            f = list(f)
            for idx,line in tqdm(enumerate(f)):
                md_text = json.loads(line)['text']
                if ModifyMarkdown(md_text).contain_chinese():
                        subprocess.call(["pandoc", "-o", output_path + '/'+ str(idx) + '.pdf', './md_files/{}.md'.format(idx), 
                         "--pdf-engine",
                         pdf_engine, 
                         "-V", "CJKmainfont:SimSun", 
                         "-V", 'CJKmainfontoptions:BoldFont=simsun.ttc, ItalicFont=simsun.ttc, BoldItalicFont=simsun.ttc',
                         "--wrap=auto",
                         "--quiet"])
                else:
                    subprocess.call(["pandoc", "-o", output_path +'/' + str(idx) + '.pdf', './md_files/{}.md'.format(idx), 
                         "--pdf-engine",
                         pdf_engine])
        
    
    print(time() -  start_time)
        
    