import type { ResponseProtocol } from '../../types/framework';
import { PRIORITY_ORDER, STAKEHOLDER_LABELS, humanize, label } from '../../lib/constants';
import { LifecycleNote } from '../Lifecycle';
import { SourceRefLink } from './SourceRefLink';

interface Props {
  protocols: ResponseProtocol[];
  focusId?: string | null;
}

export function ResponseProtocolSection({ protocols, focusId }: Props) {
  if (!protocols?.length) return null;

  const sorted = [...protocols].sort((a, b) => {
    const ai = PRIORITY_ORDER.indexOf(a.priority);
    const bi = PRIORITY_ORDER.indexOf(b.priority);
    return (ai === -1 ? 99 : ai) - (bi === -1 ? 99 : bi);
  });

  return (
    <div className="det-section" id="response-protocols">
      <h2 className="dr-section-header">
        <span>Response Protocols</span>
        <span className="dr-section-count">{protocols.length} protocols</span>
      </h2>
      {sorted.map((rp) => (
        <div
          key={rp.id}
          className={`dr-item${focusId === rp.id ? ' cited' : ''}`}
          data-item-id={rp.id}
          tabIndex={-1}
        >
          <div className="dr-item-id">{rp.id}</div>
          {rp.priority && (
            <span className={`dr-priority-badge ${rp.priority}`}>
              Response timeframe: {humanize(rp.priority)}
            </span>
          )}
          <LifecycleNote item={rp} />

          <h3 className="dr-rp-label">Trigger</h3>
          <div className="dr-rp-trigger">{rp.trigger}</div>

          <h3 className="dr-rp-label">Action</h3>
          <div className="dr-rp-action">{rp.action}</div>

          {rp.stakeholders && rp.stakeholders.length > 0 && (
            <>
              <h3 className="dr-rp-label">Stakeholders</h3>
              <div className="dr-tag-row">
                {rp.stakeholders.map((s) => (
                  <span key={s} className="dr-tag stakeholder">
                    {label(STAKEHOLDER_LABELS, s)}
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

          {rp.source_refs && rp.source_refs.length > 0 && (
            <details className="dr-details">
              <summary>Sources</summary>
              <div className="dr-details-body">
                <div className="dr-tag-row">
                  {rp.source_refs.map((ref) => (
                    <SourceRefLink key={ref} refKey={ref} />
                  ))}
                </div>
              </div>
            </details>
          )}
        </div>
      ))}
    </div>
  );
}
