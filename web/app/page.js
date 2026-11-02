import Explorer from '@/components/Explorer';
import { scanPages } from '@/lib/scan';

export const dynamic = 'force-dynamic';
export const revalidate = 0;

export default async function HomePage() {
  const data = await scanPages();
  return <Explorer initialData={data} />;
}
