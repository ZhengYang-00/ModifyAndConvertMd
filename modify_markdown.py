import re


class ModifyMarkdown(object):
    def __init__(self, markdown_text) -> None:
        self.md_text = markdown_text
        self.length = len(self.md_text)

    def __len__(self):
        return self.length
    
    def has_image(self):
        img_pattern = re.compile(r'<img\b[^>]*>', re.DOTALL)
        has_img = re.findall(img_pattern, self.md_text)
        frame_pattern = re.compile(r'<iframe.*?</iframe>', re.DOTALL)
        has_img = re.findall(frame_pattern, self.md_text) or has_img
        if has_img:
            return True
        text_lines = self.md_text.split('\n')
        for line in text_lines:
            if line.startswith('![') or line.startswith('[!'):
                has_img = True
        return has_img
        
    def contain_chinese(self):
        pattern = re.compile('[\u4e00-\u9fa5]')  # Unicode范围，包含所有中文字符
        return bool(pattern.search(self.md_text))

    def remove_head(self):
        head_pattern = re.compile(r'---\n.*?---', re.DOTALL)
        self.md_text = re.sub(head_pattern, '', self.md_text)
        self.length = len(self.md_text)
        return self.md_text

    def remove_img_frame(self):
        img_pattern = re.compile(r'<img\b[^>]*>', re.DOTALL)
        self.md_text = re.sub(img_pattern, '', self.md_text)
        frame_pattern = re.compile(r'<iframe.*?</iframe>', re.DOTALL)
        self.md_text = re.sub(frame_pattern, '', self.md_text)
        text_lines = self.md_text.split('\n')
        new_text_lines = []
        for line in text_lines:
            if line.startswith('![') or line.startswith('[!'):
                continue
            new_text_lines.append(line)
        
        self.md_text = "\n".join(new_text_lines)
        self.length = len(self.md_text)
        return self.md_text
    
    def remove_emoji(self):
        # 使用正则表达式匹配 Emoji 表情
        emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F700-\U0001F77F"  # alchemical symbols
                           u"\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
                           u"\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
                           u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
                           u"\U0001FA00-\U0001FA6F"  # Chess Symbols
                           u"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
                           u"\U00002702-\U000027B0"  # Dingbats
                           u"\U000024C2-\U00004e00" 
                           u"\U00009fff-\U0001F251"
                           "]+", flags=re.UNICODE)
    
        # 使用 sub 方法替换 Emoji 表情为空字符串
        self.md_text = emoji_pattern.sub(r'', self.md_text)
        self.length = len(self.md_text)
        return self.md_text
    
    def has_latex_formula(self):
        block_pattern = re.compile(r'```.*?```', re.DOTALL)
        text_with_no_block = re.sub(block_pattern, '', self.md_text)
        pattern = r' \$(.*?)\$ '
        match = re.search(pattern, text_with_no_block, re.DOTALL)
    
        double_dollar_pattern = r'\$\$(.*?)\$\$'
        double_dollar_match = re.search(double_dollar_pattern, text_with_no_block, re.DOTALL)

        if match:
            result = match.group(1)
            if '\n' not in result:
                return True
        return False or bool(double_dollar_match)
    
    def modify_markdown(self):
        self.remove_head()
        self.remove_img_frame()
        self.remove_emoji()
        return self.md_text
    
