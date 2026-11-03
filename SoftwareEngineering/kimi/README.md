# Kimi 开源图谱

MoonshotAI（Kimi）组织 42 个公开仓库的逐项分析，另加组织外核心项目 Mooncake。`index.html` 是索引，每个项目一个独立 HTML。

- 数据快照：2026-11-01（GitHub REST API + 各仓库 README）
- 覆盖：42 / 42 个 MoonshotAI 公开仓库 + 1 个组织外核心（Mooncake），含 1 个归档（kimi-cli）、2 个已迁移（kosong、pykaos）、3 个组织/站点类仓库
- 分类：基础模型 9、架构与研究 4、Agent 与开发工具 9、训练与推理基础设施 6、评测与基准 7、生态与组织 8
- 约定：每个页面自包含、无 CDN、可离线打开；事实与编辑判断分开标注

## 文件

| 文件 | 内容 |
| --- | --- |
| `index.html` | 索引：分层读法、四条技术主线、搜索/筛选/排序、时间线、方法与来源 |
| `kimi-k3.html` 等 43 个页面 | 每个项目的定位、架构/机制、关键规格、快速开始、生态关系、边界与来源（42 个官方 + `mooncake.html`） |

命名规则：仓库名小写、点号转连字符（如 `Kimi-K2.5` → `kimi-k2-5.html`，`.github` → `github-org.html`）。

## 重新生成

```bash
cd SoftwareEngineering/kimi
python3 build.py
```

内容在 `_data/`：

- `repos.json`：GitHub API 元数据快照
- `models.py`、`agents.py`、`infra_eval.py`、`eco.py`：42 个官方仓库的中文分析与页面数据
- `external.py`：组织外核心项目 Mooncake 的数据与元数据
- `build.py`：模板、CSS、交互与校验

## 校验

```bash
for f in *.html; do
  python3 ~/.agents/skills/building-interactive-html-docs/scripts/verify_single_html.py "$PWD/$f"
done
```

## 说明

- Stars、Forks、日期会变化；页面上的数字是 2026-11-01 的快照。
- 分类与“生态关系”“边界与注意”是编辑判断，不是官方依赖声明或选型建议。
- 许可证以各仓库 `LICENSE` / README 为准；未声明许可证的项目已在页面标注。
- Mooncake 位于 kvcache-ai 组织，因 README 明确写为 Kimi 的 serving platform 而单列；它不计入 42 个官方仓库统计。其他外部依赖（Kimina Lean Server、flash-linear-attention）只在相关页面提及。
