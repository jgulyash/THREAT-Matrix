import { MATRICES } from './constants';

// Matrices with full browser rendering; organization/infrastructure remain stubs.
export type LiveMatrix = 'person' | 'facility';
export const LIVE_MATRICES = MATRICES.filter((m) => m.version === null).map(
  (m) => m.key
) as LiveMatrix[];

export type Route =
  | { view: 'heatmap'; matrix: LiveMatrix }
  | { view: 'phase'; matrix: LiveMatrix; phase: number; track: string | null }
  | { view: 'tactic'; matrix: LiveMatrix; tacticId: string }
  | { view: 'indicator'; matrix: LiveMatrix; indicatorId: string }
  | { view: 'actors' }
  | { view: 'actorDetail'; actorId: string }
  | { view: 'stub'; matrix: 'organization' | 'infrastructure' }
  | { view: 'references' };

export function parseRoute(): Route {
  const raw = window.location.hash.replace(/^#\/?/, '');
  const p = raw.split('/').filter(Boolean);
  if (!p.length) return { view: 'heatmap', matrix: 'person' };
  if (p[0] === 'references') return { view: 'references' };
  if (p[0] === 'actors' && p.length === 1) return { view: 'actors' };
  if (p[0] === 'actors') return { view: 'actorDetail', actorId: p[1] };
  if (p[0] === 'person' || p[0] === 'facility') {
    const matrix = p[0];
    if (p[1] === 'phase') {
      return { view: 'phase', matrix, phase: parseInt(p[2], 10), track: p[3] || null };
    }
    if (p[1] === 'indicator') return { view: 'indicator', matrix, indicatorId: p[2] };
    if (p[1] === 'tactic') return { view: 'tactic', matrix, tacticId: p[2] };
    return { view: 'heatmap', matrix };
  }
  if (p[0] === 'organization' || p[0] === 'infrastructure') {
    return { view: 'stub', matrix: p[0] };
  }
  return { view: 'heatmap', matrix: 'person' };
}
