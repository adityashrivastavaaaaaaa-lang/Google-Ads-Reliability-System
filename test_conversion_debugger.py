import unittest
import tempfile
import os
import io
import sys
from unittest.mock import patch
from conversion_debugger import diagnose_drop

class TestConversionDebugger(unittest.TestCase):
    
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        
    def tearDown(self):
        self.test_dir.cleanup()

    def create_temp_csv(self, content):
        path = os.path.join(self.test_dir.name, 'test_data.csv')
        with open(path, 'w') as f:
            f.write(content)
        return path

    def test_diagnose_drop_tracking_issue(self):
        # Tracking tag issue: Clicks > 1000, Conversions < 5
        csv_content = """date,clicks,conversions
2025-01-01,1000,100
2025-01-02,1200,1
"""
        path = self.create_temp_csv(csv_content)
        
        captured_output = io.StringIO()
        with patch('sys.stdout', new=captured_output):
            diagnose_drop(path)
            
        output = captured_output.getvalue()
        self.assertIn("ALERT on 2025-01-02", output)
        self.assertIn("Tracking tag broken", output)

    def test_diagnose_drop_traffic_issue(self):
        # Traffic issue: Clicks drops significantly
        # Mean clicks = (1000 + 1000 + 100) / 3 = 700. 0.5 * 700 = 350.
        # Day 3 clicks 100 < 350 -> Traffic paused.
        # Also need conversion drop > 50%
        csv_content = """date,clicks,conversions
2025-01-01,1000,100
2025-01-02,1000,100
2025-01-03,100,2
"""
        path = self.create_temp_csv(csv_content)
        
        captured_output = io.StringIO()
        with patch('sys.stdout', new=captured_output):
            diagnose_drop(path)
            
        output = captured_output.getvalue()
        self.assertIn("ALERT on 2025-01-03", output)
        self.assertIn("Traffic source", output)

    def test_diagnose_drop_website_issue(self):
        # Website issue: Clicks normal, conversions drop but not to near zero
        # Mean clicks = 1000. 
        # Day 2: 1000 clicks. Conversions 100 -> 20. Drop 80%.
        csv_content = """date,clicks,conversions
2025-01-01,1000,100
2025-01-02,1000,20
"""
        path = self.create_temp_csv(csv_content)
        
        captured_output = io.StringIO()
        with patch('sys.stdout', new=captured_output):
            diagnose_drop(path)
            
        output = captured_output.getvalue()
        self.assertIn("ALERT on 2025-01-02", output)
        self.assertIn("Website or payment flow issue", output)

if __name__ == '__main__':
    unittest.main()
