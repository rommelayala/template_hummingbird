# 🔄 Flujo de Datos del Sistema de Reportes

Este documento explica **paso a paso** cómo fluyen los datos desde que ejecutas un test hasta que ves el reporte visual.

---

## Flujo Completo Simplificado

```
Test Code ───▶ pytest ───▶ JSON ───▶ Allure CLI ───▶ HTML ───▶ Navegador
```

Ahora vamos paso por paso en detalle...

---

## PASO 1: Escribir el Test

### Archivo: `tests/test_login.py`

```python
import allure
from playwright.sync_api import Page

@allure.feature("Autenticación")           # ← Metadata 1
@allure.story("Login exitoso")             # ← Metadata 2
@allure.severity(allure.severity_level.CRITICAL)  # ← Metadata 3
def test_login_correcto(page: Page):
    with allure.step("Navegar a login"):   # ← Metadata 4
        page.goto("https://example.com")
    
    with allure.step("Ingresar credenciales"):  # ← Metadata 5
        page.fill("#user", "admin")
        page.fill("#pass", "1234")
        
    with allure.step("Click en login"):    # ← Metadata 6
        page.click("#login-btn")
        
    # Assertion
    assert "dashboard" in page.url         # ← Resultado
```

**Qué pasa aquí:**
- Los `@allure.*` decoradores se **guardan como metadata**
- Los `allure.step()` se **registran como pasos**
- El **resultado** (pass/fail) se captura automáticamente

---

## PASO 2: Ejecutar con pytest

### Comando:
```bash
pytest tests/test_login.py
```

### Qué hace pytest:

1. **Lee el archivo** `pytest.ini`:
```ini
addopts = --alluredir=allure-results
```

2. **Activa el plugin** `allure-pytest` automáticamente

3. **Ejecuta el test** línea por línea:
```
✓ Función test_login_correcto() empieza
✓ Decoradores leídos (@allure.feature, etc.)
✓ Step 1: "Navegar a login" - ejecutado
✓ Step 2: "Ingresar credenciales" - ejecutado
✓ Step 3: "Click en login" - ejecutado
✓ Assertion: "dashboard" in URL - ¿Pasó?
    → SÍ → status = "passed"
    → NO → status = "failed"
```

4. **Llama al hook** en `conftest.py`:
```python
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Si el test falló:
    if report.failed:
        # Captura screenshot
        page.screenshot(path="screenshot.png")
        # Adjunta a Allure
        allure.attach.file("screenshot.png", ...)
```

---

## PASO 3: Generar JSON (allure-pytest)

### El plugin `allure-pytest` automáticamente crea:

**Archivo generado:** `allure-results/abc123-result.json`

```json
{
  "uuid": "abc123-456def-789ghi",
  "name": "test_login_correcto",
  "fullName": "tests.test_login::test_login_correcto",
  "status": "passed",
  "start": 1706184000000,
  "stop": 1706184002500,
  "labels": [
    {"name": "feature", "value": "Autenticación"},
    {"name": "story", "value": "Login exitoso"},
    {"name": "severity", "value": "critical"}
  ],
  "steps": [
    {
      "name": "Navegar a login",
      "status": "passed",
      "start": 1706184000100,
      "stop": 1706184000500
    },
    {
      "name": "Ingresar credenciales",
      "status": "passed",
      "start": 1706184000600,
      "stop": 1706184001200
    },
    {
      "name": "Click en login",
      "status": "passed",
      "start": 1706184001300,
      "stop": 1706184002400
    }
  ],
  "attachments": [
    {
      "name": "Screenshot - test_login",
      "source": "abc123-screenshot.png",
      "type": "image/png"
    }
  ]
}
```

**También genera:**

`allure-results/def456-container.json` (metadata del suite):
```json
{
  "uuid": "def456",
  "name": "tests.test_login",
  "children": ["abc123-456def-789ghi"]
}
```

`allure-results/abc123-screenshot.png` (si hubo fallo)

---

## PASO 4: Guardar en Historial (run_suite.sh)
### Si usaste `./run_suite.sh`:

