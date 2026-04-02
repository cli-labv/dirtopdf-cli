"""Lógica principal de conversión de imágenes a PDF."""

import logging
import shutil
from pathlib import Path
from typing import List

import img2pdf
from natsort import natsorted
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

from src.config import settings

logger = logging.getLogger(__name__)
console = Console()


class ImageToPDFConverter:
    """Clase principal para convertir imágenes a PDF."""

    def convert_folders(
        self, folders: list[dict], output_dir: Path, is_external: bool = False
    ) -> list[dict]:
        """Convierte múltiples carpetas a PDFs."""
        results = []
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            console=console,
        ) as progress:
            task = progress.add_task("[cyan]Convirtiendo...", total=len(folders))
            
            for folder_info in folders:
                result = self._convert_single_folder(folder_info, output_dir, is_external)
                results.append(result)
                progress.update(task, advance=1)
        
        # Limpiar archivos temporales
        if settings.AUTO_CLEANUP_TEMP:
            self._cleanup_temp()
        
        return results

    def _convert_single_folder(
        self, folder_info: dict, output_dir: Path, is_external: bool
    ) -> dict:
        """Convierte una carpeta a PDF."""
        try:
            folder_path = folder_info['path']
            folder_name = folder_info['name']
            images = folder_info['images']
            
            # Ordenar imágenes naturalmente
            sorted_images = natsorted(images, key=lambda x: str(x))
            
            # Si es externo, copiar a temp
            if is_external:
                temp_images = self._copy_to_temp(sorted_images, folder_name)
                images_to_convert = temp_images
            else:
                images_to_convert = sorted_images
            
            # Nombre del PDF
            pdf_path = output_dir / f"{folder_name}.pdf"
            
            # Convertir a PDF
            with open(pdf_path, "wb") as f:
                f.write(img2pdf.convert([str(img) for img in images_to_convert]))
            
            logger.info(f"✓ Creado: {pdf_path.name}")
            
            return {
                'success': True,
                'folder': folder_name,
                'pdf_path': pdf_path,
                'image_count': len(images),
            }
        
        except Exception as e:
            logger.error(f"Error al convertir {folder_info['name']}: {e}")
            return {
                'success': False,
                'folder': folder_info['name'],
                'error': str(e),
            }

    def _copy_to_temp(self, images: List[Path], folder_name: str) -> List[Path]:
        """Copia imágenes a carpeta temporal."""
        temp_folder = settings.TEMP_DIR / folder_name
        temp_folder.mkdir(parents=True, exist_ok=True)
        
        temp_images = []
        for img in images:
            temp_path = temp_folder / img.name
            shutil.copy2(img, temp_path)
            temp_images.append(temp_path)
        
        return temp_images

    def _cleanup_temp(self) -> None:
        """Limpia archivos temporales."""
        try:
            if settings.TEMP_DIR.exists():
                for item in settings.TEMP_DIR.iterdir():
                    if item.is_dir():
                        shutil.rmtree(item)
                    else:
                        item.unlink()
        except Exception as e:
            logger.warning(f"No se pudo limpiar temp: {e}")
