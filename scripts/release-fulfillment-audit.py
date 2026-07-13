#!/usr/bin/env python3
"""
THREAT Matrix — Promise-vs-Fulfillment release audit.

Run before every release:  python3 scripts/release-fulfillment-audit.py

WHY THIS EXISTS: a pure emptiness check ("is this array empty?") misses the more
important class of gap — where a structure is POPULATED but the framework's own
stated doctrine/description/contract claims something the data does not deliver
(e.g. the Detection Mesh names cross_matrix/cross_domain axes but has 0 such links;
the instance-conditioning contract says a bare type score is "non-renderable" while
the SPA renders it). This audit applies the DOCTRINE-VS-DATA lens mechanically.

It reports; it does not gate. Review each FLAG against the V1.4 backlog — some
partials are by-design (revealed-reading target fields, direct-force severity_floor).
Investigate anything not already tracked.
"""
import json, os, sys, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FW = json.load(open(os.path.join(ROOT, 'docs/data/framework.json')))
SCHEMA = json.load(open(os.path.join(ROOT, 'docs/data/framework.schema.json')))

# Partials that are intentional by design — reported but not FLAGGED as gaps.
BY_DESIGN = {
    'severity_floor',            # direct-force behaviors only
    'target_identity', 'facility_target_scope', 'within_site_focus',
    'target_identity_scope',     # revealed reading — empty when behavior reveals nothing
    'phase_4_track',             # aftermath tactics only
}

def rule(t): print('\n' + '=' * 72 + f'\n{t}\n' + '=' * 72)

def field_pop(items, props, label):
    print(f'\n{label} (n={len(items)}):')
    for f in props:
        pop = sum(1 for it in items if it.get(f) not in (None, [], {}, ''))
        if pop == len(items): continue
        tag = 'SHELL (0)' if pop == 0 else 'partial'
        note = '  [by-design]' if f in BY_DESIGN else ('  <-- FLAG' if pop == 0 else '  <-- review')
        print(f'  {f:36s} {pop}/{len(items)}  {tag}{note}')

# ---- 1. Field fulfillment ----
rule('1. FIELD FULFILLMENT — schema-defined fields vs actual population')
allind = [i for n in ('person','facility','organization','infrastructure')
          for t in FW['matrices'][n]['tactics'] for i in t['indicators']]
alltac = [t for n in ('person','facility','organization','infrastructure')
          for t in FW['matrices'][n]['tactics']]
field_pop(allind, SCHEMA['$defs']['indicator']['properties'], 'INDICATOR fields')
field_pop(alltac, SCHEMA['$defs']['tactic']['properties'], 'TACTIC fields')
aps = FW['actor_profiles']
apkeys = sorted({k for a in aps for k in a})
field_pop(aps, {k: None for k in apkeys}, 'ACTOR_PROFILE fields')

# ---- 2. Detection Mesh axis delivery ----
rule('2. DETECTION MESH — each named axis vs actual delivered links')
meta = {i['id']: (n, t['phase']) for n in ('person','facility')
        for t in FW['matrices'][n]['tactics'] for i in t['indicators']}
xphase = xmatrix = same = 0
for n in ('person','facility'):
    for t in FW['matrices'][n]['tactics']:
        for i in t['indicators']:
            for r in i.get('correlates_with', []):
                if r in meta:
                    if meta[r][0] != n: xmatrix += 1
                    elif meta[r][1] != t['phase']: xphase += 1
                    else: same += 1
def cross_matrix_count(container, field, idmap):
    c = 0
    for n in ('person','facility'):
        for t in FW['matrices'][n]['tactics']:
            for it in t.get(container, []):
                for r in it.get(field, []):
                    if idmap.get(r) and idmap[r] != n: c += 1
    return c
cm_map = {cm['id']: n for n in ('person','facility') for t in FW['matrices'][n]['tactics'] for cm in t.get('countermeasures',[])}
rp_map = {rp['id']: n for n in ('person','facility') for t in FW['matrices'][n]['tactics'] for rp in t.get('response_protocols',[])}
axes = [a['name'] for a in FW['detection_mesh']['axes']]
delivered = {
    'cross_phase': xphase,
    'cross_matrix': xmatrix,
    'cross_domain': xmatrix,
    'cross_countermeasure': cross_matrix_count('countermeasures','compensates_for',cm_map),
    'cross_stakeholder': cross_matrix_count('response_protocols','coordinates_with',rp_map),
}
print(f'  named mesh axes: {axes}')
for ax in axes:
    d = delivered.get(ax)
    if d is None:
        print(f'  {ax:22s} (cross-domain) : n/a  <-- add a delivery check')
    else:
        print(f'  {ax:22s} : {d} delivered' + ('' if d > 0 else '  <-- FLAG: named but 0 delivered'))
print(f'  (within-matrix same-phase links: {same})')

# ---- 3. Empty top-level structures ----
rule('3. TOP-LEVEL STRUCTURES — scaffolded but empty')
for k, v in FW.items():
    if isinstance(v, list) and len(v) == 0:
        print(f'  {k}: []  <-- FLAG (empty list)')
    if isinstance(v, dict) and 'tactics' in v and len(v.get('tactics', [])) == 0:
        print(f'  matrix {k}: 0 tactics  <-- FLAG (empty matrix scaffold)')

# ---- 4. Doctrine claims requiring MANUAL verification ----
rule('4. DOCTRINE CLAIMS — verify by hand each release (data cannot self-check these)')
consumer_refs = len(re.findall(r'consumer|downstream|triage tooling',
                    json.dumps(FW), flags=re.I))
print(f"""  [ ] instance_conditioning binding_contract says a bare type score is
      "non-renderable / not an assessment" — does the SPA still render bare
      severity_band / escalation_weight with no instance record? (grep
      src/components/IndicatorDetail.tsx). Contract vs showcase must agree.
  [ ] detection_mesh.principle prose ("any matrix ... anywhere else",
      "countermeasures from any domain") — matches the axis-delivery numbers in
      section 2 above?
  [ ] {consumer_refs} 'consumer/downstream/triage tooling should...' references
      describe an engine/mapping-layer that may not exist — is that still
      roadmap, and is it labeled as such (not implied as shipped)?
  [ ] Any NEW field/object added this cycle with a description that promises
      behavior — is it populated where the description says it is?""")

print('\n' + '=' * 72)
print('Audit complete. FLAG = doctrine/schema promises data does not meet.')
print('Cross-check every FLAG against the V1.4 backlog before release.')
print('=' * 72)
