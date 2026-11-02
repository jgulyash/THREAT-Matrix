export type Priority = 'urgent' | 'immediate' | 'priority' | 'routine' | 'ongoing';
export type RiskLevel = 'low' | 'medium' | 'high';
export type TimeToImplement = 'immediate' | 'days' | 'weeks' | 'months' | 'weeks_to_months';

// V1.2 escalation scoring
export type SeverityBand = 'low' | 'medium' | 'high' | 'critical';
export type InformsAxisStrength = 'strong' | 'moderate' | 'weak' | 'none';

// V1.2.2 People matrix scope sub-dimension
export type TargetIdentity =
  | 'named_individual'
  | 'role_or_identity_category'
  | 'affinity_group'
  | 'indiscriminate';

export type PrimaryObjectiveEvidenceTier =
  | 'stated'
  | 'strongly_inferred'
  | 'weakly_inferred'
  | 'unknown';

// V1.3 Facility matrix target sub-dimensions (revealed reading)
export type FacilityTargetScope =
  | 'specific_site'
  | 'site_class'
  | 'symbolic_category'
  | 'indiscriminate';

export type WithinSiteFocus =
  | 'structure'
  | 'occupants'
  | 'systems'
  | 'whole_site';

// Schema 3.0.0 tactic evidence-basis taxonomy (authoring mode). Renamed from
// the V1.1 values: operational_primary -> practice_led, hybrid ->
// practice_and_literature, literature_primary -> literature_led,
// literature_only unchanged. See docs/migration/2.1-to-3.0.md.
export type EvidenceBasis =
  | 'practice_led'
  | 'practice_and_literature'
  | 'literature_led'
  | 'literature_only';

// Schema 3.0.0 lifecycle contract (docs/DEPRECATION.md). Absent means active.
export type LifecycleState = 'active' | 'deprecated' | 'superseded' | 'reserved';

export interface LifecycleFields {
  lifecycle_state?: LifecycleState;
  deprecated_in?: string;
  superseded_by?: string;
  deprecation_reason?: string;
  reserved_reason?: string;
}

// Schema 3.0.0 actor-profile categorical enums.
export type ActorCategory =
  | 'lone_actor'
  | 'insider'
  | 'criminal'
  | 'corporate_espionage'
  | 'ideological'
  | 'nation_state'
  | 'customer_aggressor';
export type ActorCategoryLabel =
  | 'Lone Actor'
  | 'Insider'
  | 'Criminal'
  | 'Corporate Espionage'
  | 'Ideological'
  | 'Nation-State'
  | 'Customer/Client Aggressor';
export type ActorAwareness = 'witting' | 'unwitting' | 'negligent';
export type ActorDirection =
  | 'self_directed'
  | 'criminal_directed'
  | 'ideological_directed'
  | 'state_directed';
export type ActorAccessRelationship = 'external' | 'insider' | 'authorized';
export type PhaseCompressionRisk = 'low' | 'medium' | 'high' | 'very_high' | 'n/a';
export type ActorLevel = 'individual' | 'group' | 'organization';

export interface V2TacticAssociation {
  tactic_id: string;
  relevance: 'high' | 'medium' | 'low';
}

// V1.2 tactic-level assessment guidance escalation priority (Title Case;
// distinct from the lowercase Priority used on response_protocol)
export type AssessmentEscalationPriority = 'Urgent' | 'Immediate' | 'Priority' | 'Routine';

export interface EscalationAxes {
  impact_potential?: number;
  blast_radius_potential?: number;
  recoverability_inverse?: number;
  detectability?: number;
}

export interface InformsAxes {
  actor_capability?: InformsAxisStrength;
  actor_intent?: InformsAxisStrength;
  actor_opportunity?: InformsAxisStrength;
  threat_timing?: InformsAxisStrength;
  threat_target?: InformsAxisStrength;
  threat_method?: InformsAxisStrength;
}

export interface AssessmentGuidanceSection {
  criteria?: string;
  high_signal_anchors?: string[];
  low_signal_anchors?: string[];
}

export interface AssessmentGuidanceFalsePositive {
  criteria?: string;
  contexts?: string[];
}

export interface AssessmentGuidance {
  credibility?: AssessmentGuidanceSection;
  capability?: AssessmentGuidanceSection;
  intent?: AssessmentGuidanceSection;
  opportunity?: AssessmentGuidanceSection;
  false_positive_context?: AssessmentGuidanceFalsePositive;
  threshold_guidance?: string;
  escalation_priority?: AssessmentEscalationPriority;
}

export type Modality = 'physical' | 'cyber' | 'cyber_physical' | 'human_social';
export type CrossingMechanism = 'digital' | 'electromagnetic' | 'physical_implant';
export type AxisConfidenceLevel = 'established' | 'inferred' | 'thin';
export type AxisConfidence = Partial<Record<keyof EscalationAxes, AxisConfidenceLevel>>;

