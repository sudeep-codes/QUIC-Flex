class HysteresisDecision:
    def __init__(self, threshold=0.1):
        self.threshold = threshold

    def decide(self, current_path, scores, loss_rates):
        """
        current_path: ID of the currently active path (can be None at startup)
        scores: dict mapping path_id to computed score
        loss_rates: dict mapping path_id to current loss rate
        """
        if not scores:
            return current_path

        # Handle complete failure edge case: 100% loss forces score to -inf
        for pid, loss in loss_rates.items():
            if loss >= 1.0:
                scores[pid] = float('-inf')

        # Startup: if no current_path, just pick argmax. 
        # (Tie breaking to terrestrial can be handled by just sorting keys or passing 'terrestrial' as default current_path)
        
        best_path = None
        best_score = float('-inf')
        
        # Find argmax. Tie breaking: prefer current_path if scores are equal.
        for pid, score in scores.items():
            if score > best_score:
                best_score = score
                best_path = pid
            elif score == best_score:
                if current_path and pid == current_path:
                    best_path = pid

        if current_path is None:
            return best_path

        # Hysteresis check
        if best_path != current_path:
            current_score = scores.get(current_path, float('-inf'))
            # If current path failed completely (score is -inf), force switch
            if current_score == float('-inf') or (best_score - current_score > self.threshold):
                return best_path
            else:
                return current_path
        else:
            return current_path
