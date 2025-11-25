#!/bin/bash
# Script para ver estadísticas y tendencias históricas de forma gráfica
# Genera un reporte consolidado de todas las ejecuciones guardadas

set -e

# Colores
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

HISTORY_DIR="allure-history"
TRENDS_DIR="allure-trends"
TRENDS_RESULTS="$TRENDS_DIR/combined-results"

echo -e "${BLUE}📊 Generando Vista de Tendencias Históricas${NC}"
echo ""

# Verificar que existe historial
if [ ! -d "$HISTORY_DIR" ] || [ -z "$(ls -A "$HISTORY_DIR")" ]; then
    echo -e "${RED}❌ No hay historial disponible${NC}"
    echo -e "${YELLOW}💡 Ejecuta primero: ./run_tests_with_history.sh${NC}"
    exit 1
fi

# Contar reportes disponibles
REPORT_COUNT=$(ls -1 "$HISTORY_DIR" | wc -l | tr -d ' ')

echo -e "${GREEN}📚 Analizando $REPORT_COUNT ejecuciones históricas...${NC}"
echo ""

# ========================================
# ESTADÍSTICAS EN CONSOLA
# ========================================
echo -e "${CYAN}╔════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║          RESUMEN ESTADÍSTICO HISTÓRICO              ║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════════════════╝${NC}"
echo ""

total_executions=0
total_passed=0
total_failed=0
passed_executions=0
failed_executions=0

# Analizar cada ejecución
echo -e "${BLUE}Ejecuciones analizadas:${NC}"
echo ""
printf "%-4s %-20s %-12s %-10s %-10s\n" "#" "Fecha/Hora" "Estado" "Passed" "Failed"
echo "────────────────────────────────────────────────────────────────"

counter=1
for dir in $(ls -1t "$HISTORY_DIR"); do
    metadata_file="$HISTORY_DIR/$dir/metadata.txt"
    
    # Formatear timestamp
    year=${dir:0:4}
    month=${dir:4:2}
    day=${dir:6:2}
    hour=${dir:9:2}
    minute=${dir:11:2}
    formatted_date="$day/$month/$year $hour:$minute"
    
    # Leer exit code
    exit_code="?"
    if [ -f "$metadata_file" ]; then
        exit_code=$(grep "Exit Code:" "$metadata_file" | cut -d' ' -f3)
    fi
    
    # Contar tests passed/failed del reporte
    results_dir="$HISTORY_DIR/$dir/allure-results"
    passed_count=0
    failed_count=0
    
    if [ -d "$results_dir" ]; then
        # Contar archivos *-result.json y analizar status
        for result_file in "$results_dir"/*-result.json; do
            if [ -f "$result_file" ]; then
                if grep -q '"status":"passed"' "$result_file"; then
                    passed_count=$((passed_count + 1))
                elif grep -q '"status":"failed"' "$result_file"; then
                    failed_count=$((failed_count + 1))
                fi
            fi
        done
    fi
    
    # Determinar estado de la ejecución
    if [ "$exit_code" = "0" ]; then
        status="${GREEN}✅ PASSED${NC}"
        passed_executions=$((passed_executions + 1))
    elif [ "$exit_code" = "?" ]; then
        status="${YELLOW}❓ UNKNOWN${NC}"
    else
        status="${RED}❌ FAILED${NC}"
        failed_executions=$((failed_executions + 1))
    fi
    
    total_passed=$((total_passed + passed_count))
    total_failed=$((total_failed + failed_count))
    total_executions=$((total_executions + 1))
    
    printf "%-4d %-20s %-20s %-10d %-10d\n" "$counter" "$formatted_date" "$(echo -e "$status")" "$passed_count" "$failed_count"
    
    counter=$((counter + 1))
done

echo ""
echo -e "${CYAN}╔════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║              ESTADÍSTICAS TOTALES                   ║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════════════════╝${NC}"
echo ""

total_tests=$((total_passed + total_failed))
success_rate=0
if [ $total_tests -gt 0 ]; then
    success_rate=$((total_passed * 100 / total_tests))
fi

execution_success_rate=0
if [ $total_executions -gt 0 ]; then
    execution_success_rate=$((passed_executions * 100 / total_executions))
fi

echo -e "${GREEN}📊 Total de Ejecuciones:${NC} $total_executions"
echo -e "${GREEN}✅ Ejecuciones Exitosas:${NC} $passed_executions ($execution_success_rate%)"
echo -e "${RED}❌ Ejecuciones Fallidas:${NC} $failed_executions"
echo ""
echo -e "${GREEN}📝 Total de Tests Ejecutados:${NC} $total_tests"
echo -e "${GREEN}✅ Tests Passed en Total:${NC} $total_passed"
echo -e "${RED}❌ Tests Failed en Total:${NC} $total_failed"
echo -e "${CYAN}📈 Tasa de Éxito General:${NC} $success_rate%"
echo ""

# ========================================
# GENERAR REPORTE CONSOLIDADO CON ALLURE
# ========================================
echo -e "${BLUE}📊 Generando reporte visual consolidado...${NC}"
echo ""

# Limpiar directorio de tendencias anterior
rm -rf "$TRENDS_DIR"
mkdir -p "$TRENDS_RESULTS"

# Combinar todos los resultados históricos
echo -e "${YELLOW}Combinando resultados de todas las ejecuciones...${NC}"

for dir in $(ls -1t "$HISTORY_DIR" | head -n 10); do
    results_dir="$HISTORY_DIR/$dir/allure-results"
    if [ -d "$results_dir" ]; then
        cp -r "$results_dir"/* "$TRENDS_RESULTS/" 2>/dev/null || true
    fi
done

# Copiar history si existe para mantener tendencias
for dir in $(ls -1t "$HISTORY_DIR" | head -n 1); do
    history_dir="$HISTORY_DIR/$dir/allure-results/history"
    if [ -d "$history_dir" ]; then
        cp -r "$history_dir" "$TRENDS_RESULTS/" 2>/dev/null || true
    fi
done

echo -e "${GREEN}✅ Datos combinados de las últimas 10 ejecuciones${NC}"
echo ""
echo -e "${BLUE}🌐 Generando reporte HTML con gráficos de tendencias...${NC}"

# Generar reporte consolidado
allure generate "$TRENDS_RESULTS" -o "$TRENDS_DIR/report" --clean

echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  ✅ REPORTE DE TENDENCIAS GENERADO                 ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${CYAN}📊 El reporte incluye:${NC}"
echo -e "   • Gráficos de tendencias de passed/failed"
echo -e "   • Evolución de duración de tests"
echo -e "   • Comparación entre ejecuciones"
echo -e "   • Timeline consolidado"
echo -e "   • Identificación de tests inestables (flaky)"
echo ""
echo -e "${YELLOW}💡 Abriendo reporte en el navegador...${NC}"
echo ""

# Abrir reporte
allure open "$TRENDS_DIR/report"
