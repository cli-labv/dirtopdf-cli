"""Utilidades para mostrar banners animados."""

import time
from typing import Optional

import pyfiglet
from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from src.config import settings

console = Console()


def show_banner(subtitle: Optional[str] = None) -> None:
    """Muestra un banner animado de bienvenida."""
    ascii_art = pyfiglet.figlet_format("DirToPDF", font=settings.BANNER_FONT)
    banner_text = Text(ascii_art, style=f"bold {settings.BANNER_COLOR}")

    if subtitle:
        banner_text.append(f"\n{subtitle}", style="italic white")
    else:
        banner_text.append(
            "\nConvierte Carpetas de Imágenes en PDFs",
            style="italic bright_white",
        )

    panel = Panel(
        Align.center(banner_text),
        border_style=settings.BANNER_COLOR,
        padding=(1, 2),
    )

    console.clear()
    console.print(panel)
    console.print()

    with console.status("[cyan]Inicializando...[/cyan]", spinner="dots", spinner_style="cyan"):
        time.sleep(0.8)

    console.print("[green]✓[/green] Listo para comenzar!\n")


def show_section_header(title: str, icon: str = "📌") -> None:
    """Muestra un encabezado de sección."""
    console.print()
    console.rule(f"[bold cyan]{icon} {title}[/bold cyan]", style="cyan")
    console.print()


def show_success_banner(title: str, stats: dict) -> None:
    """Muestra un banner de éxito con estadísticas."""
    content = Text()
    content.append(f"🎉 {title}\n\n", style="bold green")

    for key, value in stats.items():
        content.append(f"  • {key}: ", style="white")
        content.append(f"{value}\n", style="bold cyan")

    panel = Panel(Align.center(content), border_style="green", padding=(1, 2))
    console.print("\n")
    console.print(panel)
    console.print()


def show_error_banner(message: str) -> None:
    """Muestra un banner de error."""
    panel = Panel(f"❌ {message}", border_style="red", padding=(1, 2))
    console.print()
    console.print(panel)
    console.print()


def show_warning_banner(message: str) -> None:
    """Muestra un banner de advertencia."""
    panel = Panel(f"⚠️  {message}", border_style="yellow", padding=(1, 2))
    console.print()
    console.print(panel)
    console.print()


def show_empty_folder_animation() -> None:
    """Muestra animación de carpeta vacía."""
    console.print()
    panel = Panel(
        "[yellow]📂 Carpeta vacía\n\nNo se encontraron imágenes para convertir[/yellow]",
        border_style="yellow",
        padding=(1, 2),
        title="Sin Imágenes",
    )
    console.print(panel)
    console.print()
