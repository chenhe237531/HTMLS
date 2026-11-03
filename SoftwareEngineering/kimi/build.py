# -*- coding: utf-8 -*-
"""生成 Kimi 开源图谱：一个索引页 + 每个仓库一个单文件 HTML。

数据来源：GitHub API（2026-11-01 快照）+ 各仓库 README。
运行：python3 build.py
"""

import html
import json
import os
import re
import sys
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE, "_data"))

import models
import agents
import infra_eval
import eco
import external

PROJECTS = models.PROJECTS + agents.PROJECTS + infra_eval.PROJECTS + eco.PROJECTS + external.PROJECTS

CATEGORY_LABELS = {
    "model": "基础模型",
    "architecture": "架构与研究",
    "agent": "Agent 与开发工具",
    "infra": "训练与推理基础设施",
    "eval": "评测与基准",
    "eco": "生态与组织",
}

STATUS_LABELS = {
    "active": "活跃",
    "archived": "已归档",
    "research": "研究发布",
    "moved": "已迁移",
    "demo": "演示项目",
    "meta": "组织基建",
    "external": "外部核心",
}

LICENSE_OVERRIDES = {
    "Kimi-K2": "Modified MIT",
    "Kimi-K2.5": "Modified MIT",
    "Kimi-K3": "Kimi K3 License",
    "Kimi-Dev": "未声明",
    "Kimi-Audio": "MIT + Apache-2.0（混合）",
}

CATEGORY_ORDER = ["model", "architecture", "agent", "infra", "eval", "eco"]


def esc(s):
    return html.escape(str(s), quote=True)


def fmt_num(n):
    if n >= 10000:
        return f"{n / 1000:.1f}k"
    if n >= 1000:
        return f"{n / 1000:.1f}k"
    return str(n)


def fmt_date(s):
    return (s or "")[:10]


def license_of(p, meta):
    if p["repo"] in LICENSE_OVERRIDES:
        return LICENSE_OVERRIDES[p["repo"]]
    lic = (meta.get("license") or {}).get("spdx_id") if meta.get("license") else None
    if not lic or lic in ("NOASSERTION", "NONE"):
        return "未声明"
    return lic


def load_meta():
    with open(os.path.join(BASE, "_data", "repos.json"), encoding="utf-8") as f:
        rows = json.load(f)
    return {r["name"]: r for r in rows}


