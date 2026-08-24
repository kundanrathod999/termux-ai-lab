import sys
from src.agents.ai_agent import AIAgent
from src.core.config import config
from src.core.logger import logger

def main():
    print("=" * 50)
    print("🚀 Welcome to Termux AI Lab!")
    print("=" * 50)
    print(f"Model: {config.DEFAULT_MODEL}")
    print("Type \x27exit\x27 or \x27quit\x27 to exit. Use \x27!run <command>\x27 for local shell execution.\n")

    agent = AIAgent(name="TermuxBot")

    while True:
        try:
            user_input = input("🤖 You > ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit", "q"]:
                print("\nGoodbye! 👋")
                break
            
            if user_input.startswith("!run "):
                cmd = user_input[5:].strip()
                res = agent.run_tool("execute_command", command=cmd)
                if res.get("stdout"):
                    print(f"\n[STDOUT]\n{res.get('stdout')}")
                if res.get("stderr"):
                    print(f"\n[STDERR]\n{res.get('stderr')}")
                print()
                continue

            response = agent.chat(user_input)
            print(f"\n🤖 TermuxBot > {response}\n")
        except KeyboardInterrupt:
            print("\n\nSession terminated. Goodbye! 👋")
            break
        except Exception as e:
            logger.error(f"Error in main loop: {e}")
            print(f"\n[Error] {e}\n")

if __name__ == "__main__":
    main()
