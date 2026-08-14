#!/usr/bin/env node
// scripts/score/gate-behavior-harness-report.mjs
//
// Closes this recipe's one open [TODO: DEV] item: writes a
// reports/generated/*.md human report and a logs/*.json agent log,
// matching the format the other 43 recipes use, instead of stdout only.
//
// Run: node scripts/score/gate-behavior-harness-report.mjs

import fs from 'node:fs';
import path from 'node:path';
import { scoreRole, applyProfile, CONFIG } from './role-scorer.mjs';
import { scoreRoleBrokenGateAsVote } from './BROKEN-scorer-for-harness-selftest.mjs';

const GHOST_POSTING_ROLE = {
  role_id: 'ghost-posting', company: 'Proven sponsor (ghost posting)',
  sponsorship: { p: 0.9, tier: 'Proven', source: 'record' },
  fit: { p: 0.8, source: 'model-judgment' },
  liveness: { factor: 0.0, source: 'record' },
  timeline: { factor: 0.85, source: 'your-input' },
};

const TIMELINE_GATE_ROLE = JSON.parse(
  fs.readFileSync('data/examples/gate-harness-timeline-test.json', 'utf8')
)[0];

function runAssertions() {
  const results = [];
  const check = (name, condition, detail) => results.push({ name, pass: !!condition, detail });

  const { w, needsSponsor } = applyProfile(CONFIG.weights, null);

  {
    const r = scoreRole(GHOST_POSTING_ROLE, w, needsSponsor);
    check('liveness gate zeroes composite despite high sponsorship (0.9) and fit (0.8)', r.composite === 0, `composite=${r.composite}`);
    check('liveness-gated role is classified Skip', r.recommendation === 'Skip', `recommendation=${r.recommendation}`);
    check('Skip reason names the closed gate', r.reason.includes('gated: liveness'), `reason="${r.reason}"`);
  }
  {
    const r = scoreRole(TIMELINE_GATE_ROLE, w, needsSponsor);
    check('near-zero timeline still classified Skip', r.recommendation === 'Skip', `recommendation=${r.recommendation}, composite=${r.composite}`);
    check('Skip forced by explicit gate check', r.reason.includes('gated: timeline'), `reason="${r.reason}"`);
  }
  {
    const exactZero = { ...TIMELINE_GATE_ROLE, timeline: { factor: 0.0, source: 'your-input' } };
    const r = scoreRole(exactZero, w, needsSponsor);
    check('exact-zero timeline zeroes composite exactly', r.composite === 0, `composite=${r.composite}`);
  }

  const part1 = results.slice();

  const part2 = [];
  const check2 = (name, condition, detail) => part2.push({ name, pass: !!condition, detail });
  const weights = { sponsorship: 0.35, fit: 0.30, role_quality: 0.0 };
  {
    const r = scoreRoleBrokenGateAsVote(GHOST_POSTING_ROLE, weights);
    check2('[SELF-TEST] broken scorer: liveness=0 zeroes composite?', r.composite === 0, `composite=${r.composite}`);
    check2('[SELF-TEST] broken scorer: ghost posting classified Skip?', r.recommendation === 'Skip', `recommendation=${r.recommendation}`);
  }
  {
    const r = scoreRoleBrokenGateAsVote(TIMELINE_GATE_ROLE, weights);
    check2('[SELF-TEST] broken scorer: timeline~0 zeroes composite?', r.composite === 0, `composite=${r.composite}`);
  }

  return { part1, part2 };
}

function main() {
  const { part1, part2 } = runAssertions();
  const part1AllPass = part1.every((r) => r.pass);
  const part2AllFail = part2.every((r) => !r.pass);
  const valid = part1AllPass && part2AllFail;
  const when = new Date().toISOString().slice(0, 10);

  const md = [];
  md.push(`# Gate-Behavior Harness Report — ${when}`);
  md.push('');
  md.push('## Run Summary');
  md.push(`Part 1 (real scorer): ${part1.filter(r=>r.pass).length}/${part1.length} passed. ` +
         `Part 2 (broken scorer self-test): ${part2.filter(r=>!r.pass).length}/${part2.length} correctly failed. ` +
         `**Verdict: ${valid ? 'VALID' : 'INVALID'}**`);
  md.push('');
  md.push('## Part 1 — Real Scorer (expected: all PASS)');
  md.push('| Assertion | Result | Detail |');
  md.push('|---|---|---|');
  for (const r of part1) md.push(`| ${r.name} | ${r.pass ? 'PASS' : 'FAIL'} | ${r.detail} |`);
  md.push('');
  md.push('## Part 2 — Deliberately Broken Scorer (expected: all FAIL)');
  md.push('| Assertion | Result | Detail |');
  md.push('|---|---|---|');
  for (const r of part2) md.push(`| ${r.name} | ${r.pass ? 'PASS (unexpected!)' : 'FAIL (correct)'} | ${r.detail} |`);
  md.push('');
  md.push('## Verdict');
  md.push(valid
    ? '**VALID** — the real scorer behaves as a gate, and this harness proved it can detect the specific gate-as-vote bug it targets.'
    : '**INVALID** — either the real scorer failed an assertion (a real regression) or the broken scorer passed one (the harness has no real detection power). Do not trust this recipe\'s VALID claim until investigated.');

  fs.mkdirSync('reports/generated', { recursive: true });
  const reportPath = `reports/generated/gate-behavior-harness-${when}.md`;
  fs.writeFileSync(reportPath, md.join('\n') + '\n');

  const log = {
    workflow: 'gate-behavior-harness',
    run_id: `gate-behavior-harness-${when}`,
    part1_results: part1,
    part2_results: part2,
    verdict: valid ? 'VALID' : 'INVALID',
    generated_at: new Date().toISOString(),
    report_path: reportPath,
  };
  fs.mkdirSync('logs', { recursive: true });
  const logPath = `logs/gate-behavior-harness-${when}.json`;
  fs.writeFileSync(logPath, JSON.stringify(log, null, 2));

  console.log(`Verdict: ${valid ? 'VALID' : 'INVALID'}`);
  console.log(`Wrote ${reportPath}`);
  console.log(`Wrote ${logPath}`);
  process.exit(valid ? 0 : 1);
}

main();