CSS = r"""
:root{
  --bg:#f3f4ef; --panel:#ffffff; --ink:#15181c; --muted:#626a74;
  --line:#e1e3dd; --line-strong:#c9cdc4;
  --accent:#0c6b5c; --accent-2:#0a4f45; --accent-soft:#e2f1ec;
  --lime:#c9f24d; --lime-soft:#f2fad4;
  --warn:#8a5a00; --warn-soft:#fbf0d8;
  --bad:#9c2f25; --bad-soft:#f9e7e4;
  --blue:#245c9c; --blue-soft:#e7f0fa;
  --radius:12px;
  --mono:ui-monospace,SFMono-Regular,"SF Mono",Menlo,Consolas,"Liberation Mono",monospace;
  --sans:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);font-size:15px;line-height:1.72;-webkit-font-smoothing:antialiased}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}
code{font-family:var(--mono);font-size:.88em;background:#edf0ea;padding:.12em .38em;border-radius:4px;word-break:break-word}
h1,h2,h3{line-height:1.3;letter-spacing:-.015em}
h2{font-size:22px;margin:0 0 8px}
h3{font-size:16px;margin:20px 0 6px}
p{margin:8px 0}
ul,ol{margin:8px 0;padding-left:22px}
li{margin:5px 0}
hr{border:0;border-top:1px solid var(--line);margin:26px 0}
.wrap{max-width:1160px;margin:0 auto;padding:0 22px}
.skip{position:absolute;left:-9999px;top:0;background:#fff;padding:8px 12px;z-index:100}
.skip:focus{left:8px;top:8px}

.topbar{background:#0e1417;color:#dfe7e3;border-bottom:1px solid #1f2a2c}
.topbar .wrap{display:flex;align-items:center;justify-content:space-between;gap:16px;min-height:56px;flex-wrap:wrap}
.brand{display:flex;align-items:center;gap:10px;color:#fff;font-weight:700;letter-spacing:.01em}
.brand:hover{text-decoration:none}
.brand .mark{display:inline-grid;place-items:center;width:26px;height:26px;border-radius:7px;background:var(--lime);color:#102018;font-size:14px;font-weight:800}
.topnav{display:flex;gap:16px;font-size:13.5px;flex-wrap:wrap}
.topnav a{color:#b9c7c2}
.topnav a:hover{color:#fff;text-decoration:none}

.hero{background:linear-gradient(180deg,#0d1316 0%,#122024 100%);color:#eef3f0;padding:46px 0 40px;position:relative;overflow:hidden}
.hero:after{content:"";position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.035) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.035) 1px,transparent 1px);background-size:34px 34px;pointer-events:none}
.hero .wrap{position:relative;z-index:1}
.kicker{font-size:11.5px;letter-spacing:.16em;text-transform:uppercase;color:#8fa8a0}
.hero h1{font-size:38px;margin:10px 0 10px;color:#fff;letter-spacing:-.03em}
.hero .lede{color:#b7c6c1;max-width:820px;font-size:16px;margin:0}
.hero .meta{display:flex;flex-wrap:wrap;gap:8px;margin-top:18px}
.chip{display:inline-flex;align-items:center;gap:6px;font-size:12.5px;padding:5px 10px;border-radius:999px;background:rgba(255,255,255,.075);color:#d6e2de;border:1px solid rgba(255,255,255,.13)}
.chip b{color:#fff;font-weight:650}
.chip.lime{background:rgba(201,242,77,.13);border-color:rgba(201,242,77,.32);color:#e6f7b5}

.statrow{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:26px}
.stat{background:rgba(255,255,255,.055);border:1px solid rgba(255,255,255,.11);border-radius:10px;padding:14px 16px}
.stat b{display:block;font-size:25px;color:#fff;line-height:1.15;letter-spacing:-.02em}
.stat span{font-size:12px;color:#9fb2ac}

.layout{display:grid;grid-template-columns:224px minmax(0,1fr);gap:34px;align-items:start;padding:30px 0 64px}
nav.toc{position:sticky;top:18px;font-size:13.5px}
nav.toc .toc-title{font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin:0 0 8px 10px}
nav.toc a{display:block;padding:7px 10px;border-radius:7px;color:var(--muted);border-left:2px solid transparent;line-height:1.45}
nav.toc a:hover{background:#e9ece5;color:var(--ink);text-decoration:none}
nav.toc a.active{background:var(--accent-soft);color:var(--accent);border-left-color:var(--accent);font-weight:650}
.toc-note{margin:14px 10px 0;font-size:12px;color:var(--muted);line-height:1.55}

main{min-width:0}
section{background:var(--panel);border:1px solid var(--line);border-radius:var(--radius);padding:24px 26px;margin-bottom:18px;scroll-margin-top:16px}
section > .sec-head{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap;margin-bottom:4px}
.sec-num{font-family:var(--mono);font-size:12px;color:var(--accent);background:var(--accent-soft);padding:2px 7px;border-radius:5px}
.lede{color:var(--muted);margin:2px 0 14px}

.callout{border-radius:9px;padding:12px 14px;margin:14px 0;border:1px solid;font-size:14px}
.callout.ok{background:#e8f5ee;border-color:#bfe3cd;color:#0d4f2a}
.callout.warn{background:var(--warn-soft);border-color:#eed7a8;color:#6b4200}
.callout.info{background:var(--blue-soft);border-color:#c6dbf2;color:#173f6d}
.callout b{font-weight:700}

.grid2{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.card{border:1px solid var(--line);border-radius:9px;padding:14px 16px;background:#fbfcf9}
.card h3{margin:0 0 6px;font-size:15px}
.card p{margin:4px 0;color:var(--muted);font-size:13.8px}
.card .num{font-family:var(--mono);font-size:11.5px;color:var(--accent);letter-spacing:.04em}

.points{list-style:none;padding:0;margin:10px 0 0;display:grid;gap:8px}
.points li{position:relative;padding-left:24px;margin:0}
.points li:before{content:"";position:absolute;left:4px;top:.62em;width:7px;height:7px;border-radius:50%;background:var(--accent)}
.points b{font-weight:650}

.prose h2{margin-top:0}
.prose h3{margin-top:20px}
.prose p{max-width:74ch}
.prose code{white-space:normal}

.specs{width:100%;border-collapse:collapse;margin-top:10px;font-size:14px}
.specs th,.specs td{text-align:left;padding:9px 10px;border-bottom:1px solid var(--line);vertical-align:top}
.specs th{width:38%;color:var(--muted);font-weight:600;background:#fafbf8}
.specs tr:last-child th,.specs tr:last-child td{border-bottom:0}

.codebox{background:#0f1619;color:#dfe9e4;border-radius:10px;margin:12px 0 0;overflow:hidden;border:1px solid #1d2b2e}
.codebar{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:8px 12px;background:#131e21;border-bottom:1px solid #223135;font-size:12px;color:#9fb5ad}
.codebar .lang{font-family:var(--mono);letter-spacing:.06em;text-transform:uppercase;font-size:10.5px}
.copy{border:1px solid #35484b;background:#1a292c;color:#d7e4df;border-radius:6px;padding:3px 9px;font-size:12px;cursor:pointer;font-family:inherit}
.copy:hover{background:#24383b}
.copy:focus-visible{outline:2px solid var(--lime);outline-offset:2px}
pre{margin:0;padding:15px 16px;overflow:auto;font-family:var(--mono);font-size:12.6px;line-height:1.6;tab-size:2}
pre code{background:none;padding:0;font-size:inherit;color:inherit;white-space:pre}

.rel{display:grid;gap:10px}
.rel a.rel-card{display:block;border:1px solid var(--line);border-radius:9px;padding:12px 14px;background:#fbfcf9;color:var(--ink)}
.rel a.rel-card:hover{border-color:var(--accent);text-decoration:none;background:#f6faf7}
.rel .rel-name{font-weight:650;color:var(--accent)}
.rel .rel-note{display:block;font-size:13px;color:var(--muted);margin-top:2px}

.caveats{list-style:none;padding:0;margin:8px 0 0;display:grid;gap:8px}
.caveats li{position:relative;padding-left:24px}
.caveats li:before{content:"!";position:absolute;left:4px;top:.1em;width:16px;height:16px;border-radius:50%;background:var(--warn-soft);color:var(--warn);font-size:11px;font-weight:800;display:grid;place-items:center;border:1px solid #ecd3a0}

.pager{display:flex;justify-content:space-between;gap:12px;margin-top:6px}
.pager a{flex:1;border:1px solid var(--line);border-radius:9px;padding:12px 14px;background:#fff;color:var(--ink)}
.pager a:hover{border-color:var(--accent);text-decoration:none}
.pager .dir{font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);display:block}
.pager .nm{font-weight:650;color:var(--accent)}
.pager .right{text-align:right}

.hero-grid{display:grid;grid-template-columns:minmax(0,1fr) 270px;gap:30px;align-items:start}
.hero-card{background:rgba(255,255,255,.055);border:1px solid rgba(255,255,255,.12);border-radius:12px;padding:16px 18px}
.hero-card .hc-title{font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:#8fa8a0;margin-bottom:10px}
.hero-card .hs{display:flex;justify-content:space-between;gap:10px;padding:7px 0;border-bottom:1px solid rgba(255,255,255,.09)}
.hero-card .hs:last-child{border-bottom:0}
.hero-card .hs b{color:#fff;font-size:14px;font-weight:650;text-align:right}
.hero-card .hs span{color:#a9bcb5;font-size:12.5px}
.hero-actions{display:flex;gap:10px;flex-wrap:wrap;margin-top:20px}
.btn{display:inline-flex;align-items:center;gap:7px;border-radius:8px;padding:8px 13px;font-size:13.5px;border:1px solid rgba(255,255,255,.18);color:#e9f1ee;background:rgba(255,255,255,.06)}
.btn:hover{text-decoration:none;background:rgba(255,255,255,.12)}
.btn.primary{background:var(--lime);border-color:var(--lime);color:#102018;font-weight:700}
.btn.primary:hover{background:#d6f873}

.crumbs{font-size:12.5px;color:#93a8a1;margin-bottom:14px}
.crumbs a{color:#c9d8d3}
.en{font-family:var(--mono);font-size:13px;color:#9db1aa;margin:0 0 8px}
.tagline{font-size:17px;color:#dbe6e2;max-width:780px;margin:0}

.legend{display:flex;gap:14px;flex-wrap:wrap;font-size:12px;color:var(--muted);margin-top:12px}
.legend span{display:inline-flex;align-items:center;gap:6px}
.dot{width:8px;height:8px;border-radius:50%;display:inline-block}
.dot.fact{background:var(--accent)}
.dot.judge{background:#b07a00}
.dot.time{background:var(--blue)}

/* index */
.explorer{margin-top:4px}
.controls{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin:12px 0 16px}
.search{flex:1 1 260px;min-width:220px;position:relative}
.search input{width:100%;border:1px solid var(--line-strong);background:#fff;border-radius:9px;padding:10px 12px 10px 36px;font:inherit;font-size:14px;color:var(--ink)}
.search input:focus{outline:2px solid var(--accent);outline-offset:1px;border-color:var(--accent)}
.search svg{position:absolute;left:11px;top:50%;transform:translateY(-50%);width:16px;height:16px;stroke:var(--muted)}
select{border:1px solid var(--line-strong);background:#fff;border-radius:9px;padding:10px 12px;font:inherit;font-size:13.5px;color:var(--ink)}
select:focus{outline:2px solid var(--accent);outline-offset:1px}
.chips{display:flex;gap:7px;flex-wrap:wrap;margin:0 0 6px}
.fbtn{border:1px solid var(--line-strong);background:#fff;color:var(--muted);border-radius:999px;padding:6px 11px;font:inherit;font-size:12.5px;cursor:pointer}
.fbtn:hover{border-color:var(--accent);color:var(--accent)}
.fbtn[aria-pressed="true"]{background:var(--accent);border-color:var(--accent);color:#fff;font-weight:650}
.fbtn:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.count{font-size:12.5px;color:var(--muted);margin:2px 0 14px}
.grid-proj{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:13px}
.proj{display:flex;flex-direction:column;border:1px solid var(--line);border-radius:10px;padding:15px 16px;background:#fff;color:var(--ink);min-height:150px}
.proj[hidden]{display:none}
.proj:hover{border-color:var(--accent);box-shadow:0 3px 14px rgba(12,107,92,.08);text-decoration:none;transform:translateY(-1px)}
.proj .top{display:flex;justify-content:space-between;gap:10px;align-items:flex-start}
.proj .nm{font-weight:700;font-size:15.5px;letter-spacing:-.01em}
.proj .repo{font-family:var(--mono);font-size:11.5px;color:var(--muted);margin-top:1px;word-break:break-all}
.proj .tag{font-size:13px;color:var(--muted);margin:9px 0 12px;flex:1}
.proj .bot{display:flex;justify-content:space-between;align-items:center;gap:8px;font-size:11.5px;color:var(--muted);border-top:1px solid var(--line);padding-top:9px}
.badge{font-size:10.5px;padding:2px 7px;border-radius:999px;background:var(--accent-soft);color:var(--accent);border:1px solid #c9e4da;white-space:nowrap;font-weight:650}
.badge.archived{background:#f0f0ed;color:#5f625c;border-color:#dcded6}
.badge.moved{background:var(--blue-soft);color:var(--blue);border-color:#c6dbf2}
.badge.research{background:#f4ecfb;color:#6b3fa0;border-color:#e0d0f2}
.badge.demo{background:var(--lime-soft);color:#4d5c0e;border-color:#dceba0}
.badge.meta{background:#f0f0ed;color:#5f625c;border-color:#dcded6}
.badge.external{background:#fdf1dd;color:#8a5a00;border-color:#eed7a8}
.stars{font-family:var(--mono);font-size:11.5px;color:var(--ink);font-weight:600}

.timeline{list-style:none;padding:0;margin:10px 0 0;border-left:2px solid var(--line-strong);margin-left:6px}
.timeline li{position:relative;padding:0 0 18px 22px;margin:0}
.timeline li:before{content:"";position:absolute;left:-7px;top:6px;width:12px;height:12px;border-radius:50%;background:var(--panel);border:2px solid var(--accent)}
.timeline .when{font-family:var(--mono);font-size:11.5px;color:var(--accent);letter-spacing:.03em}
.timeline .what{display:block;margin-top:1px}
.timeline .what a{font-weight:650}
.timeline .desc{display:block;color:var(--muted);font-size:13px}

.footer{border-top:1px solid var(--line);background:#eef0ea;padding:26px 0;color:var(--muted);font-size:13px}
.footer .wrap{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap}
.footer a{color:var(--accent)}

.noscript{background:var(--warn-soft);border:1px solid #eed7a8;color:#6b4200;padding:10px 12px;border-radius:8px;font-size:13px;margin:10px 0}

@media (max-width:980px){
  .layout{grid-template-columns:1fr;gap:18px}
  nav.toc{position:static;order:-1;background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:10px}
  nav.toc a{display:inline-block;border-left:0;border-bottom:2px solid transparent;padding:5px 8px}
  nav.toc a.active{border-left:0;border-bottom-color:var(--accent)}
  .toc-note{display:none}
  .hero-grid{grid-template-columns:1fr}
  .hero-card{max-width:420px}
}
@media (max-width:760px){
  .hero h1{font-size:29px}
  .statrow{grid-template-columns:1fr 1fr}
  .grid2,.grid3,.grid-proj{grid-template-columns:1fr}
  section{padding:19px 17px}
  .hero{padding:32px 0 28px}
  .specs th{width:42%}
  .pager{flex-direction:column}
  .pager .right{text-align:left}
  .topnav{gap:11px}
}
@media print{
  .topbar,.hero-actions,.controls,.copy,.pager,nav.toc{display:none!important}
  body{background:#fff}
  .layout{display:block}
  section{break-inside:avoid;border-color:#ccc}
  .hero{background:#fff;color:#000;padding:0 0 12px}
  .hero h1,.hero .lede,.hero .tagline,.en,.crumbs{color:#000}
  .hero-card{background:#fff;border-color:#ccc}
  .hero-card .hs b,.hero-card .hs span{color:#000}
}
"""

