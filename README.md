# HTMLS / ai

单文件 HTML 交付物仓库。每个目录是一份可离线打开、可分享的分析或方案。

| 目录 | 内容 |
| --- | --- |
| [`Agents/`](Agents/agent-workbench-plan.html) | Agent 工作台设计方案（OpenCode × Pi） |
| [`Agents/agents-hub/`](Agents/agents-hub/index.html) | AI Agent 全景：50 个开源 / 闭源产品与各自优点（2026-10） |
| [`MCP/mcp-hub/`](MCP/mcp-hub/index.html) | MCP Hub 导航：目录、市场与网关汇总（2026-10） |
| [`MCP/mcp-guide/`](MCP/mcp-guide/index.html) | 怎么选 MCP：从需求到验证的选型教程 |
| [`AgentsTeam/agent-fleet-1000.html`](AgentsTeam/agent-fleet-1000.html) | Agent 舰队：通往 1000+ Agent 的五条路线 |
| [`Skills/skill-atlas/`](Skills/skill-atlas/index.html) | Skill Atlas：MiniMax Code 团队 17 个 Skill 逐篇拆解（自包含，可单独发布） |
| [`Skills/skills-hub/`](Skills/skills-hub/index.html) | Skills Hub 地图：12 个 Skills 市场 / 目录 / 仓库 / CLI 的汇总与选型清单 |

## 约定

- 一个交付物一个 `.html`，CSS/JS 内联，不依赖 CDN、网络或本地服务器。
- 页面之间只用链接导航，保证单文件可独立打开。
- 事实、原文引用与推断分开标注；文末写清来源与许可。

## 校验

```bash
python3 ~/.agents/skills/building-interactive-html-docs/scripts/verify_single_html.py "$PWD/Agents/agent-workbench-plan.html"
python3 ~/.agents/skills/building-interactive-html-docs/scripts/verify_single_html.py "$PWD/Skills/skill-atlas/index.html"
```
