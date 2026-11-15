import type { Indicator } from '../../types/framework';
import {
  INDICATOR_CATEGORY_LABELS,
  DETECTION_SOURCE_LABELS,
  groupByCategory,
  label,
} from '../../lib/constants';
import { indicatorById } from '../../lib/data';
import { seg } from '../../lib/route';
import { Go } from '../../lib/nav';
import { LifecycleTag } from '../Lifecycle';
import { SourceRefLink } from './SourceRefLink';

interface Props {
  indicators: Indicator[];
}

// Links resolve the matrix from the indicator itself, so a cross-matrix
// relation opens under the right tab.
const indicatorPath = (id: string): string | null => {
  const e = indicatorById.get(id);
  return e ? `/${e.tactic.matrix}/indicator/${seg(id)}` : null;
};

export function IndicatorSection({ indicators }: Props) {
  if (!indicators?.length) return null;

  const { orderedKeys, grouped } = groupByCategory(indicators, INDICATOR_CATEGORY_LABELS);

  return (
    <div className="det-section">
      <h2 className="dr-section-header">
        <span>Indicators</span>
        <span className="dr-section-count">{indicators.length} observable</span>
      </h2>
      {orderedKeys.map((cat) => (
        <div key={cat} className="dr-category-group">
          <h3 className="dr-category-label">{label(INDICATOR_CATEGORY_LABELS, cat)}</h3>
          {(grouped.get(cat) || []).map((ind) => (
            <div key={ind.id} className="dr-item">
              <Go
                className="dr-item-id link"
                to={indicatorPath(ind.id) || '/'}
                title="View indicator detail"
                aria-label={`${ind.id}, view indicator detail`}
              >
                {ind.id} ›
              </Go>
              <LifecycleTag item={ind} />
              <div className="dr-item-body">{ind.behavior}</div>
              {ind.detection_sources && ind.detection_sources.length > 0 && (
                <div className="dr-tag-row">
                  {ind.detection_sources.map((src) => (
                    <span key={src} className="dr-tag">
                      {label(DETECTION_SOURCE_LABELS, src)}
                    </span>
                  ))}
                </div>
              )}
              {ind.correlates_with && ind.correlates_with.length > 0 && (
                <div className="dr-tag-row">
                  <span className="dr-mesh-label">Related</span>
                  {ind.correlates_with.map((relId) => {
                    const to = indicatorPath(relId);
                    const rel = indicatorById.get(relId);
                    return to ? (
                      <Go key={relId} className="dr-tag mesh link" to={to} title={rel?.indicator.behavior}>
                        {relId}
                      </Go>
                    ) : (
                      <span key={relId} className="dr-tag mesh" title="Unresolved reference">
                        {relId}
                      </span>
                    );
                  })}
                </div>
              )}
              {ind.source_refs && ind.source_refs.length > 0 && (
                <details className="dr-details">
                  <summary>Sources</summary>
                  <div className="dr-details-body">
                    <div className="dr-tag-row">
                      {ind.source_refs.map((ref) => (
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
