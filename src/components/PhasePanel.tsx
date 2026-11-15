import type { Tactic } from '../types/framework';
import { MATRIX_LABELS, PHASE_NAMES, TRACK_LABELS, tacticMatchesFilters, type MatrixKey } from '../lib/constants';
import { seg } from '../lib/route';
import { Go, useFilters } from '../lib/nav';
import { DraftTag } from './DraftTag';
import { LifecycleTag } from './Lifecycle';

interface Props {
  tactics: Tactic[];
  matrix: MatrixKey;
  phase: 1 | 2 | 3 | 4;
  track: 'flight' | 'claim' | null;
}

export function PhasePanel({ tactics, matrix, phase, track }: Props) {
  const { mode, actor } = useFilters();
  const disp = tactics.filter((t) => tacticMatchesFilters(t, mode, actor));
  const filtered = !!mode || !!actor;
  const tl = track ? TRACK_LABELS[track] : null;
  return (
    <>
      <div className="dp-header">
        <Go className="dp-back" to={`/${matrix}`}>
          ← {MATRIX_LABELS[matrix]} matrix
        </Go>
        <div className="dp-crumb">
          <span>
            {MATRIX_LABELS[matrix]}
            <DraftTag matrix={matrix} />
          </span>
          <span className="dp-crumb-sep">›</span>
          <span>Phase {phase}</span>
          <span className="dp-crumb-sep">›</span>
          <span className="dp-crumb-active">
            {PHASE_NAMES[phase]}
            {tl ? ` · ${tl}` : ''}
          </span>
        </div>
        <h1 className="dp-header-title" data-focus-target tabIndex={-1}>
          {tl ? `${tl} Tactics` : PHASE_NAMES[phase]}
        </h1>
        <div className="dp-header-sub">
          {disp.length}
          {filtered ? ` of ${tactics.length} (filtered)` : ''} tactics
        </div>
      </div>
      <div className="dp-content">
        {disp.length === 0 && (
          <div className="dp-empty">
            {filtered ? 'No tactics match the active filter in this phase.' : 'No tactics in this phase.'}
          </div>
        )}
        {disp.map((t) => (
          <Go key={t.id} className="dp-card" to={`/${t.matrix}/tactic/${seg(t.id)}`}>
            <div className="dp-card-id">
              {t.id}
              <LifecycleTag item={t} />
            </div>
            <div className="dp-card-title">{t.name}</div>
            <div className="dp-card-body">
              {t.notes ? t.notes.slice(0, 120) + (t.notes.length > 120 ? '…' : '') : ''}
            </div>
            <div className="dp-card-tags">
              {t.phase_4_track === 'evasion' && <span className="dp-ctag flight">Evade</span>}
              {t.phase_4_track === 'attribution' && <span className="dp-ctag claim">Claim</span>}
            </div>
          </Go>
        ))}
      </div>
    </>
  );
}
