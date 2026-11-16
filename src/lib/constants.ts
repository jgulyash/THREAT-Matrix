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

// The single ordered descriptor for the four target matrices: drives column
// order, display labels, and identity colors everywhere (heat map, nav tabs,
// bibliography sections). Labels are plural; data keys, routes, and the
// schema enum stay singular (matrices.person, /person) for consumer stability.
export const MATRICES = [
  { key: 'person', label: 'People', color: 'amber' },
  { key: 'facility', label: 'Facilities', color: 'teal' },
  { key: 'organization', label: 'Organizations', color: 'red' },
  { key: 'infrastructure', label: 'Infrastructure', color: 'blue' },
] as const;

export type MatrixKey = (typeof MATRICES)[number]['key'];
export const MATRIX_KEYS: MatrixKey[] = MATRICES.map((m) => m.key);

export const MATRIX_LABELS: Record<string, string> = Object.fromEntries(
  MATRICES.map((m) => [m.key, m.label])
);

export const isMatrixKey = (v: string): v is MatrixKey =>
  (MATRIX_KEYS as string[]).includes(v);

export const CATEGORY_ORDER = [
  'lone_actor',
  'insider',
  'criminal',
  'corporate_espionage',
  'ideological',
  'nation_state',
  'customer_aggressor',
];

// Readable fallback for an enum value with no label: "weeks_to_months"
// becomes "Weeks To Months". Used by label() so a value added to the data
// before the viewer learns it never shows as a raw identifier.
export function humanize(value: string): string {
  if (value === 'n/a') return 'N/A';
  return value
    .replace(/[_-]+/g, ' ')
    .trim()
    .replace(/\b[a-z]/g, (c) => c.toUpperCase());
}

// Own-property lookup with a readable fallback. Never resolves inherited
// keys such as "constructor".
export function label(labels: Record<string, string>, value: string | undefined | null): string {
  if (value === undefined || value === null || value === '') return '';
  return Object.prototype.hasOwnProperty.call(labels, value) ? labels[value] : humanize(String(value));
}

export const VECTOR_LABELS: Record<string, string> = {
  physical_primary: 'Physical',
  cyber_enabled_physical: 'Cyber-Enabled',
  cyber_initiated_physical: 'Cyber-Initiated',
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
  deepfake_voice_video: 'Deepfake Voice / Video',
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

// People matrix scope sub-dimension
export const TARGET_IDENTITY_LABELS: Record<string, string> = {
  named_individual: 'Named Individual',
  role_or_identity_category: 'Role / Identity Category',
  affinity_group: 'Affinity Group',
  indiscriminate: 'Indiscriminate',
};

// Facility matrix target sub-dimensions
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

// Temporal signature ({tempo}_{stage})
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

// informs_axes (which parts of the threat picture an indicator informs)
export const INFORMS_AXIS_LABELS: Record<string, string> = {
  actor_capability: 'Actor · Capability',
  actor_intent: 'Actor · Intent',
  actor_opportunity: 'Actor · Opportunity',
  threat_timing: 'Event · Timing',
  threat_target: 'Event · Target',
  threat_method: 'Event · Method',
};

// Display words for the informs_axes scale. The scale is resolution, not
// seriousness (METHODOLOGY section 2), so the viewer shows words that say so.
// The data values (none, weak, moderate, strong) are unchanged.
export const INFORMS_RESOLUTION_LABELS: Record<string, string> = {
  none: 'No signal',
  weak: 'Coarse',
  moderate: 'Narrowed',
  strong: 'Specific',
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
  network_segmentation: 'Network Segmentation',
  system_hardening: 'System Hardening',
  safety_system_integrity: 'Safety System Integrity',
  supply_chain_assurance: 'Supply Chain Assurance',
};

export const TIME_TO_IMPLEMENT_LABELS: Record<string, string> = {
  immediate: 'Immediate',
  days: 'Days',
  weeks: 'Weeks',
  months: 'Months',
  weeks_to_months: 'Weeks to Months',
};

export const BIB_TYPE_LABELS: Record<string, string> = {
  government_report: 'Gov Report',
  academic_paper: 'Academic',
  book: 'Book',
  court_document: 'Court Doc',
  after_action_review: 'AAR',
  news_investigation: 'Investigation',
  incident_database: 'Incident DB',
  practitioner_guide: 'Practitioner Guide',
  standard: 'Standard',
  field_observation: 'Field Observation',
  practitioner_elicitation: 'Practitioner Elicitation',
  partner_attestation: 'Partner Attestation',
  case_composite: 'Case Composite',
};

export const PRIORITY_ORDER: Priority[] = [
  'urgent',
  'immediate',
  'priority',
  'routine',
  'ongoing',
];

// Ordered, empty-skipping actor-category groups with a display label. Single
// source of truth shared by the FilterBar dropdown and the ActorProfilesView
// grid. A category present in the data but absent from CATEGORY_ORDER is
// appended, so it cannot drop from one surface while showing in the other.
export const orderedActorCategories = (
  actorsByCategory: Map<string, ActorProfile[]>
): { cat: string; label: string; actors: ActorProfile[] }[] => {
  const keys = [
    ...CATEGORY_ORDER.filter((c) => actorsByCategory.get(c)?.length),
    ...[...actorsByCategory.keys()].filter((c) => !CATEGORY_ORDER.includes(c)),
  ];
  return keys.map((cat) => {
    const actors = actorsByCategory.get(cat) || [];
    return { cat, label: actors[0]?.category_label || humanize(cat), actors };
  });
};

export const tacticMatchesFilters = (
  t: Tactic,
  modalityFilter: string,
  actorFilter: string
): boolean =>
  (!modalityFilter ||
    (t.indicators || []).some((i) => i.modality === modalityFilter)) &&
  (!actorFilter ||
    (t.actor_associations || []).some((a) => a.actor_id === actorFilter));

// Behavioral Mode (modality): display labels and one-line definitions.
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

// conditioning_guidance probe-factor labels (instance-factor enum names).
export const PROBE_FACTOR_LABELS: Record<string, string> = {
  target_focus: 'Target Focus',
  pathway_stage: 'Pathway Stage',
  means_in_hand: 'Means in Hand',
  tempo_trajectory: 'Tempo Trajectory',
  proximity_access: 'Proximity / Access',
  source_credibility: 'Source Credibility',
};

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

export const TRACK_LABELS: Record<'flight' | 'claim', string> = { flight: 'Evade', claim: 'Claim' };

export function groupByCategory<T extends { category?: string }>(
  items: T[],
  labels: Record<string, string>
): { orderedKeys: string[]; grouped: Map<string, T[]> } {
  const grouped = new Map<string, T[]>();
  items.forEach((item) => {
    const k = item.category || 'other';
    const list = grouped.get(k);
    if (list) list.push(item);
    else grouped.set(k, [item]);
  });
  const order = Object.keys(labels);
  const orderedKeys = [
    ...order.filter((k) => grouped.has(k)),
    ...[...grouped.keys()].filter((k) => !order.includes(k)),
  ];
  return { orderedKeys, grouped };
}
