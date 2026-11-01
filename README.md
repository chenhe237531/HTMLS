# HTMLS

单文件 HTML 交付物仓库。每个目录是一份可离线打开、可分享的分析、方案或内容索引。

| 目录 | 内容 |
| --- | --- |
| [`Agents/`](Agents/agent-workbench-plan.html) | Agent 工作台设计方案（OpenCode × Pi） |
| [`Agents/agents-hub/`](Agents/agents-hub/index.html) | AI Agent 全景：50 个开源 / 闭源产品与各自优点（2026-10） |
| [`date-ops/`](date-ops/index.html) | 约会运营手册：从匹配到线下的系统设计，含漏斗计算器与聊天打分器 |
| [`MCP/mcp-hub/`](MCP/mcp-hub/index.html) | MCP Hub 导航：目录、市场与网关汇总（2026-10） |
| [`MCP/mcp-guide/`](MCP/mcp-guide/index.html) | 怎么选 MCP：从需求到验证的选型教程 |
| [`AgentsTeam/agent-fleet-1000.html`](AgentsTeam/agent-fleet-1000.html) | Agent 舰队：通往 1000+ Agent 的五条路线 |
| [`Skills/skill-atlas/`](Skills/skill-atlas/index.html) | Skill Atlas：MiniMax Code 团队 17 个 Skill 逐篇拆解（自包含，可单独发布） |
| [`Skills/skills-hub/`](Skills/skills-hub/index.html) | Skills Hub 地图：12 个 Skills 市场 / 目录 / 仓库 / CLI 的汇总与选型清单 |
| [`Video/课代表立正/`](Video/课代表立正/index.html) | B站 UP「课代表立正」投稿索引：804 条视频的标题、发布日期、播放量、时长、分区、简介概述，支持主题 / 形式 / 年份筛选（2026-10 抓取） |
| [`Video/课代表立正/topics.html`](Video/课代表立正/topics.html) | 同频道的分类与资料整理：10 个主题、6 种内容形式、32 本书、45 位访谈嘉宾、87 条站外链接 |

## 约定

- 一个交付物一个 `.html` 组，CSS/JS 与图片全部内联，不依赖 CDN、网络或本地服务器。
- 页面之间只用链接导航，保证单文件可独立打开。
- 事实、原文引用与推断分开标注；文末写清来源与许可；数据类页面注明抓取时间。
- 摘录型内容保留原文，不做 AI 改写；缺失的地方如实标注。
- 自动归类（关键词、规则）要在页面上写明方法与边界，不当作人工精标。

## 校验

```bash
python3 ~/.agents/skills/building-interactive-html-docs/scripts/verify_single_html.py "$PWD/Agents/agent-workbench-plan.html"
python3 ~/.agents/skills/building-interactive-html-docs/scripts/verify_single_html.py "$PWD/Skills/skill-atlas/index.html"
for f in "$PWD"/Video/课代表立正/*.html; do
  python3 ~/.agents/skills/building-interactive-html-docs/scripts/verify_single_html.py "$f"
done
```
