import type { Indicator } from '../../types/framework';
import {
  INDICATOR_CATEGORY_LABELS,
  DETECTION_SOURCE_LABELS,
  groupByCategory,
} from '../../lib/constants';
import { SourceRefLink } from './SourceRefLink';

interface Props {
  indicators: Indicator[];
  navigate: (path: string) => void;
}

export function IndicatorSection({ indicators, navigate }: Props) {
  if (!indicators?.length) return null;

  const { orderedKeys, grouped } = groupByCategory(indicators, INDICATOR_CATEGORY_LABELS);

  return (
    <div className="det-section">
      <div className="dr-section-header">
        <span>Indicators</span>
        <span className="dr-section-count">{indicators.length} observable</span>
      </div>
      {orderedKeys.map((cat) => (
        <div key={cat} className="dr-category-group">
          <div className="dr-category-label">
            {INDICATOR_CATEGORY_LABELS[cat] || cat}
          </div>
          {grouped[cat].map((ind) => (
            <div key={ind.id} className="dr-item">
              <div className="dr-item-id">{ind.id}</div>
              <div className="dr-item-body">{ind.behavior}</div>
              {ind.detection_sources?.length > 0 && (
                <div className="dr-tag-row">
                  {ind.detection_sources.map((src) => (
                    <span key={src} className="dr-tag">
                      {DETECTION_SOURCE_LABELS[src] || src}
                    </span>
                  ))}
                </div>
              )}
              {ind.source_refs?.length > 0 && (
                <div className="dr-tag-row">
                  {ind.source_refs.map((ref) => (
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
