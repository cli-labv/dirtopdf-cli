#!/bin/bash

# DirToPDF CLI - Script de inicio automático optimizado
# Este script configura el entorno y ejecuta la aplicación
# Usa cacheo para evitar reinstalaciones innecesarias

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'
BOLD='\033[1m'

# Directorio del proyecto
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Archivo de marca para cacheo
INSTALLATION_MARKER="$SCRIPT_DIR/.installed"
VENV_MARKER="$SCRIPT_DIR/.venv_ready"

# Función para imprimir con color
print_color() {
    local color=$1
    shift
    echo -e "${color}${@}${NC}"
}

# Banner de bienvenida
print_banner() {
    echo ""
    print_color "$CYAN$BOLD" "╔════════════════════════════════════════════════════════════╗"
    print_color "$CYAN$BOLD" "║                                                            ║"
    print_color "$CYAN$BOLD" "║           📸  DIRTOPDF CLI  📄                             ║"
    print_color "$CYAN$BOLD" "║                                                            ║"
    print_color "$CYAN$BOLD" "║        Convierte Carpetas de Imágenes en PDFs              ║"
    print_color "$CYAN$BOLD" "║                                                            ║"
    print_color "$CYAN$BOLD" "╚════════════════════════════════════════════════════════════╝"
    echo ""
}

# Detectar Python
detect_python() {
    if command -v python3 &> /dev/null; then
        echo "python3"
    elif command -v python &> /dev/null; then
        PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}' | cut -d. -f1)
        if [ "$PYTHON_VERSION" == "3" ]; then
            echo "python"
        else
            print_color "$RED" "❌ Error: Python 3.9+ es requerido"
            exit 1
        fi
    else
        print_color "$RED" "❌ Error: Python no está instalado"
        exit 1
    fi
}

# Verificar versión de Python
check_python_version() {
    local python_cmd=$1
    local version=$($python_cmd --version 2>&1 | awk '{print $2}')
    local major=$(echo $version | cut -d. -f1)
    local minor=$(echo $version | cut -d. -f2)
    
    if [ "$major" -lt 3 ] || ([ "$major" -eq 3 ] && [ "$minor" -lt 9 ]); then
        print_color "$RED" "❌ Error: Se requiere Python 3.9 o superior"
        exit 1
    fi
    
    print_color "$GREEN" "✓ Python $version detectado"
}

# Crear entorno virtual
create_venv() {
    local python_cmd=$1
    
    if [ ! -d "venv" ]; then
        print_color "$YELLOW" "📦 Creando entorno virtual..."
        $python_cmd -m venv venv
        if [ $? -eq 0 ]; then
            print_color "$GREEN" "✓ Entorno virtual creado"
            touch "$VENV_MARKER"
        else
            print_color "$RED" "❌ Error al crear el entorno virtual"
            exit 1
        fi
    elif [ ! -f "$VENV_MARKER" ]; then
        print_color "$GREEN" "✓ Entorno virtual encontrado (inicializando...)"
        touch "$VENV_MARKER"
    else
        print_color "$GREEN" "✓ Entorno virtual listo (en caché)"
    fi
}

# Activar entorno virtual
activate_venv() {
    if [ -f "venv/bin/activate" ]; then
        source venv/bin/activate
    elif [ -f "venv/Scripts/activate" ]; then
        source venv/Scripts/activate
    else
        print_color "$RED" "❌ Error: No se pudo encontrar el script de activación"
        exit 1
    fi
    print_color "$GREEN" "✓ Entorno virtual activado"
}

# Instalar dependencias (optimizado con cacheo)
install_dependencies() {
    if [ -f "$INSTALLATION_MARKER" ]; then
        print_color "$GREEN" "✓ Dependencias ya instaladas (en caché)"
        return 0
    fi
    
    print_color "$YELLOW" "📥 Instalando dependencias (primera vez)..."
    print_color "$CYAN" "   Esto puede tomar un momento..."
    
    # Actualizar pip silenciosamente
    pip install --upgrade pip setuptools wheel -q 2>/dev/null || true
    
    # Instalar dependencias del proyecto
    if [ -f "pyproject.toml" ]; then
        pip install -e . -q 2>/dev/null
        if [ $? -eq 0 ]; then
            print_color "$GREEN" "✓ Dependencias instaladas exitosamente"
            touch "$INSTALLATION_MARKER"
        else
            print_color "$RED" "❌ Error al instalar dependencias"
            exit 1
        fi
    else
        print_color "$RED" "❌ Error: No se encontró pyproject.toml"
        exit 1
    fi
}

# Crear directorios necesarios
create_directories() {
    for dir in input output temp logs; do
        if [ ! -d "$dir" ]; then
            mkdir -p "$dir"
            print_color "$CYAN" "📁 Directorio '$dir/' creado"
        fi
    done
}

# ============================================================================
# MAIN
# ============================================================================

# Mostrar banner solo la primera vez o si se reinicia
if [ ! -f "$INSTALLATION_MARKER" ]; then
    print_banner
fi

# Detectar Python
PYTHON_CMD=$(detect_python)
check_python_version $PYTHON_CMD

# Crear/verificar entorno virtual
create_venv $PYTHON_CMD

# Activar entorno
activate_venv

# Instalar dependencias (con cacheo)
install_dependencies

# Crear directorios si no existen
create_directories

# Separador visual solo si es primera ejecución
if [ ! -f "$INSTALLATION_MARKER" ] && [ ! -f "$VENV_MARKER" ]; then
    echo ""
    print_color "$MAGENTA$BOLD" "════════════════════════════════════════════════════════════"
fi

print_color "$GREEN$BOLD" "🚀 Iniciando DirToPDF CLI..."
print_color "$MAGENTA$BOLD" "════════════════════════════════════════════════════════════"
echo ""

# Pequeña pausa para efecto visual (solo si es primera ejecución)
if [ ! -f "$INSTALLATION_MARKER" ]; then
    sleep 0.3
fi

# Ejecutar la aplicación
$PYTHON_CMD -m src.main "$@"

EXIT_CODE=$?

echo ""
if [ $EXIT_CODE -eq 0 ]; then
    print_color "$GREEN" "✓ Aplicación finalizada"
else
    print_color "$YELLOW" "⚠ Aplicación finalizada con código: $EXIT_CODE"
fi

echo ""
exit $EXIT_CODE
