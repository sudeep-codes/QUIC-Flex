# Adaptive Path-Scheduling for Multipath QUIC over Heterogeneous Terrestrial–Satellite Links

**Course:** Computer Networks
**Team size:** 3
**Target outcome:** Conference / workshop paper submission

---

## 1. Problem Statement

Modern devices increasingly have access to multiple network paths simultaneously — e.g., terrestrial broadband and LEO satellite links (Starlink-class). LEO satellite links offer good bandwidth but highly variable RTT and periodic loss due to handovers and atmospheric effects. Existing multipath transport approaches (MPTCP, naive multipath QUIC) either use static path preferences or round-robin scheduling, which perform poorly under such variability.

**Goal:** Design and evaluate an adaptive per-stream path-scheduling algorithm for multipath QUIC that dynamically selects between a terrestrial and a satellite-emulated path based on real-time link conditions, and demonstrate improved throughput/latency stability over existing scheduling approaches.

---

## 2. Contribution / Novelty

- A lightweight, real-time scoring-based path selection algorithm using RTT, loss rate, estimated bandwidth, and path stability.
- A hysteresis mechanism that prevents path-switching oscillation ("thrashing") under rapidly varying LEO-style link conditions — shown via ablation to be necessary, not just an add-on.
- An evaluation testbed emulating realistic LEO satellite link dynamics (variable RTT, periodic loss/handover events) alongside a stable terrestrial path.

---

## 3. Algorithm Design

### 3.1 Signals (inputs)
| Signal | Description | Measurement |
|---|---|---|
| RTT | Smoothed round-trip time per path | EWMA over recent ACKs |
| Loss rate | Recent packet loss ratio per path | Sliding window of sent/acked packets |
| Bandwidth | Estimated delivery rate per path | ACK-based delivery rate (BBR-style) |
| Stability | Variance/jitter in RTT | Rolling standard deviation |
| Switch cost | Penalty for recent path changes | Counter since last switch |

### 3.2 Scoring function
```
score(p) = w1 * (1 / RTT_p) + w2 * (1 - loss_p) + w3 * bandwidth_p - w4 * switch_penalty(p)
```

### 3.3 Decision logic with hysteresis
```
On each scheduling decision (per stream or per N packets):
    chosen_path = argmax(score(p) for p in paths)
    if chosen_path != current_path:
        if score(chosen_path) - score(current_path) > threshold:
            switch to chosen_path
        else:
            stay on current_path
```

The hysteresis threshold is the key design lever: too low and the scheduler thrashes between paths under noisy conditions; too high and it fails to adapt to genuine degradation. This trade-off is a central part of the evaluation.

---

## 4. Implementation Plan

**Tooling:** Mininet or ns-3 for network emulation; a QUIC implementation with hookable path/congestion logic (or ns-3's QUIC module) for the transport layer.

| Phase | Week(s) | Work |
|---|---|---|
| 1 | 1 | Build emulation testbed: terrestrial path + LEO-style variable-RTT/loss path |
| 2 | 2–3 | Implement scoring function, signal measurement, and hysteresis switching logic |
| 3 | 4–5 | Run full experiment matrix; compare against baselines |
| 4 | 6 | Write paper draft; finalize figures and ablations |

**Team split:**
- **Member A:** Emulation testbed — link modeling, variable RTT/loss profiles for the satellite path
- **Member B:** Core scheduling algorithm — signal measurement, scoring function, hysteresis logic
- **Member C:** Evaluation harness, baselines, statistical analysis, paper writing coordination

---

## 5. Evaluation Plan

**Baselines to compare against:**
- Single-path QUIC (terrestrial only)
- Single-path QUIC (satellite only)
- Naive round-robin multipath QUIC
- MPTCP (if feasible to set up)

**Metrics:**
- Throughput (goodput over time)
- Latency (RTT distribution, tail latency)
- Path-switch frequency (to demonstrate hysteresis effect)
- Loss recovery behavior during simulated satellite handover events

**Ablations:**
- With vs. without hysteresis
- Sensitivity of results to weight values (w1–w4), via grid search or sweep

---

## 6. Target Venue

Aim for a student/workshop track or a mid-tier IEEE conference (e.g., regional IEEE ICC/Globecom workshops, or a national-level student research symposium) — realistic acceptance bar for an undergraduate team.

---

## 7. Open Risks

- QUIC library internals (if using a real implementation instead of ns-3) can be poorly documented — budget extra time in Phase 2.
- LEO link emulation fidelity matters a lot for credible results — base the variable RTT/loss model on published satellite network measurement studies rather than arbitrary values.
- The 6-week timeline is tight — keep scope strictly to Tier 1 (scoring + hysteresis) rather than a learned/RL-based scheduler; a working simple algorithm beats an unfinished sophisticated one.
