import type { ActorProfile, Tactic } from '../types/framework';
import { VECTOR_LABELS, AI_RISK_LABELS } from '../lib/constants';

interface Props {
  actor: ActorProfile | undefined;
  navigate: (path: string) => void;
  getActorTactics: (id: string) => Tactic[];
}

export function ActorDetailView({ actor, navigate, getActorTactics }: Props) {
  if (!actor) {
    return (
      <div className="actor-detail-view">
        <div className="adv-back" onClick={() => navigate('/actors')}>
          ← All Profiles
        </div>
        <div style={{ color: 'var(--text-dim)', fontSize: '13px' }}>Actor not found.</div>
      </div>
    );
  }

  const associated = getActorTactics(actor.id);

  const attrs: Array<[string, string | undefined]> = [
    ['Awareness', actor.awareness],
    ['Direction', actor.direction],
    ['Access Relationship', actor.access_relationship],
    ['Phase Compression Risk', actor.phase_compression_risk],
    ...(actor.actor_level ? [['Actor Level', actor.actor_level] as [string, string]] : []),
  ];

  return (
    <div className="actor-detail-view">
      <div className="adv-back" onClick={() => navigate('/actors')}>
        ← All Profiles
      </div>
      <div className="adv-category-row">
        <span className="adv-category-name">{actor.category_label}</span>
        <span className="adv-category-sep">›</span>
        <span className="adv-category-id">{actor.id}</span>
      </div>
      <div className="adv-name">{actor.name}</div>
      <div className="adv-two-col">
        <div className="adv-two-col-left">
          <div className="adv-section">
            <div className="adv-section-label">Profile Attributes</div>
            <div className="adv-attrs-list">
              {attrs.map(([k, v]) => (
                <div key={k} className="adv-attr-row-new">
                  <div className="adv-attr-key">{k}</div>
                  <div className="adv-attr-val">{v}</div>
                </div>
              ))}
            </div>
          </div>
          {actor.description && (
            <div className="adv-section">
              <div className="adv-section-label">Description</div>
              <div className="adv-body">{actor.description}</div>
            </div>
          )}
          {actor.attack_vectors && actor.attack_vectors.length > 0 && (
            <div className="adv-section">
              <div className="adv-section-label">Attack Vectors</div>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
                {actor.attack_vectors.map((v) => (
                  <span key={v} className="actor-vector-tag">
                    {VECTOR_LABELS[v] || v}
                  </span>
                ))}
              </div>
            </div>
          )}
          {actor.behavioral_markers && actor.behavioral_markers.length > 0 && (
            <div className="adv-section">
              <div className="adv-section-label">Behavioral Markers</div>
              <div className="adv-markers">
                {actor.behavioral_markers.map((m, i) => (
                  <div key={i} className="adv-marker">
                    <div className="adv-marker-dot" />
                    <div>{m}</div>
                  </div>
                ))}
              </div>
            </div>
          )}
          {actor.ai_enabled_risks && actor.ai_enabled_risks.length > 0 && (
            <div className="adv-section">
              <div className="adv-section-label">AI-Enabled Risks</div>
              <div>
                {actor.ai_enabled_risks.map((r) => (
                  <span key={r} className="adv-risk-tag">
                    {AI_RISK_LABELS[r] || r}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
        <div className="adv-two-col-right">
          {associated.length > 0 && (
            <div className="adv-section">
              <div className="adv-section-label">
                Associated Tactics ({associated.length})
              </div>
              <div>
                {associated.map((t) => (
                  <div
                    key={t.id}
                    className="adv-tactic-link"
                    onClick={() => navigate(`/person/tactic/${t.id}`)}
                  >
                    <span className="adv-tactic-id">{t.id}</span>
                    <span>{t.name}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
