import type { LifecycleFields } from '../types/framework';
import { actorById, childById, indicatorById, tacticById } from '../lib/data';
import { seg } from '../lib/route';
import { Go } from '../lib/nav';

const retired = (item: LifecycleFields): 'deprecated' | 'superseded' | null =>
  item.lifecycle_state === 'deprecated' || item.lifecycle_state === 'superseded'
    ? item.lifecycle_state
    : null;

// Where a replacement ID lives, whatever its namespace.
function pathForId(id: string): string | null {
  const t = tacticById.get(id);
  if (t) return `/${t.matrix}/tactic/${seg(t.id)}`;
  const i = indicatorById.get(id);
  if (i) return `/${i.tactic.matrix}/indicator/${seg(id)}`;
  const c = childById.get(id);
  if (c) return `/${c.tactic.matrix}/tactic/${seg(c.tactic.id)}/${seg(id)}`;
  if (actorById.has(id)) return `/actors/${seg(id)}`;
  return null;
}

// Short inline marker for lists and headers.
export function LifecycleTag({ item }: { item: LifecycleFields }) {
  const state = retired(item);
  if (!state) return null;
  return <span className="type-level-tag lifecycle-tag">{state}</span>;
}

// Full marker for detail views: state, version, reason, and for a superseded
// object a link to its replacement.
export function LifecycleNote({ item }: { item: LifecycleFields }) {
  const state = retired(item);
  if (!state) return null;
  const to = item.superseded_by ? pathForId(item.superseded_by) : null;
  return (
    <div className="lifecycle-note" data-lifecycle={state}>
      <strong>{state === 'superseded' ? 'Superseded' : 'Deprecated'}</strong>
      {item.deprecated_in ? ` in version ${item.deprecated_in}` : ''}.
      {item.deprecation_reason ? ` ${item.deprecation_reason}` : ''}
      {state === 'superseded' && item.superseded_by && (
        <>
          {' '}Replaced by{' '}
          {to ? <Go to={to}>{item.superseded_by}</Go> : <span>{item.superseded_by}</span>}.
        </>
      )}
    </div>
  );
}
