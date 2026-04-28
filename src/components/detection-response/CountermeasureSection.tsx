import type { Countermeasure } from '../../types/framework';
import {
  COUNTERMEASURE_CATEGORY_LABELS,
  DOMAIN_LABELS,
  groupByCategory,
} from '../../lib/constants';
import { SourceRefLink } from './SourceRefLink';

interface Props {
  countermeasures: Countermeasure[];
  navigate: (path: string) => void;
}

export function CountermeasureSection({ countermeasures, navigate }: Props) {
  if (!countermeasures?.length) return null;

  const { orderedKeys, grouped } = groupByCategory(
    countermeasures,
    COUNTERMEASURE_CATEGORY_LABELS
  );

  return (
    <div className="det-section">
      <div className="dr-section-header">
        <span>Countermeasures</span>
        <span className="dr-section-count">{countermeasures.length} measures</span>
      </div>
      {orderedKeys.map((cat) => (
        <div key={cat} className="dr-category-group">
          <div className="dr-category-label">
            {COUNTERMEASURE_CATEGORY_LABELS[cat] || cat}
          </div>
          {grouped[cat].map((cm) => (
            <div key={cm.id} className="dr-item">
              <div className="dr-item-id">{cm.id}</div>
              <div className="dr-item-body">{cm.measure}</div>
              <div className="dr-badge-row">
                {cm.domain && (
                  <span className="dr-tag" style={{ borderColor: 'var(--slate)', color: 'var(--slate)', background: 'var(--slate-dim)' }}>
                    {DOMAIN_LABELS[cm.domain] || cm.domain}
                  </span>
                )}
                <span className={`dr-badge ${cm.cost}`}>
                  <span className="dr-badge-key">Cost</span>
                  <span>{cm.cost}</span>
                </span>
                <span className={`dr-badge ${cm.complexity}`}>
                  <span className="dr-badge-key">Complexity</span>
                  <span>{cm.complexity}</span>
                </span>
                <span className={`dr-badge ${cm.time_to_implement}`}>
                  <span className="dr-badge-key">Time</span>
                  <span>{cm.time_to_implement}</span>
                </span>
              </div>
              {cm.limitations && (
                <div className="dr-limitations">
                  <span className="dr-limitations-label">Limits</span>
                  {cm.limitations}
                </div>
              )}
              {cm.source_refs?.length > 0 && (
                <div className="dr-tag-row">
                  {cm.source_refs.map((ref) => (
                    <SourceRefLink key={ref} refKey={ref} navigate={navigate} />
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      ))}
    </div>
  );
}
