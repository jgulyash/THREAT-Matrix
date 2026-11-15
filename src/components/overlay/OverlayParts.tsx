import type { ScoringOverlay } from '../../types/overlay';
import { FRAMEWORK_VERSION } from '../../lib/data';

// Shown next to every score.
export function ScoreTag() {
  return <span className="type-level-tag score-tag">experimental, type-level, unvalidated</span>;
}

// The overlay's own notice text, shown wherever scores appear.
export function OverlayNotice({ overlay }: { overlay: ScoringOverlay }) {
  const mismatch =
    !!overlay.applies_to_framework_version && overlay.applies_to_framework_version !== FRAMEWORK_VERSION;
  return (
    <div className="overlay-notice" data-overlay-notice role="note">
      <div className="overlay-notice-head">
        Experimental scoring overlay
        {overlay.overlay_version ? ` ${overlay.overlay_version}` : ''} · non-normative · unvalidated
      </div>
      {overlay.notice && <div>{overlay.notice}</div>}
      {mismatch && (
        <div>
          This overlay was written for framework version {overlay.applies_to_framework_version}; the
          vocabulary shown is version {FRAMEWORK_VERSION}.
        </div>
      )}
    </div>
  );
}
