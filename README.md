# 🐦 Hummingbird

Framework de automatización de pruebas E2E basado en **Playwright + Python** con reportes profesionales usando **Allure**.

---

## ¿Qué es este proyecto?

Hummingbird es un template moderno para automatización de tests E2E que combina:
-  **Playwright** - Framework de testing de Microsoft (rápido y confiable)
-  **Python** - Lenguaje simple y poderoso
-  **pytest** - Framework de testing profesional
-  **Page Object Model** - Patrón de diseño para tests mantenibles
-  **Allure Reports** - Reportes visuales e interactivos (similar a Karate/Selenium)

---

## Características

-  **Reportes Allure** - Visualización profesional de resultados
-  **Screenshots automáticos** - Captura de pantalla en fallos
-  **Organización BDD** - Tests por Features y Stories
-  **Docker support** - Ejecución en contenedores
-  **Fixtures configurables** - Browser, context, page reutilizables
-  **Markers personalizados** - Organización por smoke, regression, etc.
-  **Ejecución paralela** - Tests más rápidos con pytest-xdist

---

## Requisitos

- **Python 3.10+** → [Descargar Python](https://www.python.org/downloads/)
- **Homebrew** (macOS) o gestor de paquetes equivalente
- **Allure** para reportes (se instala automáticamente)

---

## Instalación

### 1. Clonar el Repositorio
```bash
git clone <repository-url>
cd template_hummingbird
```

### 2. Crear Entorno Virtual
```bash
# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
source venv/bin/activate

# En Windows:
# venv\Scripts\activate.bat
```

### 3. Instalar Dependencias
```bash
# Actualizar pip
pip install --upgrade pip

# Instalar paquetes de Python
pip install -r requirements.txt

# Instalar navegador Chromium
playwright install chromium
```

### 4. Instalar Allure (para reportes)
```bash
# macOS
brew install allure

# Linux (Debian/Ubuntu)
sudo apt-add-repository ppa:qameta/allure
sudo apt-get update 
sudo apt-get install allure

# Windows (con Scoop)
scoop install allure
```

### 5. Dar Permisos de Ejecución a los Scripts
```bash
# Dar permisos de ejecución a los scripts de reportes
chmod +x generate_report.sh
chmod +x run_tests_with_history.sh
chmod +x view_history.sh
chmod +x view_historical_trends.sh

# Verificar permisos (opcional)
ls -la *.sh
```

**Nota:** Este paso es necesario en macOS y Linux. En Windows con Git Bash, los scripts deberían funcionar directamente.

---

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
```bash
# Solo tests smoke
pytest -m smoke

# Solo tests de login
pytest -m login

# Excluir tests lentos
pytest -m "not slow"
```

### Ejecutar en Paralelo
```bash
# Automático (usa todos los CPUs)
pytest -n auto

# Específico (4 workers)
pytest -n 4
```

---

## Generar Reportes Allure

### Opción 1: Con Historial (Recomendado) 🆕
```bash
# Ejecuta tests y guarda historial automáticamente
./run_tests_with_history.sh
```

**Características:**
- ✅ Ejecuta todos los tests
- ✅ Guarda resultados en `allure-history/` con timestamp
- ✅ Mantiene automáticamente los últimos **20 reportes**
- ✅ Genera **gráficos de tendencias** históricas
- ✅ Guarda metadata (fecha, branch, commit, usuario)
- ✅ Pregunta si deseas abrir el reporte

### Opción 2: Ver Reportes Históricos Individuales
```bash
# Lista y visualiza reportes guardados
./view_history.sh
```

**Qué hace:**
- 📋 Muestra lista de reportes con fecha y estado (PASSED/FAILED)
- 🔍 Permite seleccionar cualquier reporte anterior
- 📊 Abre el reporte histórico seleccionado

Ejemplo de salida:
```
Reportes disponibles:
 1) 24/01/2025 14:30:22 | ✅ PASSED | 20250124_143022
 2) 24/01/2025 12:15:10 | ⚠️  FAILED | 20250124_121510
 3) 24/01/2025 10:30:45 | ✅ PASSED | 20250124_103045
```

### Opción 3: Ver Tendencias y Estadísticas Históricas 🆕
```bash
# Genera resumen estadístico y gráficos de tendencias
./view_historical_trends.sh
```

**Qué muestra:**
- 📊 **Tabla estadística** en consola con todas las ejecuciones
- 📈 **Gráficos de tendencias** consolidados (últimas 10 ejecuciones)
- ✅ **Tasa de éxito** general de tests
- 🎯 **Identificación de tests inestables** (flaky tests)
- 📉 **Evolución de duración** de tests

Ejemplo de output en consola:
```
╔════════════════════════════════════════════════════╗
║          RESUMEN ESTADÍSTICO HISTÓRICO              ║
╚════════════════════════════════════════════════════╝

#    Fecha/Hora           Estado       Passed    Failed
────────────────────────────────────────────────────────
1    24/01/2025 14:30    ✅ PASSED        2         0
2    24/01/2025 12:15    ❌ FAILED        1         1
3    24/01/2025 10:30    ✅ PASSED        2         0

╔════════════════════════════════════════════════════╗
║              ESTADÍSTICAS TOTALES                   ║
╚════════════════════════════════════════════════════╝

📊 Total de Ejecuciones: 3
✅ Ejecuciones Exitosas: 2 (67%)
❌ Ejecuciones Fallidas: 1 (33%)
📈 Tasa de Éxito General: 83%
```

Luego abre un **reporte HTML consolidado** con gráficos interactivos.

### Opción 4: Script Simple (Sin Historial)
```bash
# Solo genera y abre el reporte actual
./generate_report.sh
```

### Opción 4: Comandos Manuales
```bash
# Ejecuta tests y abre reporte automáticamente
./generate_report.sh
```

### Opción 2: Comandos Manuales
```bash
# 1. Ejecutar tests (genera allure-results/)
pytest

# 2. Generar y abrir reporte
allure serve allure-results

# O generar reporte estático
allure generate allure-results -o allure-report --clean
```

El reporte mostrará:
- Dashboard con estadísticas
- Tests passed/failed con detalles
- Screenshots en fallos (automático)
- Timeline de ejecución
- Gráficos y tendencias
- Organización por Features/Stories
- **🆕 Tendencias históricas** (si usas historial)
- **🆕 Comparación entre ejecuciones**

### Gráficos de Tendencias (Con Historial)

Cuando usas `./run_tests_with_history.sh`, el reporte incluye:

**Graphs → Trend Chart**
- Evolución de tests passed/failed en el tiempo
- Duración de ejecución de tests
- Comparación entre las últimas ejecuciones

**History por Test**
- Click en cualquier test → pestaña "History"
- Ver resultados de ese test en las últimas 5-10 ejecuciones
- Identificar tests inestables (flaky tests)

---

## Arquitectura del Proyecto

```
template_hummingbird/
├── lib/                        # Utilidades y helpers
│   ├── config.py              # Configuración (URLs, credenciales)
│   ├── utilities.py           # Funciones auxiliares (legacy)
│   └── pages/                 # Page Object Model
│       └── login_page.py      # Página de login
│
├── tests/                     # Tests (pytest)
│   └── test_login.py         # Pruebas de login
│
├── integrations/              # Integraciones externas
│   └── elastic.py            # Elasticsearch (legacy)
│
├── reporting/                 # Funcionalidad de reportes
│   └── __init__.py           # Placeholder para reportes custom
│
├── allure-history/            # 🆕 Historial de ejecuciones (últimas 20)
│   ├── YYYYMMDD_HHMMSS/      # Cada ejecución con timestamp
│   │   ├── allure-results/   # Resultados completos
│   │   └── metadata.txt      # Info (fecha, branch, commit, etc.)
│   └── ...
│
├── conftest.py                # Fixtures de pytest + Allure hooks
├── pytest.ini                 # Configuración de pytest
├── requirements.txt           # Dependencias Python
├── Dockerfile                 # Containerización
├── generate_report.sh         # Script simple para reportes
├── run_tests_with_history.sh  # 🆕 Ejecutar con historial
├── view_history.sh            # 🆕 Ver reportes históricos
└── .gitlab-ci.yml            # CI/CD pipeline (legacy)
```

---

## Ejemplo de Test

```python
import allure
from playwright.sync_api import Page

@allure.feature("Autenticación")
@allure.story("Login exitoso")
@allure.severity(allure.severity_level.CRITICAL)
def test_login_exitoso(page: Page):
    with allure.step("Navegar a la página de login"):
        page.goto("https://www.saucedemo.com/")
    
    with allure.step("Ingresar credenciales válidas"):
        page.fill("#user-name", "standard_user")
        page.fill("#password", "secret_sauce")
        page.click("#login-button")
    
    with allure.step("Verificar redirección exitosa"):
        assert "inventory.html" in page.url
```

---

## Markers Disponibles

Configura tus tests con markers en `pytest.ini`:

- `@pytest.mark.smoke` - Tests rápidos y críticos
- `@pytest.mark.regression` - Suite completa de regresión
- `@pytest.mark.login` - Tests de autenticación
- `@pytest.mark.demo` - Tests para demos
- `@pytest.mark.slow` - Tests lentos
- `@pytest.mark.playwright` - Tests intensivos de Playwright

---

## Docker

### Construir Imagen
```bash
docker build -t hummingbird:latest .
```

### Ejecutar Tests en Docker
```bash
docker run --rm hummingbird:latest
```

---

## Configuración

### Variables de Entorno (Recomendado)

Crea un archivo `.env`:
```bash
BASE_URL=https://www.saucedemo.com/
TEST_USERNAME=standard_user
TEST_PASSWORD=secret_sauce
HEADLESS=true
```

### Modo Headless

Edita `conftest.py` línea 18:
```python
# Con interfaz gráfica (desarrollo)
browser = playwright_instance.chromium.launch(headless=False)

# Sin interfaz gráfica (CI/CD)
browser = playwright_instance.chromium.launch(headless=True)
```

---

## Documentación Adicional

- [Guía completa de Allure Reports](./allure_reports_guia.md) (en artifacts)
- [Sistema de Historial de Reportes](./allure_historial_guia.md) (en artifacts) 🆕
- [Playwright Documentation](https://playwright.dev/python/)
- [pytest Documentation](https://docs.pytest.org/)
- [Allure Documentation](https://docs.qameta.io/allure/)

---

## Mejoras Recientes

- ✅ Código duplicado eliminado en `conftest.py`
- ✅ Imports legacy comentados y documentados
- ✅ Allure Reports integrado con screenshots automáticos
- ✅ Tests mejorados con decoradores Allure
- ✅ **🆕 Sistema de historial automático (últimas 20 ejecuciones)**
- ✅ **🆕 Gráficos de tendencias históricas**
- ✅ **🆕 Metadata de ejecución (branch, commit, usuario)**
- ✅ Script `generate_report.sh` para reportes simples
- ✅ Documentación actualizada y typos corregidos

---

## Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## Licencia

Este proyecto está bajo la licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

---

## Autor

**Rommel Ayala** - *Trabajo inicial*

---
