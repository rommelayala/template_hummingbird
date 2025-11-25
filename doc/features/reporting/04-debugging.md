# 🐛 Guía de Debugging - Sistema de Reportes

Cómo debugear problemas con los reportes Allure paso a paso.

---

## Metodología de Debugging

Sigue este flujo cuando algo no funciona:

```
1. ¿Se ejecutó el test?
   ├─ NO → Problema con pytest
   └─ SÍ → Continuar

2. ¿Se generó allure-results/?
   ├─ NO → Problema con allure-pytest
   └─ SÍ → Continuar

3. ¿Los JSON tienen datos?
   ├─ NO → Problema con decoradores
   └─ SÍ → Continuar

4. ¿Se generó allure-report/?
   ├─ NO → Problema con Allure CLI
   └─ SÍ → Continuar

5. ¿El navegador muestra el reporte?
   ├─ NO → Problema con servidor/navegador
   └─ SÍ → ¡Funciona!
```

---

## Problema 1: Tests No Aparecen en el Reporte

### Síntoma
El reporte se genera pero no ves tus tests.

### Debug Paso a Paso

#### 1. Verificar que el test se ejecutó
```bash
pytest tests/test_login.py -v

# Output esperado:
# tests/test_login.py::test_login_correcto PASSED
```

**Si NO aparece PASSED/FAILED:**
- El test tiene errores de sintaxis
- El archivo no se llama `test_*.py`
- La función no se llama `test_*()`

---

#### 2. Verificar que se generaron JSON
```bash
ls -la allure-results/

# Output esperado:
# -rw-r--r--  1 user  staff  2431 Jan 25 14:30 abc123-result.json
# -rw-r--r--  1 user  staff   345 Jan 25 14:30 def456-container.json
```

**Si el directorio está vacío:**
```bash
# Verifica la configuración
cat pytest.ini | grep alluredir

# Debe mostrar:
# addopts = ... --alluredir=allure-results
```

**Si falta:**
```ini
# Agregar a pytest.ini
addopts = --alluredir=allure-results
```

---

#### 3. Inspeccionar el JSON
```bash
cat allure-results/*-result.json | python3 -m json.tool

# O más específico:
jq '.' allure-results/*-result.json
```

**Busca:**
- `"name": "test_login_correcto"` ← Nombre del test
- `"status": "passed"` ← Estado
- `"labels": [...]` ← Decoradores

**Si el JSON está vacío o malformado:**
- allure-pytest no se instaló correctamente
- Reinstalar: `pip install --force-reinstall allure-pytest`

---

#### 4. Verificar plugins de pytest
```bash
pytest --version

# Output esperado incluye:
# plugins: allure-pytest-2.15.0, playwright-0.7.1
```

**Si allure-pytest NO aparece:**
```bash
pip list | grep allure

# Debe mostrar:
# allure-pytest     2.15.0
# allure-python-commons  2.15.0
```

**Si no están:**
```bash
pip install allure-pytest
```

---

## Problema 2: Decoradores No Aparecen

### Síntoma
El test aparece pero sin Features, Stories, etc.

### Debug

#### 1. Verificar import
```python
# El archivo debe tener:
import allure  # ← IMPORTANTE
``` 

**Si falta**, agrégalo al inicio del archivo.

---

#### 2. Verificar sintaxis de decoradores
```python
# ✅ CORRECTO
@allure.feature("Autenticación")
def test_login():
    pass

# ❌ INCORRECTO
@allure.feature("Autenticación")  # Sin paréntesis
def test_login():
    pass
```

---

#### 3. Inspeccionar JSON
```bash
cat allure-results/*-result.json | grep -A5 "labels"

# Output esperado:
# "labels": [
#   {"name": "feature", "value": "Autenticación"},
#   {"name": "story", "value": "Login"}
# ]
```

**Si labels está vacío:**
- Los decoradores no se están leyendo
- Revisa que estén ANTES de `def test_*()`

---

## Problema 3: Screenshots No Aparecen

### Síntoma
El test falla pero no hay screenshot en el reporte.

### Debug

#### 1. Verificar que el test falló
```bash
pytest tests/test_login.py -v

# Debe mostrar FAILED, no PASSED
```

---

#### 2. Verificar el hook en conftest.py
```bash
grep -A20 "pytest_runtest_makereport" conftest.py

# Debe contener:
# if report.when == "call" and report.failed:
#     page.screenshot(...)
#     allure.attach.file(...)
```

