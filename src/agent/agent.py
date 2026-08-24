from typing import List, Dict
from src.core.llm import llm_client
from src.core.logger import logger

class AIAgent:
    def __init__(self, name: str = "TermuxBot", tools: List[str] = None):
        self.name = name
        self.tool_names = tools or []
        self.history: List[Dict[str, str]] = []
        logger.info(f"Initialized agent: {self.name}")

    def run(self, user_input: str) -> str:
        try:
            self.history.append({"role": "user", "content": user_input})
            response = llm_client.generate(user_input)
            response_text = str(response)
            self.history.append({"role": "assistant", "content": response_text})
            return response_text
        except Exception as e:
            logger.error(f"Agent execution error: {e}")
            return f"[Error] {e}"

    def reset(self):
        self.history = []
