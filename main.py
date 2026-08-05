from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

from app.agent import Agent

console = Console()
agent = Agent()


def show_banner():
    console.print()

    console.print(
        Panel.fit(
            "[bold cyan]🚀 Codebase Agent v2.1[/bold cyan]\n\n"
            "[bold]Examples[/bold]\n"
            "• Describe this project\n"
            "• Explain main.py\n"
            "• Review calculator.py\n"
            "• Run main.py\n"
            "• Create hello.py\n"
            "• Exit",
            border_style="cyan",
        )
    )


def get_multiline_input() -> str:
    """
    Read multiline input until the user types END.
    """

    console.print()
    console.print(
        "[bold green]🤖 You[/bold green] "
        "[dim](Finish with END on a new line)[/dim]"
    )

    lines = []

    while True:

        line = input()

        if line.strip() == "END":
            break

        lines.append(line)

    return "\n".join(lines).strip()


def main():

    show_banner()

    try:

        while True:

            user = get_multiline_input()

            if not user:
                continue

            if user.lower() in {"exit", "quit"}:

                console.print()
                console.print("[bold red]👋 Goodbye![/bold red]")

                break

            response = agent.chat(user)

            console.print()

            console.print(
                Panel(
                    Markdown(response),
                    title="🤖 Agent",
                    border_style="green",
                )
            )

    except KeyboardInterrupt:

        console.print()
        console.print("[bold red]👋 Goodbye![/bold red]")


if __name__ == "__main__":
    main()
