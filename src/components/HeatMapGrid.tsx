import type { Tactic } from '../types/framework';
import { PHASE_SHORT, STUB } from '../lib/constants';
import type { TacticsByPhase } from '../App';

interface HeatMapCellProps {
  tactics: Tactic[];
  track?: 'flight' | 'claim';
  isSelected: boolean;
  onClick: () => void;
  cpnFilter: boolean;
}

function HeatMapCell({ tactics, track, isSelected, onClick, cpnFilter }: HeatMapCellProps) {
  const displayed = cpnFilter ? tactics.filter((t) => t.cpn) : tactics;
  const count = displayed.length;
  const cpnCount = tactics.filter((t) => t.cpn).length;
  const col = 'amber';
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
  tacticsByPhase: TacticsByPhase;
  navigate: (path: string) => void;
  cpnFilter: boolean;
  compact: boolean;
  selectedPhase: number | null;
  selectedTrack: string | null;
  selectedTacticId: string | null;
}

export function HeatMapGrid({
  tacticsByPhase,
  navigate,
  cpnFilter,
  compact,
  selectedPhase,
  selectedTrack,
  selectedTacticId,
}: GridProps) {
  const pc = '140px';
  const gc = `${pc} 1fr 1fr 1fr 1fr`;
  return (
    <div className="hm-wrap">
      <div className="hm-header-row" style={{ gridTemplateColumns: gc }}>
        <div className="hm-col-hdr phase-col">Phase</div>
        <div className="hm-col-hdr amber">{compact ? 'Person' : 'Person · 34'}</div>
        <div className="hm-col-hdr teal">{compact ? 'Facility' : 'Facility · 40'}</div>
        <div className="hm-col-hdr red">{compact ? 'Organization' : 'Organization · 42'}</div>
        <div className="hm-col-hdr blue">{compact ? 'Infrastructure' : 'Infrastructure · 38'}</div>
      </div>
      <div className="hm-rows">
        {([1, 2, 3] as const).map((phase) => {
          const phaseTactics = tacticsByPhase[phase];
          const sel = selectedTacticId
            ? phaseTactics.some((t) => t.id === selectedTacticId)
            : selectedPhase === phase;
          return (
            <div key={phase} className="hm-row" style={{ gridTemplateColumns: gc }}>
              <div className="hm-phase-cell">
                <div className="hm-phase-name">{PHASE_SHORT[phase]}</div>
              </div>
              <HeatMapCell
                tactics={phaseTactics}
                isSelected={sel}
                onClick={() => navigate(`/person/phase/${phase}`)}
                cpnFilter={cpnFilter}
              />
              {(['facility', 'organization', 'infrastructure'] as const).map((m, i) => (
                <StubCell key={m} count={STUB[m].phases[phase]} version={`V${i + 2}`} />
              ))}
            </div>
          );
        })}
        <div className="phase4-row">
          <div className="phase4-phase-cell" style={{ width: '140px' }}>
            <div className="hm-phase-name">{PHASE_SHORT[4]}</div>
          </div>
          <div className="phase4-content">
            <div className="phase4-sub-row">
              <HeatMapCell
                tactics={tacticsByPhase[4].flight}
                track="flight"
                isSelected={
                  (!!selectedTacticId &&
                    tacticsByPhase[4].flight.some((t) => t.id === selectedTacticId)) ||
                  (!selectedTacticId && selectedPhase === 4 && selectedTrack === 'flight')
                }
                onClick={() => navigate('/person/phase/4/flight')}
                cpnFilter={cpnFilter}
              />
              <StubCell count={STUB.facility.flight} version="V2" track="flight" />
              <StubCell count={STUB.organization.flight} version="V3" track="flight" />
              <StubCell count={STUB.infrastructure.flight} version="V4" track="flight" />
            </div>
            <div className="phase4-divider" />
            <div className="phase4-sub-row">
              <HeatMapCell
                tactics={tacticsByPhase[4].claim}
                track="claim"
                isSelected={
                  (!!selectedTacticId &&
                    tacticsByPhase[4].claim.some((t) => t.id === selectedTacticId)) ||
                  (!selectedTacticId && selectedPhase === 4 && selectedTrack === 'claim')
                }
                onClick={() => navigate('/person/phase/4/claim')}
                cpnFilter={cpnFilter}
              />
              <StubCell count={STUB.facility.claim} version="V2" track="claim" />
              <StubCell count={STUB.organization.claim} version="V3" track="claim" />
              <StubCell count={STUB.infrastructure.claim} version="V4" track="claim" />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
