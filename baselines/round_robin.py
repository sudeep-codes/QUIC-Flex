import json
import time

class RoundRobinScheduler:
    def __init__(self, log_file="decision_log.jsonl"):
        self.paths = []
        self.current_index = 0
        self.current_path = None
        self.log_file = log_file

    def add_path(self, path_id):
        if path_id not in self.paths:
            self.paths.append(path_id)
        if self.current_path is None:
            self.current_path = path_id
            
    def update_signal(self, path_id, signal_type, value, timestamp=None):
        pass

    def make_decision(self):
        if not self.paths:
            return None
            
        self.current_index = (self.current_index + 1) % len(self.paths)
        chosen_path = self.paths[self.current_index]
        
        switched = (chosen_path != self.current_path)
        self.current_path = chosen_path
        
        self.log_decision(switched)
        return self.current_path

    def log_decision(self, switched):
        log_entry = {
            "timestamp": time.time(),
            "paths": {},
            "scores": {},
            "chosen_path": self.current_path,
            "switched": switched,
            "baseline": "round_robin"
        }
        with open(self.log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
