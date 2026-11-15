import type { AxisName, TypeBand } from '../../types/overlay';
import { indicatorScore, useOverlay } from '../../lib/overlay';
import { label } from '../../lib/constants';
import { LINKS } from '../../lib/links';
import { OverlayNotice, ScoreTag } from './OverlayParts';

const BAND_LABELS: Record<string, string> = {
  low: 'Low',
  medium: 'Medium',
  high: 'High',
  critical: 'Critical',
};
const BAND_ORDER: TypeBand[] = ['medium', 'high', 'critical'];

const AXIS_LABELS: Record<string, string> = {
  impact_potential: 'Impact Potential',
  blast_radius_potential: 'Blast Radius',
  recoverability_inverse: 'Recoverability (inv.)',
  detectability: 'Detectability',
};

function Band({ band }: { band: string }) {
  const cls = Object.prototype.hasOwnProperty.call(BAND_LABELS, band) ? band : 'medium';
  return <span className={`ind-sev ${cls}`}>{label(BAND_LABELS, band)}</span>;
}

// Rendered only when the user has turned the overlay on and it loaded.
export function IndicatorScores({ indicatorId }: { indicatorId: string }) {
  const { status, overlay } = useOverlay();
  if (status !== 'ready' || !overlay) return null;
  const score = indicatorScore(overlay, indicatorId);
  const axes = score?.axes
    ? (Object.entries(score.axes) as [AxisName, number | undefined][]).filter(
        (e): e is [AxisName, number] => typeof e[1] === 'number'
      )
    : [];
  const thresholds = overlay.rubric?.type_band_thresholds;
  const cutoffs = thresholds
    ? BAND_ORDER.filter((b) => typeof thresholds[b] === 'number').map(
        (b) => `${BAND_LABELS[b].toLowerCase()} at ${(thresholds[b] as number).toFixed(1)}`
      )
    : [];

  return (
    <div className="adv-section" data-overlay-section>
      <h2 className="adv-section-label">Experimental scoring overlay</h2>
      <OverlayNotice overlay={overlay} />
      {!score ? (
        <div className="overlay-empty">The overlay has no entry for {indicatorId}.</div>
      ) : (
        <>
          <div className="adv-attrs-list">
            {score.type_band && (
              <div className="adv-attr-row-new">
                <div className="adv-attr-key">Type band</div>
                <div className="adv-attr-val">
                  <Band band={score.type_band} />
                  <ScoreTag />
                </div>
              </div>
            )}
            {typeof score.type_weight === 'number' && (
              <div className="adv-attr-row-new">
                <div className="adv-attr-key">Type weight</div>
                <div className="adv-attr-val">
                  {score.type_weight.toFixed(2)}
                  <ScoreTag />
                </div>
              </div>
            )}
            {score.type_band_floor && (
              <div className="adv-attr-row-new">
                <div className="adv-attr-key">Type band floor</div>
                <div className="adv-attr-val">
                  <Band band={score.type_band_floor} />
                  <ScoreTag />
                </div>
              </div>
            )}
          </div>
          {axes.length > 0 && (
            <>
              <h3 className="ind-subhead">
                Axes (0 to 10)
                <ScoreTag />
              </h3>
              <div className="ind-axes-grid">
                {axes.map(([k, v]) => {
                  const conf = score.axis_confidence?.[k];
                  return (
                    <div key={k} className="ind-axis">
                      <div className="ind-axis-label">
                        {label(AXIS_LABELS, k)}
                        {conf && <span className="ind-axis-thin"> ◦ {conf}</span>}
                      </div>
                      <div className="ind-axis-bar">
                        <div
                          className="ind-axis-fill"
                          style={{ width: `${Math.max(0, Math.min(100, v * 10))}%` }}
                        />
                      </div>
                      <div className="ind-axis-val">{v.toFixed(1)}</div>
                    </div>
                  );
                })}
              </div>
            </>
          )}
          <div className="overlay-foot">
            {cutoffs.length > 0 && <>Bands are cut on the type weight: {cutoffs.join(', ')}. </>}
            These values describe a class of behavior, never a person or a case. See the{' '}
            <a href={LINKS.experimentalScoring} target="_blank" rel="noopener noreferrer">
              experimental scoring examples
            </a>
            .
          </div>
        </>
      )}
    </div>
  );
}
