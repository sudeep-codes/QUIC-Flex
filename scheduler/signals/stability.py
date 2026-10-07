from collections import deque
import statistics

class StabilitySignal:
    def __init__(self, window_size=20):
        self.window_size = window_size
        self.rtt_history = deque(maxlen=window_size)
        
    def update(self, rtt_sample):
        self.rtt_history.append(rtt_sample)
        
    def get_value(self):
        if len(self.rtt_history) < 2:
            return 0.0
        return statistics.stdev(self.rtt_history)
