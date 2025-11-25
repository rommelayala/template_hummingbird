#!/bin/bash
# Script para generar y abrir reportes Allure

echo "🚀 Generando reporte Allure..."

# Verificar que existen resultados
if [ ! -d "allure-results" ] || [ -z "$(ls -A allure-results)" ]; then
    echo "❌ No hay resultados de tests disponibles."
    echo "💡 Ejecuta primero: pytest"
    exit 1
fi

# Generar y abrir el reporte
allure serve allure-results

# Nota: 'allure serve' automáticamente:
# 1. Genera el reporte HTML
# 2. Inicia un servidor local
# 3. Abre el navegador con el reporte
