import { useLayoutEffect, useRef } from 'react';
import type { Tactic, ActorProfile } from '../types/framework';
import { CATEGORY_ORDER, MATRIX_LABELS, TRACK_LABELS, humanize, resolveTrack } from '../lib/constants';
import { actorById } from '../lib/data';
import { seg } from '../lib/route';
import { Go } from '../lib/nav';
import {
  IndicatorSection,
  CountermeasureSection,
  ResponseProtocolSection,
  EmptyState,
  SourceRefLink,
} from './detection-response';
import { AssessmentGuidanceView } from './AssessmentGuidanceView';
import { DraftTag } from './DraftTag';
import { LifecycleNote } from './Lifecycle';
import { TacticPriority } from './overlay/TacticPriority';

interface Props {
  tactic: Tactic;
  // A countermeasure or response protocol of this tactic to scroll to.
  focusId: string | null;
}

interface Chip {
  actor: ActorProfile;
  relevance: string;
  status: string | null;
}

export function TacticDetail({ tactic, focusId }: Props) {
  const contentRef = useRef<HTMLDivElement>(null);

  useLayoutEffect(() => {
    if (!focusId) return;
    const el = contentRef.current?.querySelector<HTMLElement>(`[data-item-id="${CSS.escape(focusId)}"]`);
    if (!el) return;
    el.scrollIntoView({ block: 'start' });
    el.focus({ preventScroll: true });
  }, [focusId, tactic.id]);

  const groups = new Map<string, Chip[]>();
  (tactic.actor_associations || []).forEach((a) => {
    const actor = actorById.get(a.actor_id);
    if (!actor) return;
    const chip: Chip = { actor, relevance: a.relevance, status: a.employment_status || null };
    const list = groups.get(actor.category);
    if (list) list.push(chip);
    else groups.set(actor.category, [chip]);
  });
  const cats = [
    ...CATEGORY_ORDER.filter((c) => groups.has(c)),
    ...[...groups.keys()].filter((c) => !CATEGORY_ORDER.includes(c)),
  ];

  const tl = resolveTrack(tactic);
  const back = `/${tactic.matrix}/phase/${tactic.phase}${tl ? '/' + tl : ''}`;

  const hasIndicators = tactic.indicators.length > 0;
  const hasCountermeasures = tactic.countermeasures.length > 0;
  const hasProtocols = tactic.response_protocols.length > 0;
  const hasAnyDR = hasIndicators || hasCountermeasures || hasProtocols;

  return (
    <>
      <div className="dp-header">
        <Go className="dp-back" to={back}>
          ← Back
        </Go>
        <div className="dp-crumb">
          <span>
            {MATRIX_LABELS[tactic.matrix]}
            <DraftTag matrix={tactic.matrix} />
          </span>
          <span className="dp-crumb-sep">›</span>
          <span>Phase {tactic.phase}</span>
          <span className="dp-crumb-sep">›</span>
          {tl && (
            <>
              <span className="dp-crumb-track">{TRACK_LABELS[tl]}</span>
              <span className="dp-crumb-sep">›</span>
            </>
          )}
          <span className="dp-crumb-active">{tactic.name}</span>
        </div>
        <div className="det-id-row">
          <span className="det-id">{tactic.id}</span>
          {tl && <span className={`det-track-badge ${tl}`}>{TRACK_LABELS[tl].toUpperCase()}</span>}
        </div>
        <div className="dp-header-title" data-focus-target tabIndex={-1}>
          {tactic.name}
        </div>
        <LifecycleNote item={tactic} />
      </div>
      <div className="dp-content" ref={contentRef}>
        <div className="det-section">
          <div className="det-section-label">Description</div>
          <div className="det-body">{tactic.notes}</div>
        </div>

        {cats.length > 0 && (
          <div className="det-section">
            <div className="det-section-label">Actor Associations</div>
            <div className="det-actor-groups">
              {cats.map((cat) => {
                const chips = groups.get(cat) || [];
                return (
                  <div key={cat}>
                    <div className="det-actor-cat-label">{chips[0].actor.category_label}</div>
                    <div className="det-actor-chips">
                      {chips.map(({ actor, relevance, status }) => (
                        <Go
                          key={`${actor.id}-${status || 'current'}`}
                          to={`/actors/${seg(actor.id)}`}
                          className={`det-actor-chip${relevance === 'high' ? ' high' : ''}`}
                          title={`${actor.id} · ${relevance} relevance${status ? ' · ' + humanize(status) : ''}`}
                        >
                          {actor.name}
                          {status ? ` (${humanize(status).toLowerCase()})` : ''}
                        </Go>
                      ))}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        <AssessmentGuidanceView guidance={tactic.assessment_guidance} />
        <TacticPriority tacticId={tactic.id} />

        {/* Detection & Response */}
        {hasAnyDR ? (
          <>
            {hasIndicators && <IndicatorSection indicators={tactic.indicators} />}
            {hasCountermeasures && (
              <CountermeasureSection countermeasures={tactic.countermeasures} focusId={focusId} />
            )}
            {hasProtocols && (
              <ResponseProtocolSection protocols={tactic.response_protocols} focusId={focusId} />
            )}
          </>
        ) : (
          <EmptyState />
        )}

        {/* Tactic source citations (aggregate) */}
        {tactic.source_refs && tactic.source_refs.length > 0 && (
          <div className="det-section">
            <div className="det-section-label">Sources</div>
            <div className="dr-tag-row">
              {tactic.source_refs.map((ref) => (
                <SourceRefLink key={ref} refKey={ref} />
              ))}
            </div>
          </div>
        )}
      </div>
    </>
  );
}
