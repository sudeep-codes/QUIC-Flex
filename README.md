# Adaptive Path-Scheduling for Multipath QUIC over Terrestrial–Satellite Links

Computer Networks team project (3 members). See `docs/01-problem.md` for the full problem statement and `FileStructure.md` for how this repo is organized.

## Quick links
- Problem & scope: `docs/01-problem.md`
- Architecture: `docs/02-architecture.md`
- Algorithm spec (source of truth for the scheduler): `docs/03-algorithm-spec.md`
- Rules / what's safe to vibe-code: `docs/04-rules.md`
- Phase plan: `docs/05-phases.md`
- Experiment log: `docs/06-experiment-log.md`

## Status
- [x] Phase 1 (testbed) — completed. Mininet setup with "terrestrial" and "satellite" links, configurable RTT/loss/bandwidth.
- [x] Phase 2 (algorithm) — completed. Working scheduler implementation with signal tracking, scoring, hysteresis.
- [x] Phase 3 (evaluation) — completed. Baselines (single-path, round-robin) and our scheduler compared under identical simulated conditions.
- [x] Phase 4 (write-up) — completed. Paper-style figures and draft materials ready.

**Result:** The scheduler improves throughput and reduces path switches compared to baselines, especially during handovers. See `paper/` for final figures and experiment summaries.
