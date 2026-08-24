import json
import urllib.request
import urllib.error
from typing import Dict, Any, Optional
from src.core.config import config
from src.core.logger import logger

class GeminiClient:
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or config.GEMINI_API_KEY
        self.model = model or config.DEFAULT_MODEL
        self.base_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"

    def generate(self, prompt: str) -> Dict[str, Any]:
        if not self.api_key:
            logger.error("GEMINI_API_KEY is not set.")
            return {"success": False, "error": "GEMINI_API_KEY is not set. Please add it to your .env file."}

        url = f"{self.base_url}?key={self.api_key}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})

        try:
            logger.info(f"Sending prompt to Gemini ({self.model})...")
            with urllib.request.urlopen(req, timeout=30) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                text = res_data["candidates"][0]["content"]["parts"][0]["text"]
                return {"success": True, "text": text, "raw": res_data}
        except urllib.error.HTTPError as e:
            err_msg = e.read().decode("utf-8")
            logger.error(f"Gemini API HTTPError: {e.code} - {err_msg}")
            return {"success": False, "error": f"HTTP {e.code}: {err_msg}"}
        except Exception as e:
            logger.error(f"Gemini API call failed: {str(e)}")
            return {"success": False, "error": str(e)}
