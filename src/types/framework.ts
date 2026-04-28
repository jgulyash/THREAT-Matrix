export type Priority = 'urgent' | 'immediate' | 'priority' | 'routine' | 'ongoing';
export type RiskLevel = 'low' | 'medium' | 'high';
export type TimeToImplement = 'immediate' | 'days' | 'weeks' | 'months';

export interface Indicator {
  id: string;
  behavior: string;
  category: string;
  detection_sources: string[];
  phase_relevance?: string[];
  source_refs: string[];
}

export interface Countermeasure {
  id: string;
  measure: string;
  category: string;
  domain?: string;
  cost: RiskLevel;
  complexity: RiskLevel;
  time_to_implement: TimeToImplement;
  limitations: string;
  source_refs: string[];
}

export interface ResponseProtocol {
  id: string;
  trigger: string;
  action: string;
  stakeholders: string[];
  priority: Priority;
  escalation_trigger: string;
  legal_notes: string;
  source_refs: string[];
}

export interface ActorAssociation {
  actor_id: string;
  relevance: 'high' | 'medium' | 'low';
  employment_status?: string;
}

export interface Tactic {
  id: string;
  name: string;
  tactic_families?: string[];
  matrix: string;
  phase: 1 | 2 | 3 | 4;
  phase_name: string;
  notes: string;
  cpn: boolean;
  cpn_id?: string;
  cpn_notes?: string;
  techniques?: unknown[];
  indicators: Indicator[];
  countermeasures: Countermeasure[];
  related_tactics?: string[];
  actor_associations?: ActorAssociation[];
  source_refs?: string[];
  response_protocols: ResponseProtocol[];
  phase_4_track?: 'evasion' | 'attribution';
}

export interface ActorProfile {
  id: string;
  name: string;
  category: string;
  category_label: string;
  awareness: string;
  direction: string;
  access_relationship: string;
  phase_compression_risk: string;
  actor_level?: string;
  attack_vectors?: string[];
  primary_matrices?: string[];
  description?: string;
  behavioral_markers?: string[];
  ai_enabled_risks?: string[];
}

export interface BibliographyEntry {
  type: string;
  title: string;
  author: string;
  date: string;
  url: string | null;
  doi?: string | null;
  relevance_summary: string;
}

export interface FrameworkData {
  name: string;
  full_name?: string;
  version: string;
  license?: string;
  matrices: {
    person: { tactics: Tactic[] };
    [k: string]: { tactics: Tactic[] };
  };
  actor_profiles: ActorProfile[];
  bibliography: Record<string, BibliographyEntry>;
  [k: string]: unknown;
}
