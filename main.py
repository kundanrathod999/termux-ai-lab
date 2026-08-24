import sys
import os
import subprocess
import time
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.text import Text
from rich.table import Table
from rich.align import Align
from rich.rule import Rule

from src.core.config import config
from src.agent.agent import AIAgent

console = Console()

def show_welcome_banner():
    console.clear()
    
    # Compact, high-contrast Cyberpunk Header for mobile
    banner_text = Text()
    banner_text.append("⚡ ", style="bold yellow")
    banner_text.append("TERMUX AI LAB", style="bold cyan")
    banner_text.append(" // ", style="dim bright_blue")
    banner_text.append("NEXT-GEN WORKBENCH", style="bold magenta")
    
    console.print()
    console.print(Align.center(banner_text))
    console.print()

    # Mobile-friendly 2-column compact info grid
    grid = Table.grid(expand=True, padding=(0, 1))
    grid.add_column(justify="left", ratio=1)
    grid.add_column(justify="right", ratio=1)

    grid.add_row(
        "[bold cyan]⚡ Engine:[/bold cyan] [bold white]" + config.PROVIDER.upper() + "[/bold white]",
        "[bold green]● Status:[/bold green] [bold white]ONLINE[/bold white]"
    )
    grid.add_row(
        "[bold cyan]🌐 Model:[/bold cyan] [dim white]" + config.MODEL + "[/dim white]",
        "[bold yellow]⏰ Time:[/bold yellow] [dim white]" + datetime.now().strftime("%H:%M") + "[/dim white]"
    )

    info_panel = Panel(
        grid,
        border_style="bright_blue",
        title="[bold green] SYSTEM STATUS [/bold green]",
        subtitle="[dim]exit • clear • !<command>[/dim]",
        padding=(0, 1)
    )
    console.print(info_panel)
    console.print()

def execute_shell(command: str):
    console.print(f"\n[bold yellow]⚡ Shell Execution:[/bold yellow] [bold cyan]{command}[/bold cyan]")
    try:
        start_t = time.time()
        res = subprocess.run(command, shell=True, capture_output=True, text=True)
        dur = round(time.time() - start_t, 2)
        
        if res.stdout:
            console.print(Panel(res.stdout.strip(), title=f"[green]STDOUT ({dur}s)[/green]", border_style="green", padding=(0, 1)))
        if res.stderr:
            console.print(Panel(res.stderr.strip(), title=f"[red]STDERR ({dur}s)[/red]", border_style="red", padding=(0, 1)))
        if not res.stdout and not res.stderr:
            console.print("[dim green]✔ Done (no output)[/dim green]")
    except Exception as e:
        console.print(f"[bold red]Execution Error:[/bold red] {e}")

def main():
    show_welcome_banner()
    agent = AIAgent(name="TermuxBot")

    while True:
        try:
            # Clean Cyberpunk Dual-line Prompt
            console.print("[dim bright_blue]╭─[/dim bright_blue] [bold cyan]TermuxLab[/bold cyan] [dim]@[/dim] [bold magenta]" + config.PROVIDER.upper() + "[/bold magenta]")
            user_input = console.input("[dim bright_blue]╰─❯[/dim bright_blue] [bold white]").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ("exit", "quit", "q"):
                console.print("\n[bold magenta]✨ Session closed. Goodbye![/bold magenta] 👋\n")
                break
                
            if user_input.lower() in ("clear", "cls"):
                show_welcome_banner()
                continue

            # Inline Shell execution (!ls, !git status, etc.)
            if user_input.startswith("!"):
                cmd = user_input[1:].strip()
                if cmd:
                    execute_shell(cmd)
                console.print()
                continue

            # Sleek Status Spinner
            with console.status("[bold bright_magenta]✦ Thinking & Searching Web...[/bold bright_magenta]", spinner="dots12"):
                response = agent.run(user_input)

            # Response Output formatted for mobile
            console.print()
            console.print(Rule(style="dim bright_blue", title="[bold cyan]TermuxBot Intelligence[/bold cyan]"))
            md_response = Markdown(str(response))
            console.print(Panel(md_response, border_style="bright_magenta", padding=(0, 1)))
            console.print()

        except KeyboardInterrupt:
            console.print("\n\n[bold yellow]Session stopped. Type exit to close.[/bold yellow]\n")
            break
        except Exception as e:
            console.print(f"\n[bold red][Error][/bold red] {e}\n")

if __name__ == "__main__":
    main()
