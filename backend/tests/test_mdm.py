import unittest
import sys
import os
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from backend.app.services.mdm_service import MDMService

class TestMDMService(unittest.TestCase):
    def setUp(self):
        self.mdm_service = MDMService()

    @patch('subprocess.Popen')
    def test_execute_adb_command(self, mock_popen):
        mock_process = MagicMock()
        mock_process.communicate.return_value = ("Success", None)
        mock_process.returncode = 0
        mock_popen.return_value = mock_process
        result = self.mdm_service.execute_adb_command("ls")
        self.assertTrue(result["success"])

if __name__ == '__main__':
    unittest.main()
