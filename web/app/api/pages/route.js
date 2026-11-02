import { scanPages } from '@/lib/scan';

export const dynamic = 'force-dynamic';
export const revalidate = 0;
export const runtime = 'nodejs';

export async function GET() {
  try {
    const data = await scanPages();
    return Response.json(data, {
      headers: {
        'cache-control': 'no-store, max-age=0',
      },
    });
  } catch (error) {
    return Response.json(
      { error: error instanceof Error ? error.message : 'Failed to scan HTML pages' },
      {
        status: 500,
        headers: { 'cache-control': 'no-store, max-age=0' },
      },
    );
  }
}
