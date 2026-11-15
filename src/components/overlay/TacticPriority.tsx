import { tacticPriority, useOverlay } from '../../lib/overlay';
import { LINKS } from '../../lib/links';
import { OverlayNotice, ScoreTag } from './OverlayParts';

const PRIORITY_CLASS: Record<string, string> = {
  Urgent: 'critical',
  Immediate: 'high',
  Priority: 'medium',
  Routine: 'low',
};

// Tactic-level priority from the overlay, joined by tactic ID. Rendered only
// when the user has turned the overlay on and it loaded.
export function TacticPriority({ tacticId }: { tacticId: string }) {
  const { status, overlay } = useOverlay();
  if (status !== 'ready' || !overlay) return null;
  const priority = tacticPriority(overlay, tacticId);
  const cls = priority && Object.prototype.hasOwnProperty.call(PRIORITY_CLASS, priority)
    ? PRIORITY_CLASS[priority]
    : 'medium';
  return (
    <div className="det-section" data-overlay-section>
      <h2 className="dr-section-header">
        <span>Experimental scoring overlay</span>
      </h2>
      <OverlayNotice overlay={overlay} />
      {priority ? (
        <div className="overlay-row">
          <span className="overlay-row-key">Tactic priority</span>
          <span className={`ind-sev ${cls}`}>{priority}</span>
          <ScoreTag />
        </div>
      ) : (
        <div className="overlay-empty">The overlay has no priority for {tacticId}.</div>
      )}
      <div className="overlay-foot">
        Indicator scores appear on each indicator page. See the{' '}
        <a href={LINKS.experimentalScoring} target="_blank" rel="noopener noreferrer">
          experimental scoring examples
        </a>
        .
      </div>
    </div>
  );
}