**Si el hook no existe:**
Ver [03-archivos-involucrados.md](./03-archivos-involucrados.md#conftest.py) para el código completo.

---

#### 3. Verificar que se creó el archivo PNG
```bash
ls -la allure-results/screenshots/

# Output esperado:
# test_login_correcto.png
```

**Si el directorio no existe:**
- El hook no se está ejecutando
- Verifica que el test use la fixture `page`

---

#### 4. Verificar que se adjuntó a Allure
```bash
cat allure-results/*-result.json | grep -A5 "attachments"

# Output esperado:
# "attachments": [
#   {
#     "name": "Screenshot - test_login",
#     "source": "abc123-attachment.png",
#     "type": "image/png"
#   }
# ]
```

---

## Problema 4: El Reporte No Se Genera

### Síntoma
`allure generate` o `allure serve` falla.

### Debug

#### 1. Verificar que Allure esté instalado
```bash
allure --version

# Output esperado:
# 2.24.0
```

**Si no está instalado:**
```bash
# macOS
brew install allure

# Linux
sudo apt-add-repository ppa:qameta/allure
sudo apt-get update
sudo apt-get install allure
```

---

#### 2. Verificar que existan resultados
```bash
ls -la allure-results/

# Debe haber archivos *.json
```

**Si está vacío:**
- Ejecuta primero `pytest`
- Verifica `pytest.ini` tenga `--alluredir=allure-results`

---

####  3. Ver errores de Allure
```bash
allure generate allure-results -o allure-report --clean 2>&1

# Lee el output completo
```

**Errores comunes:**

- `"allure-results" does not contain valid results`
  → Los JSON están corruptos o vacíos
  
- `Java not found`
  → Allure requiere Java
  → Instalar: `brew install openjdk`

---

## Problema 5: El Navegador No Abre

### Síntoma
`allure serve` ejecuta pero el navegador no abre.

### Debug

#### 1. Verificar que el servidor inició
```bash
allure serve allure-results

# Output esperado:
# Server started at http://192.168.1.100:54321
# Press <Ctrl+C> to exit
```

**Si aparece error:**
- Puerto ocupado
- Usar puerto específico: `allure serve -p 8080 allure-results`

---

#### 2. Abrir manualmente
```bash
# El output muestra la URL
# Copiar y abrir en Chrome/Firefox manualmente
```

---

#### 3. Verificar permisos del navegador
En macOS, si el navegador no abre automáticamente:
```bash
# Dar permisos a terminal
System Preferences → Security & Privacy → Automation
→ Permitir que Terminal controle navegador
```

---

## Problema 6: Historial No Se Guarda

### Síntoma
`allure-history/` está vacío después de ejecutar con historial.

### Debug

#### 1. Verificar que usaste el script correcto
```bash
# ❌ INCORRECTO
pytest
./generate_report.sh

# ✅ CORRECTO
./run_tests_with_history.sh
```

---

#### 2. Verificar permisos del script
```bash
ls -la run_tests_with_history.sh

# Debe tener 'x' (ejecutable):
# -rwxr-xr-x  1 user  staff  1234 Jan 25 14:30 run_tests_with_history.sh
```

**Si no es ejecutable:**
```bash
chmod +x run_tests_with_history.sh
```

---

#### 3. Ejecutar con debug
```bash
bash -x ./run_tests_with_history.sh 2>&1 | tee debug.log

# Revisar debug.log para ver qué falló
```

---

## Herramientas de Debugging

### 1. Inspeccionar JSON con jq
```bash
# Instalar jq
brew install jq

# Ver estructura completa
jq '.' allure-results/*-result.json

# Ver solo nombres de tests
jq '.name' allure-results/*-result.json

# Ver solo features
jq '.labels[] | select(.name=="feature") | .value' allure-results/*-result.json
```

---

### 2. Logs de pytest
```bash
# Ejecutar con máximo detalle
pytest -vvv --log-cli-level=DEBUG

# Guardar logs
pytest -vvv --log-cli-level=DEBUG > pytest_debug.log 2>&1
```

---

### 3. Verificar integración completa
```bash
# Script de verificación
cat > verify_allure.sh <<'EOF'
#!/bin/bash
echo "=== Verificando Sistema de Reportes ==="

# 1. pytest
echo "1. Verificando pytest..."
pytest --version || echo "❌ pytest no instalado"

# 2. allure-pytest
echo "2. Verificando allure-pytest..."
pip show allure-pytest || echo "❌ allure-pytest no instalado"

# 3. Allure CLI
echo "3. Verificando Allure CLI..."
allure --version || echo "❌ Allure no instalado"

# 4. pytest.ini
echo "4. Verificando pytest.ini..."
grep -q "alluredir" pytest.ini && echo "✅ pytest.ini OK" || echo "❌ pytest.ini sin alluredir"

# 5. conftest.py
echo "5. Verificando conftest.py..."
grep -q "pytest_runtest_makereport" conftest.py && echo "✅ conftest.py OK" || echo "❌ conftest.py sin hook"

echo "=== Verificación Completa ==="
EOF

chmod +x verify_allure.sh
./verify_allure.sh
```

---

## Checklist de Debugging

Cuando algo falle, verifica en orden:

- [ ]tests ejecutan correctamente con `pytest -v`
- [ ] `allure-results/` se crea y tiene archivos *.json
- [ ] JSON files tienen contenido válido (usar `jq`)
- [ ] `allure-pytest` está en `pip list`
- [ ] Allure CLI está instalado (`allure --version`)
- [ ] `pytest.ini` tiene `--alluredir=allure-results`
- [ ] `conftest.py` tiene el hook de screenshots
- [ ] Tests tienen `import allure`
- [ ] Decoradores tienen sintaxis correcta
- [ ] Scripts tienen permisos de ejecución (`chmod +x`)

---

## Errores Comunes y Soluciones Rápidas

| Error | Solución |
|-------|----------|
| "allure: command not found" | `brew install allure` |
| "No module named 'allure'" | `pip install allure-pytest` |
| JSON vacíos | Verificar `pytest.ini` |
| Screenshots no aparecen | Verificar hook en `conftest.py` |
| Decoradores no en reporte | Verificar `import allure` |
| Navegador no abre | Abrir URL manualmente |
| Historial vacío | Usar `run_tests_with_history.sh` |

---

**Siguiente:** [05-troubleshooting.md](./05-troubleshooting.md)
