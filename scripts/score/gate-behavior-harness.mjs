#!/usr/bin/env node
// scripts/score/gate-behavior-harness.mjs
//
// Gate-Behavior Unit-Test Harness (Ch.11, Ch.16).
//
// Proves that role-scorer.mjs's liveness and timeline factors behave as
// MULTIPLICATIVE GATES -- they zero the composite regardless of how high
// sponsorship/fit are -- rather than as additive votes. This is "the
// gate-as-vote bug" the assignment brief names as a capstone build failure:
// a gate that only lowers a score instead of closing it is not a gate, it's
// decoration, and it lets a ghost posting or an impossible start date sneak
// into "Apply" or "Consider" on the strength of a high fit score alone.
//
// This harness does two things, not one:
//   1. Runs real assertions against the REAL role-scorer.mjs and shows they
//      pass.
//   2. Runs the SAME assertions against a DELIBERATELY BROKEN version
//      (BROKEN-scorer-for-harness-selftest.mjs) and shows they correctly
//      fail -- proving this harness has actual detection power, not just a
//      tautology that would pass on anything.
//
// Run: node scripts/score/gate-behavior-harness.mjs

import { scoreRole, applyProfile, CONFIG } from './role-scorer.mjs';
import { scoreRoleBrokenGateAsVote } from './BROKEN-scorer-for-harness-selftest.mjs';
import fs from 'node:fs';

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

const results = [];
function check(name, condition, detail) {
  results.push({ name, pass: !!condition, detail });
  console.log(`${condition ? 'PASS' : 'FAIL'}  ${name}${detail ? '  -- ' + detail : ''}`);
}

console.log('=== Part 1: real role-scorer.mjs (expected: all PASS) ===\n');

{
  const { w, needsSponsor } = applyProfile(CONFIG.weights, null);
  const result = scoreRole(GHOST_POSTING_ROLE, w, needsSponsor);
  check(
    'liveness gate zeroes composite despite high sponsorship (0.9) and fit (0.8)',
    result.composite === 0,
    `composite=${result.composite}`
  );
  check(
    'liveness-gated role is classified Skip, not Apply/Consider',
    result.recommendation === 'Skip',
    `recommendation=${result.recommendation}`
  );
  check(
    'the Skip reason names the closed gate, not a low vote score',
    result.reason.includes('gated: liveness'),
    `reason="${result.reason}"`
  );
}

{
  const { w, needsSponsor } = applyProfile(CONFIG.weights, null);
  const result = scoreRole(TIMELINE_GATE_ROLE, w, needsSponsor);
  // NOTE: this fixture uses timeline factor 0.02 (near-zero, not exactly 0),
  // deliberately -- to test the CLASSIFICATION guarantee, not the raw
  // multiplication. The code does NOT promise composite===0 for a near-zero
  // (but nonzero) gate factor -- only that the recommendation is forced to
  // Skip via an explicit threshold check (gate_zero=0.05), independent of
  // how high sponsorship/fit are. This matches Ch.11's own wording: liveness
  // "approaching zero" makes the composite "approach zero," not necessarily
  // hit it exactly. An earlier version of this test asserted composite===0
  // here and failed -- that was this test's own miscalibrated assumption,
  // not a bug in role-scorer.mjs; fixed to test the actual contract below.
  check(
    'near-zero (but nonzero) timeline is still classified Skip, not rescued by high sponsorship/fit',
    result.recommendation === 'Skip',
    `recommendation=${result.recommendation}, composite=${result.composite}`
  );
  check(
    'the Skip is forced by the explicit gate check, not incidental low vote math',
    result.reason.includes('gated: timeline'),
    `reason="${result.reason}"`
  );
}

{
  const { w, needsSponsor } = applyProfile(CONFIG.weights, null);
  const exactZeroTimelineRole = { ...TIMELINE_GATE_ROLE, timeline: { factor: 0.0, source: 'your-input' } };
  const result = scoreRole(exactZeroTimelineRole, w, needsSponsor);
  check(
    'exact-zero timeline (the multiplicative case) does zero the composite exactly',
    result.composite === 0,
    `composite=${result.composite}`
  );
}

console.log('\n=== Part 2: deliberately BROKEN gate-as-vote scorer (expected: FAIL) ===\n');

{
  const weights = { sponsorship: 0.35, fit: 0.30, role_quality: 0.0 };
  const result = scoreRoleBrokenGateAsVote(GHOST_POSTING_ROLE, weights);
  check(
    '[SELF-TEST] broken scorer: does liveness=0 still zero the composite?',
    result.composite === 0,
    `composite=${result.composite} -- a nonzero value here means the harness ` +
    `correctly caught the gate-as-vote bug (this SHOULD fail)`
  );
  check(
    '[SELF-TEST] broken scorer: is the ghost posting classified Skip?',
    result.recommendation === 'Skip',
    `recommendation=${result.recommendation} -- if this is Apply/Consider, ` +
    `the harness correctly caught a ghost posting slipping through (this SHOULD fail)`
  );
}

{
  const weights = { sponsorship: 0.35, fit: 0.30, role_quality: 0.0 };
  const result = scoreRoleBrokenGateAsVote(TIMELINE_GATE_ROLE, weights);
  check(
    '[SELF-TEST] broken scorer: does timeline~0 still zero the composite?',
    result.composite === 0,
    `composite=${result.composite} -- a nonzero value here means the harness ` +
    `correctly caught the gate-as-vote bug (this SHOULD fail)`
  );
}

const part1 = results.slice(0, 6);
const part2 = results.slice(6);
const part1AllPass = part1.every((r) => r.pass);
const part2AllFail = part2.every((r) => !r.pass);

console.log('\n=== Summary ===');
console.log(`Part 1 (real scorer):    ${part1.filter(r=>r.pass).length}/${part1.length} passed ` +
           `${part1AllPass ? '(correct -- real scorer behaves as a gate)' : '(UNEXPECTED -- investigate the real scorer)'}`);
console.log(`Part 2 (broken scorer):  ${part2.filter(r=>!r.pass).length}/${part2.length} correctly failed ` +
           `${part2AllFail ? '(correct -- harness caught the gate-as-vote bug)' : '(HARNESS HAS NO DETECTION POWER -- it did not catch the bug)'}`);

const harnessIsValid = part1AllPass && part2AllFail;
console.log(`\nHarness self-test: ${harnessIsValid ? 'VALID -- passes on correct code, fails on the target bug' : 'INVALID -- does not distinguish correct from broken'}`);

process.exit(harnessIsValid ? 0 : 1);
