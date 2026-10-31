#!/usr/bin/env python3
"""Build the skill-explainer series from _data/skills.json.

Usage:
    python3 build.py

Outputs:
    index.html
    p/<slug>.html   (17 pages, self-contained)
"""

from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "_data" / "skills.json"
TEMPLATES = ROOT / "_templates"
OUT = ROOT / "p"

STACK_LABEL = {"ronny": "ronny stack", "jiachen": "jiachen stack"}


def load() -> dict:
    with DATA.open(encoding="utf-8") as fh:
        return json.load(fh)


def fill(template: str, values: dict[str, str]) -> str:
    out = template
    for key, value in values.items():
        out = out.replace("{{" + key + "}}", value)
    leftover = re.findall(r"\{\{[A-Z_]+\}\}", out)
    if leftover:
        raise SystemExit(f"unfilled placeholders: {sorted(set(leftover))}")
    return out


def plain(value: str) -> str:
    text = re.sub(r"<[^>]+>", "", value)
    return html.escape(text, quote=True)


def search_blob(skill: dict, groups: dict[str, str]) -> str:
    parts = [
        skill["name"],
        skill["en"],
        skill["oneline"],
        skill["problem"],
        skill["apply"],
        skill["limits"],
        groups[skill["group"]],
        " ".join(skill["mechanism"]),
        " ".join(r["k"] + " " + r["v"] for r in skill["rules"]),
    ]
    return plain(" ".join(parts)).lower()


def render_page(skill: dict, data: dict, style: str, page_tpl: str,
                prev: dict | None, next_: dict | None, total: int) -> str:
    groups = {g["id"]: g["name"] for g in data["groups"]}
    related = {s["slug"]: s for s in data["skills"]}

    mechanism = "\n".join(f"      <li>{step}</li>" for step in skill["mechanism"])
    rules = "\n".join(
        f'      <div class="rule"><dt>{html.escape(r["k"])}</dt>'
        f'<dd>{r["v"]}</dd></div>'
        for r in skill["rules"]
    )

    related_html = []
    for slug in skill["related"]:
        other = related.get(slug)
        if not other:
            raise SystemExit(f"{skill['slug']}: unknown related slug {slug}")
        related_html.append(
            f'<a href="{other["slug"]}.html">'
            f'<span class="en">{html.escape(other["en"])}</span>'
            f'<span class="zh">{html.escape(other["name"])}</span>'
            f'<span class="one">{html.escape(other["oneline"])}</span>'
            f"</a>"
        )

    pager = []
    if prev:
        pager.append(
            f'<a href="{prev["slug"]}.html" rel="prev">← {html.escape(prev["name"])}</a>'
        )
    if next_:
        pager.append(
            f'<a href="{next_["slug"]}.html" rel="next">{html.escape(next_["name"])} →</a>'
        )

    note_pill = (
        f'<span class="pill">工程笔记 {html.escape(skill["note"])}</span>'
        if skill.get("note") else ""
    )

    return fill(page_tpl, {
        "STYLE": style,
        "NAME": html.escape(skill["name"]),
        "EN": html.escape(skill["en"]),
        "ONELINE": html.escape(skill["oneline"]),
        "GROUP": html.escape(groups[skill["group"]]),
        "GROUP_EN": html.escape(skill["group"]),
        "STACK": html.escape(skill["stack"]),
        "STACK_LABEL": html.escape(STACK_LABEL.get(skill["stack"], skill["stack"])),
        "ORDER": f'{skill["order"]:02d}',
        "TOTAL": str(total),
        "NOTE_PILL": note_pill,
        "PROBLEM": f'<p>{skill["problem"]}</p>',
        "MECHANISM": mechanism,
        "RULES": rules,
        "QUOTE": html.escape(skill["quote"]),
        "APPLY": f'<p>{skill["apply"]}</p>',
        "LIMITS": f'<p>{skill["limits"]}</p>',
        "RELATED": "\n".join(related_html),
        "PAGER": "\n    ".join(pager),
        "SOURCE": html.escape(skill["source"], quote=True),
    })


def render_index(data: dict, style: str, index_tpl: str, build_date: str) -> str:
    groups = {g["id"]: g for g in data["groups"]}
    skills = sorted(data["skills"], key=lambda s: s["order"])

    cards = []
    for s in skills:
        cards.append(
            f'<a class="card" href="p/{s["slug"]}.html" '
            f'data-group="{s["group"]}" data-text="{search_blob(s, {k: v["name"] for k, v in groups.items()})}">'
            f'<span class="card-top"><span class="en">{html.escape(s["en"])}</span>'
            f'<span class="no">{s["order"]:02d}</span></span>'
            f'<span class="zh">{html.escape(s["name"])}</span>'
            f'<p>{html.escape(s["oneline"])}</p>'
            f'<span class="tag">{html.escape(groups[s["group"]]["name"])} · {html.escape(s["stack"])}</span>'
            f"</a>"
        )

    paths = []
    by_slug = {s["slug"]: s for s in skills}
    for path in data["paths"]:
        items = []
        for slug in path["items"]:
            item = by_slug[slug]
            items.append(
                f'<li><a href="p/{slug}.html">{html.escape(item["name"])}</a></li>'
            )
        paths.append(
            f'<div class="path"><h3>{html.escape(path["name"])}</h3>'
            f'<p class="why">{html.escape(path["why"])}</p>'
            f'<ol>{"".join(items)}</ol></div>'
        )

    chips = "\n        ".join(
        f'<button class="chip" type="button" data-filter="{g["id"]}" '
        f'aria-pressed="false">{html.escape(g["name"])}</button>'
        for g in data["groups"]
    )

    credits = "\n      ".join(
        f'<div class="card"><h3>{html.escape(c["title"])}</h3>'
        f'<p>{html.escape(c["body"])}</p></div>'
        for c in data["credits"]
    )

    return fill(index_tpl, {
        "STYLE": style,
        "CARDS": "\n      ".join(cards),
        "PATHS": "\n      ".join(paths),
        "CHIPS": chips,
        "CREDITS": credits,
        "TOTAL": str(len(skills)),
        "BUILT": html.escape(build_date),
    })


def main() -> int:
    data = load()
    style = (TEMPLATES / "style.css").read_text(encoding="utf-8")
    page_tpl = (TEMPLATES / "page.html").read_text(encoding="utf-8")
    index_tpl = (TEMPLATES / "index.html").read_text(encoding="utf-8")

    skills = sorted(data["skills"], key=lambda s: s["order"])
    slugs = [s["slug"] for s in skills]
    if len(set(slugs)) != len(slugs):
        raise SystemExit("duplicate slug in skills.json")
    orders = [s["order"] for s in skills]
    if orders != list(range(1, len(skills) + 1)):
        raise SystemExit(f"order must be 1..N, got {orders}")

    OUT.mkdir(exist_ok=True)
    for i, skill in enumerate(skills):
        prev = skills[i - 1] if i > 0 else None
        nxt = skills[i + 1] if i + 1 < len(skills) else None
        page = render_page(skill, data, style, page_tpl, prev, nxt, len(skills))
        (OUT / f"{skill['slug']}.html").write_text(page, encoding="utf-8")

    index = render_index(data, style, index_tpl, data["meta"]["built"])
    (ROOT / "index.html").write_text(index, encoding="utf-8")

    print(f"built index.html + {len(skills)} pages in {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
