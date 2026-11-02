import { promises as fs } from 'node:fs';
import path from 'node:path';

import { PROJECT_ROOT, isExcludedRelative } from '@/lib/scan';

export const dynamic = 'force-dynamic';
export const revalidate = 0;
export const runtime = 'nodejs';

const HTML_EXTENSION = /\.html?$/i;
const TEXT_EXTENSIONS = new Set(['.md', '.markdown', '.txt']);

function contentTypeFor(filePath) {
  const extension = path.extname(filePath).toLowerCase();
  if (HTML_EXTENSION.test(filePath)) return 'text/html; charset=utf-8';
  if (TEXT_EXTENSIONS.has(extension)) return 'text/plain; charset=utf-8';
  return null;
}

function notFound() {
  return new Response('Not found', {
    status: 404,
    headers: {
      'content-type': 'text/plain; charset=utf-8',
      'cache-control': 'no-store',
    },
  });
}

export async function GET(_request, { params }) {
  const resolved = await params;
  const segments = resolved?.path ?? [];

  if (!Array.isArray(segments) || segments.length === 0) return notFound();
  if (
    segments.some(
      (segment) =>
        !segment ||
        segment === '.' ||
        segment === '..' ||
        segment.includes('/') ||
        segment.includes('\\') ||
        segment.includes('\0') ||
        segment.startsWith('.'),
    )
  ) {
    return notFound();
  }

  let root;
  try {
    root = await fs.realpath(PROJECT_ROOT);
  } catch {
    return notFound();
  }

  let target = path.join(root, ...segments);
  try {
    const targetStat = await fs.stat(target);
    if (targetStat.isDirectory()) target = path.join(target, 'index.html');
  } catch {
    return notFound();
  }

  let realTarget;
  try {
    realTarget = await fs.realpath(target);
  } catch {
    return notFound();
  }

  if (realTarget !== root && !realTarget.startsWith(root + path.sep)) return notFound();
  const contentType = contentTypeFor(realTarget);
  if (!contentType) return notFound();

  const relativePath = path.relative(root, realTarget).split(path.sep).join('/');
  if (!relativePath || isExcludedRelative(relativePath)) return notFound();

  let stat;
  try {
    stat = await fs.stat(realTarget);
  } catch {
    return notFound();
  }
  if (!stat.isFile()) return notFound();

  const html = await fs.readFile(realTarget);

  return new Response(html, {
    headers: {
      'content-type': contentType,
      'cache-control': 'no-store, max-age=0',
      'x-content-type-options': 'nosniff',
    },
  });
}
