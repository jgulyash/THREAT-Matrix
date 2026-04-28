import type { Tactic, Priority } from '../types/framework';

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
  'facility' | 'organization' | 'system',
  { phases: Record<number, number>; flight: number; claim: number }
> = {
  facility: { phases: { 1: 10, 2: 9, 3: 9 }, flight: 8, claim: 4 },
  organization: { phases: { 1: 9, 2: 10, 3: 10 }, flight: 9, claim: 4 },
  system: { phases: { 1: 8, 2: 9, 3: 9 }, flight: 8, claim: 4 },
};

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

export const COUNTERMEASURE_CATEGORY_LABELS: Record<string, string> = {
  preventive: 'Preventive',
  detective: 'Detective',
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
