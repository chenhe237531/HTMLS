# HTMLS / video

单文件 HTML 交付物：视频平台的频道 / 内容索引，可离线打开、可分享。

| 目录 | 内容 |
| --- | --- |
| [`Video/课代表立正/`](Video/课代表立正/index.html) | B站 UP「课代表立正」投稿索引：804 条视频的标题、发布日期、播放量、时长、分区、简介概述，支持主题 / 形式 / 年份筛选（2026-10 抓取） |
| [`Video/课代表立正/topics.html`](Video/课代表立正/topics.html) | 同频道的分类与资料整理：10 个主题、6 种内容形式、32 本书、45 位访谈嘉宾、87 条站外链接 |

## 约定

- 一个交付物一个 `.html` 组，CSS/JS 与图片全部内联，不依赖 CDN、网络或本地服务器。
- 组内页面互相链接（`index.html` ↔ `topics.html`），单页仍可独立打开。
- 表格、长列表与数据来自平台公开接口；页面底部注明来源与抓取时间。
- 概述为 UP 主视频简介原文摘录，不做 AI 改写；无简介的视频如实标注。
- 分类是关键词归类的产物，页面上写明方法与边界，不把它当成人工精标。

## 校验

```bash
for f in "$PWD"/Video/课代表立正/*.html; do
  python3 ~/.agents/skills/building-interactive-html-docs/scripts/verify_single_html.py "$f"
done
```