// V1.6 conditioning_guidance — per-indicator investigative tasking (type-level).
export type ProbeFactor =
  | 'target_focus'
  | 'pathway_stage'
  | 'means_in_hand'
  | 'tempo_trajectory'
  | 'proximity_access'
  | 'source_credibility';

export interface ConditioningGuidance {
  probe_factors: ProbeFactor[];
  guidance: string;
}

export interface Indicator extends LifecycleFields {
  id: string;
  behavior: string;
  category: string;
  detection_sources: string[];
  phase_relevance?: string[];
  source_refs: string[];
  // V1.6 modality facets
  modality: Modality;
  human_social: boolean;
  crossing_mechanism?: CrossingMechanism;
  axis_confidence?: AxisConfidence;
  conditioning_guidance?: ConditioningGuidance;
  // V1.1 Detection Mesh
  correlates_with?: string[];
  // V1.2 escalation scoring
  temporal_signature?: string;
  escalation_axes?: EscalationAxes;
  escalation_weight?: number;
  severity_band?: SeverityBand;
  informs_axes?: InformsAxes;
  // V1.2.2 People matrix scope sub-dimension
  target_identity?: TargetIdentity[];
  primary_objective_evidence_tier?: PrimaryObjectiveEvidenceTier;
  // V1.3 Facility matrix target sub-dimensions (revealed reading)
  facility_target_scope?: FacilityTargetScope[];
  within_site_focus?: WithinSiteFocus[];
}

export interface Countermeasure extends LifecycleFields {
  id: string;
  measure: string;
  category: string;
  domain?: string;
  cost: RiskLevel;
  complexity: RiskLevel;
  time_to_implement: TimeToImplement;
  phase_relevance?: string[];
  limitations: string;
  source_refs: string[];
  // V1.1 Detection Mesh; V1.8 relation split: CM->CM redundancy only
  compensates_for?: string[];
  // V1.8 coverage relation: CM->indicator mitigation, typed per edge
  mitigates?: MitigatesEdge[];
}

export interface MitigatesEdge {
  indicator: string;
  function: 'prevent' | 'detect' | 'deny' | 'unreviewed';
}

export interface ResponseProtocol extends LifecycleFields {
  id: string;
  trigger: string;
  action: string;
  stakeholders: string[];
  priority: Priority;
  escalation_trigger: string;
  legal_notes: string;
  source_refs: string[];
  // V1.1 Detection Mesh
  coordinates_with?: string[];
}

export interface ActorAssociation {
  actor_id: string;
  relevance: 'high' | 'medium' | 'low';
  employment_status?: string;
}

export interface Tactic extends LifecycleFields {
  id: string;
  name: string;
  tactic_families?: string[];
  matrix: string;
  phase: 1 | 2 | 3 | 4;
  phase_name: string;
  notes: string;
  field_notes?: string;
  observed_contexts?: string[];
  evidence_basis?: EvidenceBasis;
  indicators: Indicator[];
  countermeasures: Countermeasure[];
  related_tactics?: string[];
  actor_associations?: ActorAssociation[];
  source_refs?: string[];
  response_protocols: ResponseProtocol[];
  phase_4_track?: 'evasion' | 'attribution';
  // V1.2 assessment guidance
  assessment_guidance?: AssessmentGuidance;
  // V1.2.2 People matrix scope sub-dimension
  target_identity_scope?: TargetIdentity[];
}

export interface ActorProfile extends LifecycleFields {
  id: string;
  name: string;
  category: ActorCategory;
  category_label: ActorCategoryLabel;
  awareness: ActorAwareness;
  direction: ActorDirection;
  access_relationship: ActorAccessRelationship;
  phase_compression_risk: PhaseCompressionRisk;
  actor_level?: ActorLevel;
  attack_vectors?: string[];
  primary_matrices?: string[];
  description?: string;
  behavioral_markers?: string[];
  ai_enabled_risks?: string[];
  // Schema 3.0.0: optional, typed items (was a required untyped empty array)
  v2_tactic_associations?: V2TacticAssociation[];
}

export interface BibliographyEntry {
  type: string;
  title: string;
  author: string;
  date: string;
  url: string | null;
  doi?: string | null;
  relevance_summary: string;
  // V1.3 matrix/topic tagging
  matrices?: string[];
  topics?: string[];
}

export interface MatrixContainer {
  tactics: Tactic[];
  // V1.2.2 per-matrix scope sentence
  scope?: string;
}

export interface Matrices {
  person: MatrixContainer;
  facility?: MatrixContainer;
  organization?: MatrixContainer;
  infrastructure?: MatrixContainer;
  // V1.2.2 framework-vs-operational boundary principle
  boundary_rule?: string;
}

export interface FrameworkData {
  name: string;
  full_name?: string;
  version: string;
  schema_version?: string;
  license?: string;
  matrices: Matrices;
  actor_profiles: ActorProfile[];
  bibliography: Record<string, BibliographyEntry>;
  [k: string]: unknown;
}
