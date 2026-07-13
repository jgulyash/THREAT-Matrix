import type { ActorProfile } from '../types/framework';
import { orderedActorCategories, VECTOR_LABELS } from '../lib/constants';

interface Props {
  actorsByCategory: Record<string, ActorProfile[]>;
  navigate: (path: string) => void;
}

export function ActorProfilesView({ actorsByCategory, navigate }: Props) {
  const total = Object.values(actorsByCategory).reduce((s, a) => s + a.length, 0);
  return (
    <div className="actors-view">
      <div className="actors-view-title">Actor Profiles</div>
      <div className="actors-view-sub">
        {total} profiles across {Object.keys(actorsByCategory).length} threat categories
      </div>
      {orderedActorCategories(actorsByCategory).map(({ cat, label, actors }) => {
        return (
          <div key={cat} className="actor-cat-section">
            <div className="actor-cat-label">
              {label}
              <span className="actor-cat-count">{actors.length}</span>
            </div>
            <div className="actor-cards-grid">
              {actors.map((a) => (
                <div
                  key={a.id}
                  className="actor-card"
                  onClick={() => navigate(`/actors/${a.id}`)}
                >
                  <div className="actor-card-id">{a.id}</div>
                  <div className="actor-card-name">{a.name}</div>
                  <div className="actor-card-attrs">
                    <div className="actor-attr-row">
                      <span className="actor-attr-key">Awareness</span>
                      <span>{a.awareness}</span>
                    </div>
                    <div className="actor-attr-row">
                      <span className="actor-attr-key">Direction</span>
                      <span>{a.direction}</span>
                    </div>
                    <div className="actor-attr-row">
                      <span className="actor-attr-key">Access</span>
                      <span>{a.access_relationship}</span>
                    </div>
                    <div className="actor-attr-row">
                      <span className="actor-attr-key">Phase Risk</span>
                      <span>{a.phase_compression_risk}</span>
                    </div>
                  </div>
                  {a.attack_vectors && a.attack_vectors.length > 0 && (
                    <div className="actor-vectors">
                      {a.attack_vectors.slice(0, 3).map((v) => (
                        <span key={v} className="actor-vector-tag">
                          {VECTOR_LABELS[v] || v}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        );
      })}
    </div>
  );
}
