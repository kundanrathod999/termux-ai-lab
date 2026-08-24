import json
from typing import Dict, Any, Optional
from src.agents.base import BaseAgent
from src.core.llm import GeminiClient
from src.core.memory import ConversationMemory
from src.core.logger import logger

class AIAgent(BaseAgent):
    def __init__(self, name: str = "TermuxAIAgent", api_key: Optional[str] = None, model: Optional[str] = None):
        super().__init__(name=name)
        self.llm = GeminiClient(api_key=api_key, model=model)
        self.memory = ConversationMemory()
        self.system_prompt = (
            f"You are {self.name}, an intelligent assistant running inside Termux on Android.\n"
            f"You have access to the following local tools: {list(self.tools.keys())}.\n"
            "Be concise, practical, and helpful."
        )

    def chat(self, user_input: str) -> str:
        self.memory.add_user_message(user_input)
        prompt = f"{self.system_prompt}\n\nUser: {user_input}\nAssistant:"
        
        response = self.llm.generate(prompt)
        if not response.get("success"):
            err = response.get("error", "Unknown error")
            return f"[Error] {err}"

        reply = response.get("text", "").strip()
        self.memory.add_assistant_message(reply)
        return reply