INDEX_JS = r"""
(function(){
  var cards = Array.prototype.slice.call(document.querySelectorAll('.proj'));
  var q = document.getElementById('q');
  var sort = document.getElementById('sort');
  var count = document.getElementById('count');
  var chips = Array.prototype.slice.call(document.querySelectorAll('.fbtn'));
  var cat = 'all';

  function matches(el){
    var text = (el.getAttribute('data-search') || '').toLowerCase();
    var term = (q && q.value || '').trim().toLowerCase();
    if (term && text.indexOf(term) === -1) return false;
    if (cat !== 'all' && el.getAttribute('data-cat') !== cat) return false;
    return true;
  }

  function sortCards(){
    var mode = sort ? sort.value : 'stars';
    cards.sort(function(a,b){
      if (mode === 'name') return a.getAttribute('data-name').localeCompare(b.getAttribute('data-name'));
      if (mode === 'new') return b.getAttribute('data-created').localeCompare(a.getAttribute('data-created'));
      if (mode === 'old') return a.getAttribute('data-created').localeCompare(b.getAttribute('data-created'));
      if (mode === 'stars-asc') return (+a.getAttribute('data-stars')) - (+b.getAttribute('data-stars'));
      return (+b.getAttribute('data-stars')) - (+a.getAttribute('data-stars'));
    });
    var grid = document.getElementById('grid');
    cards.forEach(function(c){ grid.appendChild(c); });
  }

  function apply(){
    var n = 0;
    cards.forEach(function(el){
      var ok = matches(el);
      el.hidden = !ok;
      if (ok) n++;
    });
    sortCards();
    if (count) count.textContent = '显示 ' + n + ' / ' + cards.length + ' 个项目';
  }

  if (q) q.addEventListener('input', apply);
  if (sort) sort.addEventListener('change', apply);
  chips.forEach(function(btn){
    btn.addEventListener('click', function(){
      cat = btn.getAttribute('data-cat');
      chips.forEach(function(b){ b.setAttribute('aria-pressed', b === btn ? 'true' : 'false'); });
      apply();
    });
  });
  apply();
})();
"""

