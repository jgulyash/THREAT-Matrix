import { useOverlay } from '../../lib/overlay';

// The one control that turns scores on. Off by default.
export function OverlayToggle() {
  const { status, setEnabled } = useOverlay();
  const on = status === 'ready' || status === 'loading';
  return (
    <span className="overlay-toggle">
      <label>
        <input
          type="checkbox"
          data-overlay-toggle
          checked={on}
          onChange={(e) => setEnabled(e.target.checked)}
        />
        Show experimental scoring overlay
      </label>
      <span className="overlay-status">Your choice is remembered in this browser.</span>
      <span role="status" aria-live="polite">
        {status === 'loading' && <span className="overlay-status">Loading overlay…</span>}
        {status === 'error' && (
          <span className="overlay-status" data-overlay-error>
            The scoring overlay could not be loaded. The viewer remains score-free.
          </span>
        )}
      </span>
    </span>
  );
}
