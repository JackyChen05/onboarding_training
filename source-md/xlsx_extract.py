# -*- coding: utf-8 -*-
"""提取 xlsx 全部单元格文本（含共享字符串表解析）"""
import zipfile, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def xlsx_lines(path):
    z = zipfile.ZipFile(path)
    shared = []
    if 'xl/sharedStrings.xml' in z.namelist():
        ss = z.read('xl/sharedStrings.xml').decode('utf-8', errors='replace')
        # 每个 <si> 可能含多个 <t>（富文本），拼接
        for si in re.findall(r'<si>(.*?)</si>', ss, re.S):
            shared.append(''.join(re.findall(r'<t[^>]*>([^<]*)</t>', si)))
    lines = []
    sheets = sorted(n for n in z.namelist() if re.match(r'xl/worksheets/sheet\d+\.xml', n))
    for si, n in enumerate(sheets, 1):
        x = z.read(n).decode('utf-8', errors='replace')
        lines.append(f'--- sheet{si} ---')
        for row in re.findall(r'<row[^>]*>(.*?)</row>', x, re.S):
            cells = []
            for cm in re.finditer(r'<c\b([^>/]*)(?:/>|>(.*?)</c>)', row, re.S):
                attrs, inner = cm.group(1), cm.group(2) or ''
                val = ''
                if 'inlineStr' in attrs:
                    val = ''.join(re.findall(r'<t[^>]*>([^<]*)</t>', inner))
                else:
                    vm = re.search(r'<v>([^<]*)</v>', inner)
                    if vm:
                        v = vm.group(1)
                        if ' t="s"' in attrs or 't="s"' in attrs:
                            try: val = shared[int(v)]
                            except Exception: val = v
                        else:
                            val = v
                cells.append(val.strip())
            if any(cells):
                lines.append(' | '.join(c for c in cells if c))
    return lines

if __name__ == '__main__':
    for p in sys.argv[1:]:
        print('=====', p.split('\\')[-1], '=====')
        ls = xlsx_lines(p)
        print('行数', len(ls))
        for l in ls:
            print(l)
        print()