PROJECT_JS = r"""
(function(){
  var toc = document.querySelectorAll('nav.toc a[href^="#"]');
  if (!('IntersectionObserver' in window) || !toc.length) return;
  var map = {};
  toc.forEach(function(a){ map[a.getAttribute('href').slice(1)] = a; });
  var obs = new IntersectionObserver(function(entries){
    entries.forEach(function(e){
      if (e.isIntersecting) {
        toc.forEach(function(a){ a.classList.remove('active'); });
        var a = map[e.target.id];
        if (a) a.classList.add('active');
      }
    });
  }, {rootMargin: '-15% 0px -70% 0px', threshold: 0});
  document.querySelectorAll('main section[id]').forEach(function(s){ obs.observe(s); });
})();

document.addEventListener('click', function(e){
  var btn = e.target.closest('.copy');
  if (!btn) return;
  var box = btn.closest('.codebox');
  var code = box ? box.querySelector('code') : null;
  if (!code) return;
  var text = code.innerText;
  function done(ok){
    var old = btn.textContent;
    btn.textContent = ok ? '已复制' : '复制失败';
    setTimeout(function(){ btn.textContent = old; }, 1400);
  }
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(text).then(function(){ done(true); }, function(){ done(false); });
  } else {
    try {
      var ta = document.createElement('textarea');
      ta.value = text; ta.style.position = 'fixed'; ta.style.left = '-9999px';
      document.body.appendChild(ta); ta.select(); document.execCommand('copy');
      document.body.removeChild(ta); done(true);
    } catch (err) { done(false); }
  }
});
"""


def page_shell(title, desc, body, extra_js=""):
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<style>{CSS}</style>
</head>
<body>
<a class="skip" href="#main">跳到正文</a>
{body}
<script>{PROJECT_JS if extra_js == "project" else INDEX_JS if extra_js == "index" else ""}</script>
</body>
</html>
"""


def topbar(active=""):
    return f"""<header class="topbar">
  <div class="wrap">
    <a class="brand" href="index.html"><span class="mark">K</span><span>Kimi 开源图谱</span></a>
    <nav class="topnav" aria-label="站点导航">
      <a href="index.html">全部项目</a>
      <a href="index.html#mainlines">技术主线</a>
      <a href="index.html#timeline">时间线</a>
      <a href="index.html#method">方法与来源</a>
      <a href="https://github.com/MoonshotAI" target="_blank" rel="noopener">GitHub 组织 ↗</a>
    </nav>
  </div>
</header>"""


def project_page(p, meta, prev_p, next_p, index):
    slug = p["slug"]
    cat = CATEGORY_LABELS[p["category"]]
    status = STATUS_LABELS[p["status"]]
    stars = meta["stargazers_count"]
    forks = meta["forks_count"]
    lang = meta.get("language") or {
        "model": "模型卡",
        "architecture": "论文/代码",
        "agent": "工具",
        "infra": "基础设施",
        "eval": "评测",
        "eco": "文档/资源",
    }.get(p["category"], "—")
    lic = license_of(p, meta)
    created = fmt_date(meta.get("created_at"))
    pushed = fmt_date(meta.get("pushed_at"))
    repo_url = meta["html_url"]
    repo_full = meta.get("full_name") or f"MoonshotAI/{p['repo']}"
    readme_url = repo_url + "#readme"
    stats = p.get("stats") or [[fmt_num(stars), "Stars"], [fmt_num(forks), "Forks"], [lang, "语言"], [created, "创建"]]

    hero_stats = "".join(
        f'<div class="hs"><span>{esc(l)}</span><b>{esc(v)}</b></div>' for v, l in stats
    )

    sections = p.get("sections") or []
    sec_html = []
    toc_items = ['<a href="#read">30 秒读懂</a>']
    for i, s in enumerate(sections, 1):
        sid = f"s{i}"
        sec_html.append(f"""<section id="{sid}">
  <div class="sec-head"><span class="sec-num">{i:02d}</span><h2>{esc(s['h'])}</h2></div>
  <div class="prose">{s['html']}</div>
