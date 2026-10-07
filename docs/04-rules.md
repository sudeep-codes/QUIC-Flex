# 04 — Rules

## What can be freely AI-generated ("vibe-coded")
- Emulation testbed boilerplate (Mininet/ns-3 topology setup, `tc`/`netem` link shaping scripts)
- Signal measurement plumbing (RTT/loss/bandwidth collection, EWMA smoothing) — standard, well-documented patterns
- Evaluation harness: experiment runner, baseline implementations (single-path, round-robin), logging
- Analysis scripts: parsing decision logs, computing metrics, generating plots
- Paper scaffolding: LaTeX structure, bibliography management, figure placement

## What must be human-designed and human-verified, line by line
- The scoring function's functional form and the hysteresis decision logic (`03-algorithm-spec.md`) — this is the paper's core claim; every team member must be able to explain it without notes
- The hysteresis threshold value and the reasoning behind it
- The LEO link emulation model (RTT/loss distribution over time) — must be grounded in published satellite network measurement studies, not arbitrary values invented by an LLM
- Any interpretation/claim in the paper about *why* a result occurred

## Hard rule
Never let an AI coding agent modify the scoring function's structure or the hysteresis logic without a human explicitly reviewing and approving the change. Tuning weight *values* is fine to iterate on freely (that's what the grid search is for) — changing which signals are used, their sign, or the switching condition is a design decision, not a bug fix.

## Library and tooling choices (pin these — do not let Antigravity silently swap them)
| Component | Locked choice | Notes |
|---|---|---|
| Emulator | Mininet (fallback: ns-3) | See `02-architecture.md` decision gate |
| QUIC library | TBD by end of Phase 1 | Once locked, treat as fixed for the rest of the project |
| Analysis | Python (pandas/matplotlib or seaborn) | Keep plots reproducible from the decision log CSV/JSON |

## Team split and ownership
| Member | Owns | Reviews |
|---|---|---|
| Member A | Emulation testbed, link modeling | Signal measurement accuracy |
| Member B | Core scheduling algorithm (scoring, hysteresis) | Evaluation methodology |
| Member C | Evaluation harness, baselines, analysis, paper writing coordination | Algorithm spec matches implementation |

Every phase deliverable (see `05-phases.md`) needs a named owner and at least one other member's review before being considered done — no single-person merges on the algorithm module.

## Working with Antigravity
- Point it at `01-problem.md` and `03-algorithm-spec.md` first for any task touching the scheduler.
- Point it at `02-architecture.md` for anything touching the testbed or QUIC integration.
- If a generated result contradicts something in `03-algorithm-spec.md`, that's a signal to stop and reconcile the spec and the code — not to silently accept whichever one Antigravity produced last.
- Log every significant design decision or pivot in `06-experiment-log.md`, even ones that happen inside a vibe-coding session — future you (and your faculty advisor) will ask why.

## Definition of "not vibe-coded" for this project
A reviewer or faculty member should be able to point at any line in the scheduler module and get a real explanation of why it's there — not "the AI wrote it that way." That's the actual bar, not whether AI assistance was used at all.
