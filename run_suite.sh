#!/bin/bash
# run_suite.sh
# Suite Unificada de Ejecución y Reportes Hummingbird
# Soporta: Allure, Cluecumber, History Management

set -e

# ==========================================
# CONFIGURACIÓN
# ==========================================
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
HISTORY_ROOT="execution-history"
CURRENT_RUN_DIR="$HISTORY_ROOT/$TIMESTAMP"

# Directorios de trabajo
ALLURE_RESULTS_DIR="allure-results"
JSON_RESULTS_DIR="json-results"
CUCUMBER_JSON="$JSON_RESULTS_DIR/cucumber_report.json"

# Colores
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# ==========================================
# ARGUMENTOS
# ==========================================
OPEN_REPORT=""

while [[ "$#" -gt 0 ]]; do
    case $1 in
        --open=*) OPEN_REPORT="${1#*=}" ;;
        --open) OPEN_REPORT="$2"; shift ;;
        --env=*) ENV="${1#*=}" ;;
        --env) ENV="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

echo -e "${BLUE}🦆 Hummingbird Test Suite Started at $TIMESTAMP${NC}"
echo -e "${BLUE}📁 Run Directory: $CURRENT_RUN_DIR${NC}"

# ==========================================
# 1. PREPARACIÓN
# ==========================================
mkdir -p "$CURRENT_RUN_DIR"
mkdir -p "$JSON_RESULTS_DIR"

# Limpiar resultados anteriores
rm -rf "$ALLURE_RESULTS_DIR"
# Limpiar carpeta de Jsons para evitar duplicados en Cluecumber
rm -rf "$JSON_RESULTS_DIR"/*

# Gestión de Historial Allure (para tendencias)
# Copiamos el historial previo a la carpeta de resultados para que Allure genere tendencias
if [ -d "allure-report/history" ]; then
    mkdir -p "$ALLURE_RESULTS_DIR/history"
    cp -r "allure-report/history/"* "$ALLURE_RESULTS_DIR/history/"
fi

# ==========================================
# 2. EJECUCIÓN DE TESTS
# ==========================================
echo -e "${BLUE}🚀 Running pytest...${NC}"

# Construir comando
CMD="./venv/bin/pytest --cucumberjson=$CUCUMBER_JSON"
if [ ! -z "$ENV" ]; then
    CMD="$CMD --env=$ENV"
fi

# Ejecutar y capturar salida
set +e # Permitir fallos de tests para generar reportes
$CMD
TEST_EXIT_CODE=$?
set -e

# ==========================================
# 3. ARCHIVADO DE RESULTADOS
# ==========================================
echo -e "${BLUE}💾 Archiving results to history...${NC}"

# Copiar Allure Results
if [ -d "$ALLURE_RESULTS_DIR" ]; then
    cp -r "$ALLURE_RESULTS_DIR" "$CURRENT_RUN_DIR/"
fi

# Copiar y Renombrar Cucumber JSON
if [ -f "$CUCUMBER_JSON" ]; then
    cp "$CUCUMBER_JSON" "$CURRENT_RUN_DIR/cucumber_$TIMESTAMP.json"
fi

# Guardar Metadata
# Guardar Metadata
BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "N/A")
COMMIT=$(git rev-parse --short HEAD 2>/dev/null || echo "N/A")
HOST=$(hostname)

cat > "$CURRENT_RUN_DIR/metadata.txt" <<EOF
Run ID: $TIMESTAMP
Date: $(date)
Environment: ${ENV:-DEV}
Exit Code: $TEST_EXIT_CODE
Branch: $BRANCH
Commit: $COMMIT
Usuario: $(whoami)
Host: $HOST
EOF

echo -e "${GREEN}✅ Execution Archived in $CURRENT_RUN_DIR${NC}"

# ==========================================
# 4. GENERACIÓN DE REPORTES
# ==========================================

# --- ALLURE ---
echo -e "${BLUE}📊 Generating Allure Report...${NC}"
allure generate "$ALLURE_RESULTS_DIR" -o "allure-report" --clean

# --- CLUECUMBER ---
if [ -f "$CUCUMBER_JSON" ]; then
    echo -e "${BLUE}🥒 Generating Cluecumber Report...${NC}"
    # Usamos el JSON timestamped para evitar conflictos? 
    # Cluecumber por defecto busca en la raíz según nuestro pom.
    # Generar usando Maven directamente
    cd reporting/cluecumber
    mvn cluecumber-report:reporting
    cd ../..
    
    # Copiar reporte generado al historial
    mkdir -p "$CURRENT_RUN_DIR/cluecumber-report"
    # El reporte se genera en cluecumber-report/ por defecto según el POM
    cp -r cluecumber-report/* "$CURRENT_RUN_DIR/cluecumber-report/"
fi

# ==========================================
# 5. ABRIR REPORTES
# ==========================================
if [ "$OPEN_REPORT" == "allure" ] || [ "$OPEN_REPORT" == "all" ]; then
    allure open "allure-report"
fi

if [ "$OPEN_REPORT" == "cluecumber" ] || [ "$OPEN_REPORT" == "all" ]; then
    open "cluecumber-report/index.html"
fi

exit $TEST_EXIT_CODE
