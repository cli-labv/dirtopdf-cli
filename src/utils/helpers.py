"""Funciones auxiliares generales."""

import logging
import sys
from pathlib import Path

from rich.console import Console
from rich.logging import RichHandler
from rich.prompt import Confirm

from src.config import settings

console = Console()


def setup_logging(verbose: bool = False) -> None:
    """Configura el sistema de logging."""
    log_level = logging.DEBUG if verbose else getattr(logging, settings.LOG_LEVEL)
    
    console_handler = RichHandler(
        console=console,
        rich_tracebacks=True,
        tracebacks_show_locals=verbose,
        markup=True,
    )
    console_handler.setLevel(log_level)
    
    handlers = [console_handler]
    
    if settings.LOG_TO_FILE:
        settings.LOG_DIR.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(
            settings.LOG_DIR / "dirtopdf_cli.log",
            encoding="utf-8",
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(logging.Formatter(settings.LOG_FORMAT))
        handlers.append(file_handler)
    
    logging.basicConfig(level=log_level, format="%(message)s", handlers=handlers)


def format_bytes(bytes_size: int) -> str:
    """Formatea bytes a formato legible."""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} PB"


def confirm_action(message: str, default: bool = True) -> bool:
    """Solicita confirmación al usuario."""
    return Confirm.ask(message, default=default, console=console)


def safe_exit(code: int = 0) -> None:
    """Salida segura de la aplicación."""
    console.print("\n[cyan]👋 ¡Hasta pronto![/cyan]\n")
    sys.exit(code)


def choose_from_menu(title: str, options: list[str], show_exit: bool = True) -> int:
    """Muestra un menú y retorna la selección."""
    from rich.prompt import IntPrompt
    
    console.print(f"\n[bold cyan]{title}[/bold cyan]\n")
    
    for idx, option in enumerate(options, 1):
        console.print(f"  [cyan]{idx}.[/cyan] {option}")
    
    if show_exit:
        console.print(f"  [yellow]0.[/yellow] Salir")
    
    console.print()
    
    try:
        max_option = len(options)
        choice = IntPrompt.ask("Selecciona una opción", console=console)
        
        if show_exit and choice == 0:
            return -1
        
        if 1 <= choice <= max_option:
            return choice - 1
        
        console.print(f"[red]❌ Opción inválida[/red]")
        return choose_from_menu(title, options, show_exit)
    
    except KeyboardInterrupt:
        return -1
