from collections import deque

class LossSignal:
    def __init__(self, window_size=100):
        self.window_size = window_size
        self.history = deque(maxlen=window_size)
        self.losses = 0
        
    def update(self, is_lost):
        if len(self.history) == self.window_size:
            if self.history.popleft():
                self.losses -= 1
        self.history.append(is_lost)
        if is_lost:
            self.losses += 1
            
    def get_value(self):
        if not self.history:
            return 0.0
        return self.losses / len(self.history)
    
    @property
    def samples(self):
        return len(self.history)
