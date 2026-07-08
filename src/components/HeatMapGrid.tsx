import type { Tactic } from '../types/framework';
import { PHASE_SHORT, STUB, MATRIX_LABELS, tacticMatchesFilters } from '../lib/constants';
import { LIVE_MATRICES, type LiveMatrix } from '../lib/route';
import type { TacticsByMatrix } from '../App';

// Column identity colors follow the header scheme (amber/teal/red/blue).
const MATRIX_COL: Record<LiveMatrix, string> = { person: 'amber', facility: 'teal' };

interface HeatMapCellProps {
  tactics: Tactic[];
  col: string;
  track?: 'flight' | 'claim';
  isSelected: boolean;
  onClick: () => void;
  cpnFilter: boolean;
  actorFilter: string;
}

function HeatMapCell({ tactics, col, track, isSelected, onClick, cpnFilter, actorFilter }: HeatMapCellProps) {
  const displayed = tactics.filter((t) => tacticMatchesFilters(t, cpnFilter, actorFilter));
  const count = displayed.length;
  const cpnCount = displayed.filter((t) => t.cpn).length;
  const cls = track === 'flight' ? 'flight-cell' : track === 'claim' ? 'claim-cell' : '';
  const limit = track ? 2 : 3;
  return (
    <div
      className={`hm-cell${cls ? ' ' + cls : ''}${isSelected ? ' selected' : ''}`}
      onClick={onClick}
    >
      {track && (
        <div className={`track-label ${track}`}>
          {track === 'flight' ? 'Evade' : 'Claim'}
        </div>
      )}
      <div className={`hm-count ${col}`}>{count}</div>
      {count > 0 && (
        <div className="hm-names">
          {displayed.slice(0, limit).map((t) => (
            <div key={t.id} className="hm-name">{t.name}</div>
          ))}
          {count > limit && <div className="hm-overflow">+{count - limit} more</div>}
        </div>
      )}
      {cpnCount > 0 && !cpnFilter && (
        <div className="cpn-strip">⌖ {cpnCount} cyber-enabled</div>
      )}
    </div>
  );
}

interface StubCellProps {
  count: number;
  version: string;
  track?: 'flight' | 'claim';
}

function StubCell({ count, version, track }: StubCellProps) {
  const col = track ? 'amber' : 'blue';
  const ex = track === 'flight' ? 'phase4-stub-flight' : track === 'claim' ? 'phase4-stub-claim' : '';
  return (
    <div className={`hm-cell stub${ex ? ' ' + ex : ''}`}>
      {track && (
        <div className={`track-label ${track}`} style={{ opacity: 0.5 }}>
          {track === 'flight' ? 'Evade' : 'Claim'}
        </div>
      )}
      <div className={`hm-count ${col}`}>{count}</div>
      <div className="stub-planned">{version} Planned</div>
    </div>
  );
}

interface GridProps {
  tacticsByMatrix: TacticsByMatrix;
  navigate: (path: string) => void;
  cpnFilter: boolean;
  actorFilter: string;
  compact: boolean;
  selectedMatrix: LiveMatrix | null;
  selectedPhase: number | null;
  selectedTrack: string | null;
  selectedTacticId: string | null;
}

