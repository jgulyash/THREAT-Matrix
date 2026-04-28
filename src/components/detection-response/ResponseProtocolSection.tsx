import type { ResponseProtocol } from '../../types/framework';
import { PRIORITY_ORDER, STAKEHOLDER_LABELS } from '../../lib/constants';
import { SourceRefLink } from './SourceRefLink';

interface Props {
  protocols: ResponseProtocol[];
  navigate: (path: string) => void;
}

export function ResponseProtocolSection({ protocols, navigate }: Props) {
  if (!protocols?.length) return null;

  const sorted = [...protocols].sort((a, b) => {
    const ai = PRIORITY_ORDER.indexOf(a.priority);
    const bi = PRIORITY_ORDER.indexOf(b.priority);
    return (ai === -1 ? 99 : ai) - (bi === -1 ? 99 : bi);
  });

  return (
    <div className="det-section">
      <div className="dr-section-header">
        <span>Response Protocols</span>
        <span className="dr-section-count">{protocols.length} protocols</span>
      </div>
      {sorted.map((rp) => (
        <div key={rp.id} className="dr-item">
          <div className="dr-item-id">{rp.id}</div>
          <span className={`dr-priority-badge ${rp.priority}`}>{rp.priority}</span>

          <div className="dr-rp-label">Trigger</div>
          <div className="dr-rp-trigger">{rp.trigger}</div>

          <div className="dr-rp-label">Action</div>
          <div className="dr-rp-action">{rp.action}</div>

          {rp.stakeholders?.length > 0 && (
            <>
              <div className="dr-rp-label">Stakeholders</div>
              <div className="dr-tag-row">
                {rp.stakeholders.map((s) => (
                  <span key={s} className="dr-tag stakeholder">
                    {STAKEHOLDER_LABELS[s] || s.replace(/_/g, ' ')}
                  </span>
                ))}
              </div>
            </>
          )}

          {rp.escalation_trigger && (
            <details className="dr-details">
              <summary>Escalation Trigger</summary>
              <div className="dr-details-body">{rp.escalation_trigger}</div>
            </details>
          )}

          {rp.legal_notes && (
            <details className="dr-details">
              <summary>Legal / Compliance Notes</summary>
              <div className="dr-details-body">{rp.legal_notes}</div>
            </details>
          )}

          {rp.source_refs?.length > 0 && (
            <div className="dr-tag-row" style={{ marginTop: '8px' }}>
              {rp.source_refs.map((ref) => (
                <SourceRefLink key={ref} refKey={ref} navigate={navigate} />
              ))}
            </div>
          )}
        </div>
      ))}
    </div>
  );
}
