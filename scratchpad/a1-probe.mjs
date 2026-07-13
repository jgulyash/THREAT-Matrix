// A1 reverse-link probe — 5 checks against the built SPA
import { createRequire } from 'module';
const require = createRequire('/Users/jgulyash/.npm/_npx/e41f203b7505f1fb/node_modules/playwright/');
const { chromium } = require('playwright');

const BASE = 'http://localhost:4173';
let pass = 0, fail = 0;
const check = (name, ok, detail) => {
  console.log(`${ok ? 'PASS' : 'FAIL'} — ${name} — ${detail}`);
  ok ? pass++ : fail++;
};

const browser = await chromium.launch();
const page = await browser.newPage();

// 1+2: one-directional target shows Referenced By with expected inbound refs
await page.goto(`${BASE}/#/person/indicator/IND-0102-01`);
await page.waitForTimeout(600);
let body = await page.textContent('body');
check('RefBy section renders on IND-0102-01', /Referenced By \(\d+\)/.test(body),
  (body.match(/Referenced By \(\d+\)/) || ['absent'])[0]);
const expected = ['IND-0101-01', 'IND-0103-02', 'IND-0105-05', 'IND-0208-06'];
check('RefBy lists the 4 known inbound-only refs',
  expected.every((id) => body.includes(id)), expected.join(','));

// 3: mutual pair IND-0101-01<->IND-0101-04 — 0101-04 must appear ONCE (Related only)
await page.goto(`${BASE}/#/person/indicator/IND-0101-01`);
await page.waitForTimeout(600);
const count = await page.locator('.adv-tactic-id', { hasText: 'IND-0101-04' }).count();
check('mutual link IND-0101-04 not duplicated', count === 1, `occurrences: ${count}`);

// 4: no-inbound indicator shows NO Referenced By section
await page.goto(`${BASE}/#/person/indicator/IND-0102-03`);
await page.waitForTimeout(600);
body = await page.textContent('body');
check('no RefBy section on IND-0102-03 (no inbound)', !body.includes('Referenced By'), 'clean');

// 5: RefBy link navigates cross-page
await page.goto(`${BASE}/#/person/indicator/IND-0102-01`);
await page.waitForTimeout(600);
await page.locator('.ind-related-link', { hasText: 'IND-0208-06' }).first().click();
await page.waitForTimeout(400);
check('RefBy link navigates', page.url().includes('IND-0208-06'), page.url());

await browser.close();
console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
