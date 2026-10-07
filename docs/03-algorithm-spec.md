# 03 — Algorithm Spec

This is the most important file in this project. Everything here must match exactly what ends up in the implementation and the paper — if the implementation diverges from this spec, update this file in the same change, not after.

## Signals

| Signal | Symbol | Description | Measurement method |
|---|---|---|---|
| RTT | `RTT_p` | Smoothed round-trip time on path `p` | EWMA over recent ACKs (same style as TCP's SRTT) |
| Loss rate | `loss_p` | Recent packet loss ratio on path `p` | Sliding window of sent vs. acked packets |
| Bandwidth | `bw_p` | Estimated delivery rate on path `p` | ACK-based delivery rate, BBR-style estimation |
| Stability | `stability_p` | RTT variance/jitter on path `p` | Rolling standard deviation of RTT samples |
| Switch penalty | `switch_p` | Penalty proportional to recency of last switch to/from `p` | Counter reset on switch, decaying over time |

## Scoring function

```
score(p) = w1 * (1 / RTT_p) + w2 * (1 - loss_p) + w3 * bw_p - w4 * switch_p
```

- `w1, w2, w3, w4` are tunable weights. Initial values: TBD via grid search (see `06-experiment-log.md`) — do not hardcode arbitrary starting weights without logging them.
- All terms should be normalized (e.g., min-max or z-score across the current signal window) before weighting, so no single term dominates purely due to units. **This normalization step is easy to forget when vibe-coding — verify it's present.**

## Decision logic (with hysteresis)

```
On each scheduling decision (per stream, or per N packets):
    for each path p in {terrestrial, satellite}:
        compute score(p)

    chosen_path = argmax(score(p) for p in paths)

    if chosen_path != current_path:
        if score(chosen_path) - score(current_path) > threshold:
            switch to chosen_path
            reset switch_penalty for chosen_path
        else:
            stay on current_path
    else:
        stay on current_path
```

### Why hysteresis matters (do not remove this without re-justifying in the paper)
Without the `> threshold` check, the scheduler will oscillate whenever two paths have close scores under noisy conditions — this is the exact failure mode we are claiming to solve. The ablation in `06-experiment-log.md` must show throughput/latency with hysteresis on vs. off to justify this design choice.

## Edge cases (must be handled explicitly)

| Case | Expected behavior |
|---|---|
| Startup, no signal history yet | Default to a neutral score (e.g., equal weight, or prefer terrestrial as a safe default) until enough samples exist for a real EWMA |
| One path fails completely (100% loss) | Score should collapse toward the minimum and force a switch even if within the hysteresis threshold — a full failure should override hysteresis |
| Both paths score equally (tie) | Prefer `current_path` (avoids gratuitous switching on a coin flip) |
| Very short flow (fewer packets than the signal window) | Fall back to whatever signal is available; do not block sending while waiting for a full window |

## Weight tuning method
Grid search or coordinate sweep over `w1–w4` (see `06-experiment-log.md` for the actual runs and results). Document *why* the final weights were chosen, not just what they are — this becomes part of the paper's methodology section.

## What counts as "novel" here (for the paper's contribution framing)
- The specific combination of signals + normalized scoring is straightforward; the **hysteresis mechanism tuned for LEO-style variability** is the actual novel contribution. Keep implementation and evaluation focus there — don't let effort drift into polishing the scoring function at the expense of the hysteresis ablation.

## Rule for Antigravity
Do not modify the scoring function's structure (which signals, which sign) without flagging it for human review — weights can be tuned freely per `06-experiment-log.md`, but the functional form itself is a design decision that must trace back to a discussion, not a silent code change.
