export const SITE = 'https://arya.wtf';
export const NAME = 'Arya Pradana';
export const IDENT =
  'Founder of Elux Space, an AI-native design studio in Yogyakarta. I help owners decide what AI should automate, what it should assist, and what it should never touch.';
export const IDENT_LEAD = 'Founder of Elux Space, an AI-native design studio in Yogyakarta.';
export const IDENT_REST =
  'I help owners decide what AI should automate, what it should assist, and what it should never touch.';

export const NAV = [
  ['/', 'Home'],
  ['/about', 'Record'],
  ['/method', 'Method'],
  ['/work', 'Work'],
  ['/log', 'Log'],
  ['/hire', 'Hire'],
  ['/now', 'Now'],
] as const;

export const PERSON_ID = `${SITE}/#person`;
export const ORG_ID = 'https://elux.space/#organization';

/** Shared JSON-LD nodes. Every page carries these so the entity resolves the same everywhere. */
export function baseGraph() {
  return [
    {
      '@type': 'Person',
      '@id': PERSON_ID,
      name: NAME,
      url: `${SITE}/`,
      image: `${SITE}/img/hero.webp`,
      jobTitle: 'Founder',
      description: IDENT,
      worksFor: { '@id': ORG_ID },
      alumniOf: [
        { '@type': 'CollegeOrUniversity', name: 'Institut Teknologi Sepuluh Nopember' },
        { '@type': 'CollegeOrUniversity', name: 'Sekolah Bisnis dan Manajemen, Institut Teknologi Bandung' },
      ],
      homeLocation: { '@type': 'Place', name: 'Yogyakarta, Indonesia' },
      knowsAbout: ['AI adoption in small businesses', 'Design studio operations', 'UI/UX design', 'Software development'],
      sameAs: ['https://www.linkedin.com/in/aryapradana/', 'https://github.com/arya-wtf', 'https://elux.space'],
    },
    {
      '@type': 'Organization',
      '@id': ORG_ID,
      name: 'Elux Space',
      url: 'https://elux.space',
      founder: { '@id': PERSON_ID },
      foundingDate: '2022-02',
      location: { '@type': 'Place', name: 'Yogyakarta, Indonesia' },
    },
    {
      '@type': 'WebSite',
      '@id': `${SITE}/#website`,
      url: `${SITE}/`,
      name: 'arya.wtf',
      publisher: { '@id': PERSON_ID },
      inLanguage: 'en',
    },
  ];
}

export function faq(items: [string, string][]) {
  return {
    '@type': 'FAQPage',
    mainEntity: items.map(([q, a]) => ({
      '@type': 'Question',
      name: q,
      acceptedAnswer: { '@type': 'Answer', text: a },
    })),
  };
}

export const iso = (d: Date) => d.toISOString().slice(0, 10);
