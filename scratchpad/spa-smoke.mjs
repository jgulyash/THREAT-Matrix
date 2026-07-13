import { chromium } from '/Users/jgulyash/.npm/_npx/e41f203b7505f1fb/node_modules/playwright/index.mjs';

const BASE = 'http://localhost:4173/';
const results = [];
const consoleErrors = [];

const t = (name, ok, evidence) => results.push({ name, ok, evidence });

const browser = await chromium.launch();
const page = await browser.newPage();
page.on('console', (msg) => {
  if (msg.type() === 'error') consoleErrors.push(msg.text().slice(0, 200));
});
page.on('pageerror', (err) => consoleErrors.push('PAGEERROR: ' + String(err).slice(0, 200)));

const go = async (hash) => {
  await page.goto(BASE + hash, { waitUntil: 'networkidle' });
  await page.waitForTimeout(250);
};

// ---------- Facility heat map ----------
await go('#/facility');
const hdrs = await page.locator('.hm-col-hdr').allTextContents();
t('F1 headers', hdrs.join('|').includes('People · 34') && hdrs.join('|').includes('Facilities · 40'),
  hdrs.join(' | '));
const rows = page.locator('.hm-row');
const rowTexts = [];
for (let i = 0; i < await rows.count(); i++) {
  const counts = await rows.nth(i).locator('.hm-count').allTextContents();
  rowTexts.push(counts.join(','));
}
// each row: person, facility, org-stub, infra-stub
t('F1 rows1-3 facility counts 10/9/9',
  rowTexts.length === 3 &&
  rowTexts[0].split(',')[1] === '10' && rowTexts[1].split(',')[1] === '9' && rowTexts[2].split(',')[1] === '9',
  JSON.stringify(rowTexts));
const p4counts = await page.locator('.phase4-sub-row .hm-count').allTextContents();
// sub-row order: person, facility, org, infra (flight) then (claim)
t('F1 phase4 facility Evade 8 / Claim 4',
  p4counts[1] === '8' && p4counts[5] === '4', JSON.stringify(p4counts));
const stubCells = await page.locator('.hm-cell.stub').count();
t('F1 org/infra stubs remain', stubCells >= 8, `stub cells: ${stubCells}`);
const activeTabs = await page.locator('.mtab.active').allTextContents();
t('F1 Facilities tab active', activeTabs.join() === 'Facilities', JSON.stringify(activeTabs));

// ---------- Facility phase panel ----------
await go('#/facility/phase/1');
const cards = await page.locator('.dp-card-id').allTextContents();
t('F2 phase-1 panel 10 TF01xx cards', cards.length === 10 && cards.every((c) => c.startsWith('TF01')),
  `${cards.length}: ${cards.slice(0, 3).join(',')}...`);
const selCell = await page.locator('.hm-cell.selected').count();
const selHasTF = await page.locator('.hm-cell.selected .hm-name').first().textContent().catch(() => '');
t('F2 selection on facility cell', selCell === 1, `selected cells: ${selCell}, first name: ${selHasTF}`);

// ---------- Facility tactic detail ----------
await go('#/facility/tactic/TF0101');
const title = await page.locator('.dp-header-title').textContent();
const indIds = await page.locator('.dr-item-id').allTextContents();
t('F3 TF0101 detail + IND-F indicators', !!title && indIds.length > 0 && indIds[0].includes('IND-F0101'),
  `title: ${title}, first ind: ${indIds[0]}`);
await page.locator('.dp-back').click();
await page.waitForTimeout(200);
t('F3 back to phase panel', page.url().includes('#/facility/phase/1'), page.url());

// ---------- Facility indicator detail ----------
await go('#/facility/indicator/IND-F0101-01');
const beh = await page.locator('.adv-body').first().textContent().catch(() => null);
const escLabel = await page.locator('.adv-section-label', { hasText: 'Escalation Profile' }).count();
const informs = await page.locator('.adv-section-label', { hasText: 'Informs Threat Picture' }).count();
const tgtId = await page.getByText('Target Identity', { exact: false }).count();
const tgtScope = await page.getByText('Target Scope', { exact: false }).count();
const backLink = await page.locator('.adv-back').textContent();
t('F4 facility indicator renders escalation + informs (V1.3 Gate 2) + Target Scope, no person Target Identity',
  !!beh && escLabel === 1 && informs === 1 && tgtId === 0 && tgtScope === 1,
  `behavior: ${!!beh}, esc: ${escLabel}, informs: ${informs}, tgtId: ${tgtId}, tgtScope: ${tgtScope}`);
