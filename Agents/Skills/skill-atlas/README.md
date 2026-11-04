# Skill Atlas · AI 编程技能解析

对 [MiniMax-AI/mcode-stack](https://github.com/MiniMax-AI/mcode-stack) 里 17 个 Skill 的中文逐篇拆解。每篇结构固定：它治什么病、机制、规则要点（附英文原句）、能落到哪个场景、什么时候不该用、和谁配套。

- 入口：`index.html`（离线可开，含 4 条阅读路径、按场景筛选、按 `/` 搜索）
- 正文：`p/<slug>.html`，共 17 篇

## 结构

```text
skill-atlas/
├─ index.html            生成物：系列封面
├─ p/                    生成物：17 篇
├─ build.py              生成器
├─ _data/skills.json     唯一事实来源
├─ _templates/
│  ├─ style.css          共用样式（内联进每个页面）
│  ├─ page.html          单篇模板
│  └─ index.html         封面模板
├─ LICENSE               MIT
├─ NOTICE.md             上游与改编部分的许可说明
└─ README.md
```

## 改内容

只改 `_data/skills.json`，然后重新生成：

```bash
python3 build.py
```

字段：

| 字段 | 用途 |
| --- | --- |
| `slug` / `en` | 文件名与英文技能名，必须与上游目录名一致 |
| `name` | 中文标题 |
| `stack` / `group` / `order` | 归属、筛选分组、篇目顺序（必须是 1..17） |
| `oneline` | 一句话结论，同时用于卡片与 meta description |
| `problem` | 失败场景，具体到能认出来 |
| `mechanism` | 步骤数组，按顺序渲染成编号流程 |
| `rules` | `{k, v}` 数组，`k` 是短语，`v` 是规则 |
| `quote` | 一句英文原句，折叠展示 |
| `apply` / `limits` | 落到本仓库场景的用法与反例 |
| `related` | 3 个相关 slug，必须存在 |
| `note` | 对应《MCode 工程笔记》期号，可为 null |
| `source` | 上游 SKILL.md 链接 |

## 校验

```bash
python3 ~/.agents/skills/building-interactive-html-docs/scripts/verify_single_html.py "$PWD/index.html"
```

每个页面均为单文件：CSS/JS 内联，无 CDN、无网络请求、无相对资源依赖；页面之间的链接只用于导航。

## 许可与出处

- `engineering-*` 六个技能改编自 Google Engineering Practices Documentation，改编部分 CC-BY 3.0。
- 其余技能以 MIT 发布；`making-content`、`lifting-loops` 的原始版本在 `yujiachen-y/dotfiles`。
- 本目录可独立上传：生成物、模板与数据都在同一层，`build.py` 以自身目录为根。
本目录是二次解读，不是原文替代品。修改或引用请回到上游核对。
