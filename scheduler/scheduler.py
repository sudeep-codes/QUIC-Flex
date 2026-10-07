import json
import time

from .signals.rtt import RTTSignal
from .signals.loss import LossSignal
from .signals.bandwidth import BandwidthSignal
from .signals.stability import StabilitySignal
from .scoring import PathScorer
from .hysteresis import HysteresisDecision

class PathState:
    def __init__(self, path_id):
        self.path_id = path_id
        self.rtt = RTTSignal()
        self.loss = LossSignal()
        self.bw = BandwidthSignal()
        self.stability = StabilitySignal()
        self.switch_penalty = 0.0
        
    def decay_penalty(self, decay_factor=0.9):
        """Decay the switch penalty over time/decisions."""
        self.switch_penalty *= decay_factor

class Scheduler:
    def __init__(self, w1=1.0, w2=1.0, w3=1.0, w4=1.0, threshold=0.1, log_file="decision_log.jsonl"):
        self.paths = {}
        self.current_path = None
        self.scorer = PathScorer(w1, w2, w3, w4)
        self.decision_logic = HysteresisDecision(threshold)
        self.log_file = log_file
        
    def add_path(self, path_id):
        self.paths[path_id] = PathState(path_id)
        if self.current_path is None:
            # Default to the first path added (edge case: startup)
            self.current_path = path_id 
            
    def update_signal(self, path_id, signal_type, value, timestamp=None):
        """
        signal_type: 'rtt', 'loss', 'bw'
        """
        if path_id not in self.paths:
            return
        p = self.paths[path_id]
        if signal_type == 'rtt':
            p.rtt.update(value)
            p.stability.update(value)
        elif signal_type == 'loss':
            # value should be boolean (True for lost, False for acked)
            p.loss.update(value)
        elif signal_type == 'bw':
            # value should be delivery rate
            p.bw.update(value)

    def make_decision(self):
        if not self.paths:
            return None

        paths_data = {}
        loss_rates = {}
        
        for pid, p in self.paths.items():
            # Decay penalty on each decision tick
            p.decay_penalty()
            
            paths_data[pid] = {
                'rtt': p.rtt.get_value(),
                'loss': p.loss.get_value(),
                'bw': p.bw.get_value(),
                'switch_penalty': p.switch_penalty
            }
            
            # Loss tracking for 100% loss edge case
            # Only consider it 100% loss if we actually have samples
            if p.loss.samples > 0:
                loss_rates[pid] = p.loss.get_value()
            else:
                loss_rates[pid] = 0.0
                
        scores = self.scorer.compute_scores(paths_data)
        
        # Decide next path
        chosen_path = self.decision_logic.decide(self.current_path, scores, loss_rates)
        
        switched = False
        if chosen_path != self.current_path:
            switched = True
            # Reset switch penalty for chosen path
            if chosen_path in self.paths:
                self.paths[chosen_path].switch_penalty = 1.0
            self.current_path = chosen_path
            
        self.log_decision(scores, switched)
        return self.current_path

    def log_decision(self, scores, switched):
        """Log decision in stable JSON schema for architecture evaluation."""
        log_entry = {
            "timestamp": time.time(),
            "paths": {},
            "scores": scores,
            "chosen_path": self.current_path,
            "switched": switched
        }
        for pid, p in self.paths.items():
            log_entry["paths"][pid] = {
                "rtt": p.rtt.get_value(),
                "loss": p.loss.get_value(),
                "bw": p.bw.get_value(),
                "stability": p.stability.get_value(),
                "switch_penalty": p.switch_penalty
            }
        
        with open(self.log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
