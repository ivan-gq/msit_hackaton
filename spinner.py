import time
from rich.console import Console

console = Console(force_terminal=True, force_interactive=True)

with console.status("[bold green]Testing spinner animation...[/bold green]", spinner="moon"):
    time.sleep(5)  # Pause for 5 seconds to observe the animation

console.print("[bold cyan]Spinner works![/bold cyan]")