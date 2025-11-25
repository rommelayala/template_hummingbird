# 📁 Archivos Involucrados en el Sistema de Reportes

Lista completa y detallada de todos los archivos relacionados con los reportes Allure.

---

## Archivos de Configuración

### `pytest.ini`
**Ubicación:** `/pytest.ini`  
**Propósito:** Configuración de pytest y Allure

**Contenido relevante:**
```ini
[pytest]
# Genera resultados Allure automáticamente
addopts = --alluredir=allure-results --clean-alluredir

# Markers personalizados
markers =
    smoke: tests rápidos
    regression: suite completa
```

**¿Qué hace?**
- `--alluredir=allure-results` → Le dice a pytest dónde guardar los JSON
- `--clean-alluredir` → Limpia resultados anteriores antes de ejecutar

**¿Cuándo se usa?** Cada vez que ejecutas `pytest`

---

### `conftest.py`
**Ubicación:** `/conftest.py`  
**Propósito:** Fixtures de pytest y hooks para Allure

**Secciones importantes:**

#### 1. Imports
```python
import os
import pytest
import allure
from playwright.sync_api import Playwright, Browser, Page
```

#### 2. Fixtures
```python
@pytest.fixture(scope="session")
def playwright_instance():
    # Inicia Playwright

@pytest.fixture(scope="session")
def browser(playwright_instance):
    # Lanza navegador

@pytest.fixture
def page(context):
    # Crea página nueva
```

#### 3. Hook de Screenshots (⭐ IMPORTANTE)
```python
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        # Busca fixture 'page'
        page = item.funcargs.get("page")
        
        if page:
            # Captura screenshot
            screenshot_path = f"allure-results/screenshots/{item.name}.png"
            page.screenshot(path=screenshot_path)
            
            # Adjunta a Allure
            allure.attach.file(
                screenshot_path,
                name=f"Screenshot - {item.name}",
                attachment_type=allure.attachment_type.PNG
            )
```

**¿Qué hace?**
- Se ejecuta **después de cada test**
- Si el test **falló**, captura screenshot
- Adjunta el screenshot al reporte Allure

**¿Cuándo se usa?** Automáticamente en cada test con fixture `page`

---

### `requirements.txt`
**Ubicación:** `/requirements.txt`  
**Propósito:** Dependencias Python

**Líneas relevantes:**
```txt
pytest==8.4.2
pytest-playwright==0.7.1
playwright==1.56.0
allure-pytest==2.15.0       # ← Plugin de Allure
```

**¿Qué instala?**
- `allure-pytest` → Plugin que conecta pytest con Allure
- También instala `allure-python-commons` como dependencia

---

## Archivos de Tests

### `tests/test_login.py`
**Ubicación:** `/tests/test_login.py`  
**Propósito:** Tests con decoradores Allure

**Estructura:**
```python
import allure                               # ← Import necesario
from playwright.sync_api import Page

@allure.feature("Autenticación")           # ← Decorador 1
@allure.story("Login exitoso")             # ← Decorador 2
@allure.severity(allure.severity_level.CRITICAL)  # ← Decorador 3
@allure.title("Verificar login correcto")  # ← Decorador 4
def test_login_correcto(page: Page):
    with allure.step("Paso 1"):            # ← Step 1
        # código
    
    with allure.step("Paso 2"):            # ← Step 2
        # código
```

**Decoradores disponibles:**
- `@allure.feature()` - Feature/Funcionalidad
- `@allure.story()` - Historia de usuario
- `@allure.severity()` - Criticidad
- `@allure.title()` - Título descriptivo
- `@allure.description()` - Descripción larga
- `@allure.link()` - Enlace a ticket
- `with allure.step()` - Paso del test

---

## Scripts de Reportes

### `generate_report.sh`
**Ubicación:** `/generate_report.sh`  
**Propósito:** Generar reporte simple sin historial

**Qué hace:**
```bash
#!/bin/bash
# 1. Verifica que existan resultados
if [ ! -d "allure-results" ]; then
    echo "No hay resultados"
    exit 1
fi

# 2. Genera y abre reporte
allure serve allure-results
```

**Cuándo usar:** Para ver el reporte de la última ejecución rápidamente

---

### `run_tests_with_history.sh`
**Ubicación:** `/run_tests_with_history.sh`  
**Propósito:** Ejecutar tests y guardar en historial

**Secciones principales:**

#### 1. Variables
```bash
HISTORY_DIR="allure-history"
RESULTS_DIR="allure-results"
REPORT_DIR="allure-report"
MAX_HISTORY=20
```

