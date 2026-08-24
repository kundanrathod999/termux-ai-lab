# 📱 Termux AI Lab

A lightweight, zero-dependency AI Agent and Automation framework designed specifically to run natively inside **Termux on Android**.

---

## 🌟 Key Features

- **Native & Ultra-Lightweight:** Runs on pure Python standard library modules without bulky heavy dependencies.
- **LLM Integration:** Powered by Google Gemini API (`gemini-2.5-flash`).
- **Autonomous Tool Execution:** Direct execution of shell commands, file reading, and writing.
- **Context Management:** Built-in sliding-window conversation memory.
- **Robust Logging:** Timed, structured logging to both terminal and `logs/termux_ai.log`.

---

## 📁 Project Structure

```text
termux-ai-lab/
├── main.py              # CLI Interactive Entry Point
├── requirements.txt     # Dependency definitions
├── tests/
│   └── test_core.py     # Automated test suite
└── src/
    ├── core/
    │   ├── config.py    # Environment & app configuration
    │   ├── logger.py    # Colorized logger setup
    │   ├── memory.py    # Conversation history tracker
    │   └── llm.py       # Gemini API client
    ├── tools/
    │   ├── base.py      # Base Tool class & registry
    │   └── system.py    # Shell & filesystem tools
    └── agents/
        ├── base.py      # Base Agent abstraction
        └── ai_agent.py  # LLM-powered interactive agent
```

---

## 🚀 Quick Setup & Run

### 1. Set API Key
```bash
echo "GEMINI_API_KEY=your_actual_gemini_api_key" > .env
```

### 2. Run Test Suite
```bash
python -m unittest tests/test_core.py
```

### 3. Launch Interactive Assistant
```bash
python main.py
```
