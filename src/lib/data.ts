// Single load point for the vocabulary (docs/data/framework.json) and every
// lookup the viewer needs. Named imports keep the sections the viewer never
// reads out of the bundle. Every ID lookup is a Map, so a URL segment such as
// "__proto__" or "constructor" can never resolve to an inherited member.
import {
  matrices as rawMatrices,
  actor_profiles as rawActorProfiles,
  bibliography as rawBibliography,
  version as rawVersion,
  license as rawLicense,
} from '../../docs/data/framework.json';
import type {
  ActorProfile,
  BibliographyEntry,
  Countermeasure,
  Indicator,
  MatrixContainer,
  MatrixMaturity,
  RawActorProfile,
  ResponseProtocol,
  Tactic,
} from '../types/framework';
import { MATRIX_KEYS, resolveTrack, type MatrixKey } from './constants';

export const FRAMEWORK_VERSION: string = String(rawVersion);
export const FRAMEWORK_LICENSE: string = String(rawLicense);

export interface IndicatorEntry {
  indicator: Indicator;
  tactic: Tactic;
}

export type ChildEntry =
  | { kind: 'countermeasure'; item: Countermeasure; tactic: Tactic }
  | { kind: 'protocol'; item: ResponseProtocol; tactic: Tactic };

export type TacticsByPhase = {
  1: Tactic[];
  2: Tactic[];
  3: Tactic[];
  4: { flight: Tactic[]; claim: Tactic[] };
};

// An object is renderable when it has a string id and is not a held
// (reserved) identifier. Reserved objects carry no content fields.
const renderable = (o: unknown): boolean =>
  !!o &&
  typeof (o as { id?: unknown }).id === 'string' &&
  (o as { lifecycle_state?: string }).lifecycle_state !== 'reserved';

const containers = rawMatrices as unknown as Record<string, MatrixContainer | string | undefined>;

export interface MatrixInfo {
  key: MatrixKey;
  maturity: MatrixMaturity;
  scope: string;
  tactics: Tactic[];
  byPhase: TacticsByPhase;
}

export const matrixInfo = new Map<MatrixKey, MatrixInfo>();
export const allTactics: Tactic[] = [];
export const tacticById = new Map<string, Tactic>();
export const indicatorById = new Map<string, IndicatorEntry>();
export const childById = new Map<string, ChildEntry>();

MATRIX_KEYS.forEach((key) => {
  const c = containers[key];
  const container = c && typeof c === 'object' ? c : undefined;
  const byPhase: TacticsByPhase = { 1: [], 2: [], 3: [], 4: { flight: [], claim: [] } };
  const tactics: Tactic[] = [];
  (container?.tactics || []).forEach((raw) => {
    if (!renderable(raw)) return;
    if (![1, 2, 3, 4].includes(raw.phase)) return;
    const t: Tactic = {
      ...raw,
      matrix: key,
      indicators: (raw.indicators || []).filter(renderable),
      countermeasures: (raw.countermeasures || []).filter(renderable),
      response_protocols: (raw.response_protocols || []).filter(renderable),
    };
    tactics.push(t);
    allTactics.push(t);
    tacticById.set(t.id, t);
    t.indicators.forEach((indicator) => indicatorById.set(indicator.id, { indicator, tactic: t }));
    t.countermeasures.forEach((item) => childById.set(item.id, { kind: 'countermeasure', item, tactic: t }));
    t.response_protocols.forEach((item) => childById.set(item.id, { kind: 'protocol', item, tactic: t }));
    if (t.phase !== 4) byPhase[t.phase].push(t);
    else if (resolveTrack(t) === 'flight') byPhase[4].flight.push(t);
    else byPhase[4].claim.push(t);
  });
  matrixInfo.set(key, {
    key,
    // Anything not explicitly marked core is treated as draft.
    maturity: container?.maturity === 'core' ? 'core' : 'draft',
    scope: container?.scope || '',
    tactics,
    byPhase,
  });
});

export const getMatrix = (key: MatrixKey): MatrixInfo => matrixInfo.get(key)!;
export const isDraft = (key: string): boolean =>
  matrixInfo.get(key as MatrixKey)?.maturity === 'draft';

export const phaseTactics = (
  key: MatrixKey,
  phase: 1 | 2 | 3 | 4,
  track: 'flight' | 'claim' | null
): Tactic[] => {
  const bp = getMatrix(key).byPhase;
  if (phase !== 4) return bp[phase];
  if (track) return bp[4][track];
  return [...bp[4].flight, ...bp[4].claim];
};

// Actor profiles. Reserved identifiers are held, not data: they are kept out
// of every list and count and are only reachable by direct route, where the
// viewer shows a short notice.
export const actors: ActorProfile[] = [];
export const actorById = new Map<string, ActorProfile>();
export const reservedActorById = new Map<string, string>();
export const actorsByCategory = new Map<string, ActorProfile[]>();

(rawActorProfiles as unknown as RawActorProfile[]).forEach((a) => {
  if (!a || typeof a.id !== 'string') return;
  if (a.lifecycle_state === 'reserved') {
    reservedActorById.set(a.id, a.reserved_reason || '');
    return;
  }
  actors.push(a);
  actorById.set(a.id, a);
  const list = actorsByCategory.get(a.category);
  if (list) list.push(a);
  else actorsByCategory.set(a.category, [a]);
});

export const actorTactics = (actorId: string): Tactic[] =>
  allTactics.filter((t) => (t.actor_associations || []).some((a) => a.actor_id === actorId));

// Bibliography and the reverse lookup of which tactics cite each entry.
export const bibliography = new Map<string, BibliographyEntry>(
  Object.entries(rawBibliography as unknown as Record<string, BibliographyEntry>)
);
export const citedBy = new Map<string, Tactic[]>();

allTactics.forEach((t) => {
  const refs = new Set<string>(t.source_refs || []);
  t.indicators.forEach((i) => (i.source_refs || []).forEach((r) => refs.add(r)));
  t.countermeasures.forEach((c) => (c.source_refs || []).forEach((r) => refs.add(r)));
  t.response_protocols.forEach((r) => (r.source_refs || []).forEach((x) => refs.add(x)));
  refs.forEach((key) => {
    const list = citedBy.get(key);
    if (list) list.push(t);
    else citedBy.set(key, [t]);
  });
});

// Reverse correlates_with edges: indicators that point at a given indicator.
export const correlatedFrom = new Map<string, IndicatorEntry[]>();
indicatorById.forEach((entry) => {
  (entry.indicator.correlates_with || []).forEach((target) => {
    const list = correlatedFrom.get(target);
    if (list) list.push(entry);
    else correlatedFrom.set(target, [entry]);
  });
});

export const COUNTS = {
  tactics: allTactics.length,
  indicators: indicatorById.size,
  profiles: actors.length,
  sources: bibliography.size,
};
