class BandwidthSignal:
    def __init__(self, window_size=10):
        self.window_size = window_size
        self.rates = []
        
    def update(self, delivery_rate):
        self.rates.append(delivery_rate)
        if len(self.rates) > self.window_size:
            self.rates.pop(0)
            
    def get_value(self):
        if not self.rates:
            return 0.0
        return max(self.rates)
