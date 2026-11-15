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
      <div className="dr-section-header">
        <span>Response Protocols</span>
        <span className="dr-section-count">{protocols.length} protocols</span>
      </div>
      {sorted.map((rp) => (
        <div
          key={rp.id}
          className={`dr-item${focusId === rp.id ? ' cited' : ''}`}
          data-item-id={rp.id}
          tabIndex={-1}
        >
          <div className="dr-item-id">{rp.id}</div>
          {rp.priority && (
            <span className={`dr-priority-badge ${rp.priority}`}>{humanize(rp.priority)}</span>
          )}
          <LifecycleNote item={rp} />

          <div className="dr-rp-label">Trigger</div>
          <div className="dr-rp-trigger">{rp.trigger}</div>

          <div className="dr-rp-label">Action</div>
          <div className="dr-rp-action">{rp.action}</div>

          {rp.stakeholders && rp.stakeholders.length > 0 && (
            <>
              <div className="dr-rp-label">Stakeholders</div>
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
