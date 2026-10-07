import matplotlib.pyplot as plt
import numpy as np
import os

# Ensure the figures directory exists
output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'paper', 'figures')
os.makedirs(output_dir, exist_ok=True)

# Data from the paper draft
configs = ['SinglePath\n(Terrestrial)', 'SinglePath\n(Satellite)', 'RoundRobin', 'QUIC-Flex\n(Our Scheduler)']
throughput = [60.39, 49.04, 54.69, 64.28]
avg_latency = [223.14, 52.63, 139.04, 51.74]
path_switches = [0, 0, 100, 5]

# 1. Throughput Comparison Plot
plt.figure(figsize=(8, 5))
bars = plt.bar(configs, throughput, color=['#d3d3d3', '#d3d3d3', '#a9a9a9', '#4682b4'])
plt.ylabel('Throughput (Mbps)', fontsize=12)
plt.title('Throughput Comparison across Schedulers', fontsize=14)
plt.ylim(0, 80)
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 1, f"{yval:.2f}", ha='center', va='bottom', fontsize=10)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'throughput_comparison.pdf'))
plt.savefig(os.path.join(output_dir, 'throughput_comparison.png'))
plt.close()

# 2. Average Latency Comparison Plot
plt.figure(figsize=(8, 5))
bars = plt.bar(configs, avg_latency, color=['#d3d3d3', '#d3d3d3', '#a9a9a9', '#4682b4'])
plt.ylabel('Average Latency (ms)', fontsize=12)
plt.title('Average Latency Comparison', fontsize=14)
plt.ylim(0, 260)
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 3, f"{yval:.2f}", ha='center', va='bottom', fontsize=10)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'latency_comparison.pdf'))
plt.savefig(os.path.join(output_dir, 'latency_comparison.png'))
plt.close()

# 3. Hysteresis Ablation
ablation_configs = ['No Hysteresis', 'With Hysteresis\n(QUIC-Flex)']
ablation_tp = [68.34, 64.28]
ablation_lat = [52.40, 51.74]

fig, ax1 = plt.subplots(figsize=(6, 5))

color = 'tab:blue'
ax1.set_ylabel('Throughput (Mbps)', color=color, fontsize=12)
bars1 = ax1.bar([0, 1], ablation_tp, width=0.3, color=color, label='Throughput')
ax1.tick_params(axis='y', labelcolor=color)
ax1.set_ylim(0, 80)

ax2 = ax1.twinx()  
color = 'tab:red'
ax2.set_ylabel('Avg Latency (ms)', color=color, fontsize=12)
bars2 = ax2.bar([0.3, 1.3], ablation_lat, width=0.3, color=color, label='Latency')
ax2.tick_params(axis='y', labelcolor=color)
ax2.set_ylim(0, 60)

ax1.set_xticks([0.15, 1.15])
ax1.set_xticklabels(ablation_configs)

plt.title('Hysteresis Ablation: Throughput vs Latency', fontsize=14)
fig.tight_layout()
plt.savefig(os.path.join(output_dir, 'hysteresis_ablation.pdf'))
plt.savefig(os.path.join(output_dir, 'hysteresis_ablation.png'))
plt.close()

print(f"Generated plots in {output_dir}")
