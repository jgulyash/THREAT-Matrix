import { chromium } from '/Users/jgulyash/.npm/_npx/e41f203b7505f1fb/node_modules/playwright/index.mjs';
const BASE='http://localhost:4173/';
const browser=await chromium.launch(); const page=await browser.newPage();
const errs=[]; page.on('pageerror',e=>errs.push(String(e).slice(0,120)));
const out=[]; const t=(n,ok,ev)=>out.push(`${ok?'PASS':'FAIL'}  ${n}  ${ev||''}`);
await page.goto(BASE, {waitUntil:'networkidle'}); await page.waitForTimeout(500);

const hdrs = await page.locator('.hm-col-hdr').allTextContents();
t('header order People,Facilities,Organizations,Infrastructure', /People/.test(hdrs[1])&&/Facilities/.test(hdrs[2])&&/Organizations/.test(hdrs[3])&&/Infrastructure/.test(hdrs[4]), hdrs.join(' | '));

// phase-1 row: children = [phaseCell, person, facility, organization(stub), infrastructure]
const row1 = page.locator('.hm-row').first();
const cellCount = await row1.locator(':scope > *').count();
t('phase-1 row has 5 columns (phase + 4 matrices)', cellCount===5, `cells=${cellCount}`);

// Click the 5th child (Infrastructure column) -> must navigate to /infrastructure
await row1.locator(':scope > *').nth(4).click().catch(()=>{});
await page.waitForTimeout(500);
let hash = await page.evaluate(()=>location.hash);
t('Infrastructure column (col 4) navigates to /infrastructure', /infrastructure\/phase\/1/.test(hash), `hash=${hash}`);

// back, click the 4th child (Organizations column) -> stub (should NOT go to infrastructure)
await page.goto(BASE, {waitUntil:'networkidle'}); await page.waitForTimeout(400);
await page.locator('.hm-row').first().locator(':scope > *').nth(3).click().catch(()=>{});
await page.waitForTimeout(400);
hash = await page.evaluate(()=>location.hash);
t('Organizations column (col 3) is NOT infrastructure', !/infrastructure/.test(hash), `hash=${hash||'(stub, no nav)'}`);

// phase-4 Evade (flight) wing under Infrastructure column must show infra flight tactics
await page.goto(BASE, {waitUntil:'networkidle'}); await page.waitForTimeout(400);
const flightRow = page.locator('.phase4-sub-row').first();
const flightCells = flightRow.locator(':scope > *');
const fc = await flightCells.count();
// 4th flight cell (index 3) = Infrastructure column
await flightCells.nth(3).click().catch(()=>{});
await page.waitForTimeout(500);
hash = await page.evaluate(()=>location.hash);
t('Aftermath/Evade(flight) Infrastructure column -> /infrastructure/phase/4/flight', /infrastructure\/phase\/4\/flight/.test(hash), `cells=${fc} hash=${hash}`);
const flightTxt = (await page.locator('body').innerText()).replace(/\s+/g,' ');
t('infra Evade wing shows tactics (TI04xx present)', /TI04\d\d/.test(flightTxt), flightTxt.match(/TI04\d\d/g)?.slice(0,4)?.join(',')||'NONE');

t('no page errors', errs.length===0, errs.slice(0,2).join(' || '));
console.log(out.join('\n'));
console.log('\nRESULT:', out.every(l=>l.startsWith('PASS'))?'ALL PASS':'FAILURES');
await browser.close();
