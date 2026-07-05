import type { Tactic, ActorProfile, BibliographyEntry } from '../types/framework';
import type { Route } from '../lib/route';
import type { TacticsByPhase } from '../App';
import { resolveTrack } from '../lib/constants';
import { HeatMapGrid } from './HeatMapGrid';
import { PhasePanel } from './PhasePanel';
import { TacticDetail } from './TacticDetail';

interface Props {
  tacticsByPhase: TacticsByPhase;
  route: Extract<Route, { view: 'phase' } | { view: 'tactic' }>;
  navigate: (path: string) => void;
  tacticMap: Record<string, Tactic>;
  actorMap: Record<string, ActorProfile>;
  bibliography: Record<string, BibliographyEntry>;
  cpnFilter: boolean;
  actorFilter: string;
}

export function SplitView({
  tacticsByPhase,
  route,
  navigate,
  tacticMap,
  actorMap,
  cpnFilter,
  actorFilter,
}: Props) {
  const ot = route.view === 'tactic' ? tacticMap[route.tacticId] : null;

  let pp: number;
  let pt: string | null;
  let ptactics: Tactic[];

  if (ot) {
    pp = ot.phase;
    if (pp === 4) {
      pt = resolveTrack(ot);
      ptactics = pt === 'flight' ? tacticsByPhase[4].flight : tacticsByPhase[4].claim;
    } else {
      pt = null;
      ptactics = tacticsByPhase[pp as 1 | 2 | 3] || [];
    }
  } else if (route.view === 'phase' && route.phase === 4) {
    pp = 4;
    pt = route.track;
    ptactics = route.track === 'flight' ? tacticsByPhase[4].flight : tacticsByPhase[4].claim;
  } else if (route.view === 'phase') {
    pp = route.phase;
    pt = null;
    ptactics = tacticsByPhase[route.phase as 1 | 2 | 3] || [];
  } else {
    pp = 1;
    pt = null;
    ptactics = [];
  }

  return (
    <div className="split-view">
      <div className="split-hm">
        <HeatMapGrid
          tacticsByPhase={tacticsByPhase}
          navigate={navigate}
          cpnFilter={cpnFilter}
          actorFilter={actorFilter}
          compact={true}
          selectedPhase={pp}
          selectedTrack={pt}
          selectedTacticId={route.view === 'tactic' ? route.tacticId : null}
        />
      </div>
      <div className="detail-panel">
        {ot ? (
          <TacticDetail
            tactic={ot}
            actorMap={actorMap}
            navigate={navigate}
            fromPhase={pp}
            fromTrack={pt}
          />
        ) : (
          <PhasePanel
            tactics={ptactics}
            phase={pp}
            track={pt}
            navigate={navigate}
            cpnFilter={cpnFilter}
            actorFilter={actorFilter}
          />
        )}
      </div>
    </div>
  );
}
