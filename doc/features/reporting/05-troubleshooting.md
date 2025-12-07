# 🔧 Troubleshooting - Problemas Comunes

Soluciones a los problemas más frecuentes con el sistema de reportes.

---

## Problema: "ModuleNotFoundError: No module named 'allure'"

### Síntomas
```bash
pytest
# ImportError: cannot import name 'allure' from '/tests/test_login.py'
```

### Causa
El paquete `allure-pytest` no está instalado.

### Solución
```bash
# 1. Activar virtual environment
source venv/bin/activate

# 2. Instalar allure-pytest
pip install allure-pytest

# 3. Verificar instalación
pip show allure-pytest

# 4. Re-ejecutar tests
pytest
```

---

## Problema: "allure: command not found"

### Síntomas
```bash
./run_suite.sh
# allure: command not found
```

### Causa
Allure CLI no está instalado en el sistema.

### Solución

**macOS:**
```bash
brew install allure
allure --version
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-add-repository ppa:qameta/allure
sudo apt-get update
sudo apt-get install allure
```

**Windows (con Scoop):**
```bash
scoop install allure
```

---

## Problema: Reporte Sin Tests

### Síntomas
- El reporte se abre pero muestra "0 tests"
- Dashboard vacío

### Causa
Los resultados no se generaron o se borraron.

### Solución
```bash
# 1. Verificar que allure-results existe
ls -la allure-results/

# 2. Si está vacío, ejecutar tests
pytest

# 3. Verificar que se crearon JSON
ls -la allure-results/*.json

# 4. Generar reporte
./run_suite.sh --open=allure
```

---

## Problema: Screenshots No Aparecen

### Síntomas
- Test falla pero no hay screenshot en el reporte
- Attachments vacío

### Causa
El hook de `conftest.py` no funciona o falta.

### Solución

#### 1. Verificar que conftest.py tiene el hook
```bash
grep -A10 "pytest_runtest_makereport" conftest.py
```

#### 2. Si no existe, agregar:
```python
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        
        if page:
            screenshot_dir = "allure-results/screenshots"
            os.makedirs(screenshot_dir, exist_ok=True)
            
            screenshot_path = os.path.join(screenshot_dir, f"{item.name}.png")
            page.screenshot(path=screenshot_path, full_page=True)
            
            allure.attach.file(
                screenshot_path,
                name=f"Screenshot - {item.name}",
                attachment_type=allure.attachment_type.PNG
            )
```

#### 3. Verificar imports
```python
import os
import allure
```

---

## Problema: Features/Stories No Aparecen

### Síntomas
- Tests aparecen en el reporte
- Pero no están organizados por Features

### Causa
Decoradores mal puestos o falta import.

### Solución

#### 1. Verificar import
```python
# Al inicio del archivo de test
import allure  # ← DEBE ESTAR
```

#### 2. Verificar decoradores
```python
# ✅ CORRECTO
@allure.feature("Autenticación")
@allure.story("Login exitoso")
def test_login():
    pass

# ❌ INCORRECTO - sin paréntesis
@allure.feature
def test_login():
    pass

# ❌ INCORRECTO - después de def
def test_login():
    @allure.feature("Auth")  # ← Mal ubicado
    pass
```

#### 3. Re-ejecutar tests
```bash
pytest
./generate_report.sh
```

---

## Problema: "Java not found" al generar reporte

### Síntomas
```bash
allure serve allure-results
# Error: Java is notinstalled or JAVA_HOME is not set
```

### Causa
Allure CLI requiere Java para ejecutarse.

### Solución

**macOS:**
```bash
brew install openjdk@11

# Agregar a PATH
echo 'export PATH="/opt/homebrew/opt/openjdk@11/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Verificar
java --version
```

**Linux:**
```bash
sudo apt install openjdk-11-jdk
java --version
```

---

## Problema: Historial No Se Guarda

### Síntomas
- Ejecutas `./run_suite.sh`
- `execution-history/` sigue vacío

### Causa
Script no tiene permisos o hay error en ejecución.

### Solución