#### 2. Copiar historial anterior
```bash
if [ -d "$REPORT_DIR/history" ]; then
    cp -r "$REPORT_DIR/history" "$RESULTS_DIR/history"
fi
```
**¿Por qué?** Para que el nuevo reporte tenga trending del anterior

#### 3. Ejecutar tests
```bash
pytest
TEST_EXIT_CODE=$?
```

#### 4. Guardar en historial
```bash
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
HISTORY_SUBDIR="$HISTORY_DIR/$TIMESTAMP"
mkdir -p "$HISTORY_SUBDIR"
cp -r "$RESULTS_DIR" "$HISTORY_SUBDIR/"
```

#### 5. Guardar metadata
```bash
cat > "$HISTORY_SUBDIR/metadata.txt" <<EOF
Fecha y Hora: $(date +"%Y-%m-%d %H:%M:%S")
Exit Code: $TEST_EXIT_CODE
Branch: $(git rev-parse --abbrev-ref HEAD)
Commit: $(git rev-parse --short HEAD)
Usuario: $(whoami)
Host: $(hostname)
EOF
```

#### 6. Limpiar historial antiguo
```bash
HISTORY_COUNT=$(ls -1 "$HISTORY_DIR" | wc -l)
if [ "$HISTORY_COUNT" -gt "$MAX_HISTORY" ]; then
    TO_DELETE=$((HISTORY_COUNT - MAX_HISTORY))
    ls -1t "$HISTORY_DIR" | tail -n "$TO_DELETE" | while read old_dir; do
        rm -rf "$HISTORY_DIR/$old_dir"
    done
fi
```

#### 7. Generar reporte
```bash
allure generate "$RESULTS_DIR" -o "$REPORT_DIR" --clean
```

**Cuándo usar:** Para ejecutar tests y mantener historial automático

---

### `view_history.sh`
**Ubicación:** `/view_history.sh`  
**Propósito:** Ver un reporte histórico individual

**Qué hace:**
```bash
# 1. Lista reportes disponibles
for dir in $(ls -1t "$HISTORY_DIR"); do
    # Muestra fecha, estado, etc.
done

# 2. Usuario selecciona número
read choice

# 3. Abre reporte seleccionado
allure serve "$HISTORY_DIR/$selected_dir/allure-results"
```

**Cuándo usar:** Para revisar una ejecución pasada específica

---

### `view_historical_trends.sh`
**Ubicación:** `/view_historical_trends.sh`  
**Propósito:** Ver estadísticas y tendencias consolidadas

**Secciones principales:**

#### 1. Análisis estadístico en consola
```bash
for dir in $(ls -1t "$HISTORY_DIR"); do
    # Lee metadata
    # Cuenta tests passed/failed
    # Muestra tabla
done
```

#### 2. Combinar resultados
```bash
for dir in $(ls -1t "$HISTORY_DIR" | head -n 10); do
    cp -r "$HISTORY_DIR/$dir/allure-results"/* "$TRENDS_RESULTS/"
done
```

#### 3. Generar reporte consolidado
```bash
allure generate "$TRENDS_RESULTS" -o "$TRENDS_DIR/report" --clean
allure open "$TRENDS_DIR/report"
```

**Cuándo usar:** Para análisis de tendencias de todas las ejecuciones

---

## Directorios de Datos

### `allure-results/`
**Propósito:** Resultados temporales de la última ejecución

**Contenido:**
```
allure-results/
├── {uuid}-result.json           # Resultado de un test
├── {uuid}-container.json        # Metadata de suite
├── {uuid}-attachment.png        # Screenshot
└── history/                     # Datos de trending (opcional)
    └── history.json
```

**Ejemplo de *-result.json:**
```json
{
  "uuid": "abc123",
  "name": "test_login_correcto",
  "status": "passed",
  "start": 1706184000000,
  "stop": 1706184002500,
  "labels": [
    {"name": "feature", "value": "Autenticación"},
    {"name": "severity", "value": "critical"}
  ],
  "steps": [...],
  "attachments": [...]
}
```

**¿Se versiona en git?** ❌ NO (está en `.gitignore`)

---

### `allure-report/`
**Propósito:** Reporte HTML generado

**Contenido:**
```
allure-report/
├── index.html                   # Página principal
├── app.js                       # JavaScript
├── styles.css                   # CSS
├── favicon.ico                  # Ícono
├── data/
│   ├── suites.json             # Tests procesados
│   ├── test-cases/             # Casos individuales
│   ├── timeline.json           # Timeline data
│   └── graph.json              # Gráficos
├── widgets/
│   ├── summary.json            # Resumen
│   ├── graph.json              # Trending
│   └── ...
├── history/                     # Trending data
│   ├── duration-trend.json
│   ├── retry-trend.json
│   └── history.json
└── plugins/
    └── ...
```

