import unittest
import os
from scheduler.scheduler import Scheduler

class TestScheduler(unittest.TestCase):
    def setUp(self):
        self.log_file = "test_log.jsonl"
        if os.path.exists(self.log_file):
            os.remove(self.log_file)
            
        self.scheduler = Scheduler(w1=1.0, w2=1.0, w3=1.0, w4=1.0, threshold=0.1, log_file=self.log_file)
        self.scheduler.add_path("terrestrial")
        self.scheduler.add_path("satellite")
        
    def tearDown(self):
        if os.path.exists(self.log_file):
            os.remove(self.log_file)

    def test_startup_edge_case(self):
        # Startup, no signal history yet -> should stay on terrestrial (default first path)
        decision = self.scheduler.make_decision()
        self.assertEqual(decision, "terrestrial")

    def test_complete_failure_edge_case(self):
        # One path fails completely (100% loss)
        self.scheduler.current_path = "terrestrial"
        # Simulate 100% loss on terrestrial
        self.scheduler.update_signal("terrestrial", "loss", True)
        self.scheduler.update_signal("terrestrial", "loss", True)
        
        # Satellite is perfect
        self.scheduler.update_signal("satellite", "loss", False)
        
        decision = self.scheduler.make_decision()
        self.assertEqual(decision, "satellite")
        
    def test_tie_edge_case(self):
        # Both paths score equally, should prefer current_path
        self.scheduler.current_path = "satellite"
        
        # Give them identical signals
        for pid in ["terrestrial", "satellite"]:
            self.scheduler.update_signal(pid, "rtt", 50.0)
            self.scheduler.update_signal(pid, "loss", False)
            self.scheduler.update_signal(pid, "bw", 1000)
            
        decision = self.scheduler.make_decision()
        self.assertEqual(decision, "satellite")

    def test_hysteresis(self):
        # Build some history so min/max bounds are wide
        self.scheduler.update_signal("terrestrial", "rtt", 100.0)
        self.scheduler.update_signal("satellite", "rtt", 100.0)
        self.scheduler.make_decision()
        
        for _ in range(10):
            self.scheduler.update_signal("terrestrial", "rtt", 50.0)
            self.scheduler.update_signal("satellite", "rtt", 50.0)
            self.scheduler.make_decision()
            
        # Now both paths are at 50 RTT and the current path is whatever won (tie breaker keeps it stable)
        current = self.scheduler.current_path
        other = "satellite" if current == "terrestrial" else "terrestrial"
        
        # Make current path slightly worse, but not enough to overcome threshold
        self.scheduler.update_signal(current, "rtt", 52.0)
        
        decision = self.scheduler.make_decision()
        self.assertEqual(decision, current)
        
        # Make current path much worse, past threshold
        self.scheduler.update_signal(current, "rtt", 200.0)
        
        decision = self.scheduler.make_decision()
        self.assertEqual(decision, other)

if __name__ == '__main__':
    unittest.main()
