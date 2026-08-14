# Onboarding Training · 嵌入式产品测试应届生培训学习站

面向嵌入式产品测试岗应届生的入职培训知识站点。内容以部门《嵌入式产品系统测试入门学习手册》和《新员工试用期目标设定》为主干，配合测试知识库专题资料摘编而成。

## 站点结构（training-site/，VitePress）

| 模块 | 内容 |
| --- | --- |
| 1-access | 接入产品：PON 架构、OMCI、DBA、TR-069/369、关键协议、Wi-Fi 指标、环境搭建 |
| 2-multimedia | 多媒体产品：机顶盒架构、IGMP/RTSP/HLS/DASH、CAS/DRM、HDMI/HDCP |
| 3-tools | 常用工具：Wireshark、串口日志、码流分析、Linux、版本与缺陷管理（导师签核 checklist） |
| 4-defects | 缺陷库：生命周期、提报规范、缺陷模式分类、证据链要求 |
| 5-cases | 典型案例：运营商入库测试、现网问题复盘、环境搭建案例 |

入口页：`docs/path.md`（20 周培训路径总览）；维护规范见 `docs/maintenance.md`。

## 本地预览

```bash
cd training-site
npm install
npm run dev   # http://localhost:5173
```

## 目录说明

- `training-site/` — VitePress 站点（docs/ 下为全部内容页）
- `source-md/` — 源文档转换中间层：`docx2md.py`（docx→Markdown）、`summarize.py`（知识库检索摘要）、手册与目标设定的 Markdown 版本、知识库摘编
- 源 docx 文档（手册、目标设定）未纳入版本库，请从部门文档渠道获取

## 内容维护约定

内容分两层：主干正文（手册驱动，低频更新）+ 扩展阅读（知识库摘编引用，须标注作者与出处，不全量复制）。详见站内「维护规范」页。
