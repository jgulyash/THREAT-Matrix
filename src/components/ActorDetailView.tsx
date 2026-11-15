import { VECTOR_LABELS, AI_RISK_LABELS, MATRIX_LABELS, humanize, label } from '../lib/constants';
import { actorById, actorTactics } from '../lib/data';
import { seg } from '../lib/route';
import { Go } from '../lib/nav';
import { DraftTag } from './DraftTag';
import { LifecycleNote } from './Lifecycle';

interface Props {
  actorId: string;
}

// The router has already confirmed that actorId is a listed profile.
export function ActorDetailView({ actorId }: Props) {
  const actor = actorById.get(actorId);
  if (!actor) return null;

  const associated = actorTactics(actor.id);

  const attrs: Array<[string, string | undefined]> = [
    ['Awareness', actor.awareness],
    ['Direction', actor.direction],
    ['Access Relationship', actor.access_relationship],
    ['Phase Compression Risk', actor.phase_compression_risk],
    ['Actor Level', actor.actor_level],
  ];

  return (
    <div className="actor-detail-view">
      <Go className="adv-back" to="/actors">
        ← All Profiles
      </Go>
      <div className="adv-category-row">
        <span className="adv-category-name">{actor.category_label}</span>
        <span className="adv-category-sep">›</span>
        <span className="adv-category-id">{actor.id}</span>
      </div>
      <div className="adv-name" data-focus-target tabIndex={-1}>
        {actor.name}
      </div>
      <LifecycleNote item={actor} />
      <div className="adv-two-col">
        <div className="adv-two-col-left">
          <div className="adv-section">
            <div className="adv-section-label">Profile Attributes</div>
            <div className="adv-attrs-list">
              {attrs
                .filter(([, v]) => !!v)
                .map(([k, v]) => (
                  <div key={k} className="adv-attr-row-new">
                    <div className="adv-attr-key">{k}</div>
                    <div className="adv-attr-val">{humanize(v || '')}</div>
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
              <div className="actor-vectors wide">
                {actor.attack_vectors.map((v) => (
                  <span key={v} className="actor-vector-tag">
                    {label(VECTOR_LABELS, v)}
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
                    {label(AI_RISK_LABELS, r)}
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
                  <Go
                    key={t.id}
                    className="adv-tactic-link"
                    to={`/${t.matrix}/tactic/${seg(t.id)}`}
                    title={MATRIX_LABELS[t.matrix]}
                  >
                    <span className="adv-tactic-id">{t.id}</span>
                    <span>{t.name}</span>
                    <DraftTag matrix={t.matrix} />
                  </Go>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
