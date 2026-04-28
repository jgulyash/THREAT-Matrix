import { useCallback, useEffect, useMemo, useState } from 'react';
import type { FrameworkData, Tactic, ActorProfile } from './types/framework';
import { parseRoute } from './lib/route';
import { resolveTrack } from './lib/constants';
import { TopNav } from './components/TopNav';
import { FilterBar } from './components/FilterBar';
import { HeatMapGrid } from './components/HeatMapGrid';
import { SplitView } from './components/SplitView';
import { ActorProfilesView } from './components/ActorProfilesView';
import { ActorDetailView } from './components/ActorDetailView';
import { StubLanding } from './components/StubLanding';
import { BibliographyView } from './components/BibliographyView';
import frameworkData from '../docs/data/framework.json';

export type TacticsByPhase = {
  1: Tactic[];
  2: Tactic[];
  3: Tactic[];
  4: { flight: Tactic[]; claim: Tactic[] };
};

export default function App() {
  const data = frameworkData as unknown as FrameworkData;

  const [route, setRoute] = useState(() => parseRoute());
  const [cpnFilter, setCpnFilter] = useState(false);
  const [theme, setThemeState] = useState<'dark' | 'light'>(() =>
    (localStorage.getItem('threat-matrix-theme') as 'dark' | 'light' | null) || 'dark'
  );

  const setTheme = useCallback((t: 'dark' | 'light') => {
    setThemeState(t);
    localStorage.setItem('threat-matrix-theme', t);
    document.documentElement.setAttribute('data-theme', t === 'light' ? 'light' : '');
  }, []);

  useEffect(() => {
    if (theme === 'light') document.documentElement.setAttribute('data-theme', 'light');
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    const h = () => setRoute(parseRoute());
    window.addEventListener('hashchange', h);
    return () => window.removeEventListener('hashchange', h);
  }, []);

  const navigate = useCallback((path: string) => {
    window.location.hash = '#' + path;
  }, []);

  const derived = useMemo(() => {
    const pt = data.matrices.person.tactics;
    const ap = data.actor_profiles;
    const bib = data.bibliography || {};

    const tacticMap: Record<string, Tactic> = {};
    pt.forEach((t) => { tacticMap[t.id] = t; });

    const actorMap: Record<string, ActorProfile> = {};
    ap.forEach((a) => { actorMap[a.id] = a; });

    const tbp: TacticsByPhase = { 1: [], 2: [], 3: [], 4: { flight: [], claim: [] } };
    pt.forEach((t) => {
      if (t.phase !== 4) tbp[t.phase as 1 | 2 | 3].push(t);
      else if (resolveTrack(t) === 'flight') tbp[4].flight.push(t);
      else tbp[4].claim.push(t);
    });

    const abc: Record<string, ActorProfile[]> = {};
    ap.forEach((a) => {
      if (!abc[a.category]) abc[a.category] = [];
      abc[a.category].push(a);
    });

    const getActorTactics = (id: string) =>
      pt.filter((t) =>
        t.actor_associations && t.actor_associations.some((a) => a.actor_id === id)
      );

    // Reverse lookup: which tactics cite each bibliography entry
    const bibReverseMap: Record<string, Tactic[]> = {};
    pt.forEach((t) => {
      const refs = new Set<string>();
      (t.source_refs || []).forEach((r) => refs.add(r));
      (t.indicators || []).forEach((i) => (i.source_refs || []).forEach((r) => refs.add(r)));
      (t.countermeasures || []).forEach((c) => (c.source_refs || []).forEach((r) => refs.add(r)));
      (t.response_protocols || []).forEach((r) => (r.source_refs || []).forEach((x) => refs.add(x)));
      refs.forEach((key) => {
        if (!bibReverseMap[key]) bibReverseMap[key] = [];
        bibReverseMap[key].push(t);
      });
    });

    return { pt, ap, tacticMap, actorMap, tbp, abc, bib, bibReverseMap, getActorTactics };
  }, [data]);

  const { tacticMap, actorMap, tbp, abc, bib, bibReverseMap, getActorTactics } = derived;
  const isActors = route.view === 'actors' || route.view === 'actorDetail';
  const isReferences = route.view === 'references';
  const sv = { facility: 'V2', organization: 'V3', system: 'V4' } as const;

  return (
    <div className="app-root">
      <TopNav route={route} navigate={navigate} theme={theme} setTheme={setTheme} />
      {!isActors && !isReferences && (
        <FilterBar cpnFilter={cpnFilter} setCpnFilter={setCpnFilter} />
      )}
      <div className="main-content">
        {route.view === 'heatmap' && (
          <HeatMapGrid
            tacticsByPhase={tbp}
            navigate={navigate}
            cpnFilter={cpnFilter}
            compact={false}
            selectedPhase={null}
            selectedTrack={null}
            selectedTacticId={null}
          />
        )}
        {(route.view === 'phase' || route.view === 'tactic') && (
          <SplitView
            tacticsByPhase={tbp}
            route={route}
            navigate={navigate}
            tacticMap={tacticMap}
            actorMap={actorMap}
            bibliography={bib}
            cpnFilter={cpnFilter}
          />
        )}
        {route.view === 'actors' && (
          <ActorProfilesView actorsByCategory={abc} navigate={navigate} />
        )}
        {route.view === 'actorDetail' && (
          <ActorDetailView
            actor={actorMap[route.actorId]}
            navigate={navigate}
            getActorTactics={getActorTactics}
          />
        )}
        {route.view === 'stub' && (
          <StubLanding matrix={route.matrix} version={sv[route.matrix]} />
        )}
        {route.view === 'references' && (
          <BibliographyView
            bibliography={bib}
            bibReverseMap={bibReverseMap}
            navigate={navigate}
          />
        )}
      </div>
    </div>
  );
}
