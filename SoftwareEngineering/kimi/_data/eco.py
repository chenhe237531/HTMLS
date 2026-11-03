# -*- coding: utf-8 -*-
"""生态、组织基建与 K3 演示类项目。"""

PROJECTS = [
    {
        "repo": "moonpalace",
        "slug": "moonpalace",
        "title": "MoonPalace（月宫）",
        "category": "eco",
        "status": "active",
        "tagline": "把 base_url 指向 localhost:9988，就能抓 Kimi API 的完整请求",
        "summary": "MoonPalace 是 Moonshot AI 提供的 API 调试代理：启动后把代码里的 base_url 换成 http://localhost:9988，它就会捕获完整请求，包括网络错误时的现场；支持按 request_id / chatcmpl_id 检索、按 predicate 筛选、一键导出 BadCase。",
        "points": [
            "全平台：macOS、Windows、Linux。",
            "捕获完整请求体，网络错误也能留下现场。",
            "按 request_id、chatcmpl_id 快速检索。",
            "导出结构化 BadCase，方便反馈给 Moonshot 改进模型。",
        ],
        "stats": [["9988", "本地端口"], ["Go", "实现"], ["3", "平台"], ["GPL-3.0", "许可证"]],
        "sections": [
            {
                "h": "解决什么调试痛点",
                "html": "<p>调 API 时最常见的问题是“模型输出不符合预期，但不知道请求到底发了什么”。MoonPalace 作为本地代理，把每次请求完整落盘，并提供自动缓存、内容截断检测、重复内容输出检测。你可以按 id 找回某次请求，也可以按条件筛出一批相似请求。</p>",
            },
            {
                "h": "使用方式",
                "html": "<p>用 <code>go install github.com/MoonshotAI/moonpalace@latest</code> 安装，或从 Releases 下载二进制；启动后改 base_url 即可。配置文件 <code>config.yaml</code> 可调缓存与检测行为；导出命令支持 id / chatcmpl / requestid 任选其一。</p>",
            },
        ],
        "specs": [
            ["类型", "API 调试代理"],
            ["语言", "Go"],
            ["默认端口", "9988"],
            ["许可证", "GPL-3.0"],
        ],
        "relations": [
            {"name": "Kimi-K2", "slug": "kimi-k2", "note": "常被调试的模型"},
            {"name": "Kimi-Vendor-Verifier", "slug": "kimi-vendor-verifier", "note": "供应商侧的质量验证"},
        ],
        "caveats": [
            "GPL-3.0：把代码集成进闭源产品前要确认许可证影响。",
            "本地代理会看到完整请求内容，注意敏感数据。",
            "最后更新在 2024-12，新 API 特性可能未覆盖。",
        ],
    },
    {
        "repo": "awesome-moonshot-api",
        "slug": "awesome-moonshot-api",
        "title": "awesome-moonshot-api",
        "category": "eco",
        "status": "active",
        "tagline": "Moonshot API 生态项目清单",
        "summary": "一份 curated list，收录与 Moonshot API 相关的开源项目：Kimi Copilot 浏览器扩展、LangChain、LlamaIndex、Dify、LobeChat、OpenAI Translator、HuixiangDou、Koishi、NoneBot 等。",
        "points": [
            "覆盖浏览器插件、Agent 框架、聊天 UI、RAG、机器人框架。",
            "列表很短，适合快速找集成入口。",
            "最后更新 2024-05，之后的新项目未收录。",
            "收录不代表官方背书。",
        ],
        "stats": [["41", "Stars"], ["2024-05", "最后更新"], ["清单", "类型"], ["未声明", "许可证"]],
        "sections": [
            {
                "h": "怎么用",
                "html": "<p>把它当作“从 Moonshot API 出发能接哪些生态”的索引，而不是完整目录。比如要在聊天软件里接 Kimi，可以看 Koishi / NoneBot；要做 RAG，可以看 LangChain / LlamaIndex；要做桌面 Chat UI，可以看 LobeChat / ChatHub。</p>",
            },
            {
                "h": "时效性提醒",
                "html": "<p>仓库最后 push 在 2024-05，Kimi 的 API 与模型此后更新了很多代。清单里的项目可能已经支持新模型，也可能停更；使用前逐个确认。</p>",
            },
        ],
        "specs": [
            ["类型", "Awesome 清单"],
            ["最后更新", "2024-05"],
            ["许可证", "仓库未声明"],
        ],
        "relations": [
            {"name": "MoonshotAI-Cookbook", "slug": "moonshotai-cookbook", "note": "官方示例代码"},
            {"name": "koishi-plugin-moonshot-api", "slug": "koishi-plugin-moonshot-api", "note": "清单中的机器人集成"},
        ],
        "caveats": [
            "久未更新，不能当作当前生态全貌。",
            "收录不等于质量或安全背书。",
            "无许可证声明。",
        ],
    },
    {
        "repo": "MoonshotAI-Cookbook",
        "slug": "moonshotai-cookbook",
        "title": "MoonshotAI Cookbook",
        "category": "eco",
        "status": "active",
        "tagline": "Moonshot API 的示例代码与指南",
        "summary": "官方 Cookbook：用 Python 示例演示 Moonshot API 的常见任务。需要 Moonshot 账号与 API key；README 很短，内容以仓库里的 notebook/脚本为主。",
        "points": [
            "Python 为主的 API 示例。",
            "覆盖常见任务，概念可迁移到其他语言。",
            "需要账号与 API key 才能运行。",
            "仓库内容较薄，更新不频繁。",
        ],
        "stats": [["20", "Stars"], ["Python", "示例"], ["API", "主题"], ["未声明", "许可证"]],
        "sections": [
            {
                "h": "定位",
                "html": "<p>它更像“官方示例集合”而不是系统教程。适合在接入 Moonshot API 时找最小可运行样例；如果要看完整 API 参考，应查 platform.moonshot.cn 的文档。</p>",
            },
        ],
        "specs": [
            ["类型", "示例代码"],
            ["语言", "Python"],
            ["许可证", "仓库未声明"],
        ],
        "relations": [
            {"name": "awesome-moonshot-api", "slug": "awesome-moonshot-api", "note": "生态项目清单"},
            {"name": "Kimi-K2", "slug": "kimi-k2", "note": "可调用的模型"},
        ],
        "caveats": [
            "示例可能随 API 版本过时。",
            "无许可证声明，复用代码前需确认。",
            "README 信息量很少，主要靠浏览仓库文件。",
        ],
    },
    {
        "repo": "koishi-plugin-moonshot-api",
        "slug": "koishi-plugin-moonshot-api",
        "title": "koishi-plugin-moonshot-api",
        "category": "eco",
        "status": "active",
        "tagline": "Koishi 聊天机器人的官方 Moonshot API 插件",
        "summary": "Koishi 是跨平台聊天机器人框架；这个插件把 Moonshot API 接进 Koishi。仓库创建于 2024-03，之后没有更新，README 只有一句介绍。",
        "points": [
            "官方 Moonshot API 的 Koishi 适配。",
            "适合在 QQ/Discord/Telegram 等聊天平台接 Kimi。",
            "创建后未再更新。",
            "文档几乎为零，需要看源码或 Koishi 插件机制。",
        ],
        "stats": [["2024-03", "创建"], ["Koishi", "框架"], ["官方", "标签"], ["MIT", "许可证"]],
        "sections": [
            {
                "h": "使用判断",
                "html": "<p>如果你已经在用 Koishi，这是最直接的官方入口；但仓库长期未更新，可能不支持新模型或新 API 特性。新项目可以优先评估社区增强版或直接用官方 SDK 自己写适配。</p>",
            },
        ],
        "specs": [
            ["类型", "Koishi 插件"],
            ["许可证", "MIT"],
            ["维护状态", "2024-03 后未更新"],
        ],
        "relations": [
            {"name": "koishi-plugin-moonshot-api-plus", "slug": "koishi-plugin-moonshot-api-plus", "note": "社区增强版"},
            {"name": "awesome-moonshot-api", "slug": "awesome-moonshot-api", "note": "生态清单"},
        ],
        "caveats": [
            "长期未更新，API 兼容性未知。",
            "README 信息不足，接入前需读源码。",
            "聊天机器人场景要注意限流与内容安全。",
        ],
    },
    {
        "repo": "koishi-plugin-moonshot-api-plus",
        "slug": "koishi-plugin-moonshot-api-plus",
        "title": "koishi-plugin-moonshot-api-plus",
        "category": "eco",
        "status": "active",
        "tagline": "Koishi 的社区增强版 Moonshot API 插件",
        "summary": "koishi-plugin-moonshot-api 的社区增强版，发布在 npm。README 只有一个 npm 徽章，没有使用说明；仓库创建于 2024-03，之后未更新。",
        "points": [
            "npm 包可直接安装。",
            "定位为官方插件的增强版。",
            "几乎没有文档。",
            "2024-03 后未更新。",
        ],
        "stats": [["5", "Stars"], ["npm", "分发"], ["2024-03", "创建"], ["未声明", "许可证"]],
        "sections": [
            {
                "h": "风险提示",
                "html": "<p>这是本次盘点里信息最少的项目之一：README 只有徽章，没有配置示例、兼容性说明或变更记录。除非你愿意读源码并自行测试，否则不建议把它作为生产依赖。</p>",
            },
        ],
        "specs": [
            ["类型", "Koishi 插件"],
            ["分发", "npm"],
            ["维护状态", "2024-03 后未更新"],
        ],
        "relations": [
            {"name": "koishi-plugin-moonshot-api", "slug": "koishi-plugin-moonshot-api", "note": "官方基础版"},
        ],
        "caveats": [
            "文档缺失，接入成本高。",
            "长期未更新，API 兼容性未知。",
            "无许可证声明。",
        ],
    },
    {
        "repo": "Branding-Guide",
        "slug": "branding-guide",
        "title": "Kimi Branding Guide",
        "category": "eco",
        "status": "active",
        "tagline": "Kimi 品牌视觉规范页",
        "summary": "一个单页 HTML，展示 Kimi 的 logo、配色与不同场景下的品牌使用示例。它不是代码库，也不是设计系统文档，更像对外公开的品牌规范页面。",
        "points": [
            "单文件 HTML，包含 logo 与场景示例。",
            "定义基础色、字体与留白。",
            "适合做二次创作或集成时参考。",
            "仓库无 LICENSE。",
        ],
        "stats": [["HTML", "形式"], ["品牌", "主题"], ["2025-12", "创建"], ["未声明", "许可证"]],
        "sections": [
            {
                "h": "内容",
                "html": "<p>页面分为 header、scenarios 等区块，用 Kimi logo 与不同背景展示品牌在浅色/深色场景下的用法。它没有提供可下载的设计 token 或组件库，实际落地仍要自己提取颜色与间距。</p>",
            },
        ],
        "specs": [
            ["类型", "品牌规范页"],
            ["形式", "单页 HTML"],
            ["许可证", "仓库未声明"],
        ],
        "relations": [
            {"name": "moonshotai.github.io", "slug": "moonshotai-github-io", "note": "组织 Pages 跳转页"},
        ],
        "caveats": [
            "品牌资产的使用受商标/版权约束，不能仅凭仓库无 LICENSE 就随意商用。",
            "没有设计 token 或组件代码。",
        ],
    },
    {
        "repo": "moonshotai.github.io",
        "slug": "moonshotai-github-io",
        "title": "moonshotai.github.io",
        "category": "eco",
        "status": "meta",
        "tagline": "组织 GitHub Pages 的跳转页（CombiBench 例外）",
        "summary": "这是 MoonshotAI 组织的 GitHub Pages 根域。它把访问者重定向到 moonshot.cn，但保留 CombiBench 相关路径，用于让 CombiBench 的 leaderboard 继续可访问。",
        "points": [
            "根域重定向到 https://www.moonshot.cn/。",
            "CombiBench 的 http/https 路径被列入例外，不跳转。",
            "仓库只有一个 index.html。",
            "不是文档站。",
        ],
        "stats": [["HTML", "形式"], ["跳转", "行为"], ["1", "文件"], ["未声明", "许可证"]],
        "sections": [
            {
                "h": "为什么存在",
                "html": "<p>GitHub Pages 的组织根域只能指向一个仓库。MoonshotAI 用它做统一跳转，同时给 CombiBench 的 leaderboard 留了例外路径。真正的产品文档在 kimi-code 的 Pages（moonshotai.github.io/kimi-code）。</p>",
            },
        ],
        "specs": [
            ["类型", "Pages 跳转页"],
            ["目标", "moonshot.cn"],
            ["例外", "CombiBench"],
        ],
        "relations": [
            {"name": "CombiBench", "slug": "combibench", "note": "被保留的例外路径"},
            {"name": "Branding-Guide", "slug": "branding-guide", "note": "另一个单页站点"},
        ],
        "caveats": [
            "没有可复用的文档内容。",
            "跳转行为依赖 JS，禁用 JS 时只显示链接。",
        ],
    },
    {
        "repo": ".github",
        "slug": "github-org",
        "title": "MoonshotAI/.github",
        "category": "eco",
        "status": "meta",
        "tagline": "组织级 GitHub 配置与 profile",
        "summary": "MoonshotAI 组织的特殊仓库：存放 profile README、组织级 LICENSE 与 .gitignore。它不包含产品代码，但决定了组织主页展示什么。",
        "points": [
            "profile/ 目录放组织主页 README。",
            "组织级 LICENSE 为 GPL-3.0。",
            "没有产品代码。",
            "用于统一组织元数据。",
        ],
        "stats": [["2", "Stars"], ["profile", "内容"], ["GPL-3.0", "组织许可"], ["—", "产品代码"]],
        "sections": [
            {
                "h": "它影响什么",
                "html": "<p>GitHub 会把 <code>.github/profile/README.md</code> 渲染成组织主页。这个仓库还放了组织级 LICENSE 与 .gitignore，属于“门面与默认配置”，不是可运行项目。</p>",
            },
        ],
        "specs": [
            ["类型", "组织元数据"],
            ["关键内容", "profile README、LICENSE"],
            ["许可证", "GPL-3.0"],
        ],
        "relations": [
            {"name": "moonshotai.github.io", "slug": "moonshotai-github-io", "note": "组织 Pages"},
        ],
        "caveats": [
            "没有产品代码，不需要单独评估技术能力。",
            "组织级 GPL-3.0 不自动适用于其他仓库，各仓库许可以各自 LICENSE 为准。",
        ],
    },
    {
        "repo": "nano-kpu",
        "slug": "nano-kpu",
        "title": "nano-kpu",
        "category": "architecture",
        "status": "demo",
        "tagline": "Kimi K3 自己设计的一颗纳米级推理芯片 RTL",
        "summary": "nano-kpu 是一颗混合注意力 MoE Transformer 推理芯片的 RTL 设计，完全由 Kimi K3 完成：KDA 线性注意力、NoPE MLA、sigmoid 路由 MoE（top-2 + 1 共享专家）、Attention Residual mixing，int4 group-128 权重，逐 token 解码。",
        "points": [
            "KDA + NoPE MLA + MoE + AttnRes 的硬件实现。",
            "int4 group-128 权重，teacher-forced 逐 token 解码。",
            "Verilator 功能仿真 + yosys/Nangate45 面积/时序评估。",
            "官方声明：这是 K3 能力演示，不是 Moonshot 官方产品。",
        ],
        "stats": [["RTL", "交付物"], ["int4", "权重"], ["KDA+MLA", "注意力"], ["Apache-2.0", "许可证"]],
        "sections": [
            {
                "h": "它包含什么",
                "html": "<p>仓库分四块：<code>rtl/</code> 是芯片 RTL（顶层 msh_chip_top），<code>reference/</code> 是 float32 黄金参考模型，<code>harness/</code> 是功能仿真与性能评估流程（Verilator testbench、SRAM/ROM 宏模型、yosys 综合脚本），<code>docs/</code> 是架构、接口、内存映射、量化与任务规格。</p>",
            },
            {
                "h": "怎么验证",
                "html": "<p>运行 <code>bash scripts/setup_env.sh</code> 创建 conda 环境（Verilator 5.x、yosys ≥0.64、Python 3.12），再 source 环境脚本。Nangate45 标准单元库不随仓库分发，而是在 setup 时从 OpenROAD-flow-scripts 按 commit 与 SHA-256 下载。之后用 Makefile 跑功能仿真与综合。</p>",
            },
        ],
        "specs": [
            ["类型", "芯片 RTL 演示"],
            ["模型", "KDA + NoPE MLA + MoE + AttnRes"],
            ["量化", "int4 group-128"],
            ["工具链", "Verilator、yosys、Nangate45"],
            ["许可证", "Apache-2.0"],
        ],
        "relations": [
            {"name": "Kimi-K3", "slug": "kimi-k3", "note": "设计与实现者"},
            {"name": "Kimi-Linear", "slug": "kimi-linear", "note": "KDA 来源"},
            {"name": "Attention-Residuals", "slug": "attention-residuals", "note": "AttnRes 来源"},
            {"name": "minitriton", "slug": "minitriton", "note": "同批 K3 演示项目"},
        ],
        "caveats": [
            "演示项目，不代表可流片或可量产。",
            "需要网络下载工具链与单元库，环境搭建较重。",
            "面积/时序数字依赖 Nangate45 与综合脚本，不能直接对标先进工艺。",
        ],
    },
    {
        "repo": "minitriton",
        "slug": "minitriton",
        "title": "MiniTriton",
        "category": "architecture",
        "status": "demo",
        "tagline": "Kimi K3 从零写的教学级 tile 编译器",
        "summary": "MiniTriton 是一个教学级但工程完整的 tile 编译器：Python 内嵌 tile DSL 经 MLIR 降到 PTX，在 NVIDIA GPU 上运行；上面还有 eager tensor / autograd / nn 库。flash attention、KDA 等应用 kernel 全部用 DSL 写，编译器本身只提供 tile 级原语。",
        "points": [
            "DSL → AST → MLIR → PTX 的完整编译链。",
            "附带 eager 执行与 tile 级编译统一的 tensor 库。",
            "所有应用 kernel 用 DSL 实现，不内置应用专用 intrinsic。",
            "由 Kimi K3 设计、实现、测量与写文档，官方声明非生产可用。",
        ],
        "stats": [["K3", "作者"], ["MLIR→PTX", "编译链"], ["DSL", "kernel"], ["Apache-2.0", "许可证"]],
        "sections": [
            {
                "h": "为什么值得看",
                "html": "<p>大多数“教学编译器”止步于 toy language；MiniTriton 把 flash attention、KDA 这类真实 kernel 用自家 DSL 写出来，并用 roofline、训练收敛等基准与 torch、torch.compile、Triton 对比。它的价值不是替代 Triton，而是展示一个 Agent 能否独立完成从 DSL 前端到 PTX 后端的全栈。</p>",
            },
            {
                "h": "结构",
                "html": "<p><code>minitriton/frontend/</code> 做 DSL → AST，<code>minitriton/compiler/</code> 做 builder → passes → PTX lowering，<code>tests/</code> 是可执行规格；<code>examples/</code> 从 vecadd、matmul 到 train_gpt 展示 API；<code>benchmarks/</code> 生成 roofline 与训练收敛图。</p>",
            },
            {
                "h": "边界",
                "html": "<p>README 明确列出 Limitations，并说明唯一“可表达性例外”是通用线性代数原语 <code>tl.solve_tril</code>。性能图里既有赢也有输，官方没有只挑好看的。它适合学习编译器与 GPU kernel，不适合生产部署。</p>",
            },
        ],
        "specs": [
            ["类型", "教学级 tile 编译器"],
            ["编译链", "Python DSL → MLIR → PTX"],
            ["附带", "eager tensor / autograd / nn"],
            ["作者", "Kimi K3"],
            ["许可证", "Apache-2.0"],
        ],
        "relations": [
            {"name": "Kimi-K3", "slug": "kimi-k3", "note": "作者模型"},
            {"name": "FlashKDA", "slug": "flashkda", "note": "生产级 KDA kernel"},
            {"name": "nano-kpu", "slug": "nano-kpu", "note": "同批 K3 演示项目"},
        ],
        "caveats": [
            "官方明确说非 Moonshot 产品、非生产可用。",
            "性能有胜有负，不能当作 Triton 的替代。",
            "需要 NVIDIA GPU、MLIR/LLVM 工具链，构建复杂。",
            "Limitations 里列出的缺口要逐个确认。",
        ],
    },
]
