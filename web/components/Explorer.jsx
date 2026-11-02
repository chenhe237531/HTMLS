'use client';

import { useCallback, useEffect, useMemo, useRef, useState } from 'react';

const REFRESH_INTERVAL_MS = 5000;

function Icon({ children, size = 16, className = '' }) {
  return (
    <svg
      className={className}
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.8"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      {children}
    </svg>
  );
}

const SearchIcon = () => (
  <Icon>
    <circle cx="11" cy="11" r="7" />
    <path d="m20 20-3.5-3.5" />
  </Icon>
);

const ChevronIcon = ({ open }) => (
  <Icon className={`chevron ${open ? 'is-open' : ''}`}>
    <path d="m9 6 6 6-6 6" />
  </Icon>
);

const FolderIcon = () => (
  <Icon>
    <path d="M3 7a2 2 0 0 1 2-2h4l2 2h6a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2Z" />
  </Icon>
);

const FileIcon = () => (
  <Icon>
    <path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8Z" />
    <path d="M14 3v5h5" />
  </Icon>
);

const RefreshIcon = () => (
  <Icon>
    <path d="M21 12a9 9 0 1 1-2.64-6.36" />
    <path d="M21 3v6h-6" />
  </Icon>
);

const SunIcon = () => (
  <Icon className="icon-sun">
    <circle cx="12" cy="12" r="4" />
    <path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41" />
  </Icon>
);

const MoonIcon = () => (
  <Icon className="icon-moon">
    <path d="M21 12.8A8.5 8.5 0 1 1 11.2 3a6.6 6.6 0 0 0 9.8 9.8Z" />
  </Icon>
);

const MenuIcon = () => (
  <Icon>
    <path d="M4 6h16M4 12h16M4 18h16" />
  </Icon>
);

const CloseIcon = () => (
  <Icon>
    <path d="M6 6l12 12M18 6 6 18" />
  </Icon>
);

const ExternalIcon = () => (
  <Icon>
    <path d="M14 4h6v6" />
    <path d="M20 4 10 14" />
    <path d="M19 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1h5" />
  </Icon>
);

const CopyIcon = () => (
  <Icon>
    <rect x="9" y="9" width="11" height="11" rx="2" />
    <path d="M5 15V5a2 2 0 0 1 2-2h10" />
  </Icon>
);

const CheckIcon = () => (
  <Icon>
    <path d="m5 12 5 5 9-9" />
  </Icon>
);

function walkPages(node, output = []) {
  for (const page of node.pages) output.push(page);
  for (const child of node.children) walkPages(child, output);
  return output;
}

function filterNode(node, query) {
  if (!query) return node;
  const pages = node.pages.filter((page) =>
    `${page.title} ${page.relPath} ${page.description}`.toLowerCase().includes(query),
  );
  const children = node.children.map((child) => filterNode(child, query)).filter(Boolean);
  if (pages.length === 0 && children.length === 0) return null;
  const matchedCount =
    pages.length + children.reduce((total, child) => total + child.matchedCount, 0);
  return { ...node, pages, children, matchedCount };
}

function formatBytes(bytes) {
  if (!bytes) return '0 B';
  const units = ['B', 'KB', 'MB', 'GB'];
  const index = Math.min(Math.floor(Math.log(bytes) / Math.log(1024)), units.length - 1);
  const value = bytes / 1024 ** index;
  return `${value >= 10 || index === 0 ? Math.round(value) : value.toFixed(1)} ${units[index]}`;
}

function formatRelative(ms, nowMs) {
  if (!ms) return '—';
  const diff = Math.max(0, nowMs - ms);
  const minute = 60000;
  const hour = 3600000;
  const day = 86400000;
  if (diff < minute) return '刚刚';
  if (diff < hour) return `${Math.floor(diff / minute)} 分钟前`;
  if (diff < day) return `${Math.floor(diff / hour)} 小时前`;
  const days = Math.floor(diff / day);
  if (days < 30) return `${days} 天前`;
  return `${Math.floor(days / 30)} 个月前`;
}

