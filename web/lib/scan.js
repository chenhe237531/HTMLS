import { createHash } from 'node:crypto';
import { promises as fs, readFileSync } from 'node:fs';
import path from 'node:path';

function resolveProjectRoot() {
  if (process.env.HTML_ROOT) return path.resolve(process.env.HTML_ROOT);
  const cwd = process.cwd();
  try {
    const manifest = JSON.parse(readFileSync(path.join(cwd, 'package.json'), 'utf8'));
    if (manifest.name === 'htmls-web-index') return path.dirname(cwd);
  } catch {
    return cwd;
  }
  return cwd;
}

export const PROJECT_ROOT = resolveProjectRoot();

const TOP_LEVEL_EXCLUDES = new Set(['web', 'node_modules']);
const HTML_EXTENSION = /\.html?$/i;
const metaCache = new Map();

export function isExcludedRelative(relativePath) {
  if (!relativePath) return false;
  const parts = relativePath.split('/');
  if (parts.some((part) => part === 'node_modules')) return true;
  if (parts.some((part) => part.startsWith('.'))) return true;
  return TOP_LEVEL_EXCLUDES.has(parts[0]);
}

function decodeEntities(value) {
  return value
    .replace(/&#x([0-9a-f]+);/gi, (match, hex) => {
      const code = Number.parseInt(hex, 16);
      return Number.isFinite(code) && code >= 0 && code <= 0x10ffff
        ? String.fromCodePoint(code)
        : match;
    })
    .replace(/&#(\d+);/g, (match, decimal) => {
      const code = Number(decimal);
      return Number.isFinite(code) && code >= 0 && code <= 0x10ffff
        ? String.fromCodePoint(code)
        : match;
    })
    .replace(/&(amp|lt|gt|quot|apos|nbsp);/g, (match, name) => {
      return { amp: '&', lt: '<', gt: '>', quot: '"', apos: "'", nbsp: ' ' }[name] ?? match;
    });
}

function cleanText(value) {
  return decodeEntities(value.replace(/<[^>]*>/g, ' '))
    .replace(/\s+/g, ' ')
    .trim();
}

function truncate(value, max) {
  return value.length > max ? `${value.slice(0, max - 1).trimEnd()}…` : value;
}

