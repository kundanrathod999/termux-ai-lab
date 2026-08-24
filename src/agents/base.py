from typing import Dict, Any, Callable
from src.core.logger import logger
from src.tools.shell import execute_command
from src.tools.file_ops import read_file, write_file

class BaseAgent:
    def __init__(self, name: str = "TermuxAgent"):
        self.name = name
        self.tools: Dict[str, Callable] = {
            "execute_command": execute_command,
            "read_file": read_file,
            "write_file": write_file,
        }
        logger.info(f"Initialized agent: {self.name} with {len(self.tools)} tools")

    def run_tool(self, tool_name: str, **kwargs) -> Any:
        if tool_name not in self.tools:
            logger.error(f"Tool {tool_name} not found")
            return {"success": False, "error": f"Tool {tool_name} not found"}
        return self.tools[tool_name](**kwargs)
