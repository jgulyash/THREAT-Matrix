import type { Countermeasure } from '../../types/framework';
import {
  COUNTERMEASURE_CATEGORY_LABELS,
  DOMAIN_LABELS,
  TIME_TO_IMPLEMENT_LABELS,
  groupByCategory,
  humanize,
  label,
} from '../../lib/constants';
import { LifecycleNote } from '../Lifecycle';
import { SourceRefLink } from './SourceRefLink';

interface Props {
  countermeasures: Countermeasure[];
  focusId?: string | null;
}

export function CountermeasureSection({ countermeasures, focusId }: Props) {
  if (!countermeasures?.length) return null;

  const { orderedKeys, grouped } = groupByCategory(
    countermeasures,
    COUNTERMEASURE_CATEGORY_LABELS
  );

  return (
    <div className="det-section">
      <h2 className="dr-section-header">
        <span>Countermeasures</span>
        <span className="dr-section-count">{countermeasures.length} measures</span>
      </h2>
      {orderedKeys.map((cat) => (
        <div key={cat} className="dr-category-group">
          <h3 className="dr-category-label">{label(COUNTERMEASURE_CATEGORY_LABELS, cat)}</h3>
          {(grouped.get(cat) || []).map((cm) => (
            <div
              key={cm.id}
              className={`dr-item${focusId === cm.id ? ' cited' : ''}`}
              data-item-id={cm.id}
              tabIndex={-1}
            >
              <div className="dr-item-id">{cm.id}</div>
              <LifecycleNote item={cm} />
              <div className="dr-item-body">{cm.measure}</div>
              <div className="dr-badge-row">
                {cm.domain && <span className="dr-tag domain">{label(DOMAIN_LABELS, cm.domain)}</span>}
                {cm.cost && (
                  <span className={`dr-badge ${cm.cost}`}>
                    <span className="dr-badge-key">Cost</span>
                    <span>{humanize(cm.cost)}</span>
                  </span>
                )}
                {cm.complexity && (
                  <span className={`dr-badge ${cm.complexity}`}>
                    <span className="dr-badge-key">Complexity</span>
                    <span>{humanize(cm.complexity)}</span>
                  </span>
                )}
                {cm.time_to_implement && (
                  <span className={`dr-badge ${cm.time_to_implement}`}>
                    <span className="dr-badge-key">Time</span>
                    <span>{label(TIME_TO_IMPLEMENT_LABELS, cm.time_to_implement)}</span>
                  </span>
                )}
              </div>
              {cm.limitations && (
                <div className="dr-limitations">
                  <span className="dr-limitations-label">Limits</span>
                  {cm.limitations}
                </div>
              )}
              {cm.source_refs && cm.source_refs.length > 0 && (
                <details className="dr-details">
                  <summary>Sources</summary>
                  <div className="dr-details-body">
                    <div className="dr-tag-row">
                      {cm.source_refs.map((ref) => (
                        <SourceRefLink key={ref} refKey={ref} />
                      ))}
                    </div>
                  </div>
                </details>
              )}
            </div>
          ))}
        </div>
      ))}
    </div>
  );
}
