import type { ActorProfile } from '../types/framework';
import { orderedActorCategories, MODALITY_ORDER, MODALITY_LABELS, MODALITY_DEFS } from '../lib/constants';

interface Props {
  modalityFilter: string;
  setModalityFilter: (v: string) => void;
  actorFilter: string;
  setActorFilter: (v: string) => void;
  actorsByCategory: Record<string, ActorProfile[]>;
}

export function FilterBar({
  modalityFilter,
  setModalityFilter,
  actorFilter,
  setActorFilter,
  actorsByCategory,
}: Props) {
  return (
    <div className="filterbar">
      <span className="fb-label">Filter</span>
      <div className="fb-sep" />
      <select
        className={`fb-select${modalityFilter ? ' amber-active' : ''}`}
        value={modalityFilter}
        onChange={(e) => setModalityFilter(e.target.value)}
        title={
          modalityFilter
            ? MODALITY_DEFS[modalityFilter]
            : 'Behavioral Mode: the mechanism a behavior operates through. Show only tactics with an indicator of the selected mode.'
        }
      >
        <option value="">Behavioral Mode · All</option>
        {MODALITY_ORDER.map((m) => (
          <option key={m} value={m} title={MODALITY_DEFS[m]}>
            {MODALITY_LABELS[m]}
          </option>
        ))}
      </select>
      <div className="fb-sep" />
      <select
        className={`fb-select${actorFilter ? ' amber-active' : ''}`}
        value={actorFilter}
        onChange={(e) => setActorFilter(e.target.value)}
        title="Show only tactics associated with an actor profile"
      >
        <option value="">Actor · All</option>
        {orderedActorCategories(actorsByCategory).map(({ cat, label, actors }) => (
          <optgroup key={cat} label={label}>
            {actors.map((a) => (
              <option key={a.id} value={a.id}>
                {a.id} · {a.name}
              </option>
            ))}
          </optgroup>
        ))}
      </select>
    </div>
  );
}
