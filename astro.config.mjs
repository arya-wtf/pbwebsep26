import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import { readdirSync, readFileSync } from 'node:fs';

// Draft entries (`draft: true` in frontmatter) are built so they can be previewed,
// but they carry <meta name="robots" content="noindex"> and are kept out of the sitemap and RSS.
const draftSlugs = readdirSync('./src/content/log')
  .filter((f) => f.endsWith('.md') && /^draft:\s*true/m.test(readFileSync(`./src/content/log/${f}`, 'utf8')))
  .map((f) => f.replace(/\.md$/, ''));

// https://astro.build/config
export default defineConfig({
  site: 'https://arya.wtf',
  output: 'static',
  trailingSlash: 'never',
  build: { format: 'file' },
  integrations: [
    sitemap({
      filter: (page) => !draftSlugs.some((s) => page.endsWith(`/log/${s}`)) && !page.endsWith('/404'),
    }),
  ],
});
