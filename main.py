import sys
from src.core.logger import logger
from src.agents.base import BaseAgent

def main():
    logger.info("Starting Termux AI Lab...")
    agent = BaseAgent(name="TermuxCLI")
    print("\n=== Termux AI Lab Interactive CLI ===")
    print("Type /help for options or /exit to quit.\n")
    while True:
        try:
            user_input = input("termux-ai > ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["/exit", "exit", "quit"]:
                print("Goodbye!")
                break
            elif user_input.lower() == "/help":
                print("Commands:\n  /exec <command>   - Execute shell command\n  /read <filepath>  - Read file\n  /exit             - Exit CLI")
            elif user_input.startswith("/exec "):
                res = agent.run_tool("execute_command", command=user_input[6:].strip())
                print(res.get("stdout") if res.get("success") else f"Error: {res.get('stderr')}")
            elif user_input.startswith("/read "):
                res = agent.run_tool("read_file", path=user_input[6:].strip())
                print(res.get("content") if res.get("success") else f"Error: {res.get('error')}")
            else:
                print("Unknown command. Type /help for assistance.")
        except (KeyboardInterrupt, EOFError):
            print("\nSession ended.")
            break

if __name__ == "__main__":
    main()
