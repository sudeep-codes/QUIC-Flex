# 02 — Architecture

## System overview

```
┌─────────────────────────────────────────────────────────────┐
│                        Emulated Testbed                       │
│                                                                 │
│   ┌────────────┐        Path A (terrestrial)     ┌──────────┐ │
│   │            │ ───────────────────────────────▶ │          │ │
│   │  Client    │                                   │  Server  │ │
│   │  (QUIC +   │        Path B (LEO-emulated)      │  (QUIC)  │ │
│   │  Scheduler)│ ───────────────────────────────▶ │          │ │
│   └────────────┘                                   └──────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────┘
```

The client runs the adaptive scheduler. Two paths are exposed to it by the emulator, each with independently controllable RTT, loss, and bandwidth characteristics. The server is a stock QUIC endpoint — no scheduling logic lives there.

## Emulation layer

| Decision | Choice | Why |
|---|---|---|
| Emulator | Mininet (preferred) or ns-3 | Mininet is faster to get a working 2-path topology; ns-3 gives finer-grained control if Mininet's `tc`/`netem` proves too coarse for LEO-style variability |
| Link shaping | Linux `tc` + `netem` (if Mininet) | Standard, well-documented, supports variable delay/loss/rate distributions |
| LEO link model | Time-varying RTT + periodic loss bursts (handover events) | A static "high RTT, some loss" link does **not** capture the actual failure mode we're testing against — variability itself is the point |

**Do not** substitute a different emulator mid-project without updating this file — baseline comparisons only make sense if every run uses the same topology.

## Transport layer

| Decision | Choice | Why |
|---|---|---|
| Protocol | QUIC | Required by problem statement |
| Library | picoquic | Chosen for its robust, hookable multipath support and straightforward C API. |
| Fallback | ns-3's QUIC module | Lower integration risk than hacking into a production library's internals, at the cost of less "real" networking code |

**Decision gate:** spend no more than 2–3 days in Phase 1 evaluating library options before committing (see `05-phases.md`). If none has a clean extension point by then, default to the ns-3 fallback rather than losing a week to integration debugging.

## Scheduler module

Lives on the client. Responsibilities:
1. Measure RTT, loss rate, bandwidth per path (see `03-algorithm-spec.md` for exact signal definitions)
2. Compute a score per path on each scheduling decision
3. Apply hysteresis before switching
4. Log every decision (timestamp, signals, score, chosen path, switched y/n) — this log is the raw data for evaluation

## Data flow for evaluation

```
Run experiment → scheduler decision log (CSV/JSON) → analysis scripts → plots + tables → paper figures
```

Keep the decision log schema stable across all experiment runs (see `06-experiment-log.md`) so analysis scripts don't need per-run special-casing.

## What Antigravity should NOT change without flagging it
- The two-path topology shape (adding a third path changes every baseline comparison)
- The QUIC library choice once locked in Phase 1
- The decision log schema once evaluation scripts depend on it