</section>""")
        toc_items.append(f'<a href="#{sid}">{esc(s["h"])}</a>')

    specs_html = ""
    if p.get("specs"):
        rows = "".join(
            f"<tr><th>{esc(k)}</th><td>{esc(v)}</td></tr>" for k, v in p["specs"]
        )
        specs_html = f"""<section id="specs">
  <div class="sec-head"><span class="sec-num">规格</span><h2>关键规格</h2></div>
  <p class="lede">以下数值来自仓库 README / 模型卡；未标注单位的比例与分数按原文。</p>
  <table class="specs"><tbody>{rows}</tbody></table>
</section>"""
        toc_items.append('<a href="#specs">关键规格</a>')

    quick_html = ""
    if p.get("quickstart"):
        q = p["quickstart"]
        quick_html = f"""<section id="quickstart">
  <div class="sec-head"><span class="sec-num">上手</span><h2>快速开始</h2></div>
  <p class="lede">{esc(q.get('note', ''))}</p>
  <div class="codebox">
    <div class="codebar"><span class="lang">{esc(q.get('lang', 'code'))}</span><button class="copy" type="button">复制</button></div>
    <pre><code>{esc(q['code'])}</code></pre>
  </div>
</section>"""
        toc_items.append('<a href="#quickstart">快速开始</a>')

    rel_html = ""
    if p.get("relations"):
        cards = []
        for r in p["relations"]:
            href = f"{r['slug']}.html" if r.get("slug") else r.get("url", "#")
            cards.append(
                f'<a class="rel-card" href="{esc(href)}"><span class="rel-name">{esc(r["name"])}</span>'
                f'<span class="rel-note">{esc(r.get("note", ""))}</span></a>'
            )
        rel_html = f"""<section id="relations">
  <div class="sec-head"><span class="sec-num">关系</span><h2>在 Kimi 生态里的位置</h2></div>
  <p class="lede">这些是同一组织下与它直接相关的项目；关系说明为编辑判断，不是官方依赖声明。</p>
  <div class="rel">{''.join(cards)}</div>
</section>"""
        toc_items.append('<a href="#relations">生态关系</a>')

    caveats = "".join(f"<li>{esc(c)}</li>" for c in (p.get("caveats") or []))
    cav_html = f"""<section id="caveats">
  <div class="sec-head"><span class="sec-num">边界</span><h2>边界与注意</h2></div>
  <ul class="caveats">{caveats}</ul>
</section>"""
    toc_items.append('<a href="#caveats">边界与注意</a>')

    sources = [
        ("GitHub 仓库", repo_url),
        ("README", readme_url),
    ]
    if meta.get("homepage"):
        sources.append(("项目主页", meta["homepage"]))
    if p.get("sources"):
        sources.extend(p["sources"])
    src_links = "".join(
        f'<li><a href="{esc(u)}" target="_blank" rel="noopener">{esc(n)} ↗</a></li>' for n, u in sources
    )
    src_html = f"""<section id="sources">
  <div class="sec-head"><span class="sec-num">来源</span><h2>来源与标注</h2></div>
  <p>本页事实主要来自 <a href="{esc(repo_url)}" target="_blank" rel="noopener">{esc(p['repo'])}</a> 的 README 与 GitHub API 元数据（快照 2026-11-01）。</p>
  <ul>{src_links}</ul>
  <div class="legend">
    <span><i class="dot fact"></i>事实：README / GitHub 元数据</span>
    <span><i class="dot judge"></i>判断：编辑分析，已尽量与事实分开</span>
    <span><i class="dot time"></i>时效：Stars、日期、榜单会变化</span>
  </div>
  <div class="callout info"><b>读法：</b>“关键规格”与正文中的数字以仓库原文为准；“边界与注意”和“生态关系”包含编辑判断，不构成官方结论或选型建议。模型能力与许可证请以实际 checkpoint / 合同为准。</div>
</section>"""
    toc_items.append('<a href="#sources">来源与标注</a>')

    prev_html = ""
    if prev_p:
        prev_html = f'<a href="{prev_p["slug"]}.html"><span class="dir">← 上一个</span><span class="nm">{esc(prev_p["title"])}</span></a>'
    else:
        prev_html = '<a href="index.html"><span class="dir">← 返回</span><span class="nm">全部仓库</span></a>'
    if next_p:
        next_html = f'<a class="right" href="{next_p["slug"]}.html"><span class="dir">下一个 →</span><span class="nm">{esc(next_p["title"])}</span></a>'
    else:
        next_html = '<a class="right" href="index.html"><span class="dir">返回 →</span><span class="nm">全部仓库</span></a>'

    points = "".join(f"<li>{pt}</li>" for pt in (p.get("points") or []))

    body = f"""{topbar()}
