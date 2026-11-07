import os
import tempfile
import unittest
from socialsuite.publishers import schedule

class SchedulerTests(unittest.TestCase):
    def test_requires_timezone(self):
        with tempfile.TemporaryDirectory() as tmp:
            os.environ["SOCIALSUITE_DB"] = os.path.join(tmp, "jobs.db")
            with self.assertRaises(ValueError): schedule("hello", "2026-12-01T10:00:00")
    def test_schedules_timezone_aware_job(self):
        with tempfile.TemporaryDirectory() as tmp:
            os.environ["SOCIALSUITE_DB"] = os.path.join(tmp, "jobs.db")
            result = schedule("hello", "2026-12-01T10:00:00+05:30")
            self.assertEqual(result["status"], "pending"); self.assertEqual(result["job_id"], 1)

if __name__ == "__main__": unittest.main()
