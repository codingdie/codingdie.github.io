#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Markdown 转微信公众号 HTML 转换器
"""

import re
import sys
import json
from pathlib import Path

class WechatHTMLConverter:
    """微信公众号 HTML 转换器"""

    def __init__(self):
        # 微信公众号样式模板
        self.styles = {
            'h1': 'font-size: 24px; font-weight: bold; color: #333; margin: 20px 0 10px 0; padding-bottom: 10px; border-bottom: 2px solid #3498db;',
            'h2': 'font-size: 20px; font-weight: bold; color: #333; margin: 18px 0 8px 0; padding-left: 10px; border-left: 4px solid #3498db;',
            'h3': 'font-size: 18px; font-weight: bold; color: #333; margin: 16px 0 8px 0;',
            'h4': 'font-size: 16px; font-weight: bold; color: #555; margin: 14px 0 6px 0;',
            'p': 'font-size: 15px; line-height: 1.8; color: #333; margin: 10px 0; text-align: justify;',
            'blockquote': 'background: #f9f9f9; border-left: 4px solid #3498db; padding: 10px 15px; margin: 15px 0; color: #666; font-style: italic;',
            'code': 'background: #f5f5f5; padding: 2px 6px; border-radius: 3px; font-family: Consolas, Monaco, monospace; color: #e74c3c; font-size: 14px;',
            'pre': 'background: #2d2d2d; color: #f8f8f2; padding: 15px; border-radius: 5px; overflow-x: auto; margin: 15px 0; font-family: Consolas, Monaco, monospace; font-size: 14px; line-height: 1.6;',
            'ul': 'margin: 10px 0; padding-left: 20px;',
            'ol': 'margin: 10px 0; padding-left: 20px;',
            'li': 'font-size: 15px; line-height: 1.8; color: #333; margin: 5px 0;',
            'a': 'color: #3498db; text-decoration: none;',
            'img': 'max-width: 100%; height: auto; display: block; margin: 15px auto;',
            'strong': 'font-weight: bold; color: #e74c3c;',
            'em': 'font-style: italic; color: #555;',
        }

    def convert(self, markdown_content):
        """转换 Markdown 到微信 HTML"""
        html = markdown_content

        # 转换标题
        html = self._convert_headers(html)

        # 转换代码块
        html = self._convert_code_blocks(html)

        # 转换行内代码
        html = self._convert_inline_code(html)

        # 转换引用
        html = self._convert_blockquotes(html)

        # 转换列表
        html = self._convert_lists(html)

        # 转换链接
        html = self._convert_links(html)

        # 转换图片
        html = self._convert_images(html)

        # 转换粗体和斜体
        html = self._convert_emphasis(html)

        # 转换段落
        html = self._convert_paragraphs(html)

        return html

    def _convert_headers(self, text):
        """转换标题"""
        for i in range(6, 0, -1):
            pattern = r'^' + '#' * i + r'\s+(.+)$'
            replacement = f'<h{i} style="{self.styles[f"h{i}" if i <= 4 else "h4"]}">\\1</h{i}>'
            text = re.sub(pattern, replacement, text, flags=re.MULTILINE)
        return text

    def _convert_code_blocks(self, text):
        """转换代码块"""
        def replace_code_block(match):
            lang = match.group(1) or ''
            code = match.group(2)
            code = code.replace('<', '&lt;').replace('>', '&gt;')
            return f'<pre style="{self.styles["pre"]}"><code>{code}</code></pre>'

        pattern = r'```(\w+)?\n(.*?)```'
        text = re.sub(pattern, replace_code_block, text, flags=re.DOTALL)
        return text

    def _convert_inline_code(self, text):
        """转换行内代码"""
        pattern = r'`([^`]+)`'
        replacement = f'<code style="{self.styles["code"]}">\\1</code>'
        text = re.sub(pattern, replacement, text)
        return text

    def _convert_blockquotes(self, text):
        """转换引用"""
        lines = text.split('\n')
        result = []
        in_quote = False
        quote_content = []

        for line in lines:
            if line.startswith('> '):
                if not in_quote:
                    in_quote = True
                    quote_content = []
                quote_content.append(line[2:])
            else:
                if in_quote:
                    content = '<br>'.join(quote_content)
                    result.append(f'<blockquote style="{self.styles["blockquote"]}">{content}</blockquote>')
                    in_quote = False
                    quote_content = []
                result.append(line)

        if in_quote:
            content = '<br>'.join(quote_content)
            result.append(f'<blockquote style="{self.styles["blockquote"]}">{content}</blockquote>')

        return '\n'.join(result)

    def _convert_lists(self, text):
        """转换列表"""
        # 无序列表
        pattern = r'^[\*\-]\s+(.+)$'
        text = re.sub(pattern, f'<li style="{self.styles["li"]}">\\1</li>', text, flags=re.MULTILINE)

        # 有序列表
        pattern = r'^\d+\.\s+(.+)$'
        text = re.sub(pattern, f'<li style="{self.styles["li"]}">\\1</li>', text, flags=re.MULTILINE)

        # 包装 ul/ol 标签
        text = re.sub(r'(<li[^>]*>.*?</li>\n)+', lambda m: f'<ul style="{self.styles["ul"]}">\n{m.group(0)}</ul>\n', text, flags=re.DOTALL)

        return text

    def _convert_links(self, text):
        """转换链接"""
        pattern = r'\[([^\]]+)\]\(([^\)]+)\)'
        replacement = f'<a href="\\2" style="{self.styles["a"]}">\\1</a>'
        text = re.sub(pattern, replacement, text)
        return text

    def _convert_images(self, text):
        """转换图片"""
        pattern = r'!\[([^\]]*)\]\(([^\)]+)\)'
        replacement = f'<img src="\\2" alt="\\1" style="{self.styles["img"]}" />'
        text = re.sub(pattern, replacement, text)
        return text

    def _convert_emphasis(self, text):
        """转换粗体和斜体"""
        # 粗体
        text = re.sub(r'\*\*([^\*]+)\*\*', f'<strong style="{self.styles["strong"]}">\\1</strong>', text)
        text = re.sub(r'__([^_]+)__', f'<strong style="{self.styles["strong"]}">\\1</strong>', text)

        # 斜体
        text = re.sub(r'\*([^\*]+)\*', f'<em style="{self.styles["em"]}">\\1</em>', text)
        text = re.sub(r'_([^_]+)_', f'<em style="{self.styles["em"]}">\\1</em>', text)

        return text

    def _convert_paragraphs(self, text):
        """转换段落"""
        lines = text.split('\n')
        result = []

        for line in lines:
            line = line.strip()
            if line and not line.startswith('<'):
                result.append(f'<p style="{self.styles["p"]}">{line}</p>')
            else:
                result.append(line)

        return '\n'.join(result)

def extract_metadata(markdown_file):
    """从 markdown 文件提取元数据"""
    content = Path(markdown_file).read_text(encoding='utf-8')

    # 提取标题（第一个 # 标题）
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    title = title_match.group(1) if title_match else Path(markdown_file).stem

    # 生成摘要（取前120字符）
    text_content = re.sub(r'#.*\n', '', content)  # 移除标题
    text_content = re.sub(r'```.*?```', '', text_content, flags=re.DOTALL)  # 移除代码块
    text_content = re.sub(r'[#*`\[\]()]', '', text_content)  # 移除 markdown 符号
    text_content = ' '.join(text_content.split())  # 规范化空白
    digest = text_content[:120] + '...' if len(text_content) > 120 else text_content

    return {
        'title': title,
        'digest': digest,
        'content': content
    }

def main():
    if len(sys.argv) < 2:
        print("用法: python3 md2wechat.py <markdown-file>")
        sys.exit(1)

    markdown_file = sys.argv[1]

    if not Path(markdown_file).exists():
        print(f"错误：文件不存在: {markdown_file}")
        sys.exit(1)

    # 提取元数据
    metadata = extract_metadata(markdown_file)

    # 转换内容
    converter = WechatHTMLConverter()
    html_content = converter.convert(metadata['content'])

    # 输出 JSON 格式
    result = {
        'title': metadata['title'],
        'digest': metadata['digest'],
        'content': html_content,
        'source_url': f'https://blog.codingdie.com/#/{markdown_file.replace(".md", "")}'
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
