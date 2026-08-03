import type { Tactic, Priority, ActorProfile } from '../types/framework';

export const PHASE_NAMES: Record<number, string> = {
  1: 'Target Development',
  2: 'Mobilization',
  3: 'Execution',
  4: 'Aftermath',
};

export const PHASE_SHORT: Record<number, string> = {
  1: 'Target Dev',
  2: 'Mobilization',
  3: 'Execution',
  4: 'Aftermath',
};

export const STUB: Record<
  'organization' | 'infrastructure',
  { phases: Record<number, number>; flight: number; claim: number }
> = {
  organization: { phases: { 1: 9, 2: 11, 3: 15 }, flight: 9, claim: 4 },
  infrastructure: { phases: { 1: 10, 2: 10, 3: 9 }, flight: 6, claim: 2 },
};

// The single ordered descriptor for the four target matrices — drives column
// order, display labels, identity colors, live-vs-stub status, and planned
// versions everywhere (heat map, nav tabs, bibliography sections, stub
// landings). Promoting a matrix to live = flipping its `version` to null.
// Labels are plural to match the V1.2.2 scope prose; data keys / routes /
// schema enum stay singular (matrices.person, /person) for consumer stability.
export const MATRICES = [
  { key: 'person', label: 'People', color: 'amber', version: null },
  { key: 'facility', label: 'Facilities', color: 'teal', version: null },
  { key: 'organization', label: 'Organizations', color: 'red', version: null },
  { key: 'infrastructure', label: 'Infrastructure', color: 'blue', version: null },
] as const;

export const MATRIX_LABELS: Record<string, string> = Object.fromEntries(
  MATRICES.map((m) => [m.key, m.label])
);

export const STUB_MATRICES = MATRICES.filter((m) => m.version !== null);

export const CATEGORY_ORDER = [
  'lone_actor',
  'insider',
  'criminal',
  'corporate_espionage',
  'ideological',
  'nation_state',
  'customer_aggressor',
];

export const VECTOR_LABELS: Record<string, string> = {
  physical_primary: 'Physical',
  cyber_enabled_physical: 'Cyber-Enabled',
  cyber_intrusion: 'Cyber',
  ai_enabled: 'AI-Enabled',
  ai_initiated_physical: 'AI-Initiated',
  digital_social_engineering: 'Social Eng.',
};

export const AI_RISK_LABELS: Record<string, string> = {
  accelerated_target_research: 'Accelerated Research',
  automated_surveillance: 'Automated Surveillance',
  synthetic_identity: 'Synthetic Identity',
  deepfake_communication: 'Deepfake Comms',
  deepfake_manipulation: 'Deepfake Manipulation',
  ai_generated_content: 'AI Content',
  autonomous_attack_planning: 'Auto Planning',
  autonomous_targeting: 'Autonomous Targeting',
  llm_social_engineering: 'LLM Social Eng.',
  spear_phishing_automation: 'Spear Phishing',
  automated_reconnaissance: 'Auto Recon',
  insider_threat_augmentation: 'Insider Augmentation',
  behavioral_mimicry: 'Behavioral Mimicry',
};

export const INDICATOR_CATEGORY_LABELS: Record<string, string> = {
  surveillance: 'Surveillance',
  acquisition: 'Acquisition',
  communication: 'Communication',
  behavioral_change: 'Behavioral Change',
  planning: 'Planning',
  access: 'Access',
  financial: 'Financial',
  digital: 'Digital',
};

// V1.2.2 People-matrix scope sub-dimension
export const TARGET_IDENTITY_LABELS: Record<string, string> = {
  named_individual: 'Named Individual',
  role_or_identity_category: 'Role / Identity Category',
  affinity_group: 'Affinity Group',
  indiscriminate: 'Indiscriminate',
};

// V1.3 Facility-matrix target sub-dimensions (revealed reading)
export const FACILITY_TARGET_SCOPE_LABELS: Record<string, string> = {
  specific_site: 'Specific Site',
  site_class: 'Site Class',
  symbolic_category: 'Symbolic Category',
  indiscriminate: 'Indiscriminate',
};

export const WITHIN_SITE_FOCUS_LABELS: Record<string, string> = {
  structure: 'Structure',
  occupants: 'Occupants',
  systems: 'Systems',
  whole_site: 'Whole Site',
};

// V1.2 escalation severity band
export const SEVERITY_BAND_LABELS: Record<string, string> = {
  low: 'Low',
  medium: 'Medium',
  high: 'High',
  critical: 'Critical',
};

// V1.2 temporal signature ({tempo}_{stage})
export const TEMPORAL_SIGNATURE_LABELS: Record<string, string> = {
  horizon: 'Horizon',
  horizon_early: 'Horizon · Early',
  horizon_late: 'Horizon · Late',
  advancing: 'Advancing',
  advancing_early: 'Advancing · Early',
  advancing_late: 'Advancing · Late',
  imminent: 'Imminent',
  imminent_early: 'Imminent · Early',
  imminent_late: 'Imminent · Late',
  staging: 'Staging',
  in_progress: 'In Progress',
  aftermath: 'Aftermath',
  aftermath_early: 'Aftermath · Early',
  aftermath_late: 'Aftermath · Late',
};

// V1.2.2 primary-objective evidence tier
export const EVIDENCE_TIER_LABELS: Record<string, string> = {
  stated: 'Stated',
  strongly_inferred: 'Strongly Inferred',
  weakly_inferred: 'Weakly Inferred',
  unknown: 'Unknown',
};

// V1.2 escalation axes (escalation_axes sub-scores)
export const ESCALATION_AXIS_LABELS: Record<string, string> = {
  impact_potential: 'Impact Potential',
  blast_radius_potential: 'Blast Radius',
  recoverability_inverse: 'Recoverability (inv.)',
  detectability: 'Detectability',
};

