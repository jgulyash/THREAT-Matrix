import type { Tactic } from '../types/framework';
import { PHASE_NAMES, tacticMatchesFilters } from '../lib/constants';

interface Props {
  tactics: Tactic[];
  matrix: string;
  phase: number;
  track: string | null;
  navigate: (path: string) => void;
  cpnFilter: boolean;
  actorFilter: string;
}

export function PhasePanel({ tactics, matrix, phase, track, navigate, cpnFilter, actorFilter }: Props) {
  const disp = tactics.filter((t) => tacticMatchesFilters(t, cpnFilter, actorFilter));
  const filtered = cpnFilter || !!actorFilter;
  const tl = track === 'flight' ? 'Evade' : track === 'claim' ? 'Claim' : null;
  return (
    <>
      <div className="dp-header">
        <div className="dp-back" onClick={() => navigate(`/${matrix}`)}>
          ← Back
        </div>
        <div className="dp-crumb">
          <span>Phase {phase}</span>
          <span className="dp-crumb-sep">›</span>
          <span className="dp-crumb-active">
            {PHASE_NAMES[phase]}
            {tl ? ` · ${tl}` : ''}
          </span>
        </div>
        <div className="dp-header-title">{tl ? `${tl} Tactics` : PHASE_NAMES[phase]}</div>
        <div className="dp-header-sub">
          {disp.length}
          {filtered ? ` of ${tactics.length} (filtered)` : ''} tactics
        </div>
      </div>
      <div className="dp-content">
        {disp.length === 0 && (
          <div style={{ color: 'var(--text-dim)', fontSize: '11px', padding: '8px 0' }}>
            No tactics match the active filter in this phase.
          </div>
        )}
        {disp.map((t) => (
          <div
            key={t.id}
            className="dp-card"
            onClick={() => navigate(`/${t.matrix}/tactic/${t.id}`)}
          >
            <div className="dp-card-id">{t.id}</div>
            <div className="dp-card-title">{t.name}</div>
            <div className="dp-card-body">
              {t.notes ? t.notes.slice(0, 120) + (t.notes.length > 120 ? '…' : '') : ''}
            </div>
            <div className="dp-card-tags">
              {t.phase_4_track === 'evasion' && <span className="dp-ctag flight">Evade</span>}
              {t.phase_4_track === 'attribution' && <span className="dp-ctag claim">Claim</span>}
              {t.cpn && <span className="dp-ctag cpn">⌖ CPN</span>}
            </div>
          </div>
        ))}
      </div>
    </>
  );
}
