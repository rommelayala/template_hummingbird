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

### `run_suite.sh`
**Ubicación:** `/run_suite.sh`
**Propósito:** Script maestro para ejecución y reportes (Allure + Cluecumber)

**Funciones principales:**
1. **Ejecución:** Corre `pytest` con configuración para ambos reportes.
2. **Historial:** Crea carpetas timestamped en `execution-history/`.
3. **Limpieza:** Limpia `json-results` y `allure-results` para evitar duplicados.
4. **Generación:** Orquesta Allure CLI y Maven Cluecumber.
5. **Archivado:** Guarda todos los artefactos de la ejecución.

**Uso:**
```bash
./run_suite.sh --env=DEV --open=all
```

---

## Directorios de Datos

### `execution-history/`
**Propósito:** Historial unificado de todas las ejecuciones.
**Contenido:** Carpetas con timestamp (ej. `20251207_220000/`) que contienen:
- `allure-results/`
- `cluecumber-report/`
- `cucumber.json`
- `metadata.txt`

### `cluecumber-report/`
**Propósito:** Reporte HTML estilo BDD generado por Maven.
**Contenido:** `index.html` y recursos CSS/JS.

### `json-results/`
**Propósito:** Directorio temporal para el `cucumber.json` de la ejecución actual. Se limpia antes de cada ejecución.

### `allure-results/`
**Propósito:** Resultados temporales de Allure. Se regenera en cada ejecución.

---

## Archivos de Configuración del Sistema

### `.gitignore`
**Ubicación:** `/.gitignore`  
**Líneas relevantes:**
```gitignore
# Unified Report History
execution-history/

# Cluecumber Reports
cluecumber-report/
json-results/
cucumber_report.json

# Allure reports
allure-results/
allure-report/
allure-trends/
```

**¿Por qué ignorar?**
- `execution-history/` - Puede crecer mucho, mejor no versionar.
- `json-results/` - Temporal, se limpia en cada run.
- `cluecumber-report/` - Generado, no es código fuente.
- `allure-results/` - Temporal.

---

## Mapa de Archivos por Función

### Para Generar Reportes
```
pytest.ini              ← Configuración
conftest.py             ← Hooks
tests/*.py              ← Tests con decoradores
allure-results/         ← Output de pytest
json-results/           ← Output para Cluecumber
```

### Para Historial y Orquestación
```
run_suite.sh               ← Script Maestro
execution-history/         ← Almacenamiento unificado
metadata.txt               ← Info de ejecución
cucumber_report.json       ← Fuente para Cluecumber
```

---

## Dependencias entre Archivos

```
pytest.ini
    │
    ├─► Configura dónde guardar resultados (allure-results)
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
                    ├─► Usa fixtures & decoradores
                    └─► Ejecuta con pytest
                            │
                            ▼
    ┌───────────────────────┴───────────────────────┐
    │                                               │
allure-results/ (JSON)                       json-results/ (Cucumber JSON)
    │                                               │
    └───────────────────────┬───────────────────────┘
                            ▼
                       run_suite.sh
                            │
                            ├─► Copia a execution-history/
                            ├─► Ejecuta 'allure generate'
                            └─► Ejecuta 'mvn cluecumber'
                                    │
                                    ▼
                            ┌───────┴───────┐
                      allure-report/   cluecumber-report/
```

---

## Checklist de Archivos Necesarios

Para que los reportes funcionen, necesitas:

- ✅ `pytest.ini` con `--alluredir=allure-results`
- ✅ `conftest.py` con hook de screenshots
- ✅ `requirements.txt` con `allure-pytest`
- ✅ `run_suite.sh` (Script Maestro)
- ✅ `pom.xml` en `reporting/cluecumber/` (para reporte BDD)

---

## Resumen

| Archivo/Directorio | Propósito | ¿Se modifica? | ¿En git? |
|-------------------|-----------|---------------|----------|
| `pytest.ini` | Config | Raramente | ✅ Sí |
| `conftest.py` | Hooks | Raramente | ✅ Sí |
| `tests/*.py` | Tests | Siempre | ✅ Sí |
| `run_suite.sh` | Orchestrator | Raramente | ✅ Sí |
| `allure-results/` | Datos temp | Automático | ❌ No |
| `json-results/` | Datos temp | Automático | ❌ No |
| `execution-history/`| Historial | Automático | ❌ No |
| `cluecumber-report/`| HTML BDD | Automático | ❌ No |

---

**Siguiente:** [04-debugging.md](./04-debugging.md)
