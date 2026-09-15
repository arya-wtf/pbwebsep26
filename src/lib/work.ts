// Temporary list — Arya will revise. Client work lives on elux.space.
export type Work = { year: string; name: string; kind: string; desc: string; url?: string; meta: string };
export const WORK: Work[] = [
  { year: '2026', name: 'arya-taste', kind: 'Open source · agent skill', desc: 'An anti-slop frontend method for coding agents. Twelve committed styles, six textures, eight bug classes that ship silently. Works across 70+ agents.', url: 'https://github.com/arya-wtf/arya-taste', meta: 'GitHub' },
  { year: '2026', name: 'vimemory', kind: 'Open source · MCP server', desc: 'A Python memory MCP server, with a local variant and a remote Cloudflare Worker.', url: 'https://github.com/arya-wtf/vimemory', meta: 'GitHub' },
  { year: '2026', name: 'Esflows', kind: 'Product · beta', desc: 'Node-based AI image studio on Cloudflare. Next.js 16, React Flow.', url: 'https://github.com/arya-wtf/esflowsbeta', meta: 'GitHub' },
  { year: '2026', name: 'mrktelx', kind: 'Internal tool', desc: 'Sales commission and deal approval for a small studio.', url: 'https://github.com/arya-wtf/mrktelx', meta: 'GitHub' },
  { year: '2025–', name: 'OpenClaw', kind: 'Open source · infrastructure', desc: 'AI infrastructure for a small team — each person gets their own agent, on a self-hosted server.', meta: 'In progress' },
  { year: '2025–', name: 'ERPS', kind: 'Internal platform', desc: 'The studio’s own ERP: project tracker, HR, money — folded into one Next.js monolith.', meta: 'Internal' },
];
