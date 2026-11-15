import {
  INDICATOR_CATEGORY_LABELS,
  DETECTION_SOURCE_LABELS,
  TARGET_IDENTITY_LABELS,
  FACILITY_TARGET_SCOPE_LABELS,
  WITHIN_SITE_FOCUS_LABELS,
  PROBE_FACTOR_LABELS,
  TEMPORAL_SIGNATURE_LABELS,
  INFORMS_AXIS_LABELS,
  PHASE_RELEVANCE_LABELS,
  MATRIX_LABELS,
  MODALITY_LABELS,
  MODALITY_DEFS,
  CROSSING_MECHANISM_LABELS,
  PRIORITY_ORDER,
  label,
} from '../lib/constants';
import { correlatedFrom, indicatorById, type IndicatorEntry } from '../lib/data';
import { LINKS } from '../lib/links';
import { seg } from '../lib/route';
import { Go } from '../lib/nav';
import { SourceRefLink } from './detection-response/SourceRefLink';
import { DraftTag } from './DraftTag';
import { LifecycleNote } from './Lifecycle';
import { IndicatorScores } from './overlay/IndicatorScores';

interface Props {
  indicatorId: string;
}

function IndicatorLinkCard({ relId, entry }: { relId: string; entry: IndicatorEntry | undefined }) {
  const body = (
    <>
      <div className="ind-related-head">
        <span className="adv-tactic-id">{relId}</span>
        {entry && <span className="ind-related-tactic">{entry.tactic.name}</span>}
      </div>
      <div className="ind-related-beh">
        {entry ? entry.indicator.behavior : 'Unresolved reference'}
      </div>
    </>
  );
  if (!entry) return <div className="ind-related-link unresolved">{body}</div>;
  return (
    <Go className="ind-related-link" to={`/${entry.tactic.matrix}/indicator/${seg(relId)}`}>
      {body}
    </Go>
  );
}

