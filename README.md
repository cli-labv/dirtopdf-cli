# 📁 DirToPDF CLI

<div align="center">

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

*Una herramienta CLI moderna para convertir carpetas de imágenes en PDFs*

</div>

## ✨ Características

- 🎨 **Interfaz Premium**: Banner animado, spinners elegantes y progress bars en tiempo real
- 📁 **Conversión por Carpetas**: Cada carpeta = 1 PDF con el nombre de la carpeta
- 🔍 **Escaneo Inteligente**: Detecta carpetas con subcarpetas automáticamente
- 📊 **Diagnóstico Previo**: Muestra lo que encontró antes de procesar
- ⚡ **Procesamiento Eficiente**: Conversión en cola, archivo por archivo
- 🖼️ **Todos los Formatos**: Acepta JPG, PNG, BMP, GIF, TIFF, WebP y más
- 📏 **Calidad Original**: Las imágenes se conservan tal cual en el PDF
- 🔒 **Manejo Automático de Permisos**: Usa sudo cuando es necesario
- 🎯 **Dos Modos de Entrada**: Carpeta input/ del proyecto o directorios externos
- 🧹 **Auto-limpieza**: Mantiene el proyecto limpio usando copias temporales

## 🚀 Inicio Rápido

### Requisitos Previos

- Python 3.9 o superior
- Sistema operativo: Linux, macOS o Windows (con WSL/Git Bash)

### Instalación y Uso

Es extremadamente simple. Solo necesitas ejecutar:

```bash
git clone <repository-url>
cd dirtopdf-cli
chmod +x start.sh
./start.sh
```

El script `start.sh` se encargará automáticamente de:
- ✅ Crear el entorno virtual si no existe
- ✅ Instalar todas las dependencias
- ✅ Activar el entorno
- ✅ Iniciar la aplicación

## 📖 Uso

### Modo Interactivo (Predeterminado)

Simplemente ejecuta:

```bash
./start.sh
```

La aplicación te guiará paso a paso:
1. Elegir entre carpeta `input/` o directorio externo
2. Escanear y mostrar diagnóstico de carpetas encontradas
3. Confirmar conversión
4. Ver progreso en tiempo real
5. Revisar PDFs generados

### Estructura de Carpetas

#### Opción 1: Usar carpeta input/

```
dirtopdf-cli/
├── input/
│   ├── Vacaciones2024/       # → output/Vacaciones2024.pdf
│   │   ├── foto1.jpg
│   │   ├── foto2.png
│   │   └── foto3.jpg
│   ├── Documentos/            # → output/Documentos.pdf
│   │   ├── scan1.png
│   │   └── scan2.jpg
│   └── Proyecto/              # → output/Proyecto.pdf
│       └── subcarpeta/
│           ├── img1.jpg
│           └── img2.png
```

#### Opción 2: Usar directorio externo

```bash
# Apuntar a cualquier carpeta de tu sistema
/home/usuario/Fotos/
├── Boda/          # → output/Boda.pdf
├── Cumpleaños/    # → output/Cumpleaños.pdf
└── Viaje/         # → output/Viaje.pdf
```

### Formatos de Imagen Soportados

- **JPG/JPEG** - Fotos y comprimidas
- **PNG** - Transparencias y alta calidad
- **BMP** - Bitmap sin comprimir
- **GIF** - Imágenes animadas (solo primer frame)
- **TIFF** - Multipágina y alta resolución
- **WebP** - Formato moderno de Google
- **Y más** - Cualquier formato que soporte Pillow

## 🏗️ Arquitectura

El proyecto sigue **Clean Architecture** y principios **SOLID**:

