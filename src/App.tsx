import { useCallback, useEffect, useMemo, useState } from 'react';
import type { FrameworkData, Tactic, ActorProfile } from './types/framework';
import { parseRoute, LIVE_MATRICES, type LiveMatrix } from './lib/route';
import { resolveTrack, tacticMatchesFilters } from './lib/constants';
import { TopNav } from './components/TopNav';
import { FilterBar } from './components/FilterBar';
import { HeatMapGrid } from './components/HeatMapGrid';
import { SplitView } from './components/SplitView';
import { ActorProfilesView } from './components/ActorProfilesView';
import { ActorDetailView } from './components/ActorDetailView';
import { IndicatorDetail, type IndicatorEntry } from './components/IndicatorDetail';
import { BibliographyView } from './components/BibliographyView';
import frameworkData from '../docs/data/framework.json';

export type TacticsByPhase = {
  1: Tactic[];
  2: Tactic[];
  3: Tactic[];
  4: { flight: Tactic[]; claim: Tactic[] };
};

export type TacticsByMatrix = Record<LiveMatrix, TacticsByPhase>;

export default function App() {
  const data = frameworkData as unknown as FrameworkData;

  const [route, setRoute] = useState(() => parseRoute());
  const [modalityFilter, setModalityFilter] = useState('');
  const [actorFilter, setActorFilter] = useState('');
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
    // All tactics across the live (rendered) matrices; IDs are globally unique
    // (TM####/TF####, IND-####/IND-F####), so the lookup maps stay flat.
    const allTactics: Tactic[] = LIVE_MATRICES.flatMap(
      (m) => data.matrices[m]?.tactics || []
    );
    const ap = data.actor_profiles;
    const bib = data.bibliography || {};

    const tacticMap: Record<string, Tactic> = {};
    allTactics.forEach((t) => { tacticMap[t.id] = t; });

    const actorMap: Record<string, ActorProfile> = {};
    ap.forEach((a) => { actorMap[a.id] = a; });

    // Flat lookup of every rendered indicator → its parent tactic
    const indicatorMap: Record<string, IndicatorEntry> = {};
    allTactics.forEach((t) => {
      (t.indicators || []).forEach((ind) => {
        indicatorMap[ind.id] = { indicator: ind, tactic: t };
      });
    });

    const tbm = {} as TacticsByMatrix;
    LIVE_MATRICES.forEach((m) => {
      const tbp: TacticsByPhase = { 1: [], 2: [], 3: [], 4: { flight: [], claim: [] } };
      (data.matrices[m]?.tactics || []).forEach((t) => {
        if (t.phase !== 4) tbp[t.phase as 1 | 2 | 3].push(t);
        else if (resolveTrack(t) === 'flight') tbp[4].flight.push(t);
        else tbp[4].claim.push(t);
      });
      tbm[m] = tbp;
    });

    const abc: Record<string, ActorProfile[]> = {};
    ap.forEach((a) => {
      if (!abc[a.category]) abc[a.category] = [];
      abc[a.category].push(a);
    });

    const getActorTactics = (id: string) =>
      allTactics.filter((t) => tacticMatchesFilters(t, '', id));

    // Reverse lookup: which tactics cite each bibliography entry
    const bibReverseMap: Record<string, Tactic[]> = {};
    allTactics.forEach((t) => {
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

    return { tacticMap, actorMap, indicatorMap, tbm, abc, bib, bibReverseMap, getActorTactics };
  }, [data]);

  const { tacticMap, actorMap, indicatorMap, tbm, abc, bib, bibReverseMap, getActorTactics } = derived;
  const isActors = route.view === 'actors' || route.view === 'actorDetail';
  const isReferences = route.view === 'references';
  const isIndicator = route.view === 'indicator';

  return (
    <div className="app-root">
      <TopNav route={route} navigate={navigate} theme={theme} setTheme={setTheme} />
      {!isActors && !isReferences && !isIndicator && (
        <FilterBar
          modalityFilter={modalityFilter}
          setModalityFilter={setModalityFilter}
          actorFilter={actorFilter}
          setActorFilter={setActorFilter}
          actorsByCategory={abc}
        />
      )}
      <div className="main-content">
        {route.view === 'heatmap' && (
          <HeatMapGrid
            tacticsByMatrix={tbm}
            navigate={navigate}
            modalityFilter={modalityFilter}
            actorFilter={actorFilter}
            compact={false}
            selectedMatrix={null}
            selectedPhase={null}
            selectedTrack={null}
            selectedTacticId={null}
          />
        )}
        {(route.view === 'phase' || route.view === 'tactic') && (
          <SplitView
            tacticsByMatrix={tbm}
            route={route}
            navigate={navigate}
            tacticMap={tacticMap}
            actorMap={actorMap}
            modalityFilter={modalityFilter}
            actorFilter={actorFilter}
          />
        )}
        {route.view === 'indicator' && (
          <IndicatorDetail
            indicatorId={route.indicatorId}
            indicatorMap={indicatorMap}
            navigate={navigate}
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
