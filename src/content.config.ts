import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

/**
 * The log. One markdown file per entry in src/content/log/.
 * Filename = slug = URL (/log/<slug>). Prefix a filename with "_" to keep it out of the sitemap.
 * Rule: no number, no entry. The eight fixed fields live in frontmatter so every entry can be compared.
 */
const log = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/log' }),
  schema: z.object({
    title: z.string(),
    summary: z.string(),
    date: z.coerce.date(),
    revised: z.coerce.date().optional(),
    verdict: z.enum(['automate', 'assist', 'leave']),
    source: z.string(), // "Elux Space · own work", "Client · logistics", "Audit", "Own build"
    draft: z.boolean().default(false),
    fields: z.object({
      work: z.string(),
      before: z.string(),
      verdict: z.string(),
      refused: z.string(),
      result: z.string(),
      uncomfortable: z.string(),
      tools: z.string(),
    }),
  }),
});

export const collections = { log };
