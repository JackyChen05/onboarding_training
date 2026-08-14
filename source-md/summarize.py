# -*- coding: utf-8 -*-
"""汇总知识库检索结果：标题 + 摘要片段，供摘编引用"""
import json, glob, os, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

D = r"C:/Users/admin/.workbuddy/projects/d-WorkbuddySpace-Testwiki/8a09368e-f9f5-428f-a98c-5b01456c5dcf/tool-results"
out = []
for fn in sorted(glob.glob(os.path.join(D, "mcp-connector-proxy-ima-mcp_search_knowledge-*.txt"))):
    try:
        j = json.loads(open(fn, encoding='utf-8').read())
    except Exception:
        continue
    items = j.get('searched_knowledge_list', [])
    out.append(f"\n## FILE {os.path.basename(fn)}  count={len(items)}")
    for it in items[:15]:
        k = it.get('knowledge', {})
        title = k.get('title', '')
        intro = (k.get('introduction') or '')[:300].replace('\n', ' ')
        out.append(f"- {title}\n  {intro}")
print('\n'.join(out))
