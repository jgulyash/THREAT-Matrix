import { Fragment, type CSSProperties } from 'react';
import type { Tactic } from '../types/framework';
import {
  PHASE_NAMES,
  PHASE_SHORT,
  MATRICES,
  MATRIX_LABELS,
  MODALITY_LABELS,
  TRACK_LABELS,
  tacticMatchesFilters,
  type MatrixKey,
} from '../lib/constants';
import { getMatrix } from '../lib/data';
import { hrefFor, pathOf, type Route } from '../lib/route';
import { Go, useFilters } from '../lib/nav';
import { DraftTag } from './DraftTag';

interface HeatMapCellProps {
  tactics: Tactic[];
  matrix: MatrixKey;
  col: string;
  phase: 1 | 2 | 3 | 4;
  track?: 'flight' | 'claim';
  isSelected: boolean;
  showAll: boolean;
}

function HeatMapCell({ tactics, matrix, col, phase, track, isSelected, showAll }: HeatMapCellProps) {
  const { mode, actor } = useFilters();
  const displayed = tactics.filter((t) => tacticMatchesFilters(t, mode, actor));
  const count = displayed.length;
  const cls = track === 'flight' ? 'flight-cell' : track === 'claim' ? 'claim-cell' : '';
  const limit = showAll ? displayed.length : track ? 2 : 3;
  const where = `${MATRIX_LABELS[matrix]}, ${PHASE_NAMES[phase]}${track ? ' ' + TRACK_LABELS[track] : ''}`;
  return (
    <Go
      to={`/${matrix}/phase/${phase}${track ? '/' + track : ''}`}
      className={`hm-cell${cls ? ' ' + cls : ''}${isSelected ? ' selected' : ''}`}
      aria-label={`${where}: ${count} ${count === 1 ? 'tactic' : 'tactics'}`}
      aria-current={isSelected ? 'true' : undefined}
    >
      {track && <div className={`track-label ${track}`}>{TRACK_LABELS[track]}</div>}
      <div className={`hm-count ${col}`}>{count}</div>
      {count > 0 && (
        <div className={`hm-names${showAll ? ' all' : ''}`}>
          {displayed.slice(0, limit).map((t) => (
            <div key={t.id} className="hm-name">
              {t.name}
              {t.lifecycle_state && t.lifecycle_state !== 'active' ? ` (${t.lifecycle_state})` : ''}
            </div>
          ))}
          {count > limit && <div className="hm-overflow">+{count - limit} more</div>}
        </div>
      )}
    </Go>
  );
}

interface GridProps {
  // null shows every matrix side by side; a key scopes the grid to that matrix.
  scope: MatrixKey | null;
  compact: boolean;
  route: Route;
  selectedPhase?: number | null;
  selectedTrack?: string | null;
  selectedTacticId?: string | null;
}

export function HeatMapGrid({
  scope,
  compact,
  route,
  selectedPhase = null,
  selectedTrack = null,
  selectedTacticId = null,
}: GridProps) {
  const { mode, actor } = useFilters();
  const cols = MATRICES.filter((m) => !scope || m.key === scope);
  const gridVars = { '--hm-cols': cols.length } as CSSProperties;

  // Filter transparency: when a filter is active, show how much is hidden so a
  // reduced heat map never reads as missing data.
  const filterActive = !!mode || !!actor;
  const shownCount = (m: MatrixKey) =>
    getMatrix(m).tactics.filter((t) => tacticMatchesFilters(t, mode, actor)).length;
  const filterLabel = [mode ? MODALITY_LABELS[mode] : null, actor || null].filter(Boolean).join(' + ');

  const phaseSelected = (m: MatrixKey, phase: 1 | 2 | 3) => {
    if (scope !== m) return false;
    return selectedTacticId
      ? getMatrix(m).byPhase[phase].some((t) => t.id === selectedTacticId)
      : selectedPhase === phase;
  };

  const trackSelected = (m: MatrixKey, track: 'flight' | 'claim') => {
    if (scope !== m) return false;
    const tactics = getMatrix(m).byPhase[4][track];
    return (
      (!!selectedTacticId && tactics.some((t) => t.id === selectedTacticId)) ||
      (!selectedTacticId && selectedPhase === 4 && (selectedTrack === track || selectedTrack === null))
    );
  };

  return (
    <div className={`hm-wrap${scope ? ' scoped' : ''}`}>
      {filterActive && (
        <div className="hm-filter-note">
          <span className="hm-filter-tag">⌖ Filtered · {filterLabel}</span>
          <span className="hm-filter-detail">
            {cols.map((m, i) => (
              <span key={m.key}>
                {i > 0 ? ' · ' : ''}
                {m.label} <strong>{shownCount(m.key)}</strong> of {getMatrix(m.key).tactics.length}
              </span>
            ))}
            {'. '}
            <a href={hrefFor(pathOf(route))}>Clear the filter</a> to see all tactics.
          </span>
        </div>
      )}
      <div className="hm-scroll">
        <div className="hm-grid" style={gridVars}>
          <div className="hm-header-row">
            <div className="hm-col-hdr phase-col">Phase</div>
            {cols.map((m) => (
              <div key={m.key} className={`hm-col-hdr ${m.color}`}>
                {compact ? m.label : `${m.label} · ${getMatrix(m.key).tactics.length}`}
                <DraftTag matrix={m.key} />
              </div>
            ))}
          </div>
          <div className="hm-rows">
            {([1, 2, 3] as const).map((phase) => (
              <div key={phase} className="hm-row">
                <div className="hm-phase-cell">
                  <div className="hm-phase-name">{PHASE_SHORT[phase]}</div>
                </div>
                {cols.map((m) => (
                  <HeatMapCell
                    key={m.key}
                    tactics={getMatrix(m.key).byPhase[phase]}
                    matrix={m.key}
                    col={m.color}
                    phase={phase}
                    isSelected={phaseSelected(m.key, phase)}
                    showAll={!!scope}
                  />
                ))}
              </div>
            ))}
            <div className="phase4-row">
              <div className="phase4-phase-cell">
                <div className="hm-phase-name">{PHASE_SHORT[4]}</div>
              </div>
              <div className="phase4-content">
                {(['flight', 'claim'] as const).map((track) => (
                  <Fragment key={track}>
                    {track === 'claim' && <div className="phase4-divider" />}
                    <div className="phase4-sub-row">
                      {cols.map((m) => (
                        <HeatMapCell
                          key={m.key}
                          tactics={getMatrix(m.key).byPhase[4][track]}
                          matrix={m.key}
                          col={m.color}
                          phase={4}
                          track={track}
                          isSelected={trackSelected(m.key, track)}
                          showAll={!!scope}
                        />
                      ))}
                    </div>
                  </Fragment>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
