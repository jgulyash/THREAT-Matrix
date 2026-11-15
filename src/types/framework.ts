// Types for docs/data/framework.json (content 2.0.0, schema 3.0.0): the
// vocabulary and evidence index. No score, band, weight, or priority field
// exists here; those live only in the opt-in overlay (see ./overlay.ts).

export type Priority = 'urgent' | 'immediate' | 'priority' | 'routine' | 'ongoing';
export type RiskLevel = 'low' | 'medium' | 'high';
export type TimeToImplement = 'immediate' | 'days' | 'weeks' | 'months' | 'weeks_to_months';

export type InformsAxisStrength = 'strong' | 'moderate' | 'weak' | 'none';

// People matrix scope sub-dimension
export type TargetIdentity =
  | 'named_individual'
  | 'role_or_identity_category'
  | 'affinity_group'
  | 'indiscriminate';

// Facility matrix target sub-dimensions
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

// Tactic evidence-basis taxonomy (authoring mode).
export type EvidenceBasis =
  | 'practice_led'
  | 'practice_and_literature'
  | 'literature_led'
  | 'literature_only';

// Lifecycle contract (docs/DEPRECATION.md). Absent means active. Only actor
// profiles may be reserved; a reserved profile carries id, lifecycle_state,
// and reserved_reason and nothing else (see ReservedActorProfile).
export interface LifecycleFields {
  lifecycle_state?: 'active' | 'deprecated' | 'superseded';
  deprecated_in?: string;
  superseded_by?: string;
  deprecation_reason?: string;
}

export type MatrixMaturity = 'core' | 'draft';

export type ActorCategory =
  | 'lone_actor'
  | 'insider'
  | 'criminal'
  | 'corporate_espionage'
  | 'ideological'
  | 'nation_state'
  | 'customer_aggressor';
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
}

export type Modality = 'physical' | 'cyber' | 'cyber_physical' | 'human_social';
export type CrossingMechanism = 'digital' | 'electromagnetic' | 'physical_implant';

// Per-indicator investigative tasking (type-level).
export type ProbeFactor =
  | 'target_focus'
  | 'pathway_stage'
  | 'means_in_hand'
  | 'tempo_trajectory'
  | 'proximity_access'
  | 'source_credibility';

export interface ConditioningGuidance {
  probe_factors?: ProbeFactor[];
  guidance: string;
}

export interface Indicator extends LifecycleFields {
  id: string;
  behavior: string;
  category: string;
  detection_sources?: string[];
  phase_relevance?: string[];
  source_refs?: string[];
  modality: Modality;
  human_social?: boolean;
  crossing_mechanism?: CrossingMechanism;
  conditioning_guidance?: ConditioningGuidance;
  correlates_with?: string[];
  temporal_signature?: string;
  informs_axes?: InformsAxes;
  target_identity?: TargetIdentity[];
  facility_target_scope?: FacilityTargetScope[];
  within_site_focus?: WithinSiteFocus[];
}

export interface MitigatesEdge {
  indicator_id: string;
  function: 'prevent' | 'detect' | 'deny' | 'unreviewed';
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
  limitations?: string;
  source_refs?: string[];
  compensates_for?: string[];
  mitigates?: MitigatesEdge[];
}

export interface ResponseProtocol extends LifecycleFields {
  id: string;
  trigger: string;
  action: string;
  stakeholders?: string[];
  priority: Priority;
  escalation_trigger?: string;
  legal_notes?: string;
  source_refs?: string[];
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
  assessment_guidance?: AssessmentGuidance;
  target_identity_scope?: TargetIdentity[];
}

export interface ActorProfile extends LifecycleFields {
  id: string;
  name: string;
  category: ActorCategory;
  category_label: string;
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
  v2_tactic_associations?: V2TacticAssociation[];
}

// A held identifier: not a profile, never listed or counted.
export interface ReservedActorProfile {
  id: string;
  lifecycle_state: 'reserved';
  reserved_reason?: string;
}

export type RawActorProfile = ActorProfile | ReservedActorProfile;

export interface BibliographyEntry {
  type: string;
  title: string;
  author: string;
  date: string;
  url: string | null;
  doi?: string | null;
  relevance_summary: string;
  matrices?: string[];
  topics?: string[];
}

export interface MatrixContainer {
  tactics: Tactic[];
  scope?: string;
  maturity?: MatrixMaturity;
}
