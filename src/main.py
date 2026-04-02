"""Punto de entrada principal de la aplicación CLI."""

import sys
from typing import Optional

import typer
from rich.console import Console

from src.config import ensure_directories
from src.utils.banner import show_banner
from src.utils.helpers import setup_logging

# Crear instancia de la aplicación Typer
app = typer.Typer(
    name="dirtopdf-cli",
    help="🔥 CLI profesional para convertir carpetas de imágenes en PDFs",
    add_completion=True,
    rich_markup_mode="rich",
    no_args_is_help=False,
)

console = Console()


def version_callback(value: bool) -> None:
    """Callback para mostrar la versión."""
    if value:
        from src import __version__

        console.print(f"[cyan]DirToPDF CLI[/cyan] versión [bold]{__version__}[/bold]")
        raise typer.Exit()


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Mostrar la versión de la aplicación",
        callback=version_callback,
        is_eager=True,
    ),
) -> None:
    """
    🔥 DirToPDF CLI - Convierte carpetas de imágenes en PDFs

    Una herramienta profesional para convertir múltiples imágenes en documentos PDF.

    \b
    Características:
    • Conversión de carpetas completas a PDF
    • Procesamiento automático de subcarpetas
    • Interfaz interactiva con animaciones
    • Soporte para todos los formatos de imagen
    • Manejo automático de permisos

    \b
    Ejemplos de uso:
      $ dirtopdf-cli                    # Modo interactivo
      $ ./start.sh                      # Inicio automático

    \b
    Para más ayuda visita el README.md
    """
    # Si no se proporcionó ningún comando, ejecutar modo interactivo
    if ctx.invoked_subcommand is None:
        try:
            # Configurar logging
            setup_logging()

            # Asegurar que existan los directorios
            ensure_directories()

            # Mostrar banner de bienvenida
            show_banner()

            # Ejecutar el flujo principal
            from src.cli.commands import run_interactive_mode

            run_interactive_mode()

        except KeyboardInterrupt:
            console.print("\n\n[yellow]⚠️  Operación cancelada por el usuario[/yellow]")
            sys.exit(0)
        except Exception as e:
            console.print(f"\n[red]❌ Error inesperado:[/red] {str(e)}")
            if "--verbose" in sys.argv:
                console.print_exception()
            sys.exit(1)


if __name__ == "__main__":
    app()
