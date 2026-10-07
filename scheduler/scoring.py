from collections import deque

class PathScorer:
    def __init__(self, w1=1.0, w2=1.0, w3=1.0, w4=1.0, window_size=20):
        self.w1 = w1
        self.w2 = w2
        self.w3 = w3
        self.w4 = w4
        self.window_size = window_size
        
        self.rtt_history = deque(maxlen=window_size)
        self.loss_history = deque(maxlen=window_size)
        self.bw_history = deque(maxlen=window_size)
        self.switch_history = deque(maxlen=window_size)

    def normalize(self, value, history):
        """Min-max normalization across the current signal window."""
        if not history:
            return 0.5
        min_v = min(history)
        max_v = max(history)
        if max_v == min_v:
            return 0.5
        return (value - min_v) / (max_v - min_v)

    def compute_scores(self, paths_data):
        """
        paths_data: dict mapping path_id to dict with keys: 'rtt', 'loss', 'bw', 'switch_penalty'
        """
        if not paths_data:
            return {}

        path_ids = list(paths_data.keys())
        
        # Add current values to history
        for pid in path_ids:
            rtt = paths_data[pid].get('rtt')
            if rtt is not None:
                self.rtt_history.append(1.0 / rtt if rtt > 0 else 1.0)
            self.loss_history.append(1.0 - paths_data[pid].get('loss', 0.0))
            self.bw_history.append(paths_data[pid].get('bw', 0.0))
            self.switch_history.append(paths_data[pid].get('switch_penalty', 0.0))

        scores = {}
        for pid in path_ids:
            rtt = paths_data[pid].get('rtt')
            inv_rtt = 1.0 / rtt if (rtt is not None and rtt > 0) else 1.0
            inv_loss = 1.0 - paths_data[pid].get('loss', 0.0)
            bw = paths_data[pid].get('bw', 0.0)
            switch = paths_data[pid].get('switch_penalty', 0.0)
            
            norm_rtt = self.normalize(inv_rtt, self.rtt_history)
            norm_loss = self.normalize(inv_loss, self.loss_history)
            norm_bw = self.normalize(bw, self.bw_history)
            norm_switch = self.normalize(switch, self.switch_history)

            score = (self.w1 * norm_rtt + 
                     self.w2 * norm_loss + 
                     self.w3 * norm_bw - 
                     self.w4 * norm_switch)
            scores[pid] = score
            
        return scores
