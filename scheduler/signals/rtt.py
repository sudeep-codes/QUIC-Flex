class RTTSignal:
    def __init__(self, alpha=0.125):
        self.alpha = alpha
        self.srtt = None
        self.samples = 0
        
    def update(self, rtt_sample):
        self.samples += 1
        if self.srtt is None:
            self.srtt = rtt_sample
        else:
            self.srtt = (1 - self.alpha) * self.srtt + self.alpha * rtt_sample
            
    def get_value(self):
        return self.srtt
