# 06 - Experiment Log

## Baselines & Ablation

| Config | Throughput (Mbps) | Avg Latency (ms) | p99 Latency (ms) | Path Switches |
|---|---|---|---|---|
| SinglePath (Terrestrial) | 60.39 | 225.12 | 500.00 | 0 |
| SinglePath (Satellite) | 49.04 | 52.13 | 59.95 | 0 |
| RoundRobin | 54.69 | 138.30 | 500.00 | 100 |
| Our Scheduler (No Hysteresis) | 65.86 | 60.85 | 500.00 | 2 |
| Our Scheduler (With Hysteresis) | 66.34 | 57.40 | 500.00 | 6 |

## Weight Sensitivity Sweep (w1=RTT, w2=Loss, w3=1, w4=1)

| w1 | w2 | Throughput (Mbps) | Avg Latency (ms) | p99 Latency (ms) | Path Switches |
|---|---|---|---|---|---|
| 0.5 | 0.5 | 60.39 | 223.16 | 500.00 | 0 |
| 0.5 | 1.0 | 65.81 | 52.72 | 500.00 | 6 |
| 0.5 | 2.0 | 64.26 | 49.47 | 59.76 | 1 |
| 1.0 | 0.5 | 68.42 | 66.37 | 500.00 | 6 |
| 1.0 | 1.0 | 63.85 | 67.90 | 500.00 | 6 |
| 1.0 | 2.0 | 63.78 | 52.13 | 500.00 | 1 |
| 2.0 | 0.5 | 67.33 | 52.82 | 500.00 | 6 |
| 2.0 | 1.0 | 64.79 | 53.36 | 500.00 | 6 |
| 2.0 | 2.0 | 63.29 | 57.35 | 500.00 | 3 |

**Best weights found:** w1=1.0, w2=0.5 (optimized for throughput)