```bash
# El script hace:
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
# Crea carpeta versionada
mkdir -p execution-history/$TIMESTAMP/

# 1. Copia Allure Results
cp -r allure-results/ execution-history/$TIMESTAMP/

# 2. Copia Cucumber Report
cp -r json-results/cucumber_report.json execution-history/$TIMESTAMP/cucumber_$TIMESTAMP.json

# 3. Guarda metadata
cat > execution-history/$TIMESTAMP/metadata.txt <<EOF
Run ID: 20250125_143022
Date: ...
Environment: DEV
Exit Code: 0
Branch: main
Commit: a1b2c3d
Usuario: rommel
Host: MacBook-Pro
EOF
```

**Resultado:**
```
execution-history/
└── 20250125_143022/
    ├── allure-results/        # Resultados Allure
    ├── cucumber_2025...json   # Resultados Cucumber
    ├── cluecumber-report/     # Reporte BDD generado
    └── metadata.txt           # Info ejecución
```

---

## PASO 5: Generar HTML (Allure CLI)

### Comando:
```bash
allure generate allure-results -o allure-report --clean
```

### Qué hace Allure:

1. **Lee todos los JSON** en `allure-results/`:
```
Leyendo: abc123-result.json
Leyendo: def456-container.json
Procesando attachments...
```

2. **Procesa los datos:**
```
Feature "Autenticación" encontrado
  └─ Story "Login exitoso"
      └─ Test "test_login_correcto" (PASSED)
          ├─ Step 1: Navegar a login (0.4s)
          ├─ Step 2: Ingresar credenciales (0.6s)
          └─ Step 3: Click en login (1.1s)
          Duration total: 2.5s
```

3. **Genera gráficos de tendencias:**
   - Si existe `allure-results/history/` de ejecuciones anteriores
   - Crea gráfico de trend (passed/failed en el tiempo)
   - Crea gráfico de duration (duración en el tiempo)

4. **Crea archivos HTML:**
```
allure-report/
├── index.html              # Página principal
├── app.js                  # JavaScript para interactividad
├── styles.css              # Estilos
├── data/
│   ├── suites.json        # Datos de tests procesados
│   ├── graph.json         # Datos para gráficos
│   └── timeline.json      # Datos de timeline
└── widgets/
    ├── summary.json       # Dashboard summary
    └── trend.json         # Trending data
```

---

## PASO 6: Abrir en Navegador

### Comando:
```bash
allure open allure-report
# O
allure serve allure-results  # Genera + abre en un paso
```

### Qué hace:

1. **Inicia servidor HTTP** local:
```
Starting web server...
Server started at http://192.168.1.100:54321
```

2. **Abre navegador** automáticamente

3. **El navegador carga** `index.html`:
```javascript
// JavaScript en el navegador lee:
fetch('data/suites.json')
  .then(data => {
    // Renderiza tests
    // Crea gráficos
    // Muestra estadísticas
  })
```

---

## Flujo Visual Detallado

```
┌──────────────────────────────────────────────────────────┐
│  PASO 1: Test Code                                       │
│  @allure.feature("Auth")                                 │
│  @allure.step("Login")                                   │
│  def test_login(): ...                                   │
└────────────────────┬─────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────┐
│  PASO 2: pytest ejecución                                │
│  ✓ Lee decoradores                                       │
│  ✓ Ejecuta test                                          │
│  ✓ Captura resultado (pass/fail)                         │
│  ✓ Llama hook de conftest                               │
└────────────────────┬─────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────┐
│  PASO 3: allure-pytest                                   │
│  ✓ Genera abc123-result.json                            │
│    - name: "test_login"                                  │
│    - status: "passed"                                    │
│    - labels: [feature, story, severity]                  │
│    - steps: [Step 1, Step 2, Step 3]                     │
│    - duration: 2.5s                                      │
│  ✓ Guarda screenshot (si falló)                          │
└────────────────────┬─────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────┐
│  allure-results/                                         │
│  ├── abc123-result.json                                  │
│  ├── def456-container.json                               │
│  └── abc123-screenshot.png                               │
└────────────────────┬─────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
        ▼                         ▼
┌───────────────┐       ┌──────────────────┐
│ PASO 4:       │       │  PASO 5:         │
│ Historial     │       │  Allure CLI      │
│ (opcional)    │       │                  │
│               │       │  Procesa JSON    │
│ Copia a:      │       │  Genera HTML     │
│ allure-       │       │  Crea gráficos   │
│ history/      │       │                  │
│ TIMESTAMP/    │       └────────┬─────────┘
└───────────────┘                │
                                 ▼
                      ┌──────────────────┐
                      │ allure-report/   │
                      │ ├── index.html   │
                      │ ├── data/        │
                      │ └── widgets/     │
                      └────────┬─────────┘
                               │
                               ▼
                      ┌──────────────────┐
                      │  PASO 6:         │
                      │  Navegador       │
                      │                  │
                      │  Usuario ve:     │
                      │  📊 Dashboard    │
                      │  ✅ Tests        │
                      │  📈 Gráficos     │
                      │  📸 Screenshots  │
                      └──────────────────┘
```

