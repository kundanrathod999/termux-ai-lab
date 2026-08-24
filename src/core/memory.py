from typing import List, Dict, Any, Optional

class ConversationMemory:
    def __init__(self, max_turns: int = 20):
        self.max_turns = max_turns
        self.history: List[Dict[str, Any]] = []

    def add_user_message(self, content: str) -> None:
        self.history.append({"role": "user", "content": content})
        self._trim()

    def add_assistant_message(self, content: str, tool_calls: Optional[List[Dict[str, Any]]] = None) -> None:
        msg = {"role": "assistant", "content": content}
        if tool_calls:
            msg["tool_calls"] = tool_calls
        self.history.append(msg)
        self._trim()

    def add_tool_result(self, tool_name: str, result: Any) -> None:
        self.history.append({"role": "tool", "name": tool_name, "content": str(result)})
        self._trim()

    def get_history(self) -> List[Dict[str, Any]]:
        return list(self.history)

    def clear(self) -> None:
        self.history.clear()

    def _trim(self) -> None:
        if len(self.history) > self.max_turns * 2:
            self.history = self.history[-(self.max_turns * 2):]
