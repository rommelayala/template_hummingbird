#!/bin/bash
# Script para ver el historial de reportes Allure guardados

# Colores
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

HISTORY_DIR="allure-history"

echo -e "${BLUE}📚 Historial de Reportes Allure${NC}"
echo ""

if [ ! -d "$HISTORY_DIR" ] || [ -z "$(ls -A "$HISTORY_DIR")" ]; then
    echo -e "${YELLOW}⚠️  No hay historial disponible todavía.${NC}"
    echo -e "${YELLOW}💡 Ejecuta primero: ./run_tests_with_history.sh${NC}"
    exit 1
fi

# Listar reportes disponibles
echo -e "${GREEN}Reportes disponibles:${NC}"
echo ""

counter=1
for dir in $(ls -1t "$HISTORY_DIR"); do
    metadata_file="$HISTORY_DIR/$dir/metadata.txt"
    
    # Formatear timestamp para display
    year=${dir:0:4}
    month=${dir:4:2}
    day=${dir:6:2}
    hour=${dir:9:2}
    minute=${dir:11:2}
    second=${dir:13:2}
    formatted_date="$day/$month/$year $hour:$minute:$second"
    
    # Leer exit code del metadata si existe
    exit_code="N/A"
    if [ -f "$metadata_file" ]; then
        exit_code=$(grep "Exit Code:" "$metadata_file" | cut -d' ' -f3)
    fi
    
    # Determinar estado
    if [ "$exit_code" = "0" ]; then
        status="${GREEN}✅ PASSED${NC}"
    elif [ "$exit_code" = "N/A" ]; then
        status="${YELLOW}❓ UNKNOWN${NC}"
    else
        status="${YELLOW}⚠️  FAILED${NC}"
    fi
    
    printf "%2d) %s | %s | %s\n" "$counter" "$formatted_date" "$status" "$dir"
    
    counter=$((counter + 1))
done

echo ""
echo -e "${BLUE}Total de reportes guardados:${NC} $(ls -1 "$HISTORY_DIR" | wc -l | tr -d ' ')"
echo ""

# Preguntar cuál ver
read -p "¿Qué reporte quieres ver? (número o 'q' para salir): " choice

if [ "$choice" = "q" ] || [ "$choice" = "Q" ]; then
    echo "👋 Adiós!"
    exit 0
fi

# Validar número
if ! [[ "$choice" =~ ^[0-9]+$ ]]; then
    echo -e "${YELLOW}⚠️  Entrada inválida${NC}"
    exit 1
fi

# Obtener el directorio seleccionado
selected_dir=$(ls -1t "$HISTORY_DIR" | sed -n "${choice}p")

if [ -z "$selected_dir" ]; then
    echo -e "${YELLOW}⚠️  Número inválido${NC}"
    exit 1
fi

echo ""
echo -e "${BLUE}📊 Generando reporte del historial: $selected_dir${NC}"
echo ""

# Mostrar metadata si existe
metadata_file="$HISTORY_DIR/$selected_dir/metadata.txt"
if [ -f "$metadata_file" ]; then
    echo -e "${GREEN}Información de la ejecución:${NC}"
    cat "$metadata_file"
    echo ""
fi

# Generar y abrir reporte del historial seleccionado
allure serve "$HISTORY_DIR/$selected_dir/allure-results"