---

## Ejemplo Práctico con Tiempos Reales

Siguiendo un test real:

```
T+0ms     : Ejecutas ./run_suite.sh --env=DEV --open=cluecumber
T+100ms   : Script prepara directorios (limpia json-results)
T+200ms   : Script copia historial previo (para tendencias)
T+500ms   : pytest inicia (genera JSONs en allure y json-results)
T+700ms   : Step 1.. Step 2.. Step 3...
T+3000ms  : Test completado
T+3200ms  : Maven genera reporte Cluecumber (desde json-results)
T+4500ms  : Script archiva TODO en execution-history/TIMESTAMP/
T+4800ms  : Script genera reporte Allure
T+5500ms  : Script abre reporte Cluecumber en navegador
T+6000ms  : Usuario ve el reporte ✅
```

**Total:** ~6 segundos desde ejecución hasta visualización completa

---

## Transformación de Datos

### Test → JSON → HTML

**En el test:**
```python
@allure.severity(allure.severity_level.CRITICAL)
```

**En el JSON:**
```json
"labels": [
  {"name": "severity", "value": "critical"}
]
```

**En el HTML:**
```html
<span class="badge badge-critical">CRITICAL</span>
```

---

**En el test:**
```python
with allure.step("Navegar a login"):
    page.goto("...")
```

**En el JSON:**
```json
"steps": [
  {
    "name": "Navegar a login",
    "status": "passed",
    "start": 1706184000100,
    "stop": 1706184000500
  }
]
```

**En el HTML:**
```html
<div class="step step-passed">
  <span class="step-name">▶ Navegar a login</span>
  <span class="step-duration">0.4s</span>
  <span class="step-status">✓</span>
</div>
```

---

## Puntos de Control para Debugging

Si algo no aparece en el reporte, verifica en orden:

1. **¿El decorador está bien?**
   ```python
   @allure.feature("Auth")  # ¿Está antes de def test_...?
   ```

2. **¿El JSON se generó?**
   ```bash
   ls -la allure-results/
   # ¿Hay archivos *-result.json?
   ```

3. **¿El JSON tiene los datos?**
   ```bash
   cat allure-results/*-result.json | grep "feature"
   # ¿Aparece "feature": "Auth"?
   ```

4. ** El HTML se generó?**
   ```bash
   ls -la allure-report/
   # ¿Hay index.html?
   ```

5. **¿El navegador carga correctamente?**
   - Abrir DevTools (F12)
   - Ver Console - ¿Errores JavaScript?
   - Ver Network - ¿Archivos JSON cargados?

---

## Resumen del Flujo

| Paso | Componente | Input | Output | Tiempo |
|------|-----------|-------|--------|--------|
| 1 | Test Code | Código Python | Decoradores | - |
| 2 | pytest | Test | Ejecución | ~2s |
| 3 | allure-pytest | Resultados | JSON | ~100ms |
| 4 | Script | JSON | Historia | ~200ms |
| 5 | Allure CLI | JSON | HTML | ~1s |
| 6 | Navegador | HTML | Visual | ~500ms |

---

**Siguiente:** [03-archivos-involucrados.md](./03-archivos-involucrados.md)
