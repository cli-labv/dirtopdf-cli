"""Configuración global de la aplicación."""

import os
from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuración de la aplicación."""

    # Rutas del proyecto
    PROJECT_ROOT: Path = Path(__file__).parent.parent
    SRC_DIR: Path = Path(__file__).parent
    INPUT_DIR: Path = PROJECT_ROOT / "input"
    OUTPUT_DIR: Path = PROJECT_ROOT / "output"
    TEMP_DIR: Path = PROJECT_ROOT / "temp"
    LOG_DIR: Path = PROJECT_ROOT / "logs"

    # Contraseña del sistema
    SUDO_PASSWORD: Optional[str] = Field(default=None)

    # Configuración de conversión
    PRESERVE_ASPECT_RATIO: bool = True
    PDF_QUALITY: int = Field(default=95, ge=1, le=100)
    IMAGE_SORT_METHOD: str = "name"  # name, date, size

    # Formatos soportados
    SUPPORTED_FORMATS: tuple = (
        ".jpg", ".jpeg", ".png", ".bmp", ".gif",
        ".tiff", ".tif", ".webp", ".jfif",
        ".JPG", ".JPEG", ".PNG", ".BMP", ".GIF",
        ".TIFF", ".TIF", ".WEBP", ".JFIF"
    )

    # Procesamiento
    MAX_WORKERS: int = 1  # Procesamiento secuencial
    AUTO_CLEANUP_TEMP: bool = True
    KEEP_TEMP_ON_ERROR: bool = False

    # Configuración de PDF
    PDF_TITLE_FROM_FOLDER: bool = True
    PDF_AUTHOR: str = ""
    PDF_SUBJECT: str = "Converted from images"
    PDF_CREATOR: str = "DirToPDF CLI"

    # Límites
    MAX_FILE_SIZE_MB: int = 500
    MAX_IMAGES_PER_PDF: int = 10000

    # UI
    SHOW_THUMBNAILS: bool = False
    SHOW_DETAILED_PROGRESS: bool = True
    BANNER_FONT: str = "slant"
    BANNER_COLOR: str = "cyan"
    PROGRESS_COLOR: str = "green"
    ERROR_COLOR: str = "red"
    WARNING_COLOR: str = "yellow"
    INFO_COLOR: str = "blue"

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_TO_FILE: bool = True
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Permisos
    AUTO_FIX_PERMISSIONS: bool = True

    class Config:
        """Configuración de Pydantic."""

        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Instancia global de configuración
settings = Settings()


def get_settings() -> Settings:
    """Obtiene la instancia de configuración.

    Returns:
        Settings: Instancia de configuración global.
    """
    return settings


def ensure_directories() -> None:
    """Crea los directorios necesarios si no existen."""
    directories = [
        settings.INPUT_DIR,
        settings.OUTPUT_DIR,
        settings.TEMP_DIR,
        settings.LOG_DIR,
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)


def get_sudo_password() -> Optional[str]:
    """Obtiene la contraseña de sudo de la configuración o del usuario.

    Returns:
        Optional[str]: Contraseña o None.
    """
    if settings.SUDO_PASSWORD:
        return settings.SUDO_PASSWORD

    # Si no está en .env, pedirla al usuario
    from rich.prompt import Prompt
    from rich.console import Console

    console = Console()
    console.print("\n[yellow]⚠️  Se necesitan permisos de administrador[/yellow]")

    try:
        password = Prompt.ask(
            "Ingresa tu contraseña de sudo",
            password=True,
            console=console
        )
        return password if password else None
    except KeyboardInterrupt:
        console.print("\n[yellow]Operación cancelada[/yellow]")
        return None
