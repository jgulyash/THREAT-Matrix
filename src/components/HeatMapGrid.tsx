import type { Tactic } from '../types/framework';
import { PHASE_SHORT, STUB, MATRICES, MATRIX_LABELS, tacticMatchesFilters } from '../lib/constants';
import { LIVE_MATRICES, type LiveMatrix } from '../lib/route';
import type { TacticsByMatrix } from '../App';

// Column identity colors come from the shared MATRICES descriptor.
const MATRIX_COL: Record<string, string> = Object.fromEntries(
  MATRICES.map((m) => [m.key, m.color])
);

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
  const stubCount = (m: keyof typeof STUB) =>
    Object.values(STUB[m].phases).reduce((n, v) => n + v, 0) + STUB[m].flight + STUB[m].claim;

  // Filter transparency: when a filter is active, show how much is hidden so a
  // reduced heat map never reads as missing/deleted data.
  const filterActive = cpnFilter || !!actorFilter;
  const shownCount = (m: LiveMatrix) => {
    const tbp = tacticsByMatrix[m];
    const all = [...tbp[1], ...tbp[2], ...tbp[3], ...tbp[4].flight, ...tbp[4].claim];
    return all.filter((t) => tacticMatchesFilters(t, cpnFilter, actorFilter)).length;
  };
  const filterLabel = [cpnFilter ? 'CPN' : null, actorFilter || null]
    .filter(Boolean)
    .join(' + ');

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
      {filterActive && (
        <div className="hm-filter-note">
          <span className="hm-filter-tag">⌖ Filtered · {filterLabel}</span>
          <span className="hm-filter-detail">
            {LIVE_MATRICES.map((m, i) => (
              <span key={m}>
                {i > 0 ? ' · ' : ''}
                {MATRIX_LABELS[m]} <strong>{shownCount(m)}</strong> of {liveCount(m)}
              </span>
            ))}
            {' — clear the filter to see all tactics'}
          </span>
        </div>
      )}
      <div className="hm-header-row" style={{ gridTemplateColumns: gc }}>
        <div className="hm-col-hdr phase-col">Phase</div>
        {MATRICES.map((m) => (
          <div key={m.key} className={`hm-col-hdr ${m.color}`}>
            {compact
              ? m.label
              : `${m.label} · ${m.version === null ? liveCount(m.key as LiveMatrix) : stubCount(m.key as keyof typeof STUB)}`}
          </div>
        ))}
      </div>
      <div className="hm-rows">
        {([1, 2, 3] as const).map((phase) => (
          <div key={phase} className="hm-row" style={{ gridTemplateColumns: gc }}>
            <div className="hm-phase-cell">
              <div className="hm-phase-name">{PHASE_SHORT[phase]}</div>
            </div>
            {MATRICES.map((m) =>
              m.version === null ? (
                <HeatMapCell
                  key={m.key}
                  tactics={tacticsByMatrix[m.key as LiveMatrix][phase]}
                  col={MATRIX_COL[m.key as LiveMatrix]}
                  isSelected={phaseSelected(m.key as LiveMatrix, phase)}
                  onClick={() => navigate(`/${m.key}/phase/${phase}`)}
                  cpnFilter={cpnFilter}
                  actorFilter={actorFilter}
                />
              ) : (
                <StubCell
                  key={m.key}
                  count={STUB[m.key as keyof typeof STUB].phases[phase]}
                  version={m.version}
                />
              )
            )}
          </div>
        ))}
        <div className="phase4-row">
          <div className="phase4-phase-cell" style={{ width: '140px' }}>
            <div className="hm-phase-name">{PHASE_SHORT[4]}</div>
          </div>
          <div className="phase4-content">
            <div className="phase4-sub-row">
              {MATRICES.map((m) =>
                m.version === null ? (
                  <HeatMapCell
                    key={m.key}
                    tactics={tacticsByMatrix[m.key as LiveMatrix][4].flight}
                    col={MATRIX_COL[m.key as LiveMatrix]}
                    track="flight"
                    isSelected={trackSelected(m.key as LiveMatrix, 'flight')}
                    onClick={() => navigate(`/${m.key}/phase/4/flight`)}
                    cpnFilter={cpnFilter}
                    actorFilter={actorFilter}
                  />
                ) : (
                  <StubCell
                    key={m.key}
                    count={STUB[m.key as keyof typeof STUB].flight}
                    version={m.version}
                    track="flight"
                  />
                )
              )}
            </div>
            <div className="phase4-divider" />
            <div className="phase4-sub-row">
              {MATRICES.map((m) =>
                m.version === null ? (
                  <HeatMapCell
                    key={m.key}
                    tactics={tacticsByMatrix[m.key as LiveMatrix][4].claim}
                    col={MATRIX_COL[m.key as LiveMatrix]}
                    track="claim"
                    isSelected={trackSelected(m.key as LiveMatrix, 'claim')}
                    onClick={() => navigate(`/${m.key}/phase/4/claim`)}
                    cpnFilter={cpnFilter}
                    actorFilter={actorFilter}
                  />
                ) : (
                  <StubCell
                    key={m.key}
                    count={STUB[m.key as keyof typeof STUB].claim}
                    version={m.version}
                    track="claim"
                  />
                )
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
