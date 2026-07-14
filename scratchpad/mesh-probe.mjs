import { createRequire } from 'module';
const require = createRequire('/Users/jgulyash/.npm/_npx/e41f203b7505f1fb/node_modules/playwright/');
const { chromium } = require('playwright');
const BASE = 'http://localhost:4173';
let pass=0, fail=0;
const check=(n,ok,d)=>{console.log(`${ok?'PASS':'FAIL'} — ${n} — ${d}`); ok?pass++:fail++;};
const b = await chromium.launch(); const p = await b.newPage();

// person side: IND-0103-01 should list facility IND-F0103-01 under Related (outbound cross-domain)
await p.goto(`${BASE}/#/person/indicator/IND-0103-01`); await p.waitForTimeout(600);
let body = await p.textContent('body');
check('person IND-0103-01 shows cross-domain Related IND-F0103-01', body.includes('IND-F0103-01'),
  body.includes('IND-F0103-01') ? 'present' : 'MISSING');

// facility side: IND-F0103-01 should show IND-0103-01 under Referenced By (A1 reverse-link, cross-domain)
await p.goto(`${BASE}/#/facility/indicator/IND-F0103-01`); await p.waitForTimeout(600);
body = await p.textContent('body');
check('facility IND-F0103-01 Referenced By shows person IND-0103-01',
  /Referenced By/.test(body) && body.includes('IND-0103-01'),
  (body.match(/Referenced By \(\d+\)/)||['no section'])[0]);

// cross-page nav from facility reverse-link back to person indicator
const link = p.locator('.ind-related-link', { hasText: 'IND-0103-01' }).first();
if (await link.count()) { await link.click(); await p.waitForTimeout(400); }
check('reverse-link navigates facility->person', p.url().includes('/person/indicator/IND-0103-01'), p.url());

await b.close();
console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail?1:0);
