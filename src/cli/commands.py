"""Comandos CLI de la aplicación."""

import sys
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt

from src.config import settings
from src.utils.banner import show_banner, show_section_header, show_empty_folder_animation, show_success_banner
from src.utils.helpers import choose_from_menu, confirm_action, safe_exit
from src.infrastructure.file_handler import FileHandler
from src.core.converter import ImageToPDFConverter

console = Console()


def run_interactive_mode() -> None:
    """Ejecuta la aplicación en modo interactivo."""
    while True:
        show_section_header("Selecciona Modo de Entrada", "🏠")
        
        options = [
            "Usar carpeta input/ del proyecto",
            "Usar directorio externo",
        ]
        
        choice = choose_from_menu("¿Dónde están las carpetas con imágenes?", options)
        
        if choice == -1:
            safe_exit(0)
        elif choice == 0:
            process_input_folder()
        elif choice == 1:
            process_external_folder()


def process_input_folder() -> None:
    """Procesa carpetas desde input/."""
    show_section_header("Escaneando Carpeta Input", "🔍")
    
    file_handler = FileHandler()
    folders = file_handler.scan_folders(settings.INPUT_DIR)
    
    if not folders:
        show_empty_folder_animation()
        handle_empty_folder(is_input=True)
        return
    
    show_folder_summary(folders)
    
    if not confirm_action(f"¿Convertir {len(folders)} carpetas a PDF?", default=True):
        console.print("[yellow]Operación cancelada[/yellow]")
        return
    
    converter = ImageToPDFConverter()
    results = converter.convert_folders(folders, settings.OUTPUT_DIR)
    
    show_conversion_results(results)


def process_external_folder() -> None:
    """Procesa carpetas desde directorio externo."""
    show_section_header("Directorio Externo", "📂")
    
    path_str = Prompt.ask("Ingresa la ruta del directorio", console=console)
    external_dir = Path(path_str).expanduser().resolve()
    
    if not external_dir.exists():
        console.print(f"[red]❌ El directorio no existe: {external_dir}[/red]")
        return
    
    file_handler = FileHandler()
    folders = file_handler.scan_folders(external_dir)
    
    if not folders:
        show_empty_folder_animation()
        handle_empty_folder(is_input=False)
        return
    
    show_folder_summary(folders)
    
    if not confirm_action(f"¿Convertir {len(folders)} carpetas a PDF?", default=True):
        console.print("[yellow]Operación cancelada[/yellow]")
        return
    
    converter = ImageToPDFConverter()
    results = converter.convert_folders(folders, settings.OUTPUT_DIR, is_external=True)
    
    show_conversion_results(results)


def handle_empty_folder(is_input: bool) -> None:
    """Maneja el caso de carpeta vacía."""
    options = [
        "Reintentar (escanear nuevamente)",
        "Usar carpeta input/" if not is_input else "Usar directorio externo",
    ]
    
    choice = choose_from_menu("¿Qué deseas hacer?", options)
    
    if choice == -1:
        safe_exit(0)
    elif choice == 0:
        return  # Reintentar
    elif choice == 1:
        if is_input:
            process_external_folder()
        else:
            process_input_folder()


def show_folder_summary(folders: list[dict]) -> None:
    """Muestra resumen de carpetas encontradas."""
    console.print(f"\n[green]✓[/green] Encontradas [bold]{len(folders)}[/bold] carpetas con imágenes\n")
    
    for i, folder in enumerate(folders[:5], 1):
        img_count = folder.get('image_count', 0)
        console.print(f"  {i}. {folder['name']} ({img_count} imágenes)")
    
    if len(folders) > 5:
        console.print(f"  ... y {len(folders) - 5} más")
    
    console.print()


def show_conversion_results(results: list[dict]) -> None:
    """Muestra resultados de conversión."""
    successful = sum(1 for r in results if r.get('success', False))
    
    show_success_banner(
        "¡Conversión completada!",
        {
            "Carpetas procesadas": f"{successful}/{len(results)}",
            "PDFs generados": f"{successful}",
            "Ubicación": str(settings.OUTPUT_DIR),
        },
    )
