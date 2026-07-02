export type Route =
  | { view: 'heatmap' }
  | { view: 'phase'; phase: number; track: string | null }
  | { view: 'tactic'; tacticId: string }
  | { view: 'indicator'; indicatorId: string }
  | { view: 'actors' }
  | { view: 'actorDetail'; actorId: string }
  | { view: 'stub'; matrix: 'facility' | 'organization' | 'infrastructure' }
  | { view: 'references' };

export function parseRoute(): Route {
  const raw = window.location.hash.replace(/^#\/?/, '');
  const p = raw.split('/').filter(Boolean);
  if (!p.length || (p[0] === 'person' && p.length === 1)) return { view: 'heatmap' };
  if (p[0] === 'references') return { view: 'references' };
  if (p[0] === 'actors' && p.length === 1) return { view: 'actors' };
  if (p[0] === 'actors') return { view: 'actorDetail', actorId: p[1] };
  if (p[0] === 'person' && p[1] === 'phase') {
    return { view: 'phase', phase: parseInt(p[2], 10), track: p[3] || null };
  }
  if (p[0] === 'person' && p[1] === 'indicator') return { view: 'indicator', indicatorId: p[2] };
  if (p[0] === 'person' && p[1] === 'tactic') return { view: 'tactic', tacticId: p[2] };
  if (p[0] === 'facility' || p[0] === 'organization' || p[0] === 'infrastructure') {
    return { view: 'stub', matrix: p[0] };
  }
  return { view: 'heatmap' };
}