t('F4 back link names TF0101', backLink.includes('TF0101'), backLink.trim().slice(0, 40));

// ---------- Facility phase-4 tracks ----------
await go('#/facility/phase/4/flight');
const evadeCards = await page.locator('.dp-card-id').allTextContents();
await go('#/facility/phase/4/claim');
const claimCards = await page.locator('.dp-card-id').allTextContents();
t('F5 Evade 8 / Claim 4 panels',
  evadeCards.length === 8 && claimCards.length === 4 &&
  claimCards.join().includes('TF0409') && claimCards.join().includes('TF0412'),
  `evade: ${evadeCards.length}, claim: ${claimCards.join(',')}`);

// ---------- References ----------
await go('#/references');
const secHdrs = await page.locator('.dr-section-header span:first-child').allTextContents();
t('F6 matrix sections present', secHdrs.includes('People') && secHdrs.includes('Facilities'),
  JSON.stringify(secHdrs));
const tfPill = page.locator('.bib-entry-cited-pill', { hasText: /^TF/ }).first();
const tfPillCount = await page.locator('.bib-entry-cited-pill', { hasText: /^TF/ }).count();
if (tfPillCount > 0) {
  await tfPill.click();
  await page.waitForTimeout(250);
}
t('F6 TF cited-by pill navigates to facility tactic',
  tfPillCount > 0 && page.url().includes('#/facility/tactic/TF'),
  `TF pills: ${tfPillCount}, url after click: ${page.url()}`);

// ---------- Person regression ----------
await go('#/person');
const pRows = [];
const rows2 = page.locator('.hm-row');
for (let i = 0; i < await rows2.count(); i++) {
  const counts = await rows2.nth(i).locator('.hm-count').allTextContents();
  pRows.push(counts.join(','));
}
const p4c = await page.locator('.phase4-sub-row .hm-count').allTextContents();
t('P1 person counts 8/9/8 + Evade 6 / Claim 3',
  pRows[0].split(',')[0] === '8' && pRows[1].split(',')[0] === '9' && pRows[2].split(',')[0] === '8' &&
  p4c[0] === '6' && p4c[4] === '3',
  `rows: ${JSON.stringify(pRows)}, p4: ${JSON.stringify(p4c)}`);
const activeTabs2 = await page.locator('.mtab.active').allTextContents();
t('P1 People tab active', activeTabs2.join() === 'People', JSON.stringify(activeTabs2));

await go('#/person/tactic/TM0103');
const pInd = await page.locator('.dr-item-id').first().textContent();
t('P2 TM0103 indicators listed', pInd.includes('IND-0103'), pInd.trim());
await go('#/person/indicator/IND-0103-01');
const informsP = await page.locator('.adv-section-label', { hasText: 'Informs Threat Picture' }).count();
const escP = await page.locator('.adv-section-label', { hasText: 'Escalation Profile' }).count();
t('P2 person indicator has Escalation + Informs sections', informsP === 1 && escP === 1,
  `informs: ${informsP}, esc: ${escP}`);

await go('#/person/phase/4/flight');
const pEvade = await page.locator('.dp-card-id').allTextContents();
t('P3 person Evade 6 cards', pEvade.length === 6, pEvade.join(','));

// ---------- Actor detail cross-matrix ----------
await go('#/actors');
const firstActor = page.locator('.actor-card, [class*=actor]').first();
await go('#/references'); // reset
await go('#/actors');
// navigate to an actor detail via any clickable actor element
const actorLinks = await page.locator('text=/Lone|Insider|Criminal/i').count();
t('P4 actors view renders', actorLinks > 0, `actor text nodes: ${actorLinks}`);

// ---------- Stubs ----------
await go('#/organization');
const stubTitle = await page.locator('.stub-landing-title').textContent().catch(() => '');
t('P5 org stub landing', stubTitle.includes('Organizations'), stubTitle);

// ---------- Console ----------
t('Console clean', consoleErrors.length === 0, consoleErrors.slice(0, 3).join(' || ') || 'none');

await browser.close();

let pass = 0, fail = 0;
for (const r of results) {
  console.log(`${r.ok ? 'PASS' : 'FAIL'} — ${r.name} — ${r.evidence}`);
  r.ok ? pass++ : fail++;
}
console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