<header class="hero">
  <div class="wrap">
    <div class="crumbs"><a href="index.html">Kimi 开源图谱</a> / <a href="index.html#explorer">{esc(cat)}</a> / <span>{esc(p['title'])}</span></div>
    <div class="hero-grid">
      <div>
        <div class="kicker">{esc(cat)} · {esc(status)}</div>
        <h1>{esc(p['title'])}</h1>
        <p class="en">{esc(repo_full)}</p>
        <p class="tagline">{esc(p['tagline'])}</p>
        <div class="meta">
          <span class="chip"><b>{fmt_num(stars)}</b> Stars</span>
          <span class="chip"><b>{fmt_num(forks)}</b> Forks</span>
          <span class="chip"><b>{esc(lang)}</b></span>
          <span class="chip"><b>{esc(lic)}</b></span>
          <span class="chip">创建 <b>{esc(created)}</b></span>
        </div>
        <div class="hero-actions">
          <a class="btn primary" href="{esc(repo_url)}" target="_blank" rel="noopener">打开 GitHub ↗</a>
          <a class="btn" href="index.html">返回索引</a>
        </div>
      </div>
      <aside class="hero-card" aria-label="关键数字">
        <div class="hc-title">关键数字</div>
        {hero_stats}
      </aside>
    </div>
  </div>
</header>

<div class="wrap layout">
  <nav class="toc" aria-label="本页目录">
    <p class="toc-title">本页目录</p>
    {''.join(toc_items)}
    <p class="toc-note">最后 push：{esc(pushed)}<br>数据快照：2026-11-01</p>
  </nav>
  <main id="main">
    <section id="read">
      <div class="sec-head"><span class="sec-num">00</span><h2>30 秒读懂</h2></div>
      <p class="lede">{esc(p['summary'])}</p>
      <ul class="points">{points}</ul>
    </section>
    {''.join(sec_html)}
    {specs_html}
    {quick_html}
    {rel_html}
    {cav_html}
    {src_html}
    <div class="pager">{prev_html}{next_html}</div>
  </main>
</div>

<footer class="footer">
  <div class="wrap">
    <span>Kimi 开源图谱 · 第 {index} / {len(PROJECTS)} 个项目</span>
    <span>数据：GitHub API 2026-11-01 · 单文件离线可读</span>
  </div>
</footer>"""
    return page_shell(f"{p['title']} · Kimi 开源图谱", p["tagline"], body, "project")


def index_page():
    total_stars = sum(m["stargazers_count"] for m in META.values())
    official = [p for p in PROJECTS if not p.get("external")]
    external_count = len(PROJECTS) - len(official)
    active = sum(1 for p in PROJECTS if p["status"] == "active")
    archived = sum(1 for p in PROJECTS if p["status"] in ("archived", "moved"))
    latest = max((m.get("pushed_at") or "")[:10] for m in META.values())
    counts = {k: sum(1 for p in PROJECTS if p["category"] == k) for k in CATEGORY_ORDER}

    cards = []
    ordered = sorted(PROJECTS, key=lambda p: (-META[p["repo"]]["stargazers_count"], p["title"]))
    for p in ordered:
        m = META[p["repo"]]
        cat = CATEGORY_LABELS[p["category"]]
        status = STATUS_LABELS[p["status"]]
        search_blob = " ".join([p["title"], p["repo"], m.get("full_name") or "", p["tagline"], p["summary"], cat, status]).lower()
        cards.append(f"""<a class="proj" href="{p['slug']}.html"
   data-name="{esc(p['title'].lower())}"
   data-cat="{esc(p['category'])}"
   data-status="{esc(p['status'])}"
   data-stars="{m['stargazers_count']}"
   data-created="{esc((m.get('created_at') or '')[:10])}"
   data-search="{esc(search_blob)}">
  <div class="top">
    <div><div class="nm">{esc(p['title'])}</div><div class="repo">{esc(m.get('full_name') or ('MoonshotAI/' + p['repo']))}</div></div>
    <span class="badge {esc(p['status'])}">{esc(status)}</span>
  </div>
  <div class="tag">{esc(p['tagline'])}</div>
  <div class="bot"><span>{esc(cat)}</span><span class="stars">★ {fmt_num(m['stargazers_count'])}</span></div>
</a>""")

    chips = ['<button class="fbtn" type="button" data-cat="all" aria-pressed="true">全部 ' + str(len(PROJECTS)) + "</button>"]
    for k in CATEGORY_ORDER:
        chips.append(f'<button class="fbtn" type="button" data-cat="{k}" aria-pressed="false">{CATEGORY_LABELS[k]} {counts[k]}</button>')

    timeline = [
        ("2023-03", ".github", "github-org", "组织成立，先有 profile 与默认配置。"),
        ("2024-06", "Mooncake", "mooncake", "Kimi 的 serving platform 开源，后来拿到 FAST'25 最佳论文。"),
        ("2024-07", "MoonPalace", "moonpalace", "API 调试代理上线，解决“请求到底发了什么”。"),
        ("2025-01", "Kimi k1.5", "kimi-k1-5", "长上下文 RL 报告，o1 级推理不靠 MCTS/PRM。"),
        ("2025-02", "MoBA / Moonlight", "moba", "长上下文块稀疏注意力；Muon 可扩展性验证。"),
        ("2025-04", "Kimi-VL / Kimi-Audio / Kimina / CombiBench", "kimi-vl", "多模态、音频、形式化证明与组合数学基准集中发布。"),
        ("2025-06", "Kimi-Dev / Kimi-Researcher", "kimi-dev", "编码模型与搜索 Agent，展示 RL 在真实任务上的效果。"),
        ("2025-07", "Kimi K2", "kimi-k2", "1T MoE、MuonClip，Agent 能力成为主线。"),
        ("2025-09", "checkpoint-engine / K2VV", "checkpoint-engine", "万亿权重 20 秒同步；供应商 toolcall 校验。"),
        ("2025-10", "Kimi Linear / kimi-cli", "kimi-linear", "KDA 混合线性注意力；Python 终端 Agent。"),
        ("2026-01", "Kimi K2.5 / Agent SDK / KimiVV", "kimi-k2-5", "视觉 Agent、多语言 SDK、跨供应商验证。"),
        ("2026-03", "Attention Residuals", "attention-residuals", "用深度方向注意力替代固定残差。"),
        ("2026-05", "kimi-code", "kimi-code", "单二进制终端 Agent，接替 Python CLI。"),
        ("2026-07", "Kimi K3 / MoonEP / nano-kpu / minitriton / PerceptionBench", "kimi-k3", "2.8T 旗舰与一整套系统/评测配套。"),
        ("2026-10", "kimi-code 持续更新", "kimi-code", "最近 push：2026-10-31。"),
    ]
    tl = "".join(
        f'<li><span class="when">{esc(w)}</span><span class="what"><a href="{esc(slug)}.html">{esc(name)}</a></span><span class="desc">{esc(desc)}</span></li>'
        for w, name, slug, desc in timeline
    )

    body = f"""{topbar()}
