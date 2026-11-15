import { isMatrixKey, MODALITY_ORDER, type MatrixKey } from './constants';
import { actorById, bibliography, childById, indicatorById, reservedActorById, tacticById } from './data';

export type LiveMatrix = MatrixKey;

export type Route =
  | { view: 'overview' }
  | { view: 'heatmap'; matrix: MatrixKey }
  | { view: 'phase'; matrix: MatrixKey; phase: 1 | 2 | 3 | 4; track: 'flight' | 'claim' | null }
  | { view: 'tactic'; matrix: MatrixKey; tacticId: string; focusId: string | null }
  | { view: 'indicator'; matrix: MatrixKey; indicatorId: string }
  | { view: 'actors' }
  | { view: 'actorDetail'; actorId: string }
  | { view: 'reservedActor'; actorId: string; reason: string }
  | { view: 'references'; citedKey: string | null }
  | { view: 'search'; query: string }
  | { view: 'notFound'; what: string };

export interface Filters {
  mode: string;
  actor: string;
}

export interface Location {
  route: Route;
  filters: Filters;
}

const NO_FILTERS: Filters = { mode: '', actor: '' };

// Anything echoed back to the page from the URL is clipped, so a very long
// hash cannot flood the not-found view.
const clip = (s: string) => (s.length > 60 ? s.slice(0, 60) + '...' : s);

const decode = (s: string): string => {
  try {
    return decodeURIComponent(s);
  } catch {
    return s;
  }
};

const notFound = (what: string): Route => ({ view: 'notFound', what: clip(what) });

export const isMatrixView = (r: Route): boolean =>
  r.view === 'overview' || r.view === 'heatmap' || r.view === 'phase' || r.view === 'tactic';

function parsePath(p: string[]): Route {
  if (!p.length) return { view: 'overview' };
  const [head, a, b, c] = p;

  if (head === 'references') {
    if (p.length === 1) return { view: 'references', citedKey: null };
    if (p.length === 2 && bibliography.has(a)) return { view: 'references', citedKey: a };
    return notFound(`Source ${a}`);
  }
  if (head === 'search') {
    if (p.length > 2) return notFound(p.join('/'));
    return { view: 'search', query: (a || '').slice(0, 200) };
  }
  if (head === 'actors') {
    if (p.length === 1) return { view: 'actors' };
    if (p.length === 2 && actorById.has(a)) return { view: 'actorDetail', actorId: a };
    if (p.length === 2 && reservedActorById.has(a)) {
      return { view: 'reservedActor', actorId: a, reason: reservedActorById.get(a) || '' };
    }
    return notFound(`Actor profile ${a}`);
  }
  if (isMatrixKey(head)) {
    if (p.length === 1) return { view: 'heatmap', matrix: head };
    if (a === 'phase' && (p.length === 3 || p.length === 4)) {
      if (!/^[1-4]$/.test(b || '')) return notFound(`Phase ${b}`);
      const phase = Number(b) as 1 | 2 | 3 | 4;
      if (p.length === 4) {
        if (phase !== 4 || (c !== 'flight' && c !== 'claim')) return notFound(`Phase ${b} track ${c}`);
        return { view: 'phase', matrix: head, phase, track: c };
      }
      return { view: 'phase', matrix: head, phase, track: null };
    }
    if (a === 'tactic' && (p.length === 3 || p.length === 4)) {
      const t = tacticById.get(b);
      if (!t) return notFound(`Tactic ${b}`);
      let focusId: string | null = null;
      if (p.length === 4) {
        const child = childById.get(c);
        if (!child || child.tactic !== t) return notFound(`${c} in tactic ${b}`);
        focusId = c;
      }
      // The matrix comes from the object, not the URL, so the active tab is
      // always the one the tactic belongs to.
      return { view: 'tactic', matrix: t.matrix as MatrixKey, tacticId: t.id, focusId };
    }
    if (a === 'indicator' && p.length === 3) {
      const e = indicatorById.get(b);
      if (!e) return notFound(`Indicator ${b}`);
      return { view: 'indicator', matrix: e.tactic.matrix as MatrixKey, indicatorId: b };
    }
  }
  return notFound(p.join('/'));
}

function parseFilters(query: string): Filters {
  if (!query) return NO_FILTERS;
  let mode = '';
  let actor = '';
  query.split('&').forEach((pair) => {
    const i = pair.indexOf('=');
    if (i < 0) return;
    const k = pair.slice(0, i);
    const v = decode(pair.slice(i + 1));
    if (k === 'mode' && MODALITY_ORDER.includes(v)) mode = v;
    if (k === 'actor' && actorById.has(v)) actor = v;
  });
  return mode || actor ? { mode, actor } : NO_FILTERS;
}

export function parseLocation(hash: string = window.location.hash): Location {
  const raw = hash.replace(/^#\/?/, '');
  const q = raw.indexOf('?');
  const path = q < 0 ? raw : raw.slice(0, q);
  const segs = path.split('/').filter(Boolean).map(decode);
  const route = parsePath(segs);
  // Filters apply to the matrix views only.
  const filters = q >= 0 && isMatrixView(route) ? parseFilters(raw.slice(q + 1)) : NO_FILTERS;
  return { route, filters };
}

export function filterQuery(f: Filters): string {
  const parts: string[] = [];
  if (f.mode) parts.push(`mode=${encodeURIComponent(f.mode)}`);
  if (f.actor) parts.push(`actor=${encodeURIComponent(f.actor)}`);
  return parts.length ? `?${parts.join('&')}` : '';
}

const MATRIX_PATH = /^\/(?:$|(?:person|facility|organization|infrastructure)(?:$|\/(?:phase|tactic)\/))/;

// Build an in-app href. Active filters ride along to matrix views so a
// filtered link can be shared and survives reload.
export function hrefFor(path: string, filters: Filters = NO_FILTERS): string {
  const carry = MATRIX_PATH.test(path) ? filterQuery(filters) : '';
  return `#${path}${carry}`;
}

export const seg = (s: string): string => encodeURIComponent(s);

// The path of the current route without filters, for rewriting the filter
// query in place.
export function pathOf(r: Route): string {
  switch (r.view) {
    case 'heatmap':
      return `/${r.matrix}`;
    case 'phase':
      return `/${r.matrix}/phase/${r.phase}${r.track ? '/' + r.track : ''}`;
    case 'tactic':
      return `/${r.matrix}/tactic/${seg(r.tacticId)}${r.focusId ? '/' + seg(r.focusId) : ''}`;
    default:
      return '/';
  }
}
