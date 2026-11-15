import { MATRIX_LABELS } from './constants';
import { actors, allTactics, bibliography } from './data';
import { seg } from './route';

export type SearchKind = 'tactic' | 'indicator' | 'countermeasure' | 'protocol' | 'actor' | 'source';

export const SEARCH_KIND_LABELS: Record<SearchKind, string> = {
  tactic: 'Tactics',
  indicator: 'Indicators',
  countermeasure: 'Countermeasures',
  protocol: 'Response Protocols',
  actor: 'Actor Profiles',
  source: 'Sources',
};

export const SEARCH_KIND_ORDER: SearchKind[] = [
  'tactic',
  'indicator',
  'countermeasure',
  'protocol',
  'actor',
  'source',
];

export interface SearchDoc {
  kind: SearchKind;
  id: string;
  title: string;
  context: string;
  matrix: string | null;
  to: string;
  idLower: string;
  titleLower: string;
  hay: string;
}

let index: SearchDoc[] | null = null;

function build(): SearchDoc[] {
  const docs: SearchDoc[] = [];
  const add = (kind: SearchKind, id: string, title: string, context: string, matrix: string | null, to: string, extra = '') => {
    const idLower = id.toLowerCase();
    const titleLower = title.toLowerCase();
    docs.push({ kind, id, title, context, matrix, to, idLower, titleLower, hay: `${idLower} ${titleLower} ${extra.toLowerCase()}` });
  };
  allTactics.forEach((t) => {
    const m = t.matrix;
    const where = `${MATRIX_LABELS[m] || m} · ${t.id} ${t.name}`;
    add('tactic', t.id, t.name, `${MATRIX_LABELS[m] || m} · Phase ${t.phase}`, m, `/${m}/tactic/${seg(t.id)}`);
    t.indicators.forEach((i) => add('indicator', i.id, i.behavior, where, m, `/${m}/indicator/${seg(i.id)}`));
    t.countermeasures.forEach((c) =>
      add('countermeasure', c.id, c.measure, where, m, `/${m}/tactic/${seg(t.id)}/${seg(c.id)}`)
    );
    t.response_protocols.forEach((r) =>
      add('protocol', r.id, r.action, where, m, `/${m}/tactic/${seg(t.id)}/${seg(r.id)}`, r.trigger)
    );
  });
  actors.forEach((a) => add('actor', a.id, a.name, a.category_label, null, `/actors/${seg(a.id)}`));
  bibliography.forEach((b, key) =>
    add('source', key, b.title, `${b.author} · ${b.date}`, null, `/references/${seg(key)}`, b.author)
  );
  return docs;
}

export interface SearchResults {
  total: number;
  groups: { kind: SearchKind; hits: SearchDoc[] }[];
}

export const MIN_QUERY = 2;

// Case-insensitive match on every whitespace-separated term. Ranked by where
// the query lands: exact ID, ID prefix, name or text start, name or text,
// then the remaining searchable text.
export function search(query: string): SearchResults {
  const q = query.trim().toLowerCase();
  if (q.length < MIN_QUERY) return { total: 0, groups: [] };
  if (!index) index = build();
  const terms = q.split(/\s+/);
  const scored: { doc: SearchDoc; rank: number }[] = [];
  for (const doc of index) {
    if (!terms.every((t) => doc.hay.includes(t))) continue;
    const rank =
      doc.idLower === q ? 0
      : doc.idLower.startsWith(q) ? 1
      : doc.titleLower.startsWith(q) ? 2
      : doc.titleLower.includes(q) ? 3
      : 4;
    scored.push({ doc, rank });
  }
  scored.sort((a, b) => a.rank - b.rank);
  const groups = SEARCH_KIND_ORDER.map((kind) => ({
    kind,
    hits: scored.filter((s) => s.doc.kind === kind).map((s) => s.doc),
  })).filter((g) => g.hits.length > 0);
  return { total: scored.length, groups };
}