<header class="hero">
  <div class="wrap">
    <div class="kicker">MoonshotAI / Kimi · Open Source Atlas</div>
    <h1>Kimi 开源了什么？</h1>
    <p class="lede">把 MoonshotAI 组织下的 42 个公开仓库，加上组织外但直接为 Kimi 提供 serving 的 Mooncake，一起放进一张图：哪些是模型，哪些是架构研究，哪些是 Agent 产品与底层系统，哪些只是评测、生态或组织基建。每个项目都有独立页面，事实与判断分开标注。</p>
    <div class="meta">
      <span class="chip lime"><b>{len(official)}</b> 个 MoonshotAI 仓库</span>
      <span class="chip lime"><b>{external_count}</b> 个组织外核心</span>
      <span class="chip"><b>{total_stars/1000:.1f}k</b> Stars 合计（含外部）</span>
      <span class="chip"><b>6</b> 个类别</span>
      <span class="chip">数据快照 <b>2026-11-01</b></span>
      <span class="chip">最近 push <b>{esc(latest)}</b></span>
    </div>
    <div class="statrow">
      <div class="stat"><b>{len(PROJECTS)}</b><span>全部页面（42 官方 + 1 外部）</span></div>
      <div class="stat"><b>{active}</b><span>状态为“活跃”的项目</span></div>
      <div class="stat"><b>{archived}</b><span>已归档或已迁移</span></div>
      <div class="stat"><b>{total_stars:,}</b><span>Stars 原始合计（含 Mooncake）</span></div>
    </div>
  </div>
</header>

<div class="wrap layout">
  <nav class="toc" aria-label="页面目录">
    <p class="toc-title">页面目录</p>
    <a href="#how">怎么读这张图</a>
    <a href="#mainlines">四条技术主线</a>
    <a href="#explorer">全部仓库</a>
    <a href="#timeline">时间线</a>
    <a href="#method">方法与来源</a>
  </nav>
  <main id="main">
    <section id="how">
      <div class="sec-head"><span class="sec-num">01</span><h2>怎么读这张图</h2></div>
      <p class="lede">43 个页面不是 43 个“模型”。把它们按职责分层，才能看出 Kimi 的开源策略；Mooncake 单列为组织外核心，避免与官方仓库统计混淆。</p>
      <div class="grid3">
        <div class="card"><div class="num">LAYER 1</div><h3>模型权重</h3><p>K3 / K2 / K2.5 / k1.5 / VL / Audio / Linear / Moonlight / Dev。决定能力上限，也决定部署门槛。</p></div>
        <div class="card"><div class="num">LAYER 2</div><h3>架构与训练方法</h3><p>MoBA、KDA、Attention Residuals、Muon。解释“为什么这一代更强/更便宜”。</p></div>
        <div class="card"><div class="num">LAYER 3</div><h3>系统与工具</h3><p>Mooncake、MoonEP、checkpoint-engine、FlashKDA、walle、batched-benchmark。把模型变成可服务、可训练的系统。</p></div>
        <div class="card"><div class="num">LAYER 4</div><h3>Agent 产品</h3><p>kimi-code、CLI、SDK、Rust 运行时、Zed/Zsh 集成。离用户最近的一层。</p></div>
        <div class="card"><div class="num">LAYER 5</div><h3>评测与基准</h3><p>PerceptionBench、WorldVQA、CombiBench、Kimina、Vendor Verifier。定义“什么叫好”。</p></div>
        <div class="card"><div class="num">LAYER 6</div><h3>生态与组织</h3><p>Cookbook、Koishi 插件、MoonPalace、Branding、Pages。降低接入与传播成本。</p></div>
      </div>
      <div class="callout warn"><b>注意：</b>本页把归档、迁移、纯元数据仓库也算进“全部”，因为问题问的是“所有项目”。如果你只关心可用的活跃项目，用下方筛选器看“活跃”，或直接读四条主线。</div>
    </section>

    <section id="mainlines">
      <div class="sec-head"><span class="sec-num">02</span><h2>四条技术主线</h2></div>
      <p class="lede">把仓库按时间与依赖串起来，Kimi 的开源路线其实很集中。</p>
      <div class="grid2">
        <div class="card"><div class="num">LINE 1 · 稀疏 MoE 与长上下文</div><h3>K2 → K2.5 → K3</h3><p>1T/32B 的 K2 证明万亿 MoE 可训练；K2.5 加视觉与 256K；K3 用 KDA + AttnRes 把总参推到 2.8T、上下文推到 1M。配套是 MoBA（块稀疏）、Kimi Linear（KDA 验证）、FlashKDA（kernel）。</p></div>
        <div class="card"><div class="num">LINE 2 · Agent 产品化</div><h3>kimi-cli → kimi-code</h3><p>Python CLI 先跑通终端 Agent、MCP、ACP；kimi-code 用单二进制重做，加入视频输入、子 Agent、插件市场与 hooks；SDK / Rust / Zed / Zsh 把同一运行时铺到更多入口。</p></div>
        <div class="card"><div class="num">LINE 3 · 训练与推理系统</div><h3>Moonlight → K2 MuonClip → Mooncake / MoonEP / checkpoint-engine</h3><p>先解决优化器可扩展性，再解决万亿 MoE 的 serving、专家并行通信与权重热更新；FlashKDA、walle、batched-benchmark 补齐 kernel、结构化输出与压测。</p></div>
        <div class="card"><div class="num">LINE 4 · 评测与可信度</div><h3>Vendor Verifier + 原子能力基准</h3><p>K2VV/KimiVV 检查不同供应商的 toolcall 与精度；PerceptionBench/WorldVQA 把多模态能力拆成原子项；CombiBench/Kimina 覆盖形式化数学；Audio-Evalkit 统一音频评测。</p></div>
      </div>
    </section>

    <section id="explorer" class="explorer">
      <div class="sec-head"><span class="sec-num">03</span><h2>全部项目</h2></div>
      <p class="lede">43 个项目 = 42 个 MoonshotAI 官方仓库 + Mooncake。按 Stars 默认排序；搜索匹配名称、仓库名、简介与类别，筛选与排序只影响显示。</p>
      <noscript><div class="noscript">JavaScript 已禁用：下方仍会显示全部 43 个项目，但搜索、筛选与排序不可用。</div></noscript>
      <div class="controls">
        <div class="search">
          <svg viewBox="0 0 24 24" fill="none" stroke-width="2" aria-hidden="true"><circle cx="11" cy="11" r="7"></circle><path d="M20 20l-3.5-3.5"></path></svg>
          <input id="q" type="search" placeholder="搜索项目、仓库名或关键词，例如 KDA、Agent、评测" aria-label="搜索项目">
        </div>
        <select id="sort" aria-label="排序方式">
          <option value="stars">Stars 从高到低</option>
          <option value="stars-asc">Stars 从低到高</option>
          <option value="new">创建时间从新到旧</option>
          <option value="old">创建时间从旧到新</option>
          <option value="name">名称 A–Z</option>
        </select>
      </div>
      <div class="chips" role="group" aria-label="按类别筛选">{''.join(chips)}</div>
      <p class="count" id="count">显示 {len(PROJECTS)} / {len(PROJECTS)} 个项目</p>
      <div class="grid-proj" id="grid">{''.join(cards)}</div>
    </section>

    <section id="timeline">
      <div class="sec-head"><span class="sec-num">04</span><h2>时间线</h2></div>
      <p class="lede">按首次发布/创建时间挑选的关键节点；完整日期见每个项目页。</p>
      <ol class="timeline">{tl}</ol>
    </section>

    <section id="method">
      <div class="sec-head"><span class="sec-num">05</span><h2>方法与来源</h2></div>
      <div class="grid2">
        <div class="card"><h3>数据</h3><p>仓库清单、Stars、Forks、语言、许可证、创建/推送时间来自 GitHub REST API（<code>orgs/MoonshotAI/repos</code>），抓取于 2026-11-01。项目内容来自各仓库 README。</p></div>
        <div class="card"><h3>分类</h3><p>6 个类别是编辑归类，依据仓库主职责，不是 GitHub topics。一个项目可能跨类（如 Kimi-Dev 既是模型也服务 Agent），这里取主要用途。</p></div>
        <div class="card"><h3>判断</h3><p>“边界与注意”“生态关系”和主线叙述含编辑判断，已尽量与 README 事实分开。没有引用来源的数字不要当作官方承诺。</p></div>
        <div class="card"><h3>时效</h3><p>Stars、榜单、许可证与模型版本都会变。归档/迁移状态以抓取日为准；使用前请回到仓库确认。</p></div>
      </div>
      <div class="callout info"><b>覆盖说明：</b>MoonshotAI 组织显示 42 个公开仓库，本页覆盖全部 42 个，包括 1 个归档（kimi-cli）、2 个已迁移（kosong、pykaos）、3 个组织/站点类仓库。另加 1 个组织外核心项目 Mooncake（kvcache-ai），因为它的 README 明确写为 Kimi 的 serving platform。Mooncake 不计入 42 个官方仓库的统计，但单独有一页。其他外部依赖（Kimina Lean Server、flash-linear-attention）只在相关页面提及。</div>
    </section>
  </main>
