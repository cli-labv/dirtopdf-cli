#!/bin/bash

# DirToPDF CLI - Script de inicio automático
# Este script configura el entorno y ejecuta la aplicación

set -e  # Salir si hay errores

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color
BOLD='\033[1m'

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
    print_color "$CYAN$BOLD" "║           📸  DIRTOPDF CLI  📄                         ║"
    print_color "$CYAN$BOLD" "║                                                            ║"
    print_color "$CYAN$BOLD" "║        Convierte Carpetas de Imágenes en PDFs              ║"
    print_color "$CYAN$BOLD" "║                                                            ║"
    print_color "$CYAN$BOLD" "╚════════════════════════════════════════════════════════════╝"
    echo ""
}

# Detectar el comando Python disponible
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
        print_color "$YELLOW" "   Por favor instala Python 3.9 o superior"
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
        print_color "$YELLOW" "   Versión actual: $version"
        exit 1
    fi
    
    print_color "$GREEN" "✓ Python $version detectado"
}

# Función para mostrar spinner
spinner() {
    local pid=$1
    local delay=0.1
    local spinstr='⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏'
    while [ "$(ps a | awk '{print $1}' | grep $pid)" ]; do
        local temp=${spinstr#?}
        printf " [%c]  " "$spinstr"
        local spinstr=$temp${spinstr%"$temp"}
        sleep $delay
        printf "\b\b\b\b\b\b"
    done
    printf "    \b\b\b\b"
}

# Mostrar banner
print_banner

# Detectar Python
print_color "$BLUE" "🔍 Detectando Python..."
PYTHON_CMD=$(detect_python)
check_python_version $PYTHON_CMD

# Verificar si existe el entorno virtual
if [ ! -d "venv" ]; then
    print_color "$YELLOW" "📦 Entorno virtual no encontrado. Creando..."
    
    $PYTHON_CMD -m venv venv
    
    if [ $? -eq 0 ]; then
        print_color "$GREEN" "✓ Entorno virtual creado exitosamente"
    else
        print_color "$RED" "❌ Error al crear el entorno virtual"
        exit 1
    fi
else
    print_color "$GREEN" "✓ Entorno virtual encontrado"
fi

# Activar el entorno virtual
print_color "$BLUE" "🔄 Activando entorno virtual..."

if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
elif [ -f "venv/Scripts/activate" ]; then
    source venv/Scripts/activate
else
    print_color "$RED" "❌ Error: No se pudo encontrar el script de activación"
    exit 1
fi

print_color "$GREEN" "✓ Entorno virtual activado"

# Verificar e instalar dependencias
print_color "$BLUE" "📚 Verificando dependencias..."

if [ -f "pyproject.toml" ]; then
    # Verificar si pip está actualizado
    print_color "$CYAN" "   Actualizando pip..."
    pip install --upgrade pip setuptools wheel --quiet
    
    # Instalar dependencias
    if ! pip show pillow &> /dev/null; then
        print_color "$YELLOW" "📥 Instalando dependencias (esto puede tomar un momento)..."
        pip install -e . --quiet &
        spinner $!
        print_color "$GREEN" "✓ Dependencias instaladas"
    else
        print_color "$GREEN" "✓ Dependencias ya instaladas"
    fi
else
    print_color "$RED" "❌ Error: No se encontró pyproject.toml"
    exit 1
fi

# Crear carpetas por defecto si no existen
for dir in input output temp logs; do
    if [ ! -d "$dir" ]; then
        mkdir -p "$dir"
        print_color "$CYAN" "📁 Carpeta '$dir/' creada"
    fi
done

# Separador visual
echo ""
print_color "$MAGENTA$BOLD" "════════════════════════════════════════════════════════════"
print_color "$GREEN$BOLD" "🚀 ¡Todo listo! Iniciando DirToPDF CLI..."
print_color "$MAGENTA$BOLD" "════════════════════════════════════════════════════════════"
echo ""

# Pequeña pausa para efecto visual
sleep 0.5

# Ejecutar la aplicación
$PYTHON_CMD -m src.main "$@"

# Capturar el código de salida
EXIT_CODE=$?

echo ""
if [ $EXIT_CODE -eq 0 ]; then
    print_color "$GREEN" "✓ Aplicación finalizada exitosamente"
else
    print_color "$YELLOW" "⚠ Aplicación finalizada con código: $EXIT_CODE"
fi

echo ""
print_color "$CYAN" "💡 Tip: Para salir presiona Ctrl+C o escribe 'exit' en los menús"
echo ""