// V1.2 informs_axes (which axes of the threat picture an indicator informs)
export const INFORMS_AXIS_LABELS: Record<string, string> = {
  actor_capability: 'Actor · Capability',
  actor_intent: 'Actor · Intent',
  actor_opportunity: 'Actor · Opportunity',
  threat_timing: 'Event · Timing',
  threat_target: 'Event · Target',
  threat_method: 'Event · Method',
};

export const PHASE_RELEVANCE_LABELS: Record<string, string> = {
  target_development: 'Target Development',
  mobilization: 'Mobilization',
  execution: 'Execution',
  aftermath: 'Aftermath',
};

export const COUNTERMEASURE_CATEGORY_LABELS: Record<string, string> = {
  preventive: 'Preventive',
  detective: 'Detection',
  corrective: 'Corrective',
  deterrent: 'Deterrent',
};

export const DETECTION_SOURCE_LABELS: Record<string, string> = {
  physical_observation: 'Physical Obs.',
  cctv: 'CCTV',
  access_logs: 'Access Logs',
  social_media: 'Social Media',
  peer_report: 'Peer Report',
  financial_records: 'Financial',
  it_logs: 'IT Logs',
  public_records: 'Public Records',
  communications_intercept: 'Comms Intercept',
  open_source: 'OSINT',
  rf_detection: 'RF Detection',
  anti_drone_systems: 'Anti-Drone',
  ot_telemetry: 'OT Telemetry',
  network_monitoring: 'Network Mon.',
  vendor_reporting: 'Vendor Report',
};

export const STAKEHOLDER_LABELS: Record<string, string> = {
  threat_management_team: 'TMT',
  security_operations: 'Sec Ops',
  protective_operations: 'Protective Ops',
  human_resources: 'HR',
  legal: 'Legal',
  law_enforcement: 'Law Enforcement',
  executive_leadership: 'Exec Leadership',
  it_security: 'IT Security',
  communications: 'Comms',
  employee_assistance: 'EAP',
};

export const DOMAIN_LABELS: Record<string, string> = {
  physical_barriers: 'Physical Barriers',
  surveillance_systems: 'Surveillance Systems',
  access_control: 'Access Control',
  personnel_security: 'Personnel Security',
  policy_procedure: 'Policy / Procedure',
  training_awareness: 'Training / Awareness',
  technical_monitoring: 'Technical Monitoring',
  environmental_design: 'Environmental Design',
  behavioral_intervention: 'Behavioral Intervention',
};

export const PRIORITY_ORDER: Priority[] = [
  'urgent',
  'immediate',
  'priority',
  'routine',
  'ongoing',
];

// Ordered, empty-skipping actor-category groups with a display label.
// Single source of truth for the CATEGORY_ORDER iteration shared by the
// FilterBar dropdown and the ActorProfilesView grid — so a category that
// appears in the data but not in CATEGORY_ORDER cannot silently drop from
// one surface while showing in the other.
export const orderedActorCategories = (
  actorsByCategory: Record<string, ActorProfile[]>
): { cat: string; label: string; actors: ActorProfile[] }[] =>
  CATEGORY_ORDER.filter((c) => actorsByCategory[c]?.length).map((cat) => ({
    cat,
    label: actorsByCategory[cat][0].category_label,
    actors: actorsByCategory[cat],
  }));

export const tacticMatchesFilters = (
  t: Tactic,
  modalityFilter: string,
  actorFilter: string
): boolean =>
  (!modalityFilter ||
    (t.indicators || []).some((i) => i.modality === modalityFilter)) &&
  (!actorFilter ||
    (t.actor_associations || []).some((a) => a.actor_id === actorFilter));

// V1.6 Behavioral Mode (modality) — display labels + one-line definitions.
// Data field stays `modality`; the UI reads "Behavioral Mode".
export const MODALITY_LABELS: Record<string, string> = {
  physical: 'Physical',
  cyber: 'Cyber',
  cyber_physical: 'Cyber-Physical',
  human_social: 'Human & Social',
};

export const MODALITY_DEFS: Record<string, string> = {
  physical: 'Instrument is matter, force, or presence (on-site acts, breaching, weapons).',
  cyber: "Instrument operates on a computing system's access, code, or data. A platform used only to carry a message does not count.",
  cyber_physical: 'The behavior crosses the seam between digital systems and physical machinery (CPN, Cyber-Physical Nexus).',
  human_social: 'Instrument operates on people or institutions (persuasion, coercion, legal or financial process), or is a human warning behavior.',
};

export const MODALITY_ORDER = ['physical', 'cyber', 'cyber_physical', 'human_social'];

export const CROSSING_MECHANISM_LABELS: Record<string, string> = {
  digital: 'Digital',
  electromagnetic: 'Electromagnetic',
  physical_implant: 'Physical Implant',
};

export const resolveTrack = (t: Tactic): 'flight' | 'claim' | null =>
  t.phase_4_track === 'evasion'
    ? 'flight'
    : t.phase_4_track === 'attribution'
    ? 'claim'
    : null;

export function groupByCategory<T extends { category?: string }>(
  items: T[],
  labels: Record<string, string>
): { orderedKeys: string[]; grouped: Record<string, T[]> } {
  const grouped = items.reduce<Record<string, T[]>>((acc, item) => {
    const k = item.category || 'other';
    if (!acc[k]) acc[k] = [];
    acc[k].push(item);
    return acc;
  }, {});
  const order = Object.keys(labels);
  const orderedKeys = [
    ...order.filter((k) => grouped[k]),
    ...Object.keys(grouped).filter((k) => !order.includes(k)),
  ];
  return { orderedKeys, grouped };
}