**¿Se versiona en git?** ❌ NO (está en `.gitignore`)

---

### `allure-history/`
**Propósito:** Historial permanente (últimas 20 ejecuciones)

**Contenido:**
```
allure-history/
├── 20250125_163000/
│   ├── allure-results/
│   │   ├── {uuid}-result.json
│   │   ├── {uuid}-container.json
│   │   └── screenshots/
│   │       └── test_name.png
│   └── metadata.txt
├── 20250125_143000/
│   └── ...
└── 20250125_103000/
    └── ...
```

**Ejemplo de metadata.txt:**
```
Fecha y Hora: 2025-01-25 14:30:22
Exit Code: 0
Branch: main
Commit: a1b2c3d
Usuario: rommel
Host: MacBook-Pro
```

**¿Se versiona en git?** ⚠️ Opcional (comentar línea en `.gitignore`)

---

### `allure-trends/`
**Propósito:** Reporte consolidado temporal

**Contenido:**
```
allure-trends/
├── combined-results/            # JSON combinados de 10 ejecuciones
│   ├── {uuid}-result.json
│   ├── {uuid}-result.json
│   └── ...
└── report/                      # HTML generado
    ├── index.html
    └── ...
```

**¿Se versiona en git?** ❌ NO (está en `.gitignore`)

---

## Archivos de Configuración del Sistema

### `.gitignore`
**Ubicación:** `/.gitignore`  
**Líneas relevantes:**
```gitignore
# Allure reports
allure-results/
allure-report/

# Allure history (optional)
allure-history/

# Allure trends
allure-trends/
```

**¿Por qué ignorar?**
- `allure-results/` - Temporal, se regenera
- `allure-report/` - Generado, no es código fuente
- `allure-trends/` - Temporal, se regenera
- `allure-history/` - Opcional, puede ser muy grande

---

## Mapa de Archivos por Función

### Para Generar Reportes
```
pytest.ini              ← Configuración
conftest.py             ← Hooks
tests/*.py              ← Tests con decoradores
allure-results/         ← Output de pytest
allure-report/          ← Output de Allure CLI
```

### Para Historial
```
run_tests_with_history.sh  ← Script
allure-history/            ← Almacenamiento
metadata.txt               ← Info de ejecución
```

### Para Tendencias
```
view_historical_trends.sh  ← Script
allure-history/            ← Fuente de datos
allure-trends/             ← Consolidado
```

---

## Dependencias entre Archivos

```
pytest.ini
    │
    ├─► Configura dónde guardar resultados
    └─► Activa allure-pytest plugin
            │
            ▼
        conftest.py
            │
            ├─► Define fixtures (page, browser)
            └─► Hook para screenshots
                    │
                    ▼
                tests/*.py
                    │
                    ├─► Usa fixtures
                    ├─► Usa decoradores @allure.*
                    └─► Ejecuta con pytest
                            │
                            ▼
                        allure-results/
                            │
                            ├─► JSON files
                            └─► Screenshots
                                    │
                                    ▼
                        run_tests_with_history.sh
                            │
                            ├─► Copia a allure-history/
                            └─► Ejecuta allure generate
                                    │
                                    ▼
                                allure-report/
                                    │
                                    └─► HTML visual
```

---

## Checklist de Archivos Necesarios

Para que los reportes funcionen, necesitas:

- ✅ `pytest.ini` con `--alluredir=allure-results`
- ✅ `conftest.py` con hook de screenshots
- ✅ `requirements.txt` con `allure-pytest`
- ✅ Tests con decoradores `@allure.*`
- ✅ Allure CLI instalado (`brew install allure`)

Opcionales para funciones avanzadas:
- ⭐ `run_tests_with_history.sh` para historial
- ⭐ `view_historical_trends.sh` para tendencias

---

## Resumen

| Archivo/Directorio | Propósito | ¿Se modifica? | ¿En git? |
|-------------------|-----------|---------------|----------|
| `pytest.ini` | Config | Raramente | ✅ Sí |
| `conftest.py` | Hooks | Raramente | ✅ Sí |
| `tests/*.py` | Tests | Siempre | ✅ Sí |
| `*.sh` | Scripts | Raramente | ✅ Sí |
| `allure-results/` | Datos temp | Automático | ❌ No |
| `allure-report/` | HTML | Automático | ❌ No |
| `allure-history/` | Historial | Automático | ⚠️ Opcional |
| `allure-trends/` | Consolidado | Automático | ❌ No |

---

**Siguiente:** [04-debugging.md](./04-debugging.md)