// The router has already confirmed that indicatorId exists.
export function IndicatorDetail({ indicatorId }: Props) {
  const entry = indicatorById.get(indicatorId);
  if (!entry) return null;

  const { indicator: ind, tactic } = entry;
  const tacticPath = `/${tactic.matrix}/tactic/${seg(tactic.id)}`;

  // Render only the populated parts of informs_axes.
  const informsRows = ind.informs_axes
    ? (Object.entries(ind.informs_axes) as [string, string | undefined][]).filter(
        ([, v]) => v && v !== 'none'
      )
    : [];

  const related = (ind.correlates_with || []).map((relId) => ({
    relId,
    entry: indicatorById.get(relId),
  }));

  // Reverse links: indicators whose correlates_with points here. Outbound links
  // already render under Related Indicators, so mutual pairs are excluded.
  const outbound = new Set(ind.correlates_with || []);
  const referencedBy = (correlatedFrom.get(ind.id) || []).filter(
    (e) => e.indicator.id !== ind.id && !outbound.has(e.indicator.id)
  );

  // The first protocol in the order the tactic view lists them.
  const firstProtocol = [...tactic.response_protocols].sort((a, b) => {
    const ai = PRIORITY_ORDER.indexOf(a.priority);
    const bi = PRIORITY_ORDER.indexOf(b.priority);
    return (ai === -1 ? 99 : ai) - (bi === -1 ? 99 : bi);
  })[0];

  return (
    <div className="actor-detail-view">
      <Go className="adv-back" to={tacticPath}>
        ← {tactic.id} {tactic.name}
      </Go>

      <div className="adv-category-row">
        <span className="adv-category-name" data-focus-target tabIndex={-1}>
          {ind.id}
        </span>
      </div>

      <div className="ind-crumb">
        <span>
          {MATRIX_LABELS[tactic.matrix]}
          <DraftTag matrix={tactic.matrix} />
        </span>
        <span className="dp-crumb-sep">›</span>
        <span>Phase {tactic.phase}</span>
        <span className="dp-crumb-sep">›</span>
        <Go className="ind-crumb-link" to={tacticPath}>
          {tactic.name}
        </Go>
        <span className="dp-crumb-sep">›</span>
        <span className="dp-crumb-active">{ind.id}</span>
      </div>

      <LifecycleNote item={ind} />

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
                <div className="adv-attr-val">{label(INDICATOR_CATEGORY_LABELS, ind.category)}</div>
              </div>
              <div className="adv-attr-row-new">
                <div className="adv-attr-key">Behavioral Mode</div>
                <div className="adv-attr-val">
                  <span
                    className={`dr-tag modality mod-${ind.modality}`}
                    title={MODALITY_DEFS[ind.modality]}
                  >
                    {label(MODALITY_LABELS, ind.modality)}
                  </span>
                  {ind.crossing_mechanism && (
                    <span className="dr-tag modality-mech">
                      {label(CROSSING_MECHANISM_LABELS, ind.crossing_mechanism)}
                    </span>
                  )}
                  {ind.human_social && ind.modality !== 'human_social' && (
                    <span
                      className="dr-tag modality-hs"
                      title="Human tradecraft or warning behavior co-occurs with this behavior's primary mode."
                    >
                      Human &amp; Social
                    </span>
                  )}
                </div>
              </div>
              {ind.phase_relevance && ind.phase_relevance.length > 0 && (
                <div className="adv-attr-row-new">
                  <div className="adv-attr-key">Phase Relevance</div>
                  <div className="adv-attr-val">
                    {ind.phase_relevance.map((p) => label(PHASE_RELEVANCE_LABELS, p)).join(', ')}
                  </div>
                </div>
              )}
              {ind.temporal_signature && (
                <div className="adv-attr-row-new">
                  <div className="adv-attr-key">Temporal Signature</div>
                  <div className="adv-attr-val">
                    {label(TEMPORAL_SIGNATURE_LABELS, ind.temporal_signature)}
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
                      {label(TARGET_IDENTITY_LABELS, ti)}
                    </span>
                  ))}
                </div>
              </>
            )}

            {ind.facility_target_scope && ind.facility_target_scope.length > 0 && (
              <>
                <div className="ind-subhead">Target Scope</div>
                <div className="dr-tag-row">
                  {ind.facility_target_scope.map((ts) => (
                    <span key={ts} className="dr-tag identity">
                      {label(FACILITY_TARGET_SCOPE_LABELS, ts)}
                    </span>
                  ))}
                </div>
              </>
            )}

            {ind.within_site_focus && ind.within_site_focus.length > 0 && (
              <>
                <div className="ind-subhead">Within-Site Focus</div>
                <div className="dr-tag-row">
                  {ind.within_site_focus.map((wf) => (
                    <span key={wf} className="dr-tag identity">
                      {label(WITHIN_SITE_FOCUS_LABELS, wf)}
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
                      {label(DETECTION_SOURCE_LABELS, src)}
                    </span>
                  ))}
                </div>
              </>
            )}
          </div>

          {ind.conditioning_guidance && (
            <div className="adv-section">
              <div className="adv-section-label">Conditioning Guidance</div>
              <div className="cond-guidance">
                <div className="cond-guidance-scope">
                  Assessment tasking only: what to establish about the case at hand. Immediate
                  response actions live in this tactic's{' '}
                  <Go
                    className="cond-guidance-rp-link"
                    to={firstProtocol ? `${tacticPath}/${seg(firstProtocol.id)}` : tacticPath}
                  >
                    Response Protocols
                  </Go>
                  . Observations are recorded in the{' '}
                  <a
                    className="cond-guidance-rp-link"
                    href={LINKS.caseWorksheet}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    case record worksheet
                  </a>
                  , which carries no score.
                </div>
                <p className="cond-guidance-text">{ind.conditioning_guidance.guidance}</p>
                <div className="dr-tag-row">
                  {(ind.conditioning_guidance.probe_factors || []).map((f) => (
                    <span key={f} className="dr-tag probe" title="Instance factor to probe at assessment time">
                      {label(PROBE_FACTOR_LABELS, f)}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          )}

          {informsRows.length > 0 && (
            <div className="adv-section">
              <div className="adv-section-label">Informs Threat Picture</div>
              <div className="adv-attrs-list">
                {informsRows.map(([k, v]) => (
                  <div key={k} className="adv-attr-row-new">
                    <div className="adv-attr-key">{label(INFORMS_AXIS_LABELS, k)}</div>
                    <div className="adv-attr-val">
                      <span className={`ind-strength ${v}`}>{v}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          <IndicatorScores indicatorId={ind.id} />
        </div>

        <div className="adv-two-col-right">
          <div className="adv-section">
            <div className="adv-section-label">
              Related Indicators ({related.length})
            </div>
            {related.length > 0 ? (
              <div>
                {related.map(({ relId, entry: rel }) => (
                  <IndicatorLinkCard key={relId} relId={relId} entry={rel} />
                ))}
              </div>
            ) : (
              <div className="adv-empty">No correlated indicators recorded.</div>
            )}
          </div>

          {referencedBy.length > 0 && (
            <div className="adv-section">
              <div className="adv-section-label">
                Referenced By ({referencedBy.length})
              </div>
              <div>
                {referencedBy.map((rel) => (
                  <IndicatorLinkCard key={rel.indicator.id} relId={rel.indicator.id} entry={rel} />
                ))}
              </div>
            </div>
          )}

          {ind.source_refs && ind.source_refs.length > 0 && (
            <div className="adv-section">
              <div className="adv-section-label">Sources</div>
              <div className="dr-tag-row">
                {ind.source_refs.map((ref) => (
                  <SourceRefLink key={ref} refKey={ref} />
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
