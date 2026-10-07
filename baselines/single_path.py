import json
import time

class SinglePathScheduler:
    def __init__(self, target_path, log_file="decision_log.jsonl"):
        self.target_path = target_path
        self.paths = {}
        self.current_path = target_path
        self.log_file = log_file

    def add_path(self, path_id):
        self.paths[path_id] = True
        
    def update_signal(self, path_id, signal_type, value, timestamp=None):
        pass

    def make_decision(self):
        switched = False
        if self.current_path != self.target_path:
            switched = True
            self.current_path = self.target_path
        
        self.log_decision(switched)
        return self.current_path

    def log_decision(self, switched):
        log_entry = {
            "timestamp": time.time(),
            "paths": {},
            "scores": {},
            "chosen_path": self.current_path,
            "switched": switched,
            "baseline": f"single_path_{self.target_path}"
        }
        with open(self.log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