function Time({ ms, nowMs }) {
  const reference = Number.isFinite(nowMs) ? nowMs : Date.now();
  return (
    <span suppressHydrationWarning title={ms ? `UTC ${new Date(ms).toISOString()}` : undefined}>
      {formatRelative(ms, reference)}
    </span>
  );
}

function pageSrc(relPath) {
  return `/view/${relPath.split('/').map(encodeURIComponent).join('/')}`;
}

function DonutChart({ distribution, total }) {
  const radius = 42;
  const circumference = 2 * Math.PI * radius;
  const safeTotal = Math.max(1, total);
  let offset = 0;
  const segments = distribution.map((item) => {
    const fraction = item.count / safeTotal;
    const segment = { ...item, fraction, dash: fraction * circumference, offset };
    offset += fraction * circumference;
    return segment;
  });

  return (
    <div className="donut-wrap">
      <svg className="donut" viewBox="0 0 120 120" role="img" aria-label="页面按顶层目录的分布">
        <circle cx="60" cy="60" r={radius} fill="none" stroke="var(--panel-2)" strokeWidth="14" />
        {segments.map((segment) => (
          <circle
            key={segment.name}
            cx="60"
            cy="60"
            r={radius}
            fill="none"
            stroke={segment.color}
            strokeWidth="14"
            strokeDasharray={`${Math.max(0.5, segment.dash - 2)} ${circumference}`}
            strokeDashoffset={-segment.offset}
            transform="rotate(-90 60 60)"
          >
            <title>{`${segment.name}: ${segment.count} 个页面（${Math.round(segment.fraction * 100)}%）`}</title>
          </circle>
        ))}
        <text className="donut-total" x="60" y="58" textAnchor="middle">
          {total}
        </text>
        <text className="donut-label" x="60" y="72" textAnchor="middle">
          页面
        </text>
      </svg>
      <ul className="donut-legend">
        {segments.map((segment) => (
          <li key={segment.name}>
            <span className="legend-dot" style={{ background: segment.color }} />
            <span className="legend-name" title={segment.name}>
              {segment.name}
            </span>
            <span className="legend-count">{segment.count}</span>
            <span className="legend-pct">{Math.round(segment.fraction * 100)}%</span>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default function Explorer({ initialData }) {
  const [data, setData] = useState(initialData);
  const [selected, setSelected] = useState(null);
  const [query, setQuery] = useState('');
  const [collapsed, setCollapsed] = useState(() => new Set());
  const [autoRefresh, setAutoRefresh] = useState(true);
  const [status, setStatus] = useState('live');
  const [previewNonce, setPreviewNonce] = useState(0);
  const [iframeLoading, setIframeLoading] = useState(false);
  const [copied, setCopied] = useState(false);
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [range, setRange] = useState(30);
  const [hoveredIndex, setHoveredIndex] = useState(null);

  const searchRef = useRef(null);
  const dataRef = useRef(data);
  const selectedRef = useRef(selected);
  const copyTimer = useRef(null);
  const refreshingRef = useRef(false);

  dataRef.current = data;
  selectedRef.current = selected;

  const filteredTree = useMemo(() => filterNode(data.tree, query.trim().toLowerCase()), [data, query]);
  const nowMs = Date.parse(data.generatedAt) || Date.now();
  const pages = useMemo(() => walkPages(data.tree), [data]);
  const selectedPage = useMemo(
    () => pages.find((page) => page.relPath === selected) ?? null,
    [pages, selected],
  );
  const recentPages = useMemo(
    () => [...pages].sort((a, b) => b.mtimeMs - a.mtimeMs).slice(0, 6),
    [pages],
  );
  const sections = useMemo(() => {
    return data.tree.children
      .map((node) => {
        const sectionPages = walkPages(node, []);
        sectionPages.sort((a, b) => b.mtimeMs - a.mtimeMs);
        return {
          name: node.name,
          path: node.path,
          count: node.pageCount,
          pages: sectionPages.slice(0, 3),
          first: sectionPages[0] ?? null,
        };
      })
      .sort((a, b) => b.count - a.count);
  }, [data]);

  const activityStats = useMemo(() => {
    const days = (data.activity ?? []).slice(-range);
    const total = days.reduce((sum, day) => sum + day.count, 0);
    const activeDays = days.filter((day) => day.count > 0).length;
    const peak = days.reduce(
      (best, day) => (day.count > best.count ? day : best),
      days[0] ?? { date: '', count: 0, bytes: 0 },
    );
    const max = Math.max(1, ...days.map((day) => day.count));
    return { days, total, activeDays, peak, max };
  }, [data.activity, range]);

  const distribution = useMemo(() => {
    const items = data.tree.children.map((node) => ({ name: node.name, count: node.pageCount }));
    if (data.tree.pages.length) items.push({ name: '根目录', count: data.tree.pages.length });
    return items
      .sort((a, b) => b.count - a.count)
      .map((item, index) => ({ ...item, color: `var(--chart-${(index % 7) + 1})` }));
  }, [data]);

  const hoveredDay = hoveredIndex === null ? null : activityStats.days[hoveredIndex] ?? null;
  const labelStep = Math.max(1, Math.ceil(activityStats.days.length / 6));

  const refresh = useCallback(async () => {
    if (refreshingRef.current) return;
    refreshingRef.current = true;
    setStatus('refreshing');
    try {
      const response = await fetch('/api/pages', { cache: 'no-store' });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const next = await response.json();
      if (next.error) throw new Error(next.error);
      const previous = dataRef.current;
      if (next.revision !== previous.revision) {
        setData(next);
        const currentSelection = selectedRef.current;
        if (currentSelection) {
          const before = walkPages(previous.tree).find((page) => page.relPath === currentSelection);
          const after = walkPages(next.tree).find((page) => page.relPath === currentSelection);
          if (!after) {
            setSelected(null);
          } else if (!before || before.mtimeMs !== after.mtimeMs || before.size !== after.size) {
            setPreviewNonce((value) => value + 1);
          }
        }
      }
      setStatus('live');
    } catch {
      setStatus('error');
    } finally {
      refreshingRef.current = false;
    }
  }, []);

  useEffect(() => {
    if (!autoRefresh) {
      setStatus('paused');
      return undefined;
    }
    refresh();
    const timer = window.setInterval(() => {
      if (document.visibilityState === 'visible') refresh();
    }, REFRESH_INTERVAL_MS);
    return () => window.clearInterval(timer);
  }, [autoRefresh, refresh]);

  useEffect(() => {
    function onKeyDown(event) {
      const target = event.target;
      const editing =
        target instanceof HTMLElement &&
        (target.tagName === 'INPUT' ||
          target.tagName === 'TEXTAREA' ||
          target.isContentEditable);
      if (editing) {
        if (event.key === 'Escape') {
          setQuery('');
          target.blur();
        }
        return;
      }
      if (event.key === '/') {
        event.preventDefault();
        searchRef.current?.focus();
      } else if (event.key === 'Escape') {
        setDrawerOpen(false);
      }
    }
    window.addEventListener('keydown', onKeyDown);
    return () => window.removeEventListener('keydown', onKeyDown);
  }, []);

  useEffect(() => {
    return () => {
      if (copyTimer.current) window.clearTimeout(copyTimer.current);
    };
  }, []);

  function toggleDirectory(directoryPath) {
    setCollapsed((current) => {
      const next = new Set(current);
      if (next.has(directoryPath)) next.delete(directoryPath);
      else next.add(directoryPath);
      return next;
    });
  }

  function selectPage(relPath) {
    if (relPath === selectedRef.current) setPreviewNonce((value) => value + 1);
    setSelected(relPath);
    setIframeLoading(true);
    setDrawerOpen(false);
  }

  async function copyLink() {
    if (!selectedPage) return;
    const url = new URL(pageSrc(selectedPage.relPath), window.location.origin).toString();
    try {
      await navigator.clipboard.writeText(url);
      setCopied(true);
      if (copyTimer.current) window.clearTimeout(copyTimer.current);
      copyTimer.current = window.setTimeout(() => setCopied(false), 1600);
    } catch {
      setCopied(false);
    }
  }

  function toggleTheme() {
    const root = document.documentElement;
    const next = root.dataset.theme === 'dark' ? 'light' : 'dark';
    root.dataset.theme = next;
    try {
      localStorage.setItem('htmls-theme', next);
    } catch {
      undefined;
    }
  }

  function renderDirectory(node, depth) {
    if (!node) return null;
    const isCollapsed = query ? false : collapsed.has(node.path);
    const indent = 10 + depth * 14;
    const count = query ? node.matchedCount ?? node.pageCount : node.pageCount;

    return (
      <div className="tree-group" key={node.path || 'root'}>
        {node.path ? (
          <button
            type="button"
            className="tree-dir"
            style={{ paddingLeft: indent }}
            onClick={() => toggleDirectory(node.path)}
            aria-expanded={!isCollapsed}
          >
            <ChevronIcon open={!isCollapsed} />
            <span className="tree-icon">
              <FolderIcon />
            </span>
            <span className="tree-label">{node.name}</span>
            <span className="tree-count">{count}</span>
          </button>
        ) : null}

        {!isCollapsed ? (
          <div className="tree-children">
            {node.children.map((child) => renderDirectory(child, node.path ? depth + 1 : depth))}
            {node.pages.map((page) => {
              const active = selected === page.relPath;
              return (
                <button
                  type="button"
                  key={page.relPath}
                  className={`tree-page ${active ? 'is-active' : ''}`}
                  style={{ paddingLeft: indent + 18 }}
                  onClick={() => selectPage(page.relPath)}
                  title={page.relPath}
                  aria-current={active ? 'page' : undefined}
                >
                  <span className="tree-icon">
                    <FileIcon />
                  </span>
                  <span className="tree-label">{page.title}</span>
                  {page.fileName.toLowerCase() !== 'index.html' ? (
                    <span className="tree-file">{page.fileName}</span>
                  ) : null}
                </button>
              );
            })}
          </div>
        ) : null}
      </div>
    );
  }

  const statusLabel =
    status === 'error'
      ? '同步失败'
      : status === 'refreshing'
        ? '同步中'
        : status === 'paused'
          ? '已暂停'
          : '实时同步';

  const previewSrc = selectedPage ? pageSrc(selectedPage.relPath) : null;
  const hasSearch = query.trim().length > 0;

  return (
    <div className="app">
      <header className="topbar">
        <button
          type="button"
          className="icon-button menu-button"
          onClick={() => setDrawerOpen(true)}
          aria-label="打开目录"
        >
          <MenuIcon />
        </button>

        <div className="brand">
          <img src="/icon.svg" alt="" width="30" height="30" className="brand-logo" />
          <div className="brand-text">
            <div className="brand-line">
              <span className="brand-name">HTMLS</span>
              <span className="brand-badge">INDEX</span>
            </div>
            <span className="brand-sub">
              {data.totalPages} 个页面 · {data.totalDirectories} 个目录 · {formatBytes(data.totalBytes)}
            </span>
          </div>
        </div>

        <div className="topbar-actions">
          <span className={`status status-${status}`} title={`索引修订 ${data.revision}`}>
            <span className="status-dot" />
            {statusLabel}
          </span>

          <button
            type="button"
            className={`toggle ${autoRefresh ? 'is-on' : ''}`}
            onClick={() => setAutoRefresh((value) => !value)}
            aria-pressed={autoRefresh}
            title="每 5 秒检测新增或修改的 HTML"
          >
            <span className="toggle-track">
              <span className="toggle-thumb" />
            </span>
            <span className="toggle-label">自动刷新</span>
          </button>

          <button type="button" className="icon-button" onClick={refresh} aria-label="立即刷新" title="立即刷新">
            <RefreshIcon />
          </button>

          <button type="button" className="icon-button" onClick={toggleTheme} aria-label="切换深浅色" title="切换深浅色">
            <SunIcon />
            <MoonIcon />
          </button>
        </div>
      </header>

      <div className="workspace">
        <aside className={`sidebar ${drawerOpen ? 'is-open' : ''}`}>
          <div className="sidebar-head">
            <div className="search">
              <span className="search-icon">
                <SearchIcon />
              </span>
              <input
                ref={searchRef}
                type="search"
                value={query}
                onChange={(event) => setQuery(event.target.value)}
                placeholder="搜索标题、路径或描述"
                aria-label="搜索页面"
                spellCheck={false}
              />
              <kbd>/</kbd>
            </div>
            <div className="sidebar-summary">
              <span>
                {hasSearch
                  ? `筛选 ${filteredTree?.matchedCount ?? 0} / ${data.totalPages}`
                  : '按目录结构索引'}
              </span>
              <button
                type="button"
                className="link-button"
                onClick={() => setCollapsed((current) => (current.size ? new Set() : new Set(collectDirectories(data.tree))))}
              >
                {collapsed.size ? '全部展开' : '全部折叠'}
              </button>
            </div>
          </div>

          <nav className="tree" aria-label="HTML 页面目录">
            {filteredTree ? (
              renderDirectory(filteredTree, 0)
            ) : (
              <div className="tree-empty">
                <p>没有匹配的页面</p>
                <button type="button" className="link-button" onClick={() => setQuery('')}>
                  清除搜索
                </button>
              </div>
            )}
          </nav>

          <footer className="sidebar-foot">
            <div className="foot-row">
              <span className="foot-label">根目录</span>
              <span className="foot-value" title={data.root}>
                {data.root}
              </span>
            </div>
            <div className="foot-row">
              <span className="foot-label">修订</span>
              <span className="foot-value">
                {data.revision} · <Time ms={Date.parse(data.generatedAt)} nowMs={nowMs} />
              </span>
            </div>
            <div className="foot-actions">
              <a href="/api/pages" target="_blank" rel="noreferrer" className="foot-link">
                JSON 索引
              </a>
              <span className="foot-hint">新增或修改后 5 秒内更新</span>
            </div>
          </footer>
        </aside>

        {drawerOpen ? (
          <button
            type="button"
            className="backdrop"
            onClick={() => setDrawerOpen(false)}
            aria-label="关闭目录"
          />
        ) : null}

        <main className="main">
          {selectedPage ? (
            <section className="preview">
              <div className="preview-bar">
                <div className="preview-title" title={selectedPage.relPath}>
                  <span className="preview-dir">{selectedPage.dir || '根目录'}</span>
                  <span className="preview-sep">/</span>
                  <strong>{selectedPage.fileName}</strong>
                </div>
                <div className="preview-meta">
                  <span className="meta-chip">{formatBytes(selectedPage.size)}</span>
                  <span className="meta-chip">
                    <Time ms={selectedPage.mtimeMs} nowMs={nowMs} />
                  </span>
                </div>
                <div className="preview-actions">
                  <button type="button" className="ghost-button" onClick={copyLink}>
                    {copied ? <CheckIcon /> : <CopyIcon />}
                    {copied ? '已复制' : '复制链接'}
                  </button>
                  <a className="ghost-button" href={previewSrc} target="_blank" rel="noreferrer">
                    <ExternalIcon />
                    新标签打开
                  </a>
                  <button
                    type="button"
                    className="icon-button close-preview"
                    onClick={() => setSelected(null)}
                    aria-label="关闭预览"
                    title="关闭预览"
                  >
                    <CloseIcon />
                  </button>
                </div>
              </div>
              {iframeLoading ? <div className="loading-bar" /> : null}
              <iframe
                key={`${selectedPage.relPath}:${selectedPage.mtimeMs}:${previewNonce}`}
                className="preview-frame"
                src={previewSrc}
                title={selectedPage.title}
                onLoad={() => setIframeLoading(false)}
                referrerPolicy="no-referrer"
              />
            </section>
          ) : (
            <section className="welcome">
              <div className="welcome-head">
                <span className="eyebrow">HTMLS · LOCAL INDEX</span>
                <h1>仓库里的每个 HTML 页面，都在这里。</h1>
                <p>
                  按当前目录结构自动扫描 {data.totalPages} 个单文件页面。新增或编辑 HTML 后，索引会在 5 秒内同步；也可以随时手动刷新。
                </p>
                <div className="welcome-actions">
                  <button
                    type="button"
                    className="primary-button"
                    disabled={!recentPages.length}
                    onClick={() => recentPages[0] && selectPage(recentPages[0].relPath)}
                  >
                    阅读最近更新的页面
                  </button>
                  <button type="button" className="ghost-button" onClick={() => searchRef.current?.focus()}>
                    <SearchIcon />
                    搜索全部页面
                  </button>
                </div>
              </div>

              <div className="stats-caption">
                <span>数据统计</span>
                <span className="stats-sync">
                  <span className={`status-dot dot-${status}`} />
                  {statusLabel} · 修订 {data.revision}
                </span>
              </div>
              <div className="stat-grid">
                <div className="stat-card">
                  <span className="stat-label">页面</span>
                  <strong>{data.totalPages}</strong>
                  <span className="stat-note">
                    {data.indexPages} 个索引页 · {data.contentPages} 个内容页
                  </span>
                </div>
                <div className="stat-card">
                  <span className="stat-label">目录</span>
                  <strong>{data.totalDirectories}</strong>
                  <span className="stat-note">
                    {data.topLevelDirectories} 个顶级 · {data.subDirectories} 个子目录
                  </span>
                </div>
                <div className="stat-card">
                  <span className="stat-label">体积</span>
                  <strong>{formatBytes(data.totalBytes)}</strong>
                  <span className="stat-note">平均 {formatBytes(data.averageBytes)} / 页</span>
                </div>
                <div
                  className="stat-card"
                  title={
                    data.latestPage
                      ? `最近更新：${data.latestPage.title}（${data.latestPage.relPath}）`
                      : undefined
                  }
                >
                  <span className="stat-label">最近更新</span>
                  <strong className="stat-time">
                    <Time ms={data.latestMtimeMs} nowMs={nowMs} />
                  </strong>
                  <span className="stat-note">
                    {data.updatedLast24h > 0
                      ? `近 24 小时更新 ${data.updatedLast24h} 个`
                      : '近 24 小时无更新'}
                  </span>
                </div>
              </div>
              <p className="stats-note">
                统计范围：项目根目录下的 .html / .htm，排除隐藏目录、node_modules 与 web 自身；更新时间为相对时间，悬停可查看 UTC 时间戳。
              </p>

              <div className="block-head">
                <h2>可视化统计</h2>
                <span>按文件修改时间与顶层目录</span>
              </div>
              <div className="chart-grid">
                <article className="chart-panel">
                  <div className="chart-head">
                    <div>
                      <h3>每日更新</h3>
                      <p>近 {range} 天 · UTC 日期 · 按文件修改时间</p>
                    </div>
                    <div className="range-toggle" role="group" aria-label="时间范围">
                      {[14, 30].map((value) => (
                        <button
                          key={value}
                          type="button"
                          className={range === value ? 'is-active' : ''}
                          aria-pressed={range === value}
                          onClick={() => {
                            setRange(value);
                            setHoveredIndex(null);
                          }}
                        >
                          {value} 天
                        </button>
                      ))}
                    </div>
                  </div>

                  <div className="chart-metrics">
                    <span>
                      <strong>{activityStats.total}</strong>更新总数
                    </span>
                    <span>
                      <strong>{activityStats.activeDays}</strong>活跃天数
                    </span>
                    <span>
                      <strong>{activityStats.peak.count}</strong>单日峰值
                    </span>
                    <span>
                      <strong>{(activityStats.total / Math.max(1, range)).toFixed(1)}</strong>日均
                    </span>
                  </div>

                  <div className="chart-readout" aria-live="polite">
                    {hoveredDay
                      ? `${hoveredDay.date} · ${hoveredDay.count} 个页面 · ${formatBytes(hoveredDay.bytes)}`
                      : '悬停或点按柱状图查看单日数据'}
                  </div>

                  <div
                    className="bar-chart"
                    role="group"
                    aria-label={`近 ${range} 天每日更新页面数`}
                  >
                    {activityStats.days.map((day, index) => {
                      const height =
                        day.count === 0
                          ? 2
                          : Math.max(4, Math.round((day.count / activityStats.max) * 100));
                      const showLabel =
                        index === 0 ||
                        index === activityStats.days.length - 1 ||
                        index % labelStep === 0;
                      return (
                        <div
                          className={`bar-col ${
                            index === activityStats.days.length - 1 ? 'is-today' : ''
                          }`}
                          key={day.date}
                        >
                          <button
                            type="button"
                            className="bar-hit"
                            title={`${day.date} · ${day.count} 个页面 · ${formatBytes(day.bytes)}`}
                            aria-label={`${day.date} 更新 ${day.count} 个页面`}
                            onMouseEnter={() => setHoveredIndex(index)}
                            onMouseLeave={() => setHoveredIndex(null)}
                            onFocus={() => setHoveredIndex(index)}
                            onBlur={() => setHoveredIndex(null)}
                            onClick={() => setHoveredIndex(index)}
                          >
                            <span
                              className={`bar ${day.count === 0 ? 'is-zero' : ''}`}
                              style={{ height: `${height}%` }}
                            />
                          </button>
                          <span className="bar-label">
                            {showLabel ? day.date.slice(5) : ''}
                          </span>
                        </div>
                      );
                    })}
                  </div>
                </article>

                <article className="chart-panel donut-panel">
                  <div className="chart-head">
                    <div>
                      <h3>目录分布</h3>
                      <p>{distribution.length} 个顶层分组 · {data.totalPages} 个页面</p>
                    </div>
                  </div>
                  <DonutChart distribution={distribution} total={data.totalPages} />
                </article>
              </div>

              <div className="block-head">
                <h2>按目录浏览</h2>
                <span>{sections.length} 个顶层目录</span>
              </div>
              <div className="section-grid">
                {sections.map((section) => (
                  <article className="section-card" key={section.path}>
                    <button
                      type="button"
                      className="section-head"
                      onClick={() => section.first && selectPage(section.first.relPath)}
                      disabled={!section.first}
                    >
                      <span className="section-name">{section.name}</span>
                      <span className="section-count">{section.count}</span>
                    </button>
                    <span className="section-share" aria-hidden="true">
                      <span
                        style={{
                          width: `${Math.max(
                            2,
                            Math.round((section.count / Math.max(1, data.totalPages)) * 100),
                          )}%`,
                        }}
                      />
                    </span>
                    <ul className="section-pages">
                      {section.pages.map((page) => (
                        <li key={page.relPath}>
                          <button type="button" onClick={() => selectPage(page.relPath)} title={page.relPath}>
                            {page.title}
                          </button>
                        </li>
                      ))}
                    </ul>
                  </article>
                ))}
              </div>

              <div className="block-head">
                <h2>最近修改</h2>
                <span>按文件时间倒序</span>
              </div>
              <ul className="recent-list">
                {recentPages.map((page) => (
                  <li key={page.relPath}>
                    <button type="button" onClick={() => selectPage(page.relPath)}>
                      <span className="recent-main">
                        <span className="recent-title">{page.title}</span>
                        <span className="recent-path">{page.relPath}</span>
                      </span>
                      <span className="recent-time">
                        <Time ms={page.mtimeMs} nowMs={nowMs} />
                      </span>
                    </button>
                  </li>
                ))}
              </ul>
            </section>
          )}
        </main>
      </div>
    </div>
  );
}

function collectDirectories(node, output = []) {
  for (const child of node.children) {
    output.push(child.path);
    collectDirectories(child, output);
  }
  return output;
}
