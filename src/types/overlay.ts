// Types for docs/data/scoring-overlay.json: the experimental, non-normative,
// type-level scoring overlay. Loaded only when the user opts in.

export type TypeBand = 'low' | 'medium' | 'high' | 'critical';
export type AxisName =
  | 'impact_potential'
  | 'blast_radius_potential'
  | 'recoverability_inverse'
  | 'detectability';
export type AxisConfidenceLevel = 'established' | 'inferred' | 'thin';

export interface IndicatorScore {
  axes?: Partial<Record<AxisName, number>>;
  type_weight?: number;
  type_band?: TypeBand;
  type_band_floor?: TypeBand;
  axis_confidence?: Partial<Record<AxisName, AxisConfidenceLevel>>;
}

export interface ScoringOverlay {
  name?: string;
  overlay_version?: string;
  applies_to_framework_version?: string;
  status?: string;
  normative?: boolean;
  validation_status?: string;
  scope?: string;
  notice?: string;
  rubric?: { type_band_thresholds?: Partial<Record<TypeBand, number>> };
  tactic_priorities?: Record<string, string>;
  indicator_scores?: Record<string, IndicatorScore>;
}
