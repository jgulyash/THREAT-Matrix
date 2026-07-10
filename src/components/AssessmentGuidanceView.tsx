import type {
  AssessmentGuidance,
  AssessmentGuidanceSection,
} from '../types/framework';

const FACTORS: Array<{ key: keyof AssessmentGuidance; label: string }> = [
  { key: 'credibility', label: 'Credibility' },
  { key: 'capability', label: 'Capability' },
  { key: 'intent', label: 'Intent' },
  { key: 'opportunity', label: 'Opportunity' },
];

// Escalation priority is an ordinal label; map to the shared severity palette
// so it reads consistently with the rest of the framework's urgency signalling.
const PRIORITY_CLASS: Record<string, string> = {
  Urgent: 'critical',
  Immediate: 'high',
  Priority: 'medium',
  Routine: 'low',
};

function FactorBlock({ label, section }: { label: string; section?: AssessmentGuidanceSection }) {
  if (!section) return null;
  const highs = section.high_signal_anchors || [];
  const lows = section.low_signal_anchors || [];
  return (
    <div className="ag-factor">
      <div className="ag-factor-label">{label}</div>
      {section.criteria && <div className="ag-criteria">{section.criteria}</div>}
      {(highs.length > 0 || lows.length > 0) && (
        <details className="dr-details">
          <summary>
            Signal anchors ({highs.length} raise · {lows.length} lower)
          </summary>
          <div className="dr-details-body">
            {highs.length > 0 && (
              <ul className="ag-anchor-list ag-raise">
                {highs.map((a, i) => (
                  <li key={`h${i}`}>{a}</li>
                ))}
              </ul>
            )}
            {lows.length > 0 && (
              <ul className="ag-anchor-list ag-lower">
                {lows.map((a, i) => (
                  <li key={`l${i}`}>{a}</li>
                ))}
              </ul>
            )}
          </div>
        </details>
      )}
    </div>
  );
}

export function AssessmentGuidanceView({ guidance }: { guidance?: AssessmentGuidance }) {
  if (!guidance) return null;
  const {
    false_positive_context: fp,
    threshold_guidance: threshold,
    escalation_priority: priority,
  } = guidance;
  const hasFactor = FACTORS.some((f) => guidance[f.key]);
  if (!hasFactor && !fp && !threshold && !priority) return null;

  return (
    <div className="det-section">
      <div className="dr-section-header">
        <span>Assessment Guidance</span>
        {priority && (
          <span className={`ind-sev ${PRIORITY_CLASS[priority] || 'medium'}`}>{priority}</span>
        )}
      </div>

      {FACTORS.map((f) => (
        <FactorBlock key={f.key} label={f.label} section={guidance[f.key] as AssessmentGuidanceSection} />
      ))}

      {fp && (fp.criteria || (fp.contexts && fp.contexts.length > 0)) && (
        <div className="ag-factor ag-fp">
          <div className="ag-factor-label">Looks Like This, But Isn't</div>
          {fp.criteria && <div className="ag-criteria">{fp.criteria}</div>}
          {fp.contexts && fp.contexts.length > 0 && (
            <details className="dr-details">
              <summary>False-positive contexts ({fp.contexts.length})</summary>
              <div className="dr-details-body">
                <ul className="ag-anchor-list ag-fp-list">
                  {fp.contexts.map((c, i) => (
                    <li key={i}>{c}</li>
                  ))}
                </ul>
              </div>
            </details>
          )}
        </div>
      )}

      {threshold && (
        <div className="ag-factor">
          <div className="ag-factor-label">Threshold Guidance</div>
          <div className="ag-criteria">{threshold}</div>
        </div>
      )}
    </div>
  );
}
