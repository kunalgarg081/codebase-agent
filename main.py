from rich.console import Console

from app.agent import Agent

console = Console()
agent = Agent()


def show_banner():
    console.print("[bold green]🚀 Codebase Agent v1.0[/bold green]\n")

    console.print("[bold cyan]Example Commands:[/bold cyan]")
    console.print("  • Describe this project")
    console.print("  • Explain main.py")
    console.print("  • Explain greet")
    console.print("  • List all functions")
    console.print("  • Review main.py")
    console.print("  • Exit\n")


def main():

    show_banner()

    try:

        while True:

            user = input("🤖 You > ").strip()

            if not user:
                continue

            if user.lower() in {"exit", "quit"}:
                console.print("\n👋 Goodbye!")
                break

            response = agent.chat(user)

            console.print(f"\n[cyan]🤖 Agent[/cyan]\n{response}\n")

    except KeyboardInterrupt:
        console.print("\n\n👋 Goodbye!")


if __name__ == "__main__":
    main()