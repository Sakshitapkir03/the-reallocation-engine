# Domain Justification — Gate-Behavior Unit-Test Harness

**Student:** Sakshi Tapkir  
**Mode:** `recipes/gate-behavior-harness.md`  
**Lifecycle:** `RUNNABLE-SAMPLE`

This mode is for an international master's student or early-career technical worker using the Reallocation Engine to decide where limited application effort should go. The exact situation is a scorer change, refactor, or review where the student needs to know whether two high-stakes signals — posting liveness and visa/application timeline feasibility — still veto a role when they should. A person on a constrained search clock can lose meaningful time if a dead posting receives a confident `Apply` simply because sponsorship and role-fit scores are strong.

The information asymmetry is not only whether a company looks attractive; it is whether the decision system is honoring evidence that should make the opportunity non-actionable. A user cannot easily see from a final composite score whether a closed gate was treated as a veto or merely diluted as another weighted feature. The harness makes that hidden implementation behavior visible by testing the production scorer and then testing the same assertions against a deliberately broken gate-as-vote implementation.

The mode connects most directly to **Job-Ops**, because posting liveness is a Job-Ops gate: a ghost or expired posting should not consume application effort. It also touches the engine's timeline logic because an infeasible timeline is likewise a veto rather than a preference. The harness does not collect live ATS data itself; instead, it verifies that once verified liveness or timeline evidence reaches the scorer, the scorer respects the gate contract.

Two domain-specific failure modes matter most. **First, ghost-posting rescue:** `liveness=0` is accidentally treated as an additive vote, so high sponsorship and fit can produce `Apply`. The people who would struggle most to catch this are students who see only the polished recommendation and do not inspect scorer internals; they may assume the system already checked that the role is real. **Second, near-zero timeline rescue:** a timeline factor below the explicit gate threshold still leaves enough weighted score to appear actionable. This is hardest for users under immigration or recruiting deadlines, because the output can look mathematically reasonable while hiding that the opportunity is operationally impossible.

The mode deliberately stops short of claiming that a real posting is live, that a specific visa timeline is feasible, or that the scorer's weights are universally correct. Its purpose is narrower and auditable: prove that the current scorer preserves the gate behavior it claims to implement, and fail loudly when the named gate-as-vote bug is introduced.
