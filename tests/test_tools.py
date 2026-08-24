import unittest
import os
from src.tools.shell import execute_command
from src.tools.file_ops import write_file, read_file

class TestTools(unittest.TestCase):
    def test_execute_command(self):
        res = execute_command("echo hello")
        self.assertTrue(res["success"])
        self.assertEqual(res["stdout"], "hello")

    def test_file_ops(self):
        test_file = "tests/temp_test.txt"
        write_res = write_file(test_file, "sample data")
        self.assertTrue(write_res["success"])
        read_res = read_file(test_file)
        self.assertTrue(read_res["success"])
        self.assertEqual(read_res["content"], "sample data")
        if os.path.exists(test_file):
            os.remove(test_file)

if __name__ == "__main__":
    unittest.main()
