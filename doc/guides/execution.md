# Guía de Ejecución y Reportes

## Ejecución de Tests

### Ejecutar Todos los Tests
```bash
pytest
```

### Ejecutar Tests Específicos
```bash
# Tests de login
pytest tests/test_login.py

# Con verbose
pytest tests/test_login.py -v

# Con logs detallados
pytest -v --log-cli-level=DEBUG
```

### Ejecutar por Markers
Configura tus tests con markers en `pytest.ini`.

```bash
# Solo tests smoke
pytest -m smoke

# Solo tests de login
pytest -m login

# Excluir tests lentos
pytest -m "not slow"
```

**Markers Disponibles:**
- `@pytest.mark.smoke` - Tests rápidos y críticos
- `@pytest.mark.regression` - Suite completa de regresión
- `@pytest.mark.login` - Tests de autenticación
- `@pytest.mark.demo` - Tests para demos
- `@pytest.mark.slow` - Tests lentos
- `@pytest.mark.playwright` - Tests intensivos de Playwright

### Ejecutar en Paralelo
```bash
# Automático (usa todos los CPUs)
pytest -n auto

# Específico (4 workers)
pytest -n 4
```

---

## Generar Reportes Allure

### 1. Con Historial (Recomendado) 🆕
Ejecuta los tests y guarda el historial automáticamente.

```bash
./run_tests_with_history.sh
```

**Características:**
- ✅ Ejecuta todos los tests
- ✅ Guarda resultados en `allure-history/` con timestamp
- ✅ Mantiene automáticamente los últimos **20 reportes**
- ✅ Genera **gráficos de tendencias** históricas
- ✅ Guarda metadata (fecha, branch, commit, usuario)
- ✅ Pregunta si deseas abrir el reporte

### 2. Ver Reportes Históricos Individuales
Lista y visualiza reportes guardados anteriormente.

```bash
./view_history.sh
```

**Qué hace:**
- 📋 Muestra lista de reportes con fecha y estado (PASSED/FAILED)
- 🔍 Permite seleccionar cualquier reporte anterior
- 📊 Abre el reporte histórico seleccionado

### 3. Ver Tendencias y Estadísticas Históricas 🆕
Genera un resumen estadístico consolidado.

```bash
./view_historical_trends.sh
```

**Qué muestra:**
- 📊 **Tabla estadística** en consola con todas las ejecuciones
- 📈 **Gráficos de tendencias** consolidados (últimas 10 ejecuciones)
- ✅ **Tasa de éxito** general de tests
- 🎯 **Identificación de tests inestables** (flaky tests)

### 4. Script Simple (Sin Historial)
Solo genera y abre el reporte de la última ejecución en `allure-results`.

```bash
./generate_report.sh
```

### 5. Comandos Manuales
```bash
# 1. Ejecutar tests (genera allure-results/)
pytest

# 2. Generar y abrir reporte
allure serve allure-results

# O generar reporte estático
allure generate allure-results -o allure-report --clean
```
