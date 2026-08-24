import os
from pathlib import Path
from src.core.logger import logger

def read_file(path: str) -> dict:
    """Reads the content of a file safely."""
    try:
        p = Path(path).resolve()
        if not p.exists():
            return {"success": False, "content": "", "error": f"File not found: {path}"}
        return {"success": True, "content": p.read_text(encoding="utf-8"), "error": ""}
    except Exception as e:
        logger.error(f"Error reading file {path}: {e}")
        return {"success": False, "content": "", "error": str(e)}

def write_file(path: str, content: str) -> dict:
    """Writes content to a file, creating parent directories if needed."""
    try:
        p = Path(path).resolve()
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        logger.info(f"Successfully wrote to {path}")
        return {"success": True, "error": ""}
    except Exception as e:
        logger.error(f"Error writing file {path}: {e}")
        return {"success": False, "error": str(e)}
