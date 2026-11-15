import { orderedActorCategories, VECTOR_LABELS, humanize, label } from '../lib/constants';
import { actors, actorsByCategory } from '../lib/data';
import { seg } from '../lib/route';
import { Go } from '../lib/nav';
import { LifecycleTag } from './Lifecycle';

export function ActorProfilesView() {
  const groups = orderedActorCategories(actorsByCategory);
  return (
    <div className="actors-view">
      <h1 className="actors-view-title" data-focus-target tabIndex={-1}>
        Actor Profiles
      </h1>
      <div className="actors-view-sub">
        {actors.length} profiles across {groups.length} categories
      </div>
      {groups.map(({ cat, label: catLabel, actors: list }) => {
        return (
          <div key={cat} className="actor-cat-section">
            <h2 className="actor-cat-label">
              {catLabel}
              <span className="actor-cat-count">{list.length}</span>
            </h2>
            <div className="actor-cards-grid">
              {list.map((a) => (
                <Go key={a.id} className="actor-card" to={`/actors/${seg(a.id)}`}>
                  <div className="actor-card-id">
                    {a.id}
                    <LifecycleTag item={a} />
                  </div>
                  <div className="actor-card-name">{a.name}</div>
                  <div className="actor-card-attrs">
                    <div className="actor-attr-row">
                      <span className="actor-attr-key">Awareness</span>
                      <span>{humanize(a.awareness || '')}</span>
                    </div>
                    <div className="actor-attr-row">
                      <span className="actor-attr-key">Direction</span>
                      <span>{humanize(a.direction || '')}</span>
                    </div>
                    <div className="actor-attr-row">
                      <span className="actor-attr-key">Access</span>
                      <span>{humanize(a.access_relationship || '')}</span>
                    </div>
                    <div className="actor-attr-row">
                      <span className="actor-attr-key">Phase Risk</span>
                      <span>{humanize(a.phase_compression_risk || '')}</span>
                    </div>
                  </div>
                  {a.attack_vectors && a.attack_vectors.length > 0 && (
                    <div className="actor-vectors">
                      {a.attack_vectors.slice(0, 3).map((v) => (
                        <span key={v} className="actor-vector-tag">
                          {label(VECTOR_LABELS, v)}
                        </span>
                      ))}
                    </div>
                  )}
                </Go>
              ))}
            </div>
          </div>
        );
      })}
    </div>
  );
}