function readMeta(html, relativePath) {
  let title = '';
  let description = '';

  const titleMatch = html.match(/<title[^>]*>([\s\S]*?)<\/title>/i);
  if (titleMatch) title = cleanText(titleMatch[1]);

  for (const tag of html.match(/<meta\b[^>]*>/gi) ?? []) {
    if (!/\bname\s*=\s*["']description["']/i.test(tag)) continue;
    const content = tag.match(/\bcontent\s*=\s*"([^"]*)"/i) ?? tag.match(/\bcontent\s*=\s*'([^']*)'/i);
    if (content) {
      description = cleanText(content[1]);
      break;
    }
  }

  if (!title) {
    const heading = html.match(/<h1[^>]*>([\s\S]*?)<\/h1>/i);
    if (heading) title = cleanText(heading[1]);
  }

  if (!title) {
    const fileName = relativePath.split('/').pop();
    if (fileName.toLowerCase() === 'index.html' || fileName.toLowerCase() === 'index.htm') {
      const parent = relativePath.split('/').slice(-2, -1)[0];
      title = parent || 'index';
    } else {
      title = fileName.replace(HTML_EXTENSION, '');
    }
  }

  return {
    title: truncate(title, 180),
    description: truncate(description, 240),
  };
}

async function collectFiles(root) {
  const files = [];

  async function visit(absoluteDir, relativeDir) {
    let entries;
    try {
      entries = await fs.readdir(absoluteDir, { withFileTypes: true });
    } catch {
      return;
    }

    for (const entry of entries) {
      const relativePath = relativeDir ? `${relativeDir}/${entry.name}` : entry.name;
      if (isExcludedRelative(relativePath)) continue;
      const absolutePath = path.join(absoluteDir, entry.name);
      if (entry.isDirectory()) {
        await visit(absolutePath, relativePath);
      } else if (entry.isFile() && HTML_EXTENSION.test(entry.name)) {
        files.push({ absolutePath, relativePath });
      }
    }
  }

  await visit(root, '');
  return files;
}

function countPages(node) {
  return node.pages.length + node.children.reduce((total, child) => total + countPages(child), 0);
}

function countDirectories(node) {
  return node.children.length + node.children.reduce((total, child) => total + countDirectories(child), 0);
}

const DAY_MS = 86400000;

function utcDayStart(ms) {
  const date = new Date(ms);
  return Date.UTC(date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate());
}

function buildDailyActivity(pages, nowMs, days) {
  const todayStart = utcDayStart(nowMs);
  const buckets = [];
  const byDate = new Map();

  for (let offset = days - 1; offset >= 0; offset -= 1) {
    const start = todayStart - offset * DAY_MS;
    const date = new Date(start).toISOString().slice(0, 10);
    const bucket = { date, count: 0, bytes: 0 };
    buckets.push(bucket);
    byDate.set(date, bucket);
  }

  for (const page of pages) {
    const date = new Date(utcDayStart(page.mtimeMs)).toISOString().slice(0, 10);
    const bucket = byDate.get(date);
    if (bucket) {
      bucket.count += 1;
      bucket.bytes += page.size;
    }
  }

  return buckets;
}

function buildTree(pages) {
  const root = { name: '', path: '', type: 'dir', children: [], pages: [], pageCount: 0 };
  const directories = new Map([['', root]]);

  function ensureDirectory(directoryPath) {
    if (directories.has(directoryPath)) return directories.get(directoryPath);
    const parentPath = directoryPath.includes('/')
      ? directoryPath.slice(0, directoryPath.lastIndexOf('/'))
      : '';
    const parent = ensureDirectory(parentPath);
    const node = {
      name: directoryPath.split('/').pop(),
      path: directoryPath,
      type: 'dir',
      children: [],
      pages: [],
      pageCount: 0,
    };
    parent.children.push(node);
    directories.set(directoryPath, node);
    return node;
  }

  for (const page of pages) ensureDirectory(page.dir).pages.push(page);

  for (const node of directories.values()) node.pageCount = countPages(node);

  function finalize(node) {
    node.children.sort((a, b) => a.name.localeCompare(b.name, 'zh-Hans-CN'));
    node.pages.sort((a, b) => a.title.localeCompare(b.title, 'zh-Hans-CN'));
    node.children.forEach(finalize);
  }

  finalize(root);
  return root;
}

export async function scanPages() {
  let root = PROJECT_ROOT;
  try {
    root = await fs.realpath(root);
  } catch {
    root = PROJECT_ROOT;
  }

  const files = await collectFiles(root);
  const pages = [];
  const seen = new Set();

  for (const file of files) {
    let stat;
    try {
      stat = await fs.stat(file.absolutePath);
    } catch {
      continue;
    }
    if (!stat.isFile()) continue;

    seen.add(file.relativePath);
    const cached = metaCache.get(file.relativePath);
    let meta;

    if (cached && cached.mtimeMs === stat.mtimeMs && cached.size === stat.size) {
      meta = cached.meta;
    } else {
      let html = '';
      try {
        html = await fs.readFile(file.absolutePath, 'utf8');
      } catch {
        html = '';
      }
      meta = readMeta(html, file.relativePath);
      metaCache.set(file.relativePath, { mtimeMs: stat.mtimeMs, size: stat.size, meta });
    }

    const directory = file.relativePath.includes('/')
      ? file.relativePath.slice(0, file.relativePath.lastIndexOf('/'))
      : '';

    pages.push({
      ...meta,
      relPath: file.relativePath,
      fileName: file.relativePath.split('/').pop(),
      dir: directory,
      size: stat.size,
      mtimeMs: stat.mtimeMs,
    });
  }

  for (const key of metaCache.keys()) {
    if (!seen.has(key)) metaCache.delete(key);
  }

  pages.sort((a, b) => a.relPath.localeCompare(b.relPath, 'zh-Hans-CN'));

  const revision = createHash('sha1')
    .update(pages.map((page) => `${page.relPath}:${page.mtimeMs}:${page.size}:${page.title}`).join('\n'))
    .digest('hex')
    .slice(0, 16);

  const tree = buildTree(pages);
  const totalBytes = pages.reduce((total, page) => total + page.size, 0);
  const totalDirectories = countDirectories(tree);
  const indexPages = pages.filter((page) => page.fileName.toLowerCase() === 'index.html').length;
  const latestPage = pages.reduce(
    (latest, page) => (!latest || page.mtimeMs > latest.mtimeMs ? page : latest),
    null,
  );
  const now = Date.now();

  return {
    generatedAt: new Date().toISOString(),
    revision,
    root,
    totalPages: pages.length,
    totalDirectories,
    totalBytes,
    latestMtimeMs: latestPage ? latestPage.mtimeMs : 0,
    indexPages,
    contentPages: pages.length - indexPages,
    topLevelDirectories: tree.children.length,
    subDirectories: totalDirectories - tree.children.length,
    averageBytes: pages.length ? Math.round(totalBytes / pages.length) : 0,
    updatedLast24h: pages.filter((page) => now - page.mtimeMs <= 86400000).length,
    latestPage: latestPage
      ? { relPath: latestPage.relPath, title: latestPage.title, mtimeMs: latestPage.mtimeMs }
      : null,
    activity: buildDailyActivity(pages, now, 30),
    tree,
  };
}
