# 05 — Phases

Six weeks, four phases. Each phase has a scoped deliverable — Antigravity sessions should stay within the current phase's scope rather than jumping ahead (e.g., don't start evaluation code during Phase 1).

## Phase 1 — Testbed (Week 1)
**Owner:** Sudeep Kumar Sahu
**Goal:** Working two-path emulated topology (terrestrial + LEO-style) with independently controllable RTT/loss/bandwidth.

**Deliverables:**
- [x] Mininet (or ns-3) topology with two paths between client and server
- [x] `tc`/`netem` (or equivalent) link shaping configured for both a stable terrestrial profile and a variable LEO profile (time-varying RTT, periodic loss bursts)
- [x] LEO link parameters grounded in published measurement data (Source: "A Multi-Faceted Look at Starlink Performance" by MacMillan et al., 2021)
- [x] QUIC library decision locked (see `02-architecture.md` decision gate) — do not enter Phase 2 without this resolved

**Exit criteria:** A basic QUIC flow can be sent over either path individually, with logged RTT/loss matching the intended profile.

## Phase 2 — Algorithm (Weeks 2–3)
**Owner:** Asmit Dutta
**Goal:** Working scheduler implementing the exact spec in `03-algorithm-spec.md`.

**Deliverables:**
- [x] Signal measurement (RTT EWMA, loss rate, bandwidth estimate, stability) per path
- [x] Scoring function implemented and normalized per spec
- [x] Hysteresis decision logic implemented
- [x] Edge cases from `03-algorithm-spec.md` handled and tested
- [x] Decision log output in the stable schema used by `02-architecture.md`

**Exit criteria:** Scheduler runs end-to-end in the testbed and produces a decision log for a full flow.

## Phase 3 — Evaluation (Weeks 4–5)
**Owner:** Agniva Chowdhury (with support from Sudeep Kumar Sahu and Asmit Dutta)
**Goal:** Full experiment matrix comparing the scheduler against baselines.

**Deliverables:**
- [x] Baselines implemented: single-path QUIC (terrestrial only), single-path QUIC (satellite only), round-robin multipath, MPTCP (if feasible)
- [x] Experiment matrix run across all baselines + our scheduler, same link conditions
- [x] Metrics computed: throughput, latency distribution, path-switch frequency, loss-recovery behavior during simulated handover events
- [x] Ablation: hysteresis on vs. off
- [x] Weight sensitivity sweep (grid search over `w1–w4`), logged in `06-experiment-log.md`

**Exit criteria:** All planned plots/tables exist and are reproducible from the decision logs.

## Phase 4 — Write-up (Week 6)
**Owner:** Agniva Chowdhury (all members contribute)
**Goal:** Paper draft ready for internal review and submission.

**Deliverables:**
- [x] Figures finalized from Phase 3 results
- [x] Methodology section matches `03-algorithm-spec.md` exactly
- [x] Ablation and sensitivity results written up with justification
- [x] Draft reviewed by all 3 members before submission

**Exit criteria:** Draft matches the definition of done in `01-problem.md`.

## Timeline discipline
The 6-week window is tight. If Phase 1 or 2 slips, cut evaluation scope (fewer baselines, smaller weight sweep) rather than compressing the write-up phase — an incomplete but honest evaluation is publishable; a rushed write-up on a good result usually isn't.
