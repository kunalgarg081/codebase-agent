from rich.console import Console

from app.agent import Agent

console = Console()

agent = Agent()

console.print("[bold green]Codebase Agent[/bold green]")
console.print("Type 'exit' to quit.\n")

while True:

    user = input("You: ")

    if user.lower() == "exit":
        break

    response = agent.chat(user)

    console.print(f"\n[cyan]Agent:[/cyan] {response}\n")