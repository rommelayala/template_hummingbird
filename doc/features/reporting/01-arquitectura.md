# 🏗️ Arquitectura del Sistema de Reportes

## Visión General

El sistema de reportes combina **3 componentes principales** que trabajan juntos:

```
┌─────────────┐      ┌──────────────┐      ┌───────────────┐
│   pytest    │ ───▶ │ allure-pytest│ ───▶ │  Allure CLI   │
│  (tests)    │      │  (plugin)    │      │  (reportes)   │
└─────────────┘      └──────────────┘      └───────────────┘
      │                     │                      │
      │                     │                      │
      ▼                     ▼                      ▼
  Ejecuta tests      Genera JSON           Crea HTML
                     con metadata          con gráficos
```

---

## Componentes Principales

### 1. pytest + conftest.py
**Responsabilidad:** Ejecutar tests y capturar datos

**Archivos:**
- `conftest.py` - Fixtures y hooks
- `pytest.ini` - Configuración

**Qué hace:**
- Ejecuta los tests con decoradores `@allure.*`
- Hook `pytest_runtest_makereport` captura screenshots en fallos
- Pasa datos a allure-pytest

---

### 2. allure-pytest (Plugin)
**Responsabilidad:** Convertir datos de pytest a formato Allure

**Instalado vía:** `pip install allure-pytest`

**Qué hace:**
- Lee decoradores (`@allure.feature`, `@allure.step`, etc.)
- Genera archivos JSON en `allure-results/`
- Guarda screenshots adjuntos
- Crea metadata (duración, status, timestamp)

**Output:**
```
allure-results/
├── abc123-result.json        # Resultado del test
├── def456-container.json     # Metadata del suite
├── attachments/              # Screenshots
└── history/                  # Para trending
```

---

### 3. Allure CLI
**Responsabilidad:** Generar reportes HTML desde JSON

**Instalado vía:** `brew install allure`

**Comandos principales:**
```bash
allure serve allure-results          # Genera + abre navegador
allure generate allure-results       # Solo genera HTML
allure open allure-report            # Abre reporte ya generado
```

**Output:**
```
allure-report/
├── index.html               # Reporte principal
├── data/                    # Datos procesados
├── widgets/                 # Gráficos interactivos
└── history/                 # Trending data
```

---

## Arquitectura en Capas

```
┌─────────────────────────────────────────────────┐
│  CAPA 4: Presentación (Navegador)               │
│  → HTML, CSS, JavaScript                        │
│  → Gráficos interactivos                        │
└─────────────────────────────────────────────────┘
                    ▲
                    │
┌─────────────────────────────────────────────────┐
│  CAPA 3: Generación (Allure CLI)                │
│  → Procesa JSON                                 │
│  → Genera HTML estático                         │
│  → Crea gráficos de tendencias                  │
└─────────────────────────────────────────────────┘
                    ▲
                    │
┌─────────────────────────────────────────────────┐
│  CAPA 2: Recolección (allure-pytest)            │
│  → Captura resultados de tests                  │
│  → Genera JSON con metadata                     │
│  → Adjunta screenshots                          │
└─────────────────────────────────────────────────┘
                    ▲
                    │
┌─────────────────────────────────────────────────┐
│  CAPA 1: Ejecución (pytest)                     │
│  → Ejecuta tests                                │
│  → Captura fallos                               │
│  → Llama hooks de conftest.py                   │
└─────────────────────────────────────────────────┘
```

---

## Sistema de Historial

### Sin Historial (Simple)
```
pytest ───▶ allure-results/ ───▶ allure-report/
                                       │
                                       ▼
                                 Navegador
```

### Con Historial (Avanzado)
```
pytest ───▶ allure-results/ ───┬───▶ allure-report/
                                │         │
                                │         ▼
                                │    Navegador
                                │
                                └───▶ allure-history/TIMESTAMP/
                                      (guardado permanente)
```

**Script:** `run_tests_with_history.sh`

**Funciones adicionales:**
1. Copia `allure-results/` a `allure-history/TIMESTAMP/`
2. Guarda metadata (branch, commit, fecha)
3. Mantiene solo últimas 20 ejecuciones
4. Preserva `history/` folder para trending

---

## Sistema de Tendencias Consolidadas

```
allure-history/
├── 20250125_143022/
├── 20250125_121510/
└── 20250125_103045/
        │
        ▼
  [Combine Results]
        │
        ▼
allure-trends/
└── combined-results/ ───▶ Reporte Consolidado
                               │
                               ▼
                          Navegador
```

**Script:** `view_historical_trends.sh`

**Proceso:**
1. Lee todos los reportes en `allure-history/`
2. Combina JSONs de últimas 10 ejecuciones
3. Genera estadísticas en consola
4. Crea reporte HTML con trending completo

---

## Hooks y Decoradores

### En `conftest.py`
```python
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Se ejecuta DESPUÉS de cada test
    # Si falló → captura screenshot
    # Adjunta screenshot a Allure
```

**Cuándo se ejecuta:** Después de cada test (passed o failed)

### En Tests
```python
@allure.feature("Autenticación")      # Agrupa por funcionalidad
@allure.story("Login exitoso")        # Caso de uso
@allure.severity(...)                 # Criticidad
@allure.step("Paso 1")               # Documenta pasos

with allure.step("Hacer algo"):      # Step en runtime
    # código
```

**Cuándo se procesa:** Durante ejecución del test

---

## Flujo de Metadata

```
Test Execution
      │
      ├─── @allure.feature ───▶ JSON: "labels": [{"name":"feature"}]
      ├─── @allure.severity ──▶ JSON: "labels": [{"name":"severity"}]
      ├─── test_name() ────────▶ JSON: "name": "test_name"
      ├─── duration ───────────▶ JSON: "stop" - "start"
      └─── status ─────────────▶ JSON: "status": "passed"/"failed"
                                          │
                                          ▼
                                  allure-results/
                                  abc123-result.json
                                          │
                                          ▼
                                    Allure CLI
                                          │
                                          ▼
                                  allure-report/
                                  index.html
```

---

## Almacenamiento de Datos

### Temporal (Se sobrescribe)
```
allure-results/     ← Borra y regenera cada pytest
allure-report/      ← Regenera cada allure generate
allure-trends/      ← Regenera cada view_historical_trends.sh
```

### Permanente (Se preserva)
```
allure-history/     ← Solo con run_tests_with_history.sh
├── TIMESTAMP/      ← Guardado hasta que pase de 20
│   ├── allure-results/
│   └── metadata.txt
```

---

## Puntos de Extensión

### 1. Nuevos Decoradores en Tests
Agregar más metadatos:
```python
@allure.link("https://jira.com/ISSUE-123")
@allure.issue("ISSUE-123")
@allure.testcase("TC-456")
```

### 2. Attachments Personalizados
En cualquier parte del test:
```python
allure.attach(data, name="API Response", 
              attachment_type=allure.attachment_type.JSON)
```

### 3. Custom Categories
Crear `categories.json` en `allure-results/`:
```json
[
  {
    "name": "Product Defects",
    "matchedStatuses": ["failed"]
  }
]
```

### 4. Nuevos Scripts
Crear scripts bash que combinen/procesen reportes de formas diferentes.

---

## Diagrama Completo de Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                    USUARIO                                   │
│  Ejecuta: ./run_tests_with_history.sh                       │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              SCRIPT: run_tests_with_history.sh               │
│  1. Copia history anterior a allure-results/                │
│  2. Ejecuta: pytest                                         │
│  3. Guarda allure-results/ en allure-history/TIMESTAMP/     │
│  4. Genera metadata.txt                                     │
│  5. Limpia historial antiguo (mantiene 20)                  │
│  6. Ejecuta: allure generate                                │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        ▼                         ▼
┌───────────────┐         ┌──────────────────┐
│    pytest     │         │  allure generate │
└───────┬───────┘         └────────┬─────────┘
        │                          │
        ▼                          ▼
┌───────────────┐         ┌──────────────────┐
│conftest.py    │         │ allure-report/   │
│+ decorators   │         │ index.html       │
└───────┬───────┘         └────────┬─────────┘
        │                          │
        ▼                          ▼
┌───────────────┐         ┌──────────────────┐
│allure-results/│         │   NAVEGADOR      │
│  *.json       │         │  (Usuario ve)    │
└───────────────┘         └──────────────────┘
        │
        ▼
┌───────────────────────────┐
│ allure-history/TIMESTAMP/ │
│  (Guardado permanente)    │
└───────────────────────────┘
```

---

## Resumen para Junior

**3 Cosas Claves:**

1. **pytest** ejecuta tests y genera JSON (via allure-pytest)
2. **Allure CLI** convierte JSON en HTML
3. **Scripts bash** orquestan todo y manejan historial

**Para entender el sistema:**
- Sigue un test desde ejecución hasta reporte
- Inspecciona los JSON en `allure-results/`
- Compara con el HTML en `allure-report/`

**Para debugear:**
- Revisa los JSON si algo no aparece en el reporte
- Verifica que los decoradores estén bien puestos
- Asegúrate que Allure CLI esté instalado

---

**Siguiente:** [02-flujo-de-datos.md](./02-flujo-de-datos.md)
