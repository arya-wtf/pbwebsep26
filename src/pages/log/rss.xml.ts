import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';
import type { APIContext } from 'astro';
import { IDENT } from '../../lib/site';

export async function GET(context: APIContext) {
  const entries = (await getCollection('log')).filter((e) => !e.data.draft).sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf());
  return rss({
    title: 'arya.wtf — the log',
    description: IDENT,
    site: context.site!,
    items: entries.map((e) => ({ title: e.data.title, description: e.data.summary, pubDate: e.data.date, link: `/log/${e.id}` })),
  });
}