```
dirtopdf-cli/
├── README.md              # Este archivo
├── start.sh               # Script de inicio automático
├── install.sh             # Script de instalación de dependencias
├── pyproject.toml         # Dependencias y configuración
├── .env.example           # Ejemplo de configuración
├── .gitignore
├── input/                 # Carpetas con imágenes a convertir
├── output/                # PDFs generados
├── temp/                  # Archivos temporales (auto-limpieza)
├── logs/                  # Logs de la aplicación
└── src/
    ├── __init__.py
    ├── main.py            # Punto de entrada CLI
    ├── config.py          # Configuración global
    ├── cli/
    │   └── commands.py    # Comandos interactivos
    ├── core/
    │   ├── converter.py   # Lógica de conversión
    │   └── models.py      # Modelos de datos
    ├── infrastructure/
    │   ├── file_handler.py    # Manejo de archivos
    │   └── pdf_creator.py     # Creación de PDFs
    └── utils/
        ├── banner.py      # Banner animado
        ├── progress.py    # Progress bars
        ├── helpers.py     # Utilidades
        └── validators.py  # Validaciones
```

## 🔧 Configuración

### Variables de Entorno (.env)

```bash
# Contraseña del sistema (opcional pero recomendado)
SUDO_PASSWORD=tu_contraseña_aqui

# Configuración de conversión
PRESERVE_ASPECT_RATIO=true
PDF_QUALITY=95
IMAGE_SORT_METHOD=name  # name, date, size

# Procesamiento
MAX_WORKERS=1  # Conversión en cola (recomendado)
AUTO_CLEANUP_TEMP=true

# UI
SHOW_THUMBNAILS=false
VERBOSE=false
```

### Permisos Automáticos

Si la app necesita permisos, automáticamente ejecuta:
```bash
sudo chmod -R 777 .
```

La contraseña se toma de:
1. Variable `SUDO_PASSWORD` en `.env` (si existe y es correcta)
2. Si falla o no existe, se pide en la CLI

## 💡 Ejemplos de Uso

### Ejemplo 1: Convertir carpetas en input/

1. Coloca tus carpetas con imágenes en `input/`:
   ```
   input/
   ├── Album_Familia/
   └── Recibos_2024/
   ```

2. Ejecuta:
   ```bash
   ./start.sh
   ```

3. Selecciona opción "Usar carpeta input/"

4. Resultado:
   ```
   output/
   ├── Album_Familia.pdf
   └── Recibos_2024.pdf
   ```

### Ejemplo 2: Convertir desde directorio externo

1. Ejecuta:
   ```bash
   ./start.sh
   ```

2. Selecciona "Usar directorio externo"

3. Ingresa ruta: `/home/usuario/Documentos/Escaneados`

4. Los PDFs se generan en `output/` sin mover archivos originales

### Ejemplo 3: Carpeta con subcarpetas

```
input/
└── ProyectoX/
    ├── Capitulo1/
    │   ├── img1.jpg
    │   └── img2.jpg
    └── Capitulo2/
        └── img3.jpg
```

Genera: `output/ProyectoX.pdf` (todas las imágenes incluidas)

## 🎯 Casos Especiales

### Carpeta Vacía

Si seleccionas una carpeta sin imágenes, la app:
- ✅ Muestra animación indicando carpeta vacía
- ✅ Ofrece 3 opciones:
  1. Reintentar (vuelve a escanear)
  2. Cambiar a input/externo
  3. Salir

### Orden de Imágenes en PDF

Las imágenes se ordenan alfabéticamente por defecto:
- `001.jpg`, `002.jpg`, `003.jpg` → Orden correcto
- `img1.jpg`, `img2.jpg`, `img10.jpg` → Natural sorting

### Imágenes Grandes

Las imágenes se mantienen en su tamaño original. El PDF se ajusta automáticamente.

## 🐛 Solución de Problemas

### El script no tiene permisos

```bash
chmod +x start.sh install.sh
```

### Error de permisos al convertir

La app pedirá tu contraseña automáticamente. Para evitarlo, configura `.env`:
```bash
cp .env.example .env
nano .env  # Agrega: SUDO_PASSWORD=tu_contraseña
```

### Falta alguna dependencia de imagen

```bash
# Ubuntu/Debian
sudo apt-get install python3-pil libjpeg-dev zlib1g-dev

# macOS
brew install pillow
```

## 🤝 Contribuir

Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## ✍️ Autor

Creado con ❤️ usando Python y las mejores prácticas de desarrollo.

---

<div align="center">

**⭐ Si te gusta este proyecto, dale una estrella! ⭐**

</div>
