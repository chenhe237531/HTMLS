# -*- coding: utf-8 -*-
"""Agent 与开发工具类项目。"""

PROJECTS = [
    {
        "repo": "kimi-code",
        "slug": "kimi-code",
        "title": "Kimi Code CLI",
        "category": "agent",
        "status": "active",
        "tagline": "单二进制、毫秒启动的终端编码 Agent，Kimi CLI 的正统继任者",
        "summary": "Kimi Code CLI 是运行在终端里的 AI 编码 Agent：能读写代码、跑 shell、搜文件、抓网页，并根据反馈决定下一步。它用官方脚本安装，不依赖 Node.js；TUI 面向长时间专注会话设计，还支持视频输入、对话式 MCP 配置、插件市场、子 Agent 与生命周期 hooks。",
        "points": [
            "单二进制分发，macOS/Linux 一行脚本，Windows 用 PowerShell；也支持 Homebrew 与 npm。",
            "内置 coder / explore / plan 三个子 Agent，在隔离上下文里并行工作。",
            "视频输入：把录屏、演示片段丢进对话，让 Agent“看”难以用文字描述的需求。",
            "ACP 集成：Zed、JetBrains 等支持 Agent Client Protocol 的编辑器可直接驱动会话。",
        ],
        "stats": [["8.1k", "Stars"], ["单二进制", "分发"], ["3", "内置子 Agent"], ["MIT", "许可证"]],
        "sections": [
            {
                "h": "它解决什么问题",
                "html": "<p>终端 Agent 的常见痛点是启动慢、依赖重、长会话容易乱。Kimi Code 的取舍是：用单二进制去掉 Node 运行时与全局模块冲突；用专门调过的 TUI 支撑长时间会话；用子 Agent 把“探索代码库”“做计划”“写代码”拆到隔离上下文，避免主对话被大量中间输出污染。</p>",
            },
            {
                "h": "值得注意的能力",
                "html": "<p><b>AI-native MCP 配置</b>：用 <code>/mcp-config</code> 对话式添加、编辑、认证 MCP server，不必手写 JSON。<b>插件生态</b>：从市场或任意 GitHub 仓库安装 skills、MCP server、数据源，并在安装时展示信任级别。<b>生命周期 hooks</b>：在关键节点跑本地命令，用于拦截高风险工具调用、审计、桌面通知或接自己的自动化。</p><p><b>视频输入</b>是它与多数编码 CLI 的差异点：官方举的例子包括把参考片段转成 LUT、把长视频剪短、把录屏变成可运行代码。</p>",
            },
            {
                "h": "与旧版 Kimi CLI 的关系",
                "html": "<p>旧的 Python 版 <code>kimi-cli</code> 已归档，官方要求迁移到 Kimi Code。首次启动会检测 <code>~/.kimi/</code> 里的配置、MCP server、输入历史与会话，并询问是否迁移；原数据不会被修改或删除，也可以随时运行 <code>kimi migrate</code>。</p>",
            },
        ],
        "specs": [
            ["实现语言", "TypeScript"],
            ["分发", "单二进制 / Homebrew / npm"],
            ["子 Agent", "coder、explore、plan"],
            ["编辑器集成", "ACP（Zed、JetBrains 等）"],
            ["许可证", "MIT"],
        ],
        "quickstart": {
            "lang": "bash",
            "note": "官方安装脚本；Windows 需先装 Git for Windows。",
            "code": "# macOS / Linux\ncurl -fsSL https://code.kimi.com/kimi-code/install.sh | bash\n\n# Windows PowerShell\n# irm https://code.kimi.com/kimi-code/install.ps1 | iex\n\nkimi --version\nkimi",
        },
        "relations": [
            {"name": "kimi-cli", "slug": "kimi-cli", "note": "已归档的 Python 前身，可迁移"},
            {"name": "kimi-agent-sdk", "slug": "kimi-agent-sdk", "note": "把同一运行时嵌进 Go/Node/Python 应用"},
            {"name": "kimi-agent-rs", "slug": "kimi-agent-rs", "note": "Rust 重写，wire 协议兼容"},
            {"name": "kimi-code-zed-extension", "slug": "kimi-code-zed-extension", "note": "Zed 编辑器集成"},
            {"name": "zsh-kimi-cli", "slug": "zsh-kimi-cli", "note": "Zsh 里的 Ctrl-X 快捷入口"},
        ],
        "caveats": [
            "默认走 Kimi 模型，但也可以配置其他兼容 provider；换 provider 后工具调用质量要重新验证。",
            "插件与 MCP server 能执行本地代码，安装前务必看信任级别。",
            "视频输入、ACP 等能力依赖版本，旧版文档可能不适用。",
        ],
    },
    {
        "repo": "kimi-cli",
        "slug": "kimi-cli",
        "title": "Kimi CLI（已归档）",
        "category": "agent",
        "status": "archived",
        "tagline": "Python 版终端 Agent，已被 Kimi Code CLI 取代",
        "summary": "Kimi CLI 是早期的 Python 终端 Agent，包含 kosong（LLM 抽象）与 kaos（OS 抽象）等包，支持 shell 命令模式、VS Code 扩展、ACP、Zsh 集成与 MCP。仓库已于 2026 年归档，只读，不再发布、修复或提供安全更新。",
        "points": [
            "Python 实现，仓库内含 kosong 与 kaos 两个基础包。",
            "支持 MCP（stdio / streamable HTTP / OAuth）、ACP、VS Code、Zsh。",
            "归档后现有安装将停止工作，官方要求迁移到 kimi-code。",
            "迁移会保留 ~/.kimi 原数据，可运行 kimi migrate。",
        ],
        "stats": [["11.4k", "Stars"], ["已归档", "状态"], ["Python", "语言"], ["Apache-2.0", "许可证"]],
        "sections": [
            {
                "h": "为什么仍值得看",
                "html": "<p>它是理解 Kimi Agent 运行时演化的最好样本：kosong 负责 messages、tool schema、provider 抽象；kaos 负责本地文件系统、路径语义与沙箱；上层 CLI 负责会话、工具调用、MCP 与编辑器集成。后来的 Rust 重写（kimi-agent-rs）明确要求与 Python 版在 wire 协议、消息格式、<code>~/.kimi</code> 数据布局、工具 schema 上兼容，并把 Python 版当作 source of truth。</p>",
            },
            {
                "h": "迁移而不是继续用",
                "html": "<p>README 的警告很直接：仓库只读，不再有 release、bug fix 或安全更新，现有安装会停止工作。迁移步骤是安装 Kimi Code CLI，然后首次启动按提示迁移，或运行 <code>kimi migrate</code>。原 <code>~/.kimi/</code> 不会被修改或删除。</p>",
            },
        ],
        "specs": [
            ["实现语言", "Python"],
            ["状态", "Archived（2026）"],
            ["核心包", "kosong、kaos"],
            ["集成", "MCP、ACP、VS Code、Zsh"],
            ["许可证", "Apache-2.0"],
        ],
        "relations": [
            {"name": "kimi-code", "slug": "kimi-code", "note": "官方继任者"},
            {"name": "kosong", "slug": "kosong", "note": "LLM 抽象层，已并入本仓库 monorepo"},
            {"name": "pykaos", "slug": "pykaos", "note": "OS 抽象层，已并入本仓库 monorepo"},
            {"name": "kimi-agent-rs", "slug": "kimi-agent-rs", "note": "保持 wire 兼容的 Rust 重写"},
        ],
        "caveats": [
            "不要在新项目中使用；不会有安全修复。",
            "旧文档与旧安装可能随时失效。",
            "迁移后要重新检查 MCP server 与工具权限配置。",
        ],
    },
    {
        "repo": "kimi-agent-sdk",
        "slug": "kimi-agent-sdk",
        "title": "Kimi Agent SDK",
        "category": "agent",
        "status": "active",
        "tagline": "用 Go / Node / Python 把 Kimi CLI 当作 Agent 运行时嵌进产品",
        "summary": "Kimi Agent SDK 是一组多语言薄客户端，复用 Kimi Code（Kimi CLI）的配置、工具、skills 与 MCP server。它把 CLI 当执行引擎，向外提供流式响应、工具调用、审批请求与会话编排能力。",
        "points": [
            "三种语言：Go、Node.js、Python，分别有独立包。",
            "复用 CLI 的配置、工具、skills、MCP，不必在 SDK 里重写一套。",
            "实时流式输出，暴露 approval 与 tool call。",
            "支持注册自定义工具、脚本化多轮会话。",
        ],
        "stats": [["3", "语言 SDK"], ["580", "Stars"], ["CLI", "执行引擎"], ["Apache-2.0", "许可证"]],
        "sections": [
            {
                "h": "定位：不是另一个 Agent 框架",
                "html": "<p>很多 SDK 会自己实现 Agent 循环、工具注册、上下文管理；Kimi Agent SDK 选择把这些问题留给 CLI，自己只做“语言原生客户端”。好处是配置、工具、skills、MCP 只有一份，CLI 升级后 SDK 自动受益；代价是部署时必须带上 CLI，且要接受 CLI 的协议与版本节奏。</p>",
            },
            {
                "h": "适合什么场景",
                "html": "<p>把 Kimi Agent 接进 IDE 插件、内部自动化、CI 机器人、客服后台，或者做需要程序化审批的多轮任务。SDK 明确列出四类能力：构建自定义应用、自动化任务、扩展工具、处理审批。</p>",
            },
        ],
        "specs": [
            ["语言", "Go / Node.js / Python"],
            ["运行时", "Kimi Code CLI"],
            ["能力", "流式、工具调用、审批、自定义工具"],
            ["许可证", "Apache-2.0"],
        ],
        "quickstart": {
            "lang": "bash",
            "note": "三种语言的包名不同；具体 API 见仓库各语言目录。",
            "code": "# Python\npip install kimi-agent-sdk\n\n# Node.js\nnpm install @moonshot-ai/kimi-agent-sdk\n\n# Go\ngo get github.com/MoonshotAI/kimi-agent-sdk/go",
        },
        "relations": [
            {"name": "kimi-code", "slug": "kimi-code", "note": "SDK 的执行引擎"},
            {"name": "kimi-cli", "slug": "kimi-cli", "note": "旧版运行时（已归档）"},
            {"name": "kimi-agent-rs", "slug": "kimi-agent-rs", "note": "另一条 Rust 运行时实现"},
        ],
        "caveats": [
            "必须先安装并配置好 Kimi CLI，SDK 不是独立运行时。",
            "审批语义与权限模型由 CLI 决定，嵌入产品时要设计好用户确认流程。",
            "多语言包的 API 可能不完全同步，升级前看各自 changelog。",
        ],
    },
    {
        "repo": "kimi-agent-rs",
        "slug": "kimi-agent-rs",
        "title": "Kimi Agent (Rust)",
        "category": "agent",
        "status": "research",
        "tagline": "Kimi CLI 的 Rust 重写，wire 协议与 Python 版严格兼容",
        "summary": "kimi-agent-rs 是 Kimi Code CLI 的 Rust 实现，定位为“wire-only JSON-RPC agent server over stdio”。工作区包含 kimi-agent（主二进制、工具、Agent 循环、MCP）、kosong（LLM 抽象）、kaos（OS 抽象）三个 crate。",
        "points": [
            "JSON-RPC over stdio，只走 wire 协议。",
            "与 Python 版在协议、消息格式、~/.kimi 布局、工具 schema 上必须兼容。",
            "Python 版是 source of truth，版本号必须完全一致。",
            "把 kimi-cli 作为 git submodule 固定。",
        ],
        "stats": [["Rust", "语言"], ["3", "crate"], ["stdio", "传输"], ["Apache-2.0", "许可证"]],
        "sections": [
            {
                "h": "为什么重写",
                "html": "<p>Rust 版的目标不是另起炉灶，而是给同一套 Agent 运行时换一个更轻、更容易单二进制分发的实现。README 把兼容性写得很硬：wire 协议、消息格式、<code>~/.kimi</code> 数据布局、工具 schema 以及所有外部可观察行为都要与 Python 版一致；版本号也必须匹配。这意味着它更像“可替换的运行时内核”，而不是一个独立产品。</p>",
            },
            {
                "h": "工作区",
                "html": "<p><code>kimi-agent</code> 是主二进制，包含 wire server、工具、Agent 循环与 MCP；<code>kosong</code> 负责 messages、tool schemas 与 provider；<code>kaos</code> 负责 LocalKaos 与路径语义。测试也按 crate 拆分。</p>",
            },
        ],
        "specs": [
            ["语言", "Rust"],
            ["传输", "JSON-RPC over stdio"],
            ["crate", "kimi-agent / kosong / kaos"],
            ["兼容目标", "Python kimi-cli"],
            ["许可证", "Apache-2.0"],
        ],
        "quickstart": {
            "lang": "bash",
            "note": "构建与测试入口。",
            "code": "cargo build -p kimi-agent\n./target/debug/kimi-agent\n\ncargo test\ncargo test -p kimi-agent\ncargo test -p kosong\ncargo test -p kaos",
        },
        "relations": [
            {"name": "kimi-code", "slug": "kimi-code", "note": "产品化的终端 Agent"},
            {"name": "kimi-cli", "slug": "kimi-cli", "note": "兼容性基准（已归档）"},
            {"name": "kimi-agent-sdk", "slug": "kimi-agent-sdk", "note": "多语言客户端"},
        ],
        "caveats": [
            "项目很早期，最后一次 push 停留在 2026-02。",
            "强兼容约束意味着不能随意改协议，创新空间有限。",
            "需要 Rust 工具链与 Python 版子模块才能完整构建/测试。",
        ],
    },
    {
        "repo": "kosong",
        "slug": "kosong",
        "title": "Kosong",
        "category": "agent",
        "status": "moved",
        "tagline": "Agent 应用的 LLM 抽象层（已并入 kimi-cli monorepo）",
        "summary": "Kosong 原本是 Kimi Agent 的 LLM 抽象层，统一 messages、tool schemas 与 provider。现在开发已迁移到 kimi-cli 仓库的 packages/kosong，本仓库只保留迁移提示。",
        "points": [
            "统一不同 LLM provider 的消息与工具调用格式。",
            "为 Agent 循环提供稳定的模型接口。",
            "代码已迁移到 kimi-cli/tree/main/packages/kosong。",
            "本仓库不再接受开发。",
        ],
        "stats": [["524", "Stars"], ["已迁移", "状态"], ["LLM", "抽象层"], ["未声明", "许可证"]],
        "sections": [
            {
                "h": "它抽象了什么",
                "html": "<p>Agent 应用最难移植的部分往往不是业务逻辑，而是各家模型的消息格式、tool schema、流式事件与错误语义。Kosong 把这些收敛成一套内部接口，让上层 Agent 不必为每个 provider 写分支。它也是 Rust 重写版里保留的同名 crate。</p>",
            },
            {
                "h": "现在去哪里找",
                "html": "<p>README 只有一句话：开发已移到 <code>kimi-cli</code> monorepo 的 <code>packages/kosong</code>。如果你在找可安装的包或源码，应直接去 kimi-cli 仓库，而不是这里。</p>",
            },
        ],
        "specs": [
            ["类型", "LLM 抽象层"],
            ["状态", "已迁移"],
            ["新位置", "kimi-cli/packages/kosong"],
        ],
        "relations": [
            {"name": "kimi-cli", "slug": "kimi-cli", "note": "新的开发位置"},
            {"name": "pykaos", "slug": "pykaos", "note": "同批迁移的 OS 抽象层"},
            {"name": "kimi-agent-rs", "slug": "kimi-agent-rs", "note": "Rust 工作区保留同名 crate"},
        ],
        "caveats": [
            "本仓库是空壳，不要在这里提 issue 或 PR。",
            "独立包可能已停止发布，安装前确认来源。",
        ],
    },
    {
        "repo": "pykaos",
        "slug": "pykaos",
        "title": "PyKAOS",
        "category": "agent",
        "status": "moved",
        "tagline": "Agent 的轻量 OS 抽象层（已并入 kimi-cli monorepo）",
        "summary": "PyKAOS 是 Kimi Agent 的 OS 抽象层，提供 LocalKaos、路径语义与沙箱相关能力。开发已迁移到 kimi-cli 仓库的 packages/kaos，本仓库只保留迁移提示。",
        "points": [
            "把文件系统、路径、执行环境抽象成 Agent 可用的接口。",
            "为工具调用提供一致的本地/沙箱语义。",
            "代码已迁移到 kimi-cli/tree/main/packages/kaos。",
            "Rust 重写版保留同名 kaos crate。",
        ],
        "stats": [["20", "Stars"], ["已迁移", "状态"], ["OS", "抽象层"], ["未声明", "许可证"]],
        "sections": [
            {
                "h": "为什么 Agent 需要 OS 抽象",
                "html": "<p>Agent 的工具调用最终要落到文件读写、命令执行、路径解析上。如果这些逻辑散落在每个工具里，沙箱、权限与跨平台行为就会不一致。KAOS 把“Agent 眼中的操作系统”收敛成一层接口，LocalKaos 是本地实现，路径语义则保证不同平台下行为可预测。</p>",
            },
            {
                "h": "现在去哪里找",
                "html": "<p>开发位置是 <code>kimi-cli/packages/kaos</code>。本仓库没有可运行代码，只有迁移说明。</p>",
            },
        ],
        "specs": [
            ["类型", "OS 抽象层"],
            ["状态", "已迁移"],
            ["新位置", "kimi-cli/packages/kaos"],
        ],
        "relations": [
            {"name": "kimi-cli", "slug": "kimi-cli", "note": "新的开发位置"},
            {"name": "kosong", "slug": "kosong", "note": "同批迁移的 LLM 抽象层"},
            {"name": "kimi-agent-rs", "slug": "kimi-agent-rs", "note": "Rust 工作区保留同名 crate"},
        ],
        "caveats": [
            "本仓库是空壳，不要在这里提 issue 或 PR。",
            "沙箱能力与宿主 OS 相关，跨平台行为需实测。",
        ],
    },
    {
        "repo": "zsh-kimi-cli",
        "slug": "zsh-kimi-cli",
        "title": "zsh-kimi-cli",
        "category": "agent",
        "status": "active",
        "tagline": "在 Zsh 里按 Ctrl-X，直接跟 Kimi 对话",
        "summary": "一个很小的 Zsh 插件：按 Ctrl-X 进入 Kimi CLI 模式，再按一次退出。支持手动 source、Oh My Zsh、Antigen、Zinit、Znap、Fig、Zplug 等常见插件管理器。",
        "points": [
            "Ctrl-X 切换 Kimi CLI 模式。",
            "要求 Zsh 5.4+，且 kimi 二进制在 PATH 中。",
            "安装方式覆盖主流 Zsh 插件管理器。",
            "不改变 Kimi CLI 本身的行为，只是快捷入口。",
        ],
        "stats": [["67", "Stars"], ["Ctrl-X", "快捷键"], ["Zsh 5.4+", "要求"], ["Shell", "语言"]],
        "sections": [
            {
                "h": "它做什么、不做什么",
                "html": "<p>它不实现 Agent，也不封装 API；只是把“打开终端 → 输入 kimi → 退出”压缩成一个快捷键。适合已经把 Kimi CLI 当日常工具、希望随时问一句就回到 shell 的人。</p>",
            },
            {
                "h": "安装",
                "html": "<p>手动方式是在 <code>.zshrc</code> 里 source 插件文件；Oh My Zsh 把仓库克隆到 custom/plugins 并加入 plugins 数组；其余管理器各有一行命令。装完开新 shell 或 <code>exec zsh</code> 生效。</p>",
            },
        ],
        "specs": [
            ["类型", "Zsh 插件"],
            ["快捷键", "Ctrl-X"],
            ["依赖", "Zsh 5.4+、kimi"],
            ["许可证", "仓库未声明"],
        ],
        "relations": [
            {"name": "kimi-code", "slug": "kimi-code", "note": "提供 kimi 二进制"},
            {"name": "kimi-cli", "slug": "kimi-cli", "note": "旧版 CLI，插件名沿用"},
        ],
        "caveats": [
            "只对 Zsh 有效，bash/fish 不适用。",
            "kimi 不在 PATH 时快捷键无效。",
            "仓库无许可证声明。",
        ],
    },
    {
        "repo": "kimi-code-zed-extension",
        "slug": "kimi-code-zed-extension",
        "title": "Kimi CLI Zed Extension",
        "category": "agent",
        "status": "active",
        "tagline": "在 Zed 的 Agent Panel 里直接用 Kimi Code",
        "summary": "把 Kimi CLI 作为 ACP（Agent Client Protocol）Agent 接进 Zed 编辑器。扩展会自动下载并配置二进制，首次使用通过 /setup 选择 provider 并输入 API key，之后可以在 Zed 里直接开 Kimi 线程。",
        "points": [
            "ACP Agent 集成，跨 macOS / Linux / Windows。",
            "自动下载与配置 Kimi CLI 二进制。",
            "首次使用在终端里跑 /setup 完成认证。",
            "支持 Kimi、OpenAI、Anthropic 等 provider。",
        ],
        "stats": [["13", "Stars"], ["ACP", "协议"], ["3", "平台"], ["Apache-2.0", "许可证"]],
        "sections": [
            {
                "h": "使用流程",
                "html": "<p>在 Zed 扩展市场搜 “Kimi CLI” 安装；用 <code>Cmd+?</code>（macOS）或 <code>Ctrl+?</code> 打开 Agent Panel，点右上角 + 新建线程；首次会提示用 <code>/setup</code> 配置 LLM，终端里选 provider、填 API key；完成后即可在编辑器内对话。</p>",
            },
            {
                "h": "为什么用 ACP 而不是自己写 UI",
                "html": "<p>ACP 让编辑器负责 UI 与会话管理，Agent 负责推理与工具调用。这样同一套 Kimi CLI 可以同时服务 Zed、JetBrains 和终端，不必为每个编辑器维护一套插件逻辑。</p>",
            },
        ],
        "specs": [
            ["类型", "Zed 扩展"],
            ["协议", "ACP"],
            ["平台", "macOS / Linux / Windows"],
            ["许可证", "Apache-2.0"],
        ],
        "relations": [
            {"name": "kimi-code", "slug": "kimi-code", "note": "底层 Agent"},
            {"name": "kimi-cli", "slug": "kimi-cli", "note": "扩展名沿用旧称"},
        ],
        "caveats": [
            "需要 Zed 支持 ACP 的版本。",
            "首次认证要离开编辑器到终端完成。",
            "自动下载二进制的网络环境可能受限。",
        ],
    },
    {
        "repo": "Kimi-Researcher",
        "slug": "kimi-researcher",
        "title": "Kimi-Researcher",
        "category": "agent",
        "status": "research",
        "tagline": "用端到端 Agentic RL 训出的搜索研究 Agent",
        "summary": "Kimi-Researcher 是一个自主的多轮搜索与推理 Agent，平均每个任务 23 个推理步骤、探索 200+ URL。它基于内部 k 系列模型，完全通过端到端 Agentic RL 训练；HLE Pass@1 从 8.6% 提升到 26.9%，Pass@4 40.17%。",
        "points": [
            "平均 23 个 reasoning steps、200+ URL / 任务。",
            "HLE Pass@1 26.9%，Pass@4 40.17%，官方称当时 SOTA。",
            "xbench-DeepSearch 69% pass@1（4 次平均），超过带搜索工具的 o3。",
            "工具箱：并行实时搜索、文本浏览器、代码执行。",
        ],
        "stats": [["26.9%", "HLE Pass@1"], ["23", "平均步数"], ["200+", "URL/任务"], ["69%", "xbench-DeepSearch"]],
        "sections": [
            {
                "h": "方法：从 8.6% 到 26.9% 几乎全靠 RL",
                "html": "<p>官方页面强调，Kimi-Researcher 的 HLE 分数从初始 8.6% 提升到 26.9%，几乎完全来自端到端 Agentic RL，而不是蒸馏或人工写死的搜索流程。训练时模型在“思考 → 工具调用 → 观察 → 再思考”的循环里学习，动作可以是搜索、打开网页、执行代码，或结束任务。</p>",
            },
            {
                "h": "仓库里有什么",
                "html": "<p>这个仓库只有一个项目页 HTML，<b>没有训练代码、权重或可运行 Agent</b>。它的价值是公开的方法叙述与评测结果：多轮搜索 Agent 的能力可以通过 RL 直接优化，而不是靠复杂的多 Agent 编排。</p><p>页面也提醒：搜索工具波动会影响成绩；HLE 测于 2025-06-17，其他基准测于 2025-06-18，结果用 o3-mini 评判。</p>",
            },
        ],
        "specs": [
            ["类型", "项目页 / 技术博客"],
            ["HLE Pass@1", "26.9%"],
            ["HLE Pass@4", "40.17%"],
            ["平均步数", "23"],
            ["代码/权重", "未发布"],
        ],
        "relations": [
            {"name": "Kimi-k1.5", "slug": "kimi-k1-5", "note": "同一条 RL  scaling 方法线"},
            {"name": "Kimi-K2", "slug": "kimi-k2", "note": "后续的 Agent 基座"},
        ],
        "caveats": [
            "仓库只有静态页面，不能直接复现实验。",
            "搜索类 benchmark 受工具、时间与数据污染影响大。",
            "结果基于内部模型版本，外部无法用同一 checkpoint 验证。",
        ],
    },
]
