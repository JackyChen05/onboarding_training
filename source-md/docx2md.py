# -*- coding: utf-8 -*-
"""将 docx 转换为结构化 Markdown（保留标题层级、列表、表格）"""
import zipfile, re, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def parse_docx(path):
    z = zipfile.ZipFile(path)
    xml = z.read('word/document.xml').decode('utf-8')
    return xml

def extract_runs(p):
    """提取段落内所有文本 run"""
    texts = re.findall(r'<w:t[^>]*>([^<]*)</w:t>', p)
    return ''.join(texts)

def esc(t):
    t = t.replace('&quot;', '"').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&apos;', "'")
    return t

def is_table_start(p):
    return '<w:tbl>' in p

def docx_to_md(path):
    xml = parse_docx(path)
    # split by body-level elements: paragraphs and tables
    # first, protect tables by extracting them
    lines = []
    # iterate through tokens: split on </w:p> but also handle tables
    # Simple approach: replace table rows/cells with markers first
    def table_repl(m):
        tbl = m.group(0)
        rows = re.findall(r'<w:tr[ >].*?</w:tr>', tbl, re.S)
        md_rows = []
        for r in rows:
            cells = re.findall(r'<w:tc>.*?</w:tc>', r, re.S)
            cell_texts = []
            for c in cells:
                ps = re.findall(r'<w:t[^>]*>([^<]*)</w:t>', c)
                cell_texts.append(esc(''.join(ps)).strip().replace('|', '/'))
            md_rows.append('| ' + ' | '.join(cell_texts) + ' |')
        if not md_rows:
            return ''
        # header separator after first row
        header = md_rows[0]
        ncols = header.count('|') - 1
        sep = '|' + ' --- |' * max(ncols, 1)
        return '\n@@TABLE@@' + header + '\n' + sep + '\n' + '\n'.join(md_rows[1:]) + '\n@@ENDTABLE@@\n'

    xml2 = re.sub(r'<w:tbl>.*?</w:tbl>', table_repl, xml, flags=re.S)

    paras = re.split(r'</w:p>', xml2)
    md = []
    in_table = False
    for p in paras:
        style_m = re.search(r'w:pStyle w:val="([^"]+)"', p)
        style = style_m.group(1) if style_m else ''
        text = esc(extract_runs(p)).strip()

        # table chunks: p may contain table markers
        if '@@TABLE@@' in p:
            # extract table block
            tbl_match = re.search(r'@@TABLE@@(.*?)@@ENDTABLE@@', p, re.S)
            if tbl_match:
                md.append('')
                md.append(tbl_match.group(1).strip())
                md.append('')
            # also capture any text before marker
            pre = p.split('@@TABLE@@')[0]
            pre_text = esc(extract_runs(pre)).strip() if '<w:t' in pre else ''
            if pre_text:
                md.append(pre_text)
            continue

        if not text:
            continue

        if style == 'Heading1':
            md.append('')
            md.append('# ' + text)
            md.append('')
        elif style == 'Heading2':
            md.append('')
            md.append('## ' + text)
            md.append('')
        elif style == 'Heading3':
            md.append('')
            md.append('### ' + text)
            md.append('')
        elif style == 'ListParagraph':
            md.append('- ' + text)
        else:
            md.append(text)
            md.append('')
    return '\n'.join(md)

if __name__ == '__main__':
    src = sys.argv[1]
    dst = sys.argv[2]
    md = docx_to_md(src)
    with open(dst, 'w', encoding='utf-8') as f:
        f.write(md)
    print(f'OK: {dst}  ({len(md)} chars)')
