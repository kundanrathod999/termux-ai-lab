import unittest
from src.agents.base import BaseAgent

class TestBaseAgent(unittest.TestCase):
    def setUp(self):
        self.agent = BaseAgent(name="TestAgent")

    def test_initialization(self):
        self.assertEqual(self.agent.name, "TestAgent")
        self.assertIn("execute_command", self.agent.tools)
        self.assertIn("read_file", self.agent.tools)
        self.assertIn("write_file", self.agent.tools)

    def test_run_tool(self):
        result = self.agent.run_tool("execute_command", command="echo agent test")
        self.assertTrue(result.get("success"))
        self.assertEqual(result.get("stdout"), "agent test")

    def test_unknown_tool(self):
        result = self.agent.run_tool("non_existent_tool")
        self.assertFalse(result.get("success"))

if __name__ == "__main__":
    unittest.main()