#### 1. Dar permisos
```bash
chmod +x run_suite.sh
```

#### 2. Ejecutar con debug
```bash
bash -x ./run_suite.sh --env=DEV
```

#### 3. Verificar manualmente
```bash
# Después de ejecutar, debe existir:
ls -la execution-history/

# Debe mostrar carpetas con timestamp:
# drwxr-xr-x  4 user  staff  128 Jan 25 14:30 20250125_143000
```

---

## Problema: Tendencias No Muestran Datos Históricos

### Síntomas
- El reporte se abre
- Pero "Trend" muestra solo la última ejecución

### Causa
No se está copiando el `history/` folder entre ejecuciones.

### Solución

#### 1. Usar siempre el script maestro
```bash
# ❌ NO USAR SOLAMENTE
pytest

# ✅ USAR SIEMPRE
./run_suite.sh --env=DEV
```

#### 2. El script automatically copia history
Busca esta sección en `run_suite.sh`:
```bash
if [ -d "allure-report/history" ]; then
    mkdir -p "$ALLURE_RESULTS_DIR/history"
    cp -r "allure-report/history/"* "$ALLURE_RESULTS_DIR/history/"
fi
```

#### 3. Ejecutar múltiples veces
```bash
./run_suite.sh --env=DEV
./run_suite.sh --env=DEV
./run_suite.sh --open=allure
```

---

## Problema: Navegador No Abre Automáticamente

### Síntomas
```bash
./generate_report.sh
# Server started at http://...
# Pero navegador no abre
```

### Causa
Permisos bloqueados o configuración del sistema.

### Solución

#### 1. Abrir manualmente
```bash
# Copiar la URL del output y abrir en navegador
# Por ejemplo: http://192.168.1.100:54321
```

#### 2. macOS - Dar permisos
```
System Preferences → Security & Privacy → Privacy → Automation
→ Permitir que Terminal controle el navegador
```

#### 3. Usar allure open
```bash
allure generate allure-results -o allure-report --clean
allure open allure-report
```

---

## Problema: Port Already in Use

### Síntomas
```bash
allure serve allure-results
# Error: Port 54321 already in use
```

### Causa
Otro proceso tiene el puerto ocupado (probablemente otro Allure).

### Solución

#### 1. Matar proceso anterior
```bash
# Buscar proceso
lsof -i :54321

# Matar proceso
kill -9 <PID>
```

#### 2. Usar otro puerto
```bash
allure serve -p 8080 allure-results
```

---

## Problema: Tests Lentos / Timeout

### Síntomas
- Tests tardan mucho
- Timeouts en navegador

### Causa
Playwright esperando elementos que no aparecen.

### Solución

#### 1. Reducir timeouts
```python
# En conftest.py o test
page.set_default_timeout(5000)  # 5 segundos en lugar de 30
```

#### 2. Usar headless mode
```python
# conftest.py
browser = playwright_instance.chromium.launch(headless=True)
```

#### 3. Paralelizar tests
```bash
pytest -n auto  # Usa todos los CPUs
pytest -n 4     # Usa 4 workers
```

---

## Problema: "Permission Denied" en Scripts

### Síntomas
```bash
./run_suite.sh --open=allure
```

---

## Problema: "Permission Denied" en Scripts

### Síntomas
```bash
./run_suite.sh
# bash: ./run_suite.sh: Permission denied
```

### Causa
El script no tiene permisos de ejecución.

### Solución
```bash
chmod +x run_suite.sh

# Verificar
ls -la run_suite.sh
# Debe mostrar -rwxr-xr-x
```

---

## Problema: Allure-Results Se Borra

### Síntomas
- Ejecutas pytest
- Resultados desaparecen

### Causa
`--clean-alluredir` en pytest.ini borra antes de ejecutar.

### Solución (Si quieres acumular resultados)

#### Opción 1: Quitar --clean-alluredir
```ini
# pytest.ini
# Remover o comentar:
# addopts = ... --clean-alluredir
```

### Solución (Si quieres acumular resultados)

#### Usar historial (Recomendado)
```bash
# En lugar de pytest directo
./run_suite.sh
# Este script gestiona el historial automáticamente en execution-history
```

