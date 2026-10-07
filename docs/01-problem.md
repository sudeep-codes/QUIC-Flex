# 01 — Problem

## Context
Devices now commonly have access to more than one network path at once — e.g., terrestrial broadband and a LEO satellite link (Starlink-class). LEO links offer strong bandwidth but highly variable RTT and periodic loss caused by handovers and atmospheric effects. Existing multipath transport schedulers (MPTCP, naive multipath QUIC) use static path preference or round-robin selection, both of which perform poorly under this kind of variability.

## Problem statement
There is no lightweight, real-time path scheduler for multipath QUIC that is specifically designed to handle rapidly varying LEO-satellite-style link conditions without oscillating between paths.

## Our contribution
1. A real-time, per-path scoring function using RTT, loss rate, estimated bandwidth, and RTT stability.
2. A hysteresis mechanism that prevents path-switching oscillation ("thrashing") under noisy conditions.
3. An evaluation testbed emulating realistic LEO satellite link dynamics (variable RTT, periodic loss/handover events) alongside a stable terrestrial path, with a head-to-head comparison against existing scheduling approaches.

## Non-goals (explicitly out of scope)
- No learned/RL-based scheduler (Tier 3) — deliberately out of scope for a 6-week timeline. Do not let implementation drift toward this.
- No patent filing — this project targets a conference/workshop paper only.
- No production-grade QUIC client/server — the implementation only needs to be correct and instrumented enough to produce evaluation data, not deployment-ready.
- No mobile/real-device testing — emulated testbed only (Mininet or ns-3).

## Definition of done
The project is "done" when we have:
- A working scheduler implementation (scoring + hysteresis) running in the emulated testbed
- Comparative results (throughput, latency, path-switch frequency) against all baselines in `03-algorithm-spec.md`
- An ablation showing hysteresis on vs. off
- A weight-sensitivity result (grid search or sweep)
- A paper draft with these results written up, ready for submission to the target venue

## Target venue
Student/workshop track or a mid-tier IEEE conference (e.g., regional IEEE ICC/Globecom workshop, or a national-level student research symposium).

## Team
3 members. See `04-rules.md` for role/ownership split and `05-phases.md` for the week-by-week plan.

## Why this doc exists
Antigravity (or any AI coding agent) should treat this file as the single source of truth for *what we are building and why*. If a generated feature, test, or refactor doesn't trace back to something in this file, it's out of scope — flag it rather than building it.
