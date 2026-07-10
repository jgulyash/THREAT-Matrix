import type { Tactic, ActorProfile } from '../types/framework';
import { CATEGORY_ORDER, resolveTrack } from '../lib/constants';
import {
  IndicatorSection,
  CountermeasureSection,
  ResponseProtocolSection,
  EmptyState,
  SourceRefLink,
} from './detection-response';
import { AssessmentGuidanceView } from './AssessmentGuidanceView';

interface Props {
  tactic: Tactic | undefined;
  actorMap: Record<string, ActorProfile>;
  navigate: (path: string) => void;
  fromPhase?: number | null;
  fromTrack?: string | null;
}

export function TacticDetail({ tactic, actorMap, navigate, fromPhase, fromTrack }: Props) {
  if (!tactic) {
    return (
      <div style={{ padding: '20px', color: 'var(--text-dim)' }}>Tactic not found.</div>
    );
  }

  const abc: Record<string, Array<{ actor: ActorProfile; relevance: string }>> = {};
  (tactic.actor_associations || []).forEach((a) => {
    const actor = actorMap[a.actor_id];
    if (!actor) return;
    if (!abc[actor.category]) abc[actor.category] = [];
    abc[actor.category].push({ actor, relevance: a.relevance });
  });
  const cats = CATEGORY_ORDER.filter((c) => abc[c]);

  const back = fromPhase
    ? fromTrack
      ? `/${tactic.matrix}/phase/${fromPhase}/${fromTrack}`
      : `/${tactic.matrix}/phase/${fromPhase}`
    : `/${tactic.matrix}`;
  const tl = resolveTrack(tactic);

  const hasIndicators = (tactic.indicators || []).length > 0;
  const hasCountermeasures = (tactic.countermeasures || []).length > 0;
  const hasProtocols = (tactic.response_protocols || []).length > 0;
  const hasAnyDR = hasIndicators || hasCountermeasures || hasProtocols;

  return (
    <>
      <div className="dp-header">
        <div className="dp-back" onClick={() => navigate(back)}>
          ← Back
        </div>
        <div className="dp-crumb">
          <span>Phase {tactic.phase}</span>
          <span className="dp-crumb-sep">›</span>
          {tl && (
            <>
              <span style={{ color: 'var(--slate)' }}>
                {tl === 'flight' ? 'Evade' : 'Claim'}
              </span>
              <span className="dp-crumb-sep">›</span>
            </>
          )}
          <span className="dp-crumb-active">{tactic.name}</span>
        </div>
        <div className="det-id-row">
          <span className="det-id">{tactic.id}</span>
          {tl && (
            <span className={`det-track-badge ${tl}`}>
              {tl === 'flight' ? 'EVADE' : 'CLAIM'}
            </span>
          )}
        </div>
        <div className="dp-header-title">{tactic.name}</div>
      </div>
      <div className="dp-content">
        {tactic.cpn && tactic.cpn_id && (
          <div className="det-cpn-badge">
            <span className="det-cpn-mark">⌖</span> {tactic.cpn_id}
          </div>
        )}

        <div className="det-section">
          <div className="det-section-label">Description</div>
          <div className="det-body">{tactic.notes}</div>
        </div>

        <AssessmentGuidanceView guidance={tactic.assessment_guidance} />

        {tactic.cpn && tactic.cpn_notes && (
          <div className="det-section">
            <div className="det-section-label">Cyber-Physical Nexus</div>
            <div className="det-cpn-section">{tactic.cpn_notes}</div>
          </div>
        )}

        {cats.length > 0 && (
          <div className="det-section">
            <div className="det-section-label">Actor Associations</div>
            <div className="det-actor-groups">
              {cats.map((cat) => (
                <div key={cat}>
                  <div className="det-actor-cat-label">
                    {abc[cat][0].actor.category_label}
                  </div>
                  <div className="det-actor-chips">
                    {abc[cat].map(({ actor, relevance }, i) => (
                      <span
                        key={`${actor.id}-${i}`}
                        className={`det-actor-chip${relevance === 'high' ? ' high' : ''}`}
                        onClick={() => navigate(`/actors/${actor.id}`)}
                        title={`${actor.id} · ${relevance} relevance`}
                      >
                        {actor.name}
                      </span>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Detection & Response */}
        {hasAnyDR ? (
          <>
            {hasIndicators && (
              <IndicatorSection indicators={tactic.indicators} matrix={tactic.matrix} navigate={navigate} />
            )}
            {hasCountermeasures && (
              <CountermeasureSection
                countermeasures={tactic.countermeasures}
                navigate={navigate}
              />
            )}
            {hasProtocols && (
              <ResponseProtocolSection
                protocols={tactic.response_protocols}
                navigate={navigate}
              />
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
                <SourceRefLink key={ref} refKey={ref} navigate={navigate} />
              ))}
            </div>
          </div>
        )}
      </div>
    </>
  );
}