---

## Problema: Screenshots Muy Grandes

### Síntomas
- `allure-results/` ocupa mucho espacio
- Screenshots de 5+ MB cada uno

### Causa
Screenshots  de página completa en alta resolución.

### Solución

#### 1. Capturar solo viewport
```python
# En conftest.py, cambiar:
page.screenshot(path=..., full_page=False)  # Solo viewport visible
```

#### 2. Reducir calidad
```python
page.screenshot(path=..., quality=50)  # Para JPEG
```

#### 3. Limpiar historial antiguo
El script `run_suite.sh` acumula ejecuciones. Puedes limpiar `execution-history` manualmente de vez en cuando.

---

## Problema: Git Muestra Muchos Cambios en allure-*

### Síntomas
- `git status` muestra cambios en `allure-results/`
- Miles de archivos sin seguimiento

### Causa
Directorios de Allure no están en `.gitignore`.

### Solución
```bash
# Verificar .gitignore
cat .gitignore | grep allure

# Debe tener:
allure-results/
allure-report/
execution-history/  # ← Nuevo unified history
json-results/
cluecumber-report/

# Si no están, agregar:
echo "execution-history/" >> .gitignore
echo "json-results/" >> .gitignore
echo "cluecumber-report/" >> .gitignore

# Limpiar cache de git
git rm -r --cached allure-results/
git rm -r --cached allure-report/
```

---

## Problema: Flaky Tests en CI/CD

### Síntomas
- Tests pasan localmente
- Fallan en CI/CD intermitentemente

### Causas Comunes
- Timeouts muy cortos
- Condiciones de carrera
- Elementos no esperan carga completa

### Soluciones

#### 1. Aumentar timeouts
```python
page.set_default_timeout(30000)  # 30 segundos
```

#### 2. Esperar por estado de red
```python
page.goto(url)
page.wait_for_load_state("networkidle")
```

#### 3. Usar retry con Allure
```python
import pytest

@pytest.mark.flaky(reruns=3, reruns_delay=2)
@allure.feature("Checkout")
def test_flaky():
    # Test que puede fallar ocasionalmente
    pass
```

---

## Checklist de Troubleshooting

Cuando tengas un problema:

1. - [ ] Verificar dependencias instaladas (`pip list`)
2. - [ ] Verificar Allure CLI (`allure --version`)
3. - [ ] Revisar `pytest.ini` configuración
4. - [ ] Revisar `conftest.py` hooks
5. - [ ] Verificar permisos de scripts (`ls -la *.sh`)
6. - [ ] Ejecutar con verbose (`pytest -vv`)
7. - [ ] Inspeccionar JSON (`ls -la allure-results/`)
8. - [ ] Revisar logs de error
9. - [ ] Comprobar `.gitignore`
10. - [ ] Intentar en entorno limpio

---

## Recursos Adicionales

### Logs Útiles
```bash
# pytest con máximo detalle
pytest -vvv --log-cli-level=DEBUG > debug.log 2>&1

# Allure con verbose
allure serve allure-results -v

# Script con debug
bash -x ./run_tests_with_history.sh 2>&1 | tee script_debug.log
```

### Validar Instalación Completa
```bash
# Script de validación
cat > validate.sh <<'EOF'
#!/bin/bash
echo "Validando instalación..."
python --version && echo "✅ Python OK" || echo "❌ Python falta"
pip show pytest && echo "✅ pytest OK" || echo "❌ pytest falta"
pip show allure-pytest && echo "✅ allure-pytest OK" || echo "❌ allure-pytest falta"
allure --version && echo "✅ Allure CLI OK" || echo "❌ Allure CLI falta"
[ -f pytest.ini ] && echo "✅ pytest.ini OK" || echo "❌ pytest.ini falta"
[ -f conftest.py ] && echo "✅ conftest.py OK" || echo "❌ conftest.py falta"
EOF

chmod +x validate.sh
./validate.sh
```

---

**Siguiente:** [06-ejemplos.md](./06-ejemplos.md)
