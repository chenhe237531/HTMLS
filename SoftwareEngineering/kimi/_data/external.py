# -*- coding: utf-8 -*-
"""组织外但与 Kimi 服务直接相关的核心项目。

Mooncake 的 README 明确写着 “the serving platform for Kimi”，但仓库位于
kvcache-ai 组织，因此不混入 MoonshotAI 的 42 个官方仓库统计。
"""

META = {
    "Mooncake": {
        "name": "Mooncake",
        "full_name": "kvcache-ai/Mooncake",
        "description": "Mooncake is the serving platform for Kimi, a leading LLM service provided by Moonshot AI.",
        "html_url": "https://github.com/kvcache-ai/Mooncake",
        "homepage": "https://kvcache-ai.github.io/Mooncake/",
        "stargazers_count": 6945,
        "forks_count": 1414,
        "open_issues_count": 903,
        "language": "C++",
        "license": {"spdx_id": "Apache-2.0"},
        "created_at": "2024-06-25T05:21:05Z",
        "pushed_at": "2026-11-01T12:06:17Z",
        "archived": False,
        "external": True,
        "owner": "kvcache-ai",
    }
}

PROJECTS = [
    {
        "repo": "Mooncake",
        "slug": "mooncake",
        "title": "Mooncake",
        "category": "infra",
        "status": "external",
        "external": True,
        "owner": "kvcache-ai",
        "tagline": "Kimi 的以 KVCache 为中心的推理服务平台，FAST'25 最佳论文",
        "summary": "Mooncake 是 Kimi 的 serving platform，核心是 KVCache-centric 的解耦架构：把 prefill 与 decode 拆到不同集群，并把 GPU 集群里闲置的 CPU、DRAM、SSD 组织成分布式 KV cache 池。它包含 Transfer Engine、Store、EP/PG 等组件，已深度接入 vLLM、SGLang、TensorRT-LLM 等生态。",
        "points": [
            "KVCache-centric 解耦：prefill 与 decode 分离，KV cache 跨实例复用。",
            "官方称在真实负载下让 Kimi 多处理 75% 的请求且满足 SLO。",
            "Kimi-K2 在 128 张 H200 上达到 224k tokens/s prefill、288k tokens/s decode。",
            "FAST'25 最佳论文；Mooncake Store 已被 vLLM、SGLang 等采用。",
        ],
        "stats": [["6.9k", "Stars"], ["75%", "更多请求"], ["128", "H200 部署"], ["Apache-2.0", "许可证"]],
        "sections": [
            {
                "h": "架构：把 KV cache 当成一等公民",
                "html": "<p>传统推理把 prefill 与 decode 放在同一组 GPU 上，长上下文请求会让 KV cache 迅速吃满显存。Mooncake 的做法是把两者拆开：prefill 集群负责算 prompt，decode 集群负责逐 token 生成，中间通过高速网络搬运 KV cache。同时，它把 GPU 集群里未被充分利用的 CPU 内存、DRAM 与 SSD 组织成分布式缓存池，让 KV cache 可以跨请求、跨实例复用。</p><p>这带来两个直接收益：一是缓存命中时不必重复计算 prompt；二是 decode 集群的显存压力下降，可以承载更多并发。</p>",
            },
            {
                "h": "组件",
                "html": "<p><b>Transfer Engine</b>：面向异构网络与加速器的高性能数据传输层，支持 RDMA 等路径，是 KV cache 与权重搬运的基础。<b>Mooncake Store</b>：分布式 KV cache 与模型权重管理，提供内容寻址的缓存池。<b>Mooncake EP &amp; PG</b>：面向弹性 MoE 服务的专家并行与进程组能力。</p><p>这些组件不是绑死在 Kimi 内部：vLLM、SGLang、TensorRT-LLM、LMDeploy、LMCache、NIXL、Dynamo、llm-d 等都有集成；checkpoint-engine 的 P2P 权重同步也复用了 Mooncake Transfer Engine。</p>",
            },
            {
                "h": "实测与影响",
                "html": "<p>README 给出的关键数字：真实负载下 Kimi 多处理 75% 请求且满足 SLO；Kimi-K2 在 128 张 H200 上做 PD 解耦与大规模专家并行，达到 224k tokens/s prefill、288k tokens/s decode；SGLang 用 Mooncake TransferEngine 做 1T 参数 K2 的 P2P 权重更新，从 53 秒降到 7.2 秒。</p><p>它也是 Kimi 开源栈里少见的“系统论文 + 生产系统 + 多框架集成”三件套，影响超出 MoonshotAI 自身。</p>",
            },
        ],
        "specs": [
            ["类型", "LLM 推理服务平台"],
            ["核心架构", "KVCache-centric 解耦（PD 分离）"],
            ["主要组件", "Transfer Engine、Store、EP/PG"],
            ["代表部署", "Kimi-K2，128×H200"],
            ["论文", "FAST'25 Best Paper"],
            ["许可证", "Apache-2.0"],
        ],
        "quickstart": {
            "lang": "bash",
            "note": "Mooncake 以 C++/RDMA 为主，安装与部署请以官方文档为准；下面是 PyPI 包的入口。",
            "code": "# Transfer Engine 的 Python 包\npip install mooncake-transfer-engine\n\n# 文档与部署指南\n# https://kvcache-ai.github.io/Mooncake/",
        },
        "relations": [
            {"name": "checkpoint-engine", "slug": "checkpoint-engine", "note": "P2P 权重同步复用 Mooncake Transfer Engine"},
            {"name": "Kimi-K2", "slug": "kimi-k2", "note": "官方 128×H200 部署案例"},
            {"name": "Kimi-K3", "slug": "kimi-k3", "note": "后续旗舰模型的 serving 基础设施"},
            {"name": "MoonEP", "slug": "moonep", "note": "另一条 MoE 专家并行通信路线"},
        ],
        "caveats": [
            "仓库属于 kvcache-ai 组织，不是 MoonshotAI 官方仓库；本页单列为“组织外核心”。",
            "部署依赖 RDMA/高速网络与特定硬件，个人开发者很难完整复现。",
            "集成面很广、迭代很快，接口与版本兼容性要按所用框架确认。",
            "README 的 75% 数字来自特定真实负载与 SLO，不能直接套到你的业务。",
        ],
        "sources": [
            ("Mooncake 文档", "https://kvcache-ai.github.io/Mooncake/"),
            ("FAST'25 论文", "https://www.usenix.org/system/files/fast25-qin.pdf"),
        ],
    },
]
