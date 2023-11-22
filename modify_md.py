from tqdm import tqdm
from time import time
import json

from modify_markdown import ModifyMarkdown


data_path = "/seaweedfs_mount_hdd/lts_data/vision/synth_dataset/corpus/markdown/markdown_0000.jsonl"

if __name__ == '__main__':
    with open(data_path) as f:
        cnt = 0
        start_time = time()
        for line in tqdm(f):
            text = json.loads(line)['text']
            # mdm = ModifyMarkdown(text)
            # text = mdm.modify_markdown()
            md_file_path = 'md_files/{}.md'.format(cnt)
            with open(md_file_path, 'w', encoding='utf-8') as f:
                f.write(text)
            cnt += 1
            if cnt == 1000:
                break
        
        print(time() - start_time)
            