# FileStructure.md

This file documents the repo layout so any AI coding agent (Antigravity or otherwise) puts new code in the right place instead of inventing its own structure. If you're about to create a file, check here first for where it belongs — and if nothing fits, that's a signal to flag it for human review rather than guessing.

## Full tree

```
QUIC-Flex/
├── docs/                         # Planning & spec docs — read these before writing code
│   ├── 01-problem.md             # What we're building, scope, definition of done
│   ├── 02-architecture.md        # Testbed + transport layer design decisions
│   ├── 03-algorithm-spec.md      # SOURCE OF TRUTH for the scheduler — scoring fn, hysteresis, edge cases
│   ├── 04-rules.md               # What's safe to vibe-code vs. needs human review, team ownership
│   ├── 05-phases.md              # 6-week plan with per-phase deliverables and exit criteria
│   ├── 06-experiment-log.md      # Running log of decisions, results, weight sweeps, pivots
│   ├── 07-paper-draft.md         # Draft of the paper
│   └── FileStructure.md          # This file
│
├── testbed/                      # Phase 1 — emulation layer
│   ├── topology.py               # Mininet/ns-3 two-path topology setup
│   ├── link-profiles/
│   │   ├── terrestrial.yaml      # Stable path parameters (low RTT, low loss)
│   │   └── leo-satellite.yaml    # Variable RTT + periodic loss/handover model
│   └── scripts/                  # One-off setup/teardown/debug scripts for the testbed
│
├── scheduler/                    # Phase 2 — the core contribution, matches 03-algorithm-spec.md exactly
│   ├── signals/
│   │   ├── rtt.py                # EWMA RTT measurement
│   │   ├── loss.py                # Sliding-window loss rate
│   │   ├── bandwidth.py           # ACK-based delivery rate estimate
│   │   └── stability.py           # RTT variance/jitter
│   ├── scoring.py                # score(p) = w1*(1/RTT) + w2*(1-loss) + w3*bw - w4*switch
│   ├── hysteresis.py             # Switch-decision logic + threshold
│   ├── scheduler.py              # Ties signals + scoring + hysteresis together, writes decision log
│   └── test_scheduler.py         # Unit tests for the scheduler
│
├── baselines/                    # Phase 3 — comparison schemes, kept separate from our scheduler
│   ├── single_path.py            # Terrestrial-only and satellite-only baselines
│   ├── round_robin.py            # Naive round-robin multipath baseline
│   └── mptcp/
│       └── README.md             # Setup notes/config for MPTCP comparison (OS-level, not a Python module)
│
├── evaluation/                   # Phase 3 — experiment orchestration
│   ├── run_experiment.py         # Runs a given scheme against a given link-profile config
│   ├── experiment_matrix.yaml    # Declares the full set of (scheme × link profile × seed) runs
│   └── logs/                     # Raw decision logs from experiment runs — gitignored, regenerable
│
├── analysis/                     # Phase 3–4 — turns raw logs into paper-ready results
│   ├── parse_logs.py             # Loads evaluation/logs/* into a common dataframe
│   ├── plots.py                  # Throughput/latency/switch-frequency figures
│   ├── weight_sweep.py           # Grid search over w1–w4, writes results into docs/06-experiment-log.md format
│   └── figures/                  # Generated plots, copied into paper/figures/ when finalized
│
├── paper/                        # Phase 4 — the actual submission
│   ├── main.tex
│   ├── refs.bib
│   ├── sections/                 # One .tex file per section (intro, related work, design, eval, conclusion)
│   └── figures/                  # Final figures used in the paper (copied from analysis/figures/)
│
├── README.md                     # Entry point — links out to docs/
├── adaptive-multipath-quic-project.md # Original project proposal
├── adaptive-multipath-quic-project.md.pdf # PDF of the proposal
└── .gitignore
```

## Where new code goes (quick rules)

| If you're writing... | It goes in... |
|---|---|
| Anything about link shaping, `tc`/`netem`, Mininet/ns-3 setup | `testbed/` |
| Anything touching the scoring function or hysteresis logic | `scheduler/` — and check `docs/03-algorithm-spec.md` first |
| A comparison scheme that isn't our scheduler | `baselines/` |
| Code that runs an experiment and produces logs | `evaluation/` |
| Code that reads logs and produces plots/tables | `analysis/` |
| Anything destined for the submission itself | `paper/` |
| A design decision, result, or pivot worth remembering | `docs/06-experiment-log.md` — not a code comment, not a Slack message |

## What should never live in code comments instead of `docs/`
- Why a particular weight value or threshold was chosen → `docs/06-experiment-log.md`
- Why a library or emulator was picked → `docs/02-architecture.md`
- A change to the scoring function's structure → must be reflected in `docs/03-algorithm-spec.md` in the same change

## Notes
- `evaluation/logs/` and `analysis/figures/` (generated content) are gitignored except for `.gitkeep` — don't hand-edit files there, regenerate them from `evaluation/run_experiment.py` and `analysis/plots.py`.
- `paper/figures/` is **not** gitignored — only finalized figures copied in deliberately for the submission belong there.
