# 06 - Experiment Log

## Baselines & Ablation

| Config | Throughput (Mbps) | Avg Latency (ms) | p99 Latency (ms) | Path Switches |
|---|---|---|---|---|
| SinglePath (Terrestrial) | 60.39 | 223.14 | 500.00 | 0 |
| SinglePath (Satellite) | 49.04 | 52.63 | 59.92 | 0 |
| RoundRobin | 54.69 | 139.04 | 500.00 | 100 |
| Our Scheduler (No Hysteresis) | 68.34 | 52.40 | 500.00 | 2 |
| Our Scheduler (With Hysteresis) | 64.28 | 51.74 | 500.00 | 5 |

## Weight Sensitivity Sweep (w1=RTT, w2=Loss, w3=1, w4=1)

| w1 | w2 | Throughput (Mbps) | Avg Latency (ms) | p99 Latency (ms) | Path Switches |
|---|---|---|---|---|---|
| 0.5 | 0.5 | 60.39 | 224.77 | 500.00 | 0 |
| 0.5 | 1.0 | 66.82 | 52.50 | 500.00 | 6 |
| 0.5 | 2.0 | 64.26 | 48.88 | 59.96 | 1 |
| 1.0 | 0.5 | 66.97 | 78.08 | 500.00 | 6 |
| 1.0 | 1.0 | 66.34 | 57.01 | 500.00 | 6 |
| 1.0 | 2.0 | 64.26 | 48.15 | 59.51 | 1 |
| 2.0 | 0.5 | 67.84 | 51.83 | 500.00 | 6 |
| 2.0 | 1.0 | 63.78 | 53.69 | 500.00 | 3 |
| 2.0 | 2.0 | 64.28 | 51.35 | 500.00 | 3 |

**Best weights found:** w1=2.0, w2=0.5 (optimized for throughput)
