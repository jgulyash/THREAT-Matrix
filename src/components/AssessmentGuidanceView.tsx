import type { ReactNode } from 'react';
import type {
  AssessmentGuidance,
  AssessmentGuidanceSection,
} from '../types/framework';

type FactorKey = 'credibility' | 'capability' | 'intent' | 'opportunity';

const FACTORS: Array<{ key: FactorKey; label: string }> = [
  { key: 'credibility', label: 'Credibility' },
  { key: 'capability', label: 'Capability' },
  { key: 'intent', label: 'Intent' },
  { key: 'opportunity', label: 'Opportunity' },
];

// Fixed per-block descriptors, curated to fit one line at any panel width, so a
// collapsed row reads as an intentional label rather than a truncated sentence.
const TEASERS: Record<string, string> = {
  credibility: 'How much to trust the finding',
  capability: "What the actor's skill signals",
  intent: 'Whether intent to act is forming',
  opportunity: 'Whether the actor can reach the target',
  false_positive: 'Benign activities that mimic it',
  threshold: 'When findings warrant further action',
};

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
        {teaserText && <span className="ag-acc-teaser">{teaserText}</span>}
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
  const { false_positive_context: fp, threshold_guidance: threshold } = guidance;
  const hasFactor = FACTORS.some((f) => guidance[f.key]);
  if (!hasFactor && !fp && !threshold) return null;

  return (
    <div className="det-section">
      <h2 className="dr-section-header">
        <span>Assessment Guidance</span>
      </h2>
      <div className="ag-subtitle">How to weigh observed findings of this tactic.</div>

      {FACTORS.map((f) => {
        const section = guidance[f.key];
        if (!section) return null;
        return (
          <Accordion key={f.key} label={f.label} teaserText={TEASERS[f.key]}>
            <AnchorLists section={section} />
          </Accordion>
        );
      })}

      {fp && (fp.criteria || (fp.contexts && fp.contexts.length > 0)) && (
        <Accordion label="Looks Like This, But Isn't" teaserText={TEASERS.false_positive}>
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
        <Accordion label="Threshold Guidance" teaserText={TEASERS.threshold}>
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
