# -*- coding: utf-8 -*-
"""批量提取经验文档的文本预览（标题+开头），供摘编写摘要"""
import zipfile, re, os, sys, io, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ROOT = r"D:\WorkbuddySpace\Testwiki\经验文档"
SKIP_EXT = {'.exe','.dll','.bin','.zip','.rar','.7z','.ipk','.mp4','.pcap','.pcapng',
            '.ilk','.pdb','.lnk','.tmp','.db','.so','.tcc','.xmind','.log','.cfg','.startup'}

def text_runs(b):
    x = b.decode('utf-8', errors='replace')
    return re.findall(r'<(?:w:t|a:t)[^>]*>([^<]+)</(?:w:t|a:t)>', x)

def preview(path):
    ext = os.path.splitext(path)[1].lower()
    base = os.path.basename(path)
    if base.startswith('~$') or ext in SKIP_EXT:
        return None
    try:
        if ext in ('.docx', '.pptx'):
            z = zipfile.ZipFile(path)
            names = z.namelist()
            parts = []
            if ext == '.docx':
                parts = text_runs(z.read('word/document.xml'))
            else:
                slides = sorted(n for n in names if re.match(r'ppt/slides/slide\d+\.xml', n))
                for s in slides:
                    parts += text_runs(z.read(s))
            txt = ' '.join(t.strip() for t in parts if t.strip())
            return re.sub(r'\s+', ' ', txt)[:280]
        if ext == '.doc':
            # OLE2: try to salvage readable utf16/gbk strings
            raw = open(path, 'rb').read()
            u = raw.decode('utf-16-le', errors='ignore')
            han = re.findall(r'[一-鿿　-〿＀-￯0-9A-Za-z]{6,}', u)
            if len(''.join(han)) < 40:
                g = raw.decode('gbk', errors='ignore')
                han = re.findall(r'[一-鿿　-〿＀-￯0-9A-Za-z]{6,}', g)
            return re.sub(r'\s+', ' ', ' '.join(han))[:280]
        if ext in ('.txt', '.md'):
            return open(path, encoding='utf-8', errors='replace').read()[:280]
        if ext == '.pdf':
            return '[PDF 未提取]'
    except Exception as e:
        return f'[提取失败 {e}]'
    return None

for dirpath, _, files in os.walk(ROOT):
    for f in sorted(files):
        p = os.path.join(dirpath, f)
        pv = preview(p)
        if pv is None:
            continue
        rel = os.path.relpath(p, ROOT)
        print(f"\n### {rel}\n{pv}")
