"""Manejo de archivos y carpetas del sistema."""

import logging
from pathlib import Path
from typing import List

from rich.console import Console

from src.config import settings

logger = logging.getLogger(__name__)
console = Console()


class FileHandler:
    """Clase para manejar operaciones con archivos y directorios."""

    def scan_folders(self, base_dir: Path) -> list[dict]:
        """Escanea directorios en busca de carpetas con imágenes."""
        if not base_dir.exists() or not base_dir.is_dir():
            return []
        
        folders_with_images = []
        
        # Buscar carpetas directamente en base_dir
        for item in base_dir.iterdir():
            if item.is_dir():
                images = self._find_images_in_folder(item)
                if images:
                    folders_with_images.append({
                        'path': item,
                        'name': item.name,
                        'images': images,
                        'image_count': len(images),
                    })
        
        return sorted(folders_with_images, key=lambda x: x['name'])

    def _find_images_in_folder(self, folder: Path) -> List[Path]:
        """Encuentra todas las imágenes en una carpeta y subcarpetas."""
        images = []
        
        try:
            # Buscar recursivamente
            for ext in settings.SUPPORTED_FORMATS:
                images.extend(folder.rglob(f"*{ext}"))
        except PermissionError:
            logger.warning(f"Sin permisos para acceder a {folder}")
        
        return sorted(images)

    def create_directory(self, directory: Path) -> bool:
        """Crea un directorio."""
        try:
            directory.mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            logger.error(f"Error al crear directorio: {e}")
            return False
