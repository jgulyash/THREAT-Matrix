import type { ActorProfile } from '../types/framework';
import { orderedActorCategories } from '../lib/constants';

interface Props {
  cpnFilter: boolean;
  setCpnFilter: (fn: (v: boolean) => boolean) => void;
  actorFilter: string;
  setActorFilter: (v: string) => void;
  actorsByCategory: Record<string, ActorProfile[]>;
}

export function FilterBar({
  cpnFilter,
  setCpnFilter,
  actorFilter,
  setActorFilter,
  actorsByCategory,
}: Props) {
  return (
    <div className="filterbar">
      <span className="fb-label">Filter</span>
      <div className="fb-sep" />
      <span
        className={`fb-chip${cpnFilter ? ' amber-active' : ' dim'}`}
        onClick={() => setCpnFilter((v) => !v)}
        title="Show only Cyber-Physical Nexus tactics"
      >
        ⌖ CPN
      </span>
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
