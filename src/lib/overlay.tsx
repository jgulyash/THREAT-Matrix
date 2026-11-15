import { createContext, useCallback, useContext, useEffect, useMemo, useState, type ReactNode } from 'react';
import type { IndicatorScore, ScoringOverlay } from '../types/overlay';
import { readPref, writePref } from './storage';

// The experimental scoring overlay is opt-in. It is off on every load unless
// the user turned it on in this browser, and its data is fetched as a
// separate chunk only then, so the default bundle carries no scores.
const PREF_KEY = 'threat-matrix-scoring-overlay';

export type OverlayStatus = 'off' | 'loading' | 'ready' | 'error';

interface OverlayState {
  status: OverlayStatus;
  overlay: ScoringOverlay | null;
  setEnabled: (on: boolean) => void;
}

const OverlayContext = createContext<OverlayState>({
  status: 'off',
  overlay: null,
  setEnabled: () => {},
});

const isRecord = (v: unknown): v is Record<string, unknown> =>
  !!v && typeof v === 'object' && !Array.isArray(v);

export function OverlayProvider({ children }: { children: ReactNode }) {
  const [status, setStatus] = useState<OverlayStatus>('off');
  const [overlay, setOverlay] = useState<ScoringOverlay | null>(null);

  const load = useCallback(() => {
    setStatus('loading');
    import('../../docs/data/scoring-overlay.json')
      .then((mod) => {
        const data = mod.default as unknown;
        if (!isRecord(data) || !isRecord(data.indicator_scores)) throw new Error('overlay shape');
        setOverlay(data as ScoringOverlay);
        setStatus('ready');
      })
      .catch(() => {
        // Stay score-free and do not retry silently on the next load.
        setOverlay(null);
        setStatus('error');
        writePref(PREF_KEY, null);
      });
  }, []);

  useEffect(() => {
    if (readPref(PREF_KEY) === '1') load();
  }, [load]);

  const setEnabled = useCallback(
    (on: boolean) => {
      if (on) {
        writePref(PREF_KEY, '1');
        load();
      } else {
        writePref(PREF_KEY, null);
        setStatus('off');
      }
    },
    [load]
  );

  const value = useMemo(() => ({ status, overlay, setEnabled }), [status, overlay, setEnabled]);
  return <OverlayContext.Provider value={value}>{children}</OverlayContext.Provider>;
}

export const useOverlay = (): OverlayState => useContext(OverlayContext);

const own = <T,>(rec: Record<string, T> | undefined, key: string): T | undefined =>
  rec && Object.prototype.hasOwnProperty.call(rec, key) ? rec[key] : undefined;

// Scores join by indicator ID; tactic priority joins by tactic ID.
export const indicatorScore = (o: ScoringOverlay | null, id: string): IndicatorScore | undefined =>
  o ? own(o.indicator_scores, id) : undefined;

export const tacticPriority = (o: ScoringOverlay | null, id: string): string | undefined => {
  const v = o ? own(o.tactic_priorities, id) : undefined;
  return typeof v === 'string' ? v : undefined;
};
