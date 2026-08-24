import sys
import os

# Ensure current project directory is in python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.core.config import config
from src.agent.agent import AIAgent

def main():
    print("=" * 50)
    print("🚀 Welcome to Termux AI Lab!")
    print("=" * 50)
    print(f"Provider: {config.PROVIDER.upper()} | Model: {config.MODEL}")
    print("Type 'exit' or 'quit' to exit.")
    print("-" * 50)

    agent = AIAgent(name="TermuxBot")

    while True:
        try:
            user_input = input("\n🤖 You > ").strip()
            if not user_input:
                continue
            if user_input.lower() in ("exit", "quit"):
                print("Goodbye! 👋")
                break
            
            response = agent.run(user_input)
            print(f"\n🤖 TermuxBot > {response}")
        except KeyboardInterrupt:
            print("\nSession stopped.")
            break
        except Exception as e:
            print(f"\n[Error] {e}")

if __name__ == "__main__":
    main()
