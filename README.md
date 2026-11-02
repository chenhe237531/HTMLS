# HTMLS / ai

单文件 HTML 交付物仓库。每个目录是一份可离线打开、可分享的分析或方案。

| 目录 | 内容 |
| --- | --- |
| [`Agents/agent-workbench/`](Agents/agent-workbench/index.html) | Agent 工作台设计方案（OpenCode × Pi）；[公众号文章分析（含 17 张原文配图）](Agents/agent-workbench/wechat-agent-automation-analysis.html) |
| [`Agents/agents-hub/`](Agents/agents-hub/index.html) | AI Agent 全景：68 个产品与各自优点，含 18 个消费级助手与用量数据（2026-10） |
| [`Agents/Tools/`](Agents/Tools/index.html) | Agent 工具调研：Orca、OpenCode、Hermes、Pi、Goose、OpenHands、agent-desktop、ECC、T3 Code、cmux、herdr、Paseo、Orchestrator.inc、CoreSpeed Tie、Mainplane、PraisonAI、oh-my-pi、CLI-Anything 等（20 篇） |
| [`Agents/FreeAPI/`](Agents/FreeAPI/index.html) | FreeLLMAPI 拆解：34 家免费额度聚合成一个 /v1 端点，含路由机制、安装与限制 |
| [`MCP/mcp-hub/`](MCP/mcp-hub/index.html) | MCP Hub 导航：目录、市场与网关汇总（2026-10） |
| [`MCP/mcp-guide/`](MCP/mcp-guide/index.html) | 怎么选 MCP：从需求到验证的选型教程 |
| [`MCP/interop-protocols/`](MCP/interop-protocols/index.html) | Agent 互操作协议图谱：MCP 之外的 13 个协议、优劣与趋势 |
| [`MCP/interop-protocols/x402/`](MCP/interop-protocols/x402/index.html) | x402 深度解析：按请求付费的 HTTP 支付协议、流程、生态与风险 |
| [`MCP/interop-protocols/ap2/`](MCP/interop-protocols/ap2/index.html) | AP2 深度解析：代理支付的授权凭证、两种模式与现状 |
| [`MCP/interop-protocols/ucp/`](MCP/interop-protocols/ucp/index.html) | UCP 深度解析：代理商业的发现、协商、结账与支付 |
| [`Web3/x402/`](Web3/x402/index.html) | x402 与 Web3：14 个相关项目的代币经济模型与价值捕获 |
| [`LocalLLM/`](LocalLLM/index.html) | 本地 LLM 硬件路线：Mac Studio vs 双 Jetson Thor T5000 的配置、瓶颈与 TCO 分析 |
| [`CloudAgent/`](CloudAgent/index.html) | Agent37 分析：YC F26 的低价 Agent 沙箱、Freemium 单位经济、gVisor 路径与风险（2026-10） |
| [`Prompt/`](Prompt/index.html) | Prompt 工作台：25 条常用提示词与 11 个开源项目 |
| [`Prompt/prompt-engineering-guide/`](Prompt/prompt-engineering-guide/index.html) | Prompt Engineering Guide 使用指南：结构、学习路线与本地运行 |
| [`Agents/agent-sandbox/`](Agents/agent-sandbox/index.html) | Agent 沙箱技术白皮书：隔离方案、安全防护、资源调度与利用率（2026-10） |
| [`AgentsTeam/`](AgentsTeam/agent-fleet-1000.html) | Agent 舰队：通往 1000+ Agent 的五条路线 + [开源项目实证报告](AgentsTeam/agent-fleet-at-scale.html) |
| [`Context/`](Context/index.html) | 上下文工程：注意力预算、压缩与记忆、工具输出、多 Agent 隔离与度量（2026-10） |
| [`Context/caching/`](Context/caching/index.html) | 缓存机制：KV cache、prompt caching、语义/工具缓存、失效原因与盈亏平衡（2026-10） |
| [`AgentsTeam/agentsociety/`](AgentsTeam/agentsociety/index.html) | AgentSociety 深度介绍 · [对比斯坦福小镇](AgentsTeam/agentsociety/vs-smallville.html) · [复刻方案](AgentsTeam/agentsociety/plan.html) |
| [`AgentsTeam/race-condition/`](AgentsTeam/race-condition/index.html) | Google Race Condition 拆解：1000 agent 马拉松、0 LLM 调用技巧与复现方案 |
| [`Skills/skill-atlas/`](Skills/skill-atlas/index.html) | Skill Atlas：MiniMax Code 团队 17 个 Skill 逐篇拆解（自包含，可单独发布） |
| [`Skills/skills-hub/`](Skills/skills-hub/index.html) | Skills Hub 地图：12 个 Skills 市场 / 目录 / 仓库 / CLI 的汇总与选型清单 |
| [`Hackathons/`](Hackathons/index.html) | AI 黑客松：8 个找赛平台地图 + [商业逻辑分析](Hackathons/business.html) |

## 约定

- 一个交付物一个 `.html`，CSS/JS 内联，不依赖 CDN、网络或本地服务器。
- 页面之间只用链接导航，保证单文件可独立打开。
- 事实、原文引用与推断分开标注；文末写清来源与许可。

## 校验

```bash
python3 ~/.agents/skills/building-interactive-html-docs/scripts/verify_single_html.py "$PWD/Agents/agent-workbench/index.html"
python3 ~/.agents/skills/building-interactive-html-docs/scripts/verify_single_html.py "$PWD/Agents/agent-workbench/wechat-agent-automation-analysis.html"
python3 ~/.agents/skills/building-interactive-html-docs/scripts/verify_single_html.py "$PWD/Agents/Tools/index.html"
python3 ~/.agents/skills/building-interactive-html-docs/scripts/verify_single_html.py "$PWD/Skills/skill-atlas/index.html"
```
