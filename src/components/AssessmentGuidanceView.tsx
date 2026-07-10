import type { ReactNode } from 'react';
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

// First ~14 words of a block, so a collapsed row carries information scent.
function teaser(text?: string): string {
  if (!text) return '';
  const words = text.trim().split(/\s+/);
  const head = words.slice(0, 14).join(' ');
  return words.length > 14 ? head + '…' : head;
}

interface AccProps {
  label: string;
  teaserText?: string;
  children: ReactNode;
}

function Accordion({ label, teaserText, children }: AccProps) {
  return (
    <details className="ag-acc">
      <summary>
        <span className="ag-acc-label">{label}</span>
        {teaserText && <span className="ag-acc-teaser">{teaser(teaserText)}</span>}
      </summary>
      <div className="ag-acc-body">{children}</div>
    </details>
  );
}

function AnchorLists({ section }: { section: AssessmentGuidanceSection }) {
  const highs = section.high_signal_anchors || [];
  const lows = section.low_signal_anchors || [];
  return (
    <>
      {section.criteria && <div className="ag-criteria">{section.criteria}</div>}
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
    </>
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

      {FACTORS.map((f) => {
        const section = guidance[f.key] as AssessmentGuidanceSection | undefined;
        if (!section) return null;
        return (
          <Accordion key={f.key} label={f.label} teaserText={section.criteria}>
            <AnchorLists section={section} />
          </Accordion>
        );
      })}

      {fp && (fp.criteria || (fp.contexts && fp.contexts.length > 0)) && (
        <Accordion label="Looks Like This, But Isn't" teaserText={fp.criteria}>
          <div className="ag-fp">
            {fp.criteria && <div className="ag-criteria">{fp.criteria}</div>}
            {fp.contexts && fp.contexts.length > 0 && (
              <ul className="ag-anchor-list ag-fp-list">
                {fp.contexts.map((c, i) => (
                  <li key={i}>{c}</li>
                ))}
              </ul>
            )}
          </div>
        </Accordion>
      )}

      {threshold && (
        <Accordion label="Threshold Guidance" teaserText={threshold}>
          {threshold.split('\n\n').map((para, i) => (
            <p key={i} className="ag-para">
              {para}
            </p>
          ))}
        </Accordion>
      )}
    </div>
  );
}
