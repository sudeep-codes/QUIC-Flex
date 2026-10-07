import yaml
import sys
import os
import random
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scheduler.scheduler import Scheduler
from baselines.single_path import SinglePathScheduler
from baselines.round_robin import RoundRobinScheduler

def load_profile(name):
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'testbed', 'link-profiles', f'{name}.yaml')
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def run_simulation(scheduler, terr_profile, leo_profile, duration=100, handover_at=50):
    """
    Runs a simple discrete time simulation.
    duration in arbitrary decision ticks.
    """
    switches = 0
    total_latency = []
    total_delivered = 0
    
    # Initialize scheduler
    scheduler.add_path('terrestrial')
    scheduler.add_path('satellite')
    
    for tick in range(duration):
        # Simulate terrestrial (with intermittent failure/high noise to trigger switches)
        if tick >= 30 and tick < 70:
            terr_loss = 99.0 # basically total failure
            terr_rtt = 500.0
        else:
            # Introduce high jitter that might occasionally make it look worse than satellite
            terr_rtt = terr_profile.get('delay', 20) + random.uniform(0, 40)
            terr_loss = terr_profile.get('loss', 0.01)
        terr_bw = terr_profile.get('bandwidth', 100)
        
        # Simulate satellite (with handover)
        is_handover = (tick >= handover_at and tick < handover_at + (leo_profile.get('handover_duration', 500) / 100))
        
        leo_rtt = leo_profile.get('delay', 45) + random.uniform(0, leo_profile.get('jitter', 15))
        leo_loss = leo_profile.get('handover_loss', 10) if is_handover else leo_profile.get('loss', 1.5)
        leo_loss = float(leo_loss) / 100.0 # Convert % to ratio
        leo_bw = leo_profile.get('bandwidth', 50)
        
        # Feed signals
        scheduler.update_signal('terrestrial', 'rtt', terr_rtt)
        scheduler.update_signal('terrestrial', 'loss', random.random() < float(terr_loss) / 100.0)
        scheduler.update_signal('terrestrial', 'bw', terr_bw)
        
        scheduler.update_signal('satellite', 'rtt', leo_rtt)
        scheduler.update_signal('satellite', 'loss', random.random() < leo_loss)
        scheduler.update_signal('satellite', 'bw', leo_bw)
        
        prev_path = getattr(scheduler, 'current_path', None)
        chosen = scheduler.make_decision()
        
        if prev_path != chosen and prev_path is not None:
            switches += 1
            
        # Record metrics based on chosen path
        if chosen == 'terrestrial':
            total_latency.append(terr_rtt)
            total_delivered += terr_bw * (1 - float(terr_loss) / 100.0)
        else:
            total_latency.append(leo_rtt)
            total_delivered += leo_bw * (1 - leo_loss)
            
    avg_latency = sum(total_latency) / len(total_latency) if total_latency else 0
    p99_latency = sorted(total_latency)[int(len(total_latency) * 0.99)] if len(total_latency) >= 100 else max(total_latency)
    
    return {
        'throughput': total_delivered / duration,
        'avg_latency': avg_latency,
        'p99_latency': p99_latency,
        'switches': switches
    }

def main():
    terr = load_profile('terrestrial')
    leo = load_profile('leo-satellite')
    
    results = {}
    
    # 1. Baselines
    print("Running baselines...")
    sp_terr = SinglePathScheduler('terrestrial', log_file='evaluation/logs/single_path_terr.jsonl')
    results['SinglePath (Terrestrial)'] = run_simulation(sp_terr, terr, leo)
    
    sp_sat = SinglePathScheduler('satellite', log_file='evaluation/logs/single_path_sat.jsonl')
    results['SinglePath (Satellite)'] = run_simulation(sp_sat, terr, leo)
    
    rr = RoundRobinScheduler(log_file='evaluation/logs/round_robin.jsonl')
    results['RoundRobin'] = run_simulation(rr, terr, leo)
    
    # 2. Ablation: Hysteresis on vs off
    print("Running ablation...")
    sched_no_hyst = Scheduler(w1=1, w2=1, w3=1, w4=0, threshold=0.0, log_file='evaluation/logs/no_hysteresis.jsonl')
    results['Our Scheduler (No Hysteresis)'] = run_simulation(sched_no_hyst, terr, leo)
    
    sched_hyst = Scheduler(w1=1, w2=1, w3=1, w4=1, threshold=0.1, log_file='evaluation/logs/with_hysteresis.jsonl')
    results['Our Scheduler (With Hysteresis)'] = run_simulation(sched_hyst, terr, leo)
    
    # 3. Weight sensitivity sweep
    print("Running weight sweep...")
    best_throughput = 0
    best_weights = None
    
    sweep_results = []
    
    for w1 in [0.5, 1.0, 2.0]:
        for w2 in [0.5, 1.0, 2.0]:
            sched = Scheduler(w1=w1, w2=w2, w3=1, w4=1, threshold=0.1, log_file=f'evaluation/logs/sweep_{w1}_{w2}.jsonl')
            res = run_simulation(sched, terr, leo)
            sweep_results.append((w1, w2, res))
            if res['throughput'] > best_throughput:
                best_throughput = res['throughput']
                best_weights = (w1, w2)
                
    # Generate 06-experiment-log.md
    log_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'docs', '06-experiment-log.md')
    with open(log_path, 'w') as f:
        f.write("# 06 - Experiment Log\n\n")
        f.write("## Baselines & Ablation\n\n")
        f.write("| Config | Throughput (Mbps) | Avg Latency (ms) | p99 Latency (ms) | Path Switches |\n")
        f.write("|---|---|---|---|---|\n")
        
        for name, metrics in results.items():
            f.write(f"| {name} | {metrics['throughput']:.2f} | {metrics['avg_latency']:.2f} | {metrics['p99_latency']:.2f} | {metrics['switches']} |\n")
            
        f.write("\n## Weight Sensitivity Sweep (w1=RTT, w2=Loss, w3=1, w4=1)\n\n")
        f.write("| w1 | w2 | Throughput (Mbps) | Avg Latency (ms) | p99 Latency (ms) | Path Switches |\n")
        f.write("|---|---|---|---|---|---|\n")
        
        for w1, w2, res in sweep_results:
            f.write(f"| {w1} | {w2} | {res['throughput']:.2f} | {res['avg_latency']:.2f} | {res['p99_latency']:.2f} | {res['switches']} |\n")
            
        f.write(f"\n**Best weights found:** w1={best_weights[0]}, w2={best_weights[1]} (optimized for throughput)\n")
        
    print(f"Done. Wrote results to {log_path}")

if __name__ == '__main__':
    os.makedirs('evaluation/logs', exist_ok=True)
    main()