</div>

<footer class="footer">
  <div class="wrap">
    <span>Kimi 开源图谱 · 42 个官方仓库 + 1 个外部核心 · 每项一页</span>
    <span>单文件 HTML · 无 CDN · 可离线打开</span>
  </div>
</footer>"""
    return page_shell("Kimi 开源图谱 · 43 个项目", "MoonshotAI 42 个公开仓库 + Mooncake 的分类、分析与逐项页面。", body, "index")


def validate():
    repos = [p["repo"] for p in PROJECTS]
    assert len(PROJECTS) == 43, f"expected 43, got {len(PROJECTS)}"
    assert sum(1 for p in PROJECTS if not p.get("external")) == 42, "expected 42 official"
    assert sum(1 for p in PROJECTS if p.get("external")) == 1, "expected 1 external"
    assert len(set(repos)) == len(repos), "duplicate repo"
    missing = set(repos) - set(META)
    extra = set(META) - set(repos)
    assert not missing, f"missing metadata: {missing}"
    assert not extra, f"extra metadata: {extra}"
    slugs = [p["slug"] for p in PROJECTS]
    assert len(set(slugs)) == len(slugs), "duplicate slug"
    for p in PROJECTS:
        for k in ("repo", "slug", "title", "category", "status", "tagline", "summary", "points", "caveats"):
            assert p.get(k), f"{p.get('repo')} missing {k}"
        assert p["category"] in CATEGORY_LABELS, p["repo"]
        assert p["status"] in STATUS_LABELS, p["repo"]
    return True


def main():
    validate()
    out = BASE
    # deterministic order: category then stars desc
    order = []
    for cat in CATEGORY_ORDER:
        rows = [p for p in PROJECTS if p["category"] == cat]
        rows.sort(key=lambda p: (-META[p["repo"]]["stargazers_count"], p["title"]))
        order.extend(rows)

    for i, p in enumerate(order):
        prev_p = order[i - 1] if i > 0 else None
        next_p = order[i + 1] if i + 1 < len(order) else None
        html_out = project_page(p, META[p["repo"]], prev_p, next_p, i + 1)
        with open(os.path.join(out, p["slug"] + ".html"), "w", encoding="utf-8") as f:
            f.write(html_out)

    with open(os.path.join(out, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_page())

    print(f"wrote {len(order) + 1} html files to {out}")
    print("total stars:", sum(m["stargazers_count"] for m in META.values()))


META = load_meta()
META.update(external.META)

if __name__ == "__main__":
    main()