export function HeatMapGrid({
  tacticsByMatrix,
  navigate,
  cpnFilter,
  actorFilter,
  compact,
  selectedMatrix,
  selectedPhase,
  selectedTrack,
  selectedTacticId,
}: GridProps) {
  const pc = '140px';
  const gc = `${pc} 1fr 1fr 1fr 1fr`;

  // Live column counts derive from the data; stub totals from the STUB plan.
  const liveCount = (m: LiveMatrix) => {
    const tbp = tacticsByMatrix[m];
    return tbp[1].length + tbp[2].length + tbp[3].length + tbp[4].flight.length + tbp[4].claim.length;
  };
  const stubCount = (m: 'organization' | 'infrastructure') =>
    Object.values(STUB[m].phases).reduce((n, v) => n + v, 0) + STUB[m].flight + STUB[m].claim;

  const phaseSelected = (m: LiveMatrix, phase: 1 | 2 | 3) => {
    if (selectedMatrix !== m) return false;
    return selectedTacticId
      ? tacticsByMatrix[m][phase].some((t) => t.id === selectedTacticId)
      : selectedPhase === phase;
  };

  const trackSelected = (m: LiveMatrix, track: 'flight' | 'claim') => {
    if (selectedMatrix !== m) return false;
    const tactics = tacticsByMatrix[m][4][track];
    return (
      (!!selectedTacticId && tactics.some((t) => t.id === selectedTacticId)) ||
      (!selectedTacticId && selectedPhase === 4 && selectedTrack === track)
    );
  };

  return (
    <div className="hm-wrap">
      <div className="hm-header-row" style={{ gridTemplateColumns: gc }}>
        <div className="hm-col-hdr phase-col">Phase</div>
        {LIVE_MATRICES.map((m) => (
          <div key={m} className={`hm-col-hdr ${MATRIX_COL[m]}`}>
            {compact ? MATRIX_LABELS[m] : `${MATRIX_LABELS[m]} · ${liveCount(m)}`}
          </div>
        ))}
        <div className="hm-col-hdr red">{compact ? MATRIX_LABELS.organization : `${MATRIX_LABELS.organization} · ${stubCount('organization')}`}</div>
        <div className="hm-col-hdr blue">{compact ? MATRIX_LABELS.infrastructure : `${MATRIX_LABELS.infrastructure} · ${stubCount('infrastructure')}`}</div>
      </div>
      <div className="hm-rows">
        {([1, 2, 3] as const).map((phase) => (
          <div key={phase} className="hm-row" style={{ gridTemplateColumns: gc }}>
            <div className="hm-phase-cell">
              <div className="hm-phase-name">{PHASE_SHORT[phase]}</div>
            </div>
            {LIVE_MATRICES.map((m) => (
              <HeatMapCell
                key={m}
                tactics={tacticsByMatrix[m][phase]}
                col={MATRIX_COL[m]}
                isSelected={phaseSelected(m, phase)}
                onClick={() => navigate(`/${m}/phase/${phase}`)}
                cpnFilter={cpnFilter}
                actorFilter={actorFilter}
              />
            ))}
            {(['organization', 'infrastructure'] as const).map((m, i) => (
              <StubCell key={m} count={STUB[m].phases[phase]} version={`V1.${i + 4}`} />
            ))}
          </div>
        ))}
        <div className="phase4-row">
          <div className="phase4-phase-cell" style={{ width: '140px' }}>
            <div className="hm-phase-name">{PHASE_SHORT[4]}</div>
          </div>
          <div className="phase4-content">
            <div className="phase4-sub-row">
              {LIVE_MATRICES.map((m) => (
                <HeatMapCell
                  key={m}
                  tactics={tacticsByMatrix[m][4].flight}
                  col={MATRIX_COL[m]}
                  track="flight"
                  isSelected={trackSelected(m, 'flight')}
                  onClick={() => navigate(`/${m}/phase/4/flight`)}
                  cpnFilter={cpnFilter}
                  actorFilter={actorFilter}
                />
              ))}
              <StubCell count={STUB.organization.flight} version="V1.4" track="flight" />
              <StubCell count={STUB.infrastructure.flight} version="V1.5" track="flight" />
            </div>
            <div className="phase4-divider" />
            <div className="phase4-sub-row">
              {LIVE_MATRICES.map((m) => (
                <HeatMapCell
                  key={m}
                  tactics={tacticsByMatrix[m][4].claim}
                  col={MATRIX_COL[m]}
                  track="claim"
                  isSelected={trackSelected(m, 'claim')}
                  onClick={() => navigate(`/${m}/phase/4/claim`)}
                  cpnFilter={cpnFilter}
                  actorFilter={actorFilter}
                />
              ))}
              <StubCell count={STUB.organization.claim} version="V1.4" track="claim" />
              <StubCell count={STUB.infrastructure.claim} version="V1.5" track="claim" />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
