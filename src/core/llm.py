import json
import urllib.request
import urllib.error
import ssl
import os
import traceback
from typing import List, Dict, Any, Union
from src.core.config import config
from src.core.logger import logger

ctx = ssl.create_default_context()

class LLMResponse(str):
    def __new__(cls, content: str, raw: dict = None):
        obj = super().__new__(cls, str(content) if content is not None else "")
        obj.raw = raw or {}
        obj.text = str(content) if content is not None else ""
        obj.content = str(content) if content is not None else ""
        return obj

    def get(self, key, default=None):
        if key in ("text", "content", "response"):
            return str(self)
        if isinstance(self.raw, dict):
            return self.raw.get(key, default)
        return default

    def __getitem__(self, item):
        if item in ("text", "content", "response"):
            return str(self)
        if isinstance(self.raw, dict) and item in self.raw:
            return self.raw[item]
        return str(self)

class LLMClient:
    def __init__(self, provider=None, model=None, api_key=None, timeout=60, **kwargs):
        self.provider = (provider or getattr(config, "PROVIDER", None) or os.getenv("AI_PROVIDER", "you")).lower()
        self.model = model or getattr(config, "MODEL", None) or "you-answer"
        self.api_key = api_key
        self.timeout = timeout

    def generate(self, prompt: Any = "", system_instruction: str = "", **kwargs) -> LLMResponse:
        return self.generate_response(prompt, system_instruction=system_instruction, **kwargs)

    def chat(self, prompt: Any = "", **kwargs) -> LLMResponse:
        return self.generate_response(prompt, **kwargs)

    def generate_response(self, messages: Any, system_instruction: str = "", **kwargs) -> LLMResponse:
        # Extract query text safely
        query_text = ""
        if isinstance(messages, str):
            query_text = messages
        elif isinstance(messages, list) and len(messages) > 0:
            last = messages[-1]
            if isinstance(last, dict):
                query_text = last.get("content") or last.get("text") or str(last)
            else:
                query_text = str(last)
        elif isinstance(messages, dict):
            query_text = messages.get("content") or messages.get("text") or str(messages)
        else:
            query_text = str(messages)

        key = (
            self.api_key
            or os.getenv("YOU_API_KEY")
            or os.getenv("YOU_KEY")
            or getattr(config, "YOU_API_KEY", None)
            or (config.get_api_key(self.provider) if hasattr(config, "get_api_key") else None)
        )

        if not key:
            err = "YOU_API_KEY not found. Check your .env file."
            logger.error(err)
            return LLMResponse(f"[Error] {err}")

        logger.info(f"Sending request to {self.provider.upper()} API...")

        try:
            url = "https://api.you.com/v1/answer"
            payload = json.dumps({"query": query_text}).encode("utf-8")
            headers = {
                "Authorization": f"Bearer {key.strip()}",
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 Chrome/125.0 Mobile Safari/537.36"
            }
            
            req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=self.timeout, context=ctx) as resp:
                res_data = json.loads(resp.read().decode("utf-8"))
                ans = res_data.get("answer") or res_data.get("result") or json.dumps(res_data, indent=2)
                return LLMResponse(ans, raw=res_data)

        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            logger.error(f"HTTP {e.code}: {body}")
            return LLMResponse(f"[Error] HTTP {e.code}: {body}")
        except urllib.error.URLError as e:
            logger.error(f"Network error: {e.reason}")
            return LLMResponse(f"[Error] Network connection failed: {e.reason}")
        except Exception as e:
            logger.error(f"Unexpected error: {traceback.format_exc()}")
            return LLMResponse(f"[Error] {str(e)}")

llm_client = LLMClient()
GeminiClient = LLMClient
gemini_client = llm_client
