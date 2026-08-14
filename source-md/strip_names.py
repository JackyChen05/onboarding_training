# -*- coding: utf-8 -*-
"""删除站点 md 中的人名署名。剥离「《标题》- 作者」与「》- 作者 ——」等格式。"""
import re, os, glob, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

NAMES = ["杜琴","骆聪","周鹏","刘明","齐丹凤","徐雄","徐惠恩","田鸣","黄强","黄波","郭树亮","卓志锷",
         "石才勇","熊锦","李文平","罗琪","罗君","王琰琳","易秋兰","柯美灯","肖群凤","陈金祥","陈泽榜",
         "谭健伟","李小雄","钱礼","雷亚光","朱丽","茹炳晟","黄成","肖志祥","王溆","陈龙","吕冬冬","武汉齐丹凤"]
# 长名在前，避免短名先匹配
NAMES.sort(key=len, reverse=True)
NAME_RE = "|".join(map(re.escape, NAMES))

DOCS = r"D:\WorkbuddySpace\Testwiki\training-site\docs"
changed = []

for path in glob.glob(os.path.join(DOCS, "**", "*.md"), recursive=True):
    s = open(path, encoding="utf-8").read()
    orig = s
    # 1) 《标题》- 作者   →  《标题》   （含 _作者、-作者、--作者 等结尾，作者后到行尾是分隔符或行尾）
    s = re.sub(r"(》[ _]*[-—]{1,2}[ _]*(?:" + NAME_RE + r"))(?=[ _]*(?:——|--|-|$|\n|\(|\（))", "", s)
    # 2) 标题中残留 _作者 / -作者（在书名号内部，如 《10、移动入库测试经验总结_黄强》）
    s = re.sub(r"(_(?:" + NAME_RE + r"))(?=》)", "", s)
    # 3) 正文括号内人名：（测试部 易秋兰）→（测试部）；（周鹏）→ 删除整对空括号内容
    s = re.sub(r"（(?:" + NAME_RE + r")）", "", s)
    s = re.sub(r"（([^（）]*?)(?:" + NAME_RE + r")([^（）]*?)）", lambda m: "（" + (m.group(1) + m.group(2)).strip() + "）", s)
    # 清理空括号
    s = re.sub(r"（\s*）", "", s)
    if s != orig:
        open(path, "w", encoding="utf-8").write(s)
        changed.append(os.path.relpath(path, DOCS))

print("\n".join(changed))
print("---残留检查---")
for path in glob.glob(os.path.join(DOCS, "**", "*.md"), recursive=True):
    s = open(path, encoding="utf-8").read()
    for n in NAMES:
        if n in s:
            print("LEFT", os.path.relpath(path, DOCS), n)
