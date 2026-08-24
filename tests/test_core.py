import unittest
from src.core.config import config
from src.core.memory import ConversationMemory
from src.agents.ai_agent import AIAgent

class TestTermuxAILab(unittest.TestCase):
    def test_config(self):
        self.assertEqual(config.DEFAULT_MODEL, "gemini-2.5-flash")

    def test_memory(self):
        mem = ConversationMemory(max_turns=2)
        mem.add_user_message("hello")
        mem.add_assistant_message("hi there")
        self.assertEqual(len(mem.get_history()), 2)

    def test_agent_tools(self):
        agent = AIAgent(name="TestAgent")
        res = agent.run_tool("execute_command", command="echo hello_termux")
        self.assertTrue(res["success"])
        self.assertIn("hello_termux", res["stdout"])

if __name__ == "__main__":
    unittest.main()
