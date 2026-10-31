# HTMLS / ai

单文件 HTML 交付物仓库。每个目录是一份可离线打开、可分享的分析或方案。

| 目录 | 内容 |
| --- | --- |
| [`Agents/`](Agents/agent-workbench-plan.html) | Agent 工作台设计方案（OpenCode × Pi） |
| [`skill-atlas/`](skill-atlas/index.html) | Skill Atlas：MiniMax Code 团队 17 个 Skill 逐篇拆解（自包含，可单独发布） |

## 约定

- 一个交付物一个 `.html`，CSS/JS 内联，不依赖 CDN、网络或本地服务器。
- 页面之间只用链接导航，保证单文件可独立打开。
- 事实、原文引用与推断分开标注；文末写清来源与许可。

## 校验

```bash
python3 ~/.agents/skills/building-interactive-html-docs/scripts/verify_single_html.py "$PWD/Agents/agent-workbench-plan.html"
python3 ~/.agents/skills/building-interactive-html-docs/scripts/verify_single_html.py "$PWD/skill-atlas/index.html"
```
