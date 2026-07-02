import type { Indicator, Tactic } from '../types/framework';
import {
  INDICATOR_CATEGORY_LABELS,
  DETECTION_SOURCE_LABELS,
  TARGET_IDENTITY_LABELS,
  SEVERITY_BAND_LABELS,
  TEMPORAL_SIGNATURE_LABELS,
  EVIDENCE_TIER_LABELS,
  ESCALATION_AXIS_LABELS,
  INFORMS_AXIS_LABELS,
  PHASE_RELEVANCE_LABELS,
} from '../lib/constants';
import { SourceRefLink } from './detection-response/SourceRefLink';

export interface IndicatorEntry {
  indicator: Indicator;
  tactic: Tactic;
}

interface Props {
  indicatorId: string;
  indicatorMap: Record<string, IndicatorEntry>;
  navigate: (path: string) => void;
}

export function IndicatorDetail({ indicatorId, indicatorMap, navigate }: Props) {
  const entry = indicatorMap[indicatorId];

  if (!entry) {
    return (
      <div className="actor-detail-view">
        <div className="adv-back" onClick={() => navigate('/person')}>
          ← Heat Map
        </div>
        <div style={{ color: 'var(--text-dim)', fontSize: '13px' }}>
          Indicator <strong>{indicatorId}</strong> not found.
        </div>
      </div>
    );
  }

  const { indicator: ind, tactic } = entry;
  const catLabel = INDICATOR_CATEGORY_LABELS[ind.category] || ind.category;

  // informs_axes is sparse pre-IRR-consensus; render only populated axes
  const informsRows = ind.informs_axes
    ? (Object.entries(ind.informs_axes) as [string, string | undefined][]).filter(
        ([, v]) => v && v !== 'none'
      )
    : [];

  const escalationAxes = ind.escalation_axes
    ? (Object.entries(ind.escalation_axes) as [string, number | undefined][]).filter(
        ([, v]) => typeof v === 'number'
      )
    : [];

  const related = (ind.correlates_with || []).map((relId) => ({
    relId,
    entry: indicatorMap[relId] as IndicatorEntry | undefined,
  }));

  return (
    <div className="actor-detail-view">
      <div
        className="adv-back"
        onClick={() => navigate(`/person/tactic/${tactic.id}`)}
      >
        ← {tactic.id} {tactic.name}
      </div>

      <div className="adv-category-row">
        <span className="adv-category-name">{catLabel}</span>
        <span className="adv-category-sep">›</span>
        <span className="adv-category-id">{ind.id}</span>
      </div>

      <div className="ind-crumb">
        <span>Phase {tactic.phase}</span>
        <span className="dp-crumb-sep">›</span>
        <span
          className="ind-crumb-link"
          onClick={() => navigate(`/person/tactic/${tactic.id}`)}
        >
          {tactic.name}
        </span>
        <span className="dp-crumb-sep">›</span>
        <span className="dp-crumb-active">{ind.id}</span>
      </div>

      <div className="adv-two-col">
        <div className="adv-two-col-left">
          <div className="adv-section">
            <div className="adv-section-label">Observable Behavior</div>
            <div className="adv-body">{ind.behavior}</div>
          </div>

          <div className="adv-section">
            <div className="adv-section-label">Classification</div>
            <div className="adv-attrs-list">
              <div className="adv-attr-row-new">
                <div className="adv-attr-key">Category</div>
                <div className="adv-attr-val">{catLabel}</div>
              </div>
              {ind.phase_relevance && ind.phase_relevance.length > 0 && (
                <div className="adv-attr-row-new">
                  <div className="adv-attr-key">Phase Relevance</div>
                  <div className="adv-attr-val">
                    {ind.phase_relevance
                      .map((p) => PHASE_RELEVANCE_LABELS[p] || p)
                      .join(', ')}
                  </div>
                </div>
              )}
              {ind.primary_objective_evidence_tier && (
                <div className="adv-attr-row-new">
                  <div className="adv-attr-key">Objective Evidence</div>
                  <div className="adv-attr-val">
                    {EVIDENCE_TIER_LABELS[ind.primary_objective_evidence_tier] ||
                      ind.primary_objective_evidence_tier}
                  </div>
                </div>
              )}
            </div>

            {ind.target_identity && ind.target_identity.length > 0 && (
              <>
                <div className="ind-subhead">Target Identity</div>
                <div className="dr-tag-row">
                  {ind.target_identity.map((ti) => (
                    <span key={ti} className="dr-tag identity">
                      {TARGET_IDENTITY_LABELS[ti] || ti}
                    </span>
                  ))}
                </div>
              </>
            )}

            {ind.detection_sources && ind.detection_sources.length > 0 && (
              <>
                <div className="ind-subhead">Detection Sources</div>
                <div className="dr-tag-row">
                  {ind.detection_sources.map((src) => (
                    <span key={src} className="dr-tag">
                      {DETECTION_SOURCE_LABELS[src] || src}
                    </span>
                  ))}
                </div>
              </>
            )}
          </div>

          {(ind.temporal_signature ||
            ind.severity_band ||
            typeof ind.escalation_weight === 'number' ||
            escalationAxes.length > 0) && (
            <div className="adv-section">
              <div className="adv-section-label">Escalation Profile</div>
              <div className="adv-attrs-list">
                {ind.temporal_signature && (
                  <div className="adv-attr-row-new">
                    <div className="adv-attr-key">Temporal Signature</div>
                    <div className="adv-attr-val">
                      {TEMPORAL_SIGNATURE_LABELS[ind.temporal_signature] ||
                        ind.temporal_signature}
                    </div>
                  </div>
                )}
                {ind.severity_band && (
                  <div className="adv-attr-row-new">
                    <div className="adv-attr-key">Severity Band</div>
                    <div className="adv-attr-val">
                      <span className={`ind-sev ${ind.severity_band}`}>
                        {SEVERITY_BAND_LABELS[ind.severity_band] || ind.severity_band}
                      </span>
                    </div>
                  </div>
                )}
                {typeof ind.escalation_weight === 'number' && (
                  <div className="adv-attr-row-new">
                    <div className="adv-attr-key">Escalation Weight</div>
                    <div className="adv-attr-val">{ind.escalation_weight.toFixed(2)}</div>
                  </div>
                )}
              </div>
              {escalationAxes.length > 0 && (
                <>
                  <div className="ind-subhead">Escalation Axes</div>
                  <div className="ind-axes-grid">
                    {escalationAxes.map(([k, v]) => (
                      <div key={k} className="ind-axis">
                        <div className="ind-axis-label">
                          {ESCALATION_AXIS_LABELS[k] || k}
                        </div>
                        <div className="ind-axis-bar">
                          <div
                            className="ind-axis-fill"
                            style={{ width: `${Math.min(100, (v as number) * 10)}%` }}
                          />
                        </div>
                        <div className="ind-axis-val">{(v as number).toFixed(1)}</div>
                      </div>
                    ))}
                  </div>
                </>
              )}
            </div>
          )}

          {informsRows.length > 0 && (
            <div className="adv-section">
              <div className="adv-section-label">Informs Threat Picture</div>
              <div className="adv-attrs-list">
                {informsRows.map(([k, v]) => (
                  <div key={k} className="adv-attr-row-new">
                    <div className="adv-attr-key">{INFORMS_AXIS_LABELS[k] || k}</div>
                    <div className="adv-attr-val">
                      <span className={`ind-strength ${v}`}>{v}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        <div className="adv-two-col-right">
          <div className="adv-section">
            <div className="adv-section-label">
              Related Indicators ({related.length})
            </div>
            {related.length > 0 ? (
              <div>
                {related.map(({ relId, entry: rel }) => (
                  <div
                    key={relId}
                    className="ind-related-link"
                    role="button"
                    tabIndex={0}
                    onClick={() => navigate(`/person/indicator/${relId}`)}
                    onKeyDown={(e) => {
                      if (e.key === 'Enter' || e.key === ' ') {
                        e.preventDefault();
                        navigate(`/person/indicator/${relId}`);
                      }
                    }}
                  >
                    <div className="ind-related-head">
                      <span className="adv-tactic-id">{relId}</span>
                      {rel && (
                        <span className="ind-related-tactic">{rel.tactic.name}</span>
                      )}
                    </div>
                    <div className="ind-related-beh">
                      {rel ? rel.indicator.behavior : 'Unresolved reference'}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div style={{ color: 'var(--text-dim)', fontSize: '13px' }}>
                No correlated indicators recorded.
              </div>
            )}
          </div>

          {ind.source_refs && ind.source_refs.length > 0 && (
            <div className="adv-section">
              <div className="adv-section-label">Sources</div>
              <div className="dr-tag-row">
                {ind.source_refs.map((ref) => (
                  <SourceRefLink key={ref} refKey={ref} navigate={navigate} />
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
