#!/bin/bash
# Script para ejecutar tests y mantener historial de reportes Allure
# Mantiene automáticamente los últimos 20 reportes

set -e  # Salir si hay errores

# Colores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🧪 Ejecutando tests con historial Allure...${NC}"

# Directorios
HISTORY_DIR="allure-history"
RESULTS_DIR="allure-results"
REPORT_DIR="allure-report"
MAX_HISTORY=20

# Crear directorio de historial si no existe
mkdir -p "$HISTORY_DIR"

# ========================================
# 1. GUARDAR HISTORIAL ANTERIOR (si existe)
# ========================================
if [ -d "$REPORT_DIR/history" ]; then
    echo -e "${YELLOW}📚 Guardando historial anterior...${NC}"
    cp -r "$REPORT_DIR/history" "$RESULTS_DIR/history" 2>/dev/null || true
fi

# ========================================
# 2. EJECUTAR TESTS
# ========================================
echo -e "${BLUE}🚀 Ejecutando tests...${NC}"
pytest

# Guardar código de salida de pytest
TEST_EXIT_CODE=$?

if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✅ Todos los tests pasaron${NC}"
else
    echo -e "${YELLOW}⚠️  Algunos tests fallaron (código: $TEST_EXIT_CODE)${NC}"
fi

# ========================================
# 3. GENERAR TIMESTAMP Y COPIAR RESULTADOS
# ========================================
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
HISTORY_SUBDIR="$HISTORY_DIR/$TIMESTAMP"

echo -e "${BLUE}💾 Guardando resultados en historial: $TIMESTAMP${NC}"
mkdir -p "$HISTORY_SUBDIR"
cp -r "$RESULTS_DIR" "$HISTORY_SUBDIR/"

# Guardar metadata de ejecución
cat > "$HISTORY_SUBDIR/metadata.txt" <<EOF
Fecha y Hora: $(date +"%Y-%m-%d %H:%M:%S")
Exit Code: $TEST_EXIT_CODE
Branch: $(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "N/A")
Commit: $(git rev-parse --short HEAD 2>/dev/null || echo "N/A")
Usuario: $(whoami)
Host: $(hostname)
EOF

# ========================================
# 4. LIMPIAR HISTORIAL ANTIGUO (mantener solo últimos 20)
# ========================================
echo -e "${BLUE}🧹 Limpiando historial antiguo (manteniendo últimos $MAX_HISTORY)...${NC}"

# Contar directorios en historial
HISTORY_COUNT=$(ls -1 "$HISTORY_DIR" | wc -l | tr -d ' ')

if [ "$HISTORY_COUNT" -gt "$MAX_HISTORY" ]; then
    # Calcular cuántos eliminar
    TO_DELETE=$((HISTORY_COUNT - MAX_HISTORY))
    
    echo -e "${YELLOW}📊 Historial actual: $HISTORY_COUNT reportes${NC}"
    echo -e "${YELLOW}🗑️  Eliminando los $TO_DELETE reportes más antiguos...${NC}"
    
    # Eliminar los más antiguos (primeros en orden alfabético = más antiguos por timestamp)
    ls -1t "$HISTORY_DIR" | tail -n "$TO_DELETE" | while read -r old_dir; do
        echo "   Eliminando: $old_dir"
        rm -rf "$HISTORY_DIR/$old_dir"
    done
    
    echo -e "${GREEN}✅ Historial limpiado. Reportes actuales: $MAX_HISTORY${NC}"
else
    echo -e "${GREEN}✅ Historial OK: $HISTORY_COUNT/$MAX_HISTORY reportes${NC}"
fi

# ========================================
# 5. GENERAR REPORTE ALLURE CON HISTORIAL
# ========================================
echo -e "${BLUE}📊 Generando reporte Allure con tendencias históricas...${NC}"

# Generar reporte con historial
allure generate "$RESULTS_DIR" -o "$REPORT_DIR" --clean

echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  ✅ REPORTE GENERADO CON ÉXITO                     ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}📁 Resultados guardados en:${NC} $HISTORY_SUBDIR"
echo -e "${BLUE}📊 Reporte HTML en:${NC} $REPORT_DIR/index.html"
echo -e "${BLUE}📚 Historial total:${NC} $(ls -1 "$HISTORY_DIR" | wc -l | tr -d ' ') reportes"
echo ""
echo -e "${YELLOW}💡 Para ver el reporte:${NC}"
echo -e "   ${GREEN}allure open $REPORT_DIR${NC}"
echo -e "   ${GREEN}o simplemente: ./generate_report.sh${NC}"
echo ""

# ========================================
# 6. ABRIR REPORTE (OPCIONAL)
# ========================================
read -p "¿Abrir reporte ahora? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${BLUE}🌐 Abriendo reporte...${NC}"
    allure open "$REPORT_DIR"
fi

# Retornar el código de salida original de pytest
exit $TEST_EXIT_CODE
