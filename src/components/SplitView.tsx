import type { Route } from '../lib/route';
import { resolveTrack } from '../lib/constants';
import { phaseTactics, tacticById } from '../lib/data';
import { HeatMapGrid } from './HeatMapGrid';
import { PhasePanel } from './PhasePanel';
import { TacticDetail } from './TacticDetail';

interface Props {
  route: Extract<Route, { view: 'phase' } | { view: 'tactic' }>;
}

// The router has already validated the route: a tactic route always resolves
// to a tactic, and a phase route always carries a phase from 1 to 4.
export function SplitView({ route }: Props) {
  const matrix = route.matrix;
  const tactic = route.view === 'tactic' ? tacticById.get(route.tacticId) : undefined;
  const phase = tactic ? tactic.phase : route.view === 'phase' ? route.phase : 1;
  const track = tactic ? resolveTrack(tactic) : route.view === 'phase' ? route.track : null;

  return (
    <div className="split-view">
      <div className="split-hm">
        <HeatMapGrid
          scope={matrix}
          compact={true}
          route={route}
          selectedPhase={phase}
          selectedTrack={track}
          selectedTacticId={tactic ? tactic.id : null}
        />
      </div>
      <div className="detail-panel">
        {tactic ? (
          <TacticDetail
            tactic={tactic}
            focusId={route.view === 'tactic' ? route.focusId : null}
          />
        ) : (
          <PhasePanel
            tactics={phaseTactics(matrix, phase, track)}
            matrix={matrix}
            phase={phase}
            track={track}
          />
        )}
      </div>
    </div>
  );
}
