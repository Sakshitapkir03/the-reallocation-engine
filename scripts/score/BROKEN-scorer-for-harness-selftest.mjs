// scripts/score/BROKEN-scorer-for-harness-selftest.mjs
//
// THIS FILE IS DELIBERATELY BROKEN. It exists for exactly one purpose: to
// prove gate-behavior-harness.mjs actually detects the bug it claims to
// detect, rather than passing on anything you hand it.
//
// The bug it reproduces is named directly in the assignment brief: "the
// gate-as-vote bug." Chapter 11 of the book is explicit that liveness and
// timeline must be MULTIPLIERS (gates) on the composite, not ADDITIVE VOTES
// alongside sponsorship and fit -- "No amount of fit or sponsorship can carry
// a role through a gate that is closed." This file implements the version
// the chapter warns against: it adds a small weighted contribution for
// liveness/timeline instead of multiplying by them, so a closed gate (factor
// 0) merely lowers the composite instead of zeroing it -- exactly the
// silent failure mode Ch.16 names as the capstone's own build bug.
//
// DO NOT import this file for any real scoring. It is test fixture code,
// not production code, and is never wired into the real role-scorer.mjs.

const CONFIG_BROKEN = {
  weights: { sponsorship: 0.35, fit: 0.30, role_quality: 0.0 },
  gate_weights: { liveness: 0.20, timeline: 0.15 }, // THE BUG: gates given additive weights
  apply_threshold: 0.30,
  consider_floor: 0.20,
};

const num = (x) => (typeof x === 'number' && isFinite(x) ? x : null);

export function scoreRoleBrokenGateAsVote(role, weights) {
  const votes = [];
  const push = (key, obj) => {
    const p = num(obj?.p);
    if (p == null) return;
    votes.push({ key, p, weight: weights[key] ?? 0 });
  };
  push('sponsorship', role.sponsorship);
  push('fit', role.fit);
  push('role_quality', role.role_quality);

  const voteSum = votes.reduce((s, v) => s + v.p * v.weight, 0);

  // THE BUG: liveness/timeline treated as additional weighted VOTES,
  // added to the sum, instead of multiplicative GATES applied to it.
  const liveness = num(role.liveness?.factor) ?? 1;
  const timeline = num(role.timeline?.factor) ?? 1;
  const gateContribution =
    liveness * CONFIG_BROKEN.gate_weights.liveness +
    timeline * CONFIG_BROKEN.gate_weights.timeline;

  const composite = voteSum + gateContribution; // additive, not multiplicative

  let rec;
  if (composite >= CONFIG_BROKEN.apply_threshold) rec = 'Apply';
  else if (composite >= CONFIG_BROKEN.consider_floor) rec = 'Consider';
  else rec = 'Skip';

  return {
    role_id: role.role_id ?? null,
    composite: Number(composite.toFixed(4)),
    recommendation: rec,
  };
}

export const CONFIG_BROKEN_EXPORT = CONFIG_BROKEN;
