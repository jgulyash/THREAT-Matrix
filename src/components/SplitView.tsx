import type { Tactic, ActorProfile } from '../types/framework';
import type { Route } from '../lib/route';
import type { TacticsByMatrix } from '../App';
import { resolveTrack } from '../lib/constants';
import { HeatMapGrid } from './HeatMapGrid';
import { PhasePanel } from './PhasePanel';
import { TacticDetail } from './TacticDetail';

interface Props {
  tacticsByMatrix: TacticsByMatrix;
  route: Extract<Route, { view: 'phase' } | { view: 'tactic' }>;
  navigate: (path: string) => void;
  tacticMap: Record<string, Tactic>;
  actorMap: Record<string, ActorProfile>;
  modalityFilter: string;
  actorFilter: string;
}

export function SplitView({
  tacticsByMatrix,
  route,
  navigate,
  tacticMap,
  actorMap,
  modalityFilter,
  actorFilter,
}: Props) {
  const matrix = route.matrix;
  const tacticsByPhase = tacticsByMatrix[matrix];
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
          tacticsByMatrix={tacticsByMatrix}
          navigate={navigate}
          modalityFilter={modalityFilter}
          actorFilter={actorFilter}
          compact={true}
          selectedMatrix={matrix}
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
            matrix={matrix}
            phase={pp}
            track={pt}
            navigate={navigate}
            modalityFilter={modalityFilter}
            actorFilter={actorFilter}
          />
        )}
      </div>
    </div>
  );
}
