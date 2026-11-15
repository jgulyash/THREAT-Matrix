import { orderedActorCategories, MODALITY_ORDER, MODALITY_LABELS, MODALITY_DEFS } from '../lib/constants';
import { actorsByCategory } from '../lib/data';
import { hrefFor, pathOf, type Filters, type Route } from '../lib/route';

interface Props {
  route: Route;
  filters: Filters;
}

// Filter state lives in the URL (?mode=...&actor=...), so a filtered view can
// be linked, survives reload, and is cleared by one control.
export function FilterBar({ route, filters }: Props) {
  const path = pathOf(route);
  const apply = (next: Filters) => {
    window.location.hash = hrefFor(path, next);
  };
  const active = !!filters.mode || !!filters.actor;
  return (
    <div className="filterbar" role="group" aria-label="Filter tactics">
      <span className="fb-label">Filter</span>
      <div className="fb-sep" />
      <select
        className={`fb-select${filters.mode ? ' amber-active' : ''}`}
        value={filters.mode}
        onChange={(e) => apply({ ...filters, mode: e.target.value })}
        aria-label="Filter by behavioral mode"
        title={
          filters.mode
            ? MODALITY_DEFS[filters.mode]
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
        className={`fb-select${filters.actor ? ' amber-active' : ''}`}
        value={filters.actor}
        onChange={(e) => apply({ ...filters, actor: e.target.value })}
        aria-label="Filter by actor profile"
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
      {active && (
        <a className="fb-clear" data-filter-clear href={hrefFor(path)}>
          Clear filter
        </a>
      )}
    </div>
  );
}
