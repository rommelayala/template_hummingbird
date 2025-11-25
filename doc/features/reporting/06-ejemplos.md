# 💡 Ejemplos Prácticos - Sistema de Reportes

Casos de uso reales con código completo y outputs esperados.

---

## Ejemplo 1: Test Básico con Allure

### Código
```python
# tests/test_example_basic.py
import allure
from playwright.sync_api import Page

@allure.feature("Ejemplo Básico")
@allure.story("Mi Primer Test con Allure")
@allure.severity(allure.severity_level.NORMAL)
def test_basico(page: Page):
    with allure.step("Navegar a Google"):
        page.goto("https://www.google.com")
    
    with allure.step("Verificar título"):
        assert "Google" in page.title()
```

### Ejecutar
```bash
pytest tests/test_example_basic.py
./generate_report.sh
```

### Output Esperado
```
✅ Reporte muestra:
  Feature: Ejemplo Básico
    Story: Mi Primer Test con Allure
      Test: test_basico (PASSED)
        Steps:
          1. Navegar a Google ✓
          2. Verificar título ✓
```

---

## Ejemplo 2: Test con Screenshot Automático

### Código
```python
# tests/test_screenshot.py
import allure
from playwright.sync_api import Page

@allure.feature("Screenshots")
@allure.story("Captura en Fallo")
def test_que_falla(page: Page):
    with allure.step("Navegar a página"):
        page.goto("https://example.com")
    
    with allure.step("Buscar elemento que no existe"):
        # Esto va a fallar
        assert page.locator("#elemento-inexistente").is_visible()
```

### Ejecutar
```bash
pytest tests/test_screenshot.py
./generate_report.sh
```

### Output Esperado
```
❌ Test falla
✅ Hook de conftest.py captura screenshot automáticamente
✅ Reporte muestra:
  - Test: test_que_falla (FAILED)
  - Attachments: Screenshot - test_que_falla.png
  - Error: AssertionError
```

---

## Ejemplo 3: Agregar Datos Personalizados

### Código
```python
# tests/test_custom_data.py
import allure
import json
from playwright.sync_api import Page

@allure.feature("API")
@allure.story("Verificar Respuesta JSON")
def test_con_datos_adjuntos(page: Page):
    with allure.step("Navegar a API"):
        page.goto("https://jsonplaceholder.typicode.com/posts/1")
    
    with allure.step("Obtener respuesta JSON"):
        content = page.content()
        # Extraer JSON del HTML
        json_data = page.evaluate("() => document.body.innerText")
        
        # Adjuntar JSON al reporte
        allure.attach(
            json_data,
            name="API Response",
            attachment_type=allure.attachment_type.JSON
        )
    
    with allure.step("Verificar datos"):
        data = json.loads(json_data)
        assert data["userId"] == 1
        
        # Adjuntar más info
        allure.attach(
            f"User ID: {data['userId']}\nTitle: {data['title']}",
            name="Extracted Data",
            attachment_type=allure.attachment_type.TEXT
        )
```

### Output Esperado
```
✅ Reporte muestra:
  - Test: test_con_datos_adjuntos (PASSED)
  - Attachments:
      • API Response (JSON) - Expandible
      • Extracted Data (TEXT)
```

---

## Ejemplo 4: Test Parametrizado

### Código
```python
# tests/test_parametrizado.py
import allure
import pytest
from playwright.sync_api import Page

@allure.feature("Login")
@allure.story("Login con Múltiples Usuarios")
@pytest.mark.parametrize("username,password,expected", [
    ("standard_user", "secret_sauce", True),
    ("locked_out_user", "secret_sauce", False),
    ("invalid_user", "wrong_pass", False),
])
def test_login_parametrizado(page: Page, username, password, expected):
    with allure.step(f"Login con usuario: {username}"):
        page.goto("https://www.saucedemo.com/")
        page.fill("#user-name", username)
        page.fill("#password", password)
        page.click("#login-button")
    
    with allure.step("Verificar resultado"):
        if expected:
            assert "inventory.html" in page.url
        else:
            assert page.locator(".error-message-container").is_visible()
    
    # Adjuntar datos del test
    allure.attach(
        f"Usuario: {username}\nPassword: {password}\nEsperado: {'Login exitoso' if expected else 'Login fallido'}",
        name="Test Parameters",
        attachment_type=allure.attachment_type.TEXT
    )
```

### Output Esperado
```
✅ Reporte muestra 3 tests:
  1. test_login_parametrizado[standard_user-secret_sauce-True] (PASSED)
  2. test_login_parametrizado[locked_out_user-secret_sauce-False] (PASSED)
  3. test_login_parametrizado[invalid_user-wrong_pass-False] (PASSED)

Cada uno con:
  - Attachment: Test Parameters mostrando usuario y contraseña usados
```

---

## Ejemplo 5: Usar con Historial

### Escenario
Ejecutar tests múltiples veces y ver tendencias.

### Comandos
```bash
# Primera ejecución
./run_tests_with_history.sh

# Segunda ejecución (cambia algo en el código)
./run_tests_with_history.sh

# Tercera ejecución
./run_tests_with_history.sh

# Ver tendencias consolidadas
./view_historical_trends.sh
```

### Output Esperado
```
Primera vez:
  📊 Overview → Graphs → Trend: 1 punto de datos

Segunda vez:
  📊 Overview → Graphs → Trend: 2 puntos, empieza a mostrar línea

Tercera vez:
  📊 Overview → Graphs → Trend: 3 puntos, tendencia visible

view_historical_trends.sh:
  📊 Estadísticas en consola:
    Total de Ejecuciones: 3
    Tasa de Éxito General: 100%
  
  📈 Reporte consolidado con trending de las 3 ejecuciones
```

---

## Ejemplo 6: Suite Completa con Organización

### Estructura
```python
# tests/test_suite_completa.py
import allure
from playwright.sync_api import Page

class TestAutenticacion:
    """Suite de tests de autenticación"""
    
    @allure.feature("Autenticación")
    @allure.story("Login Exitoso")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("Usuario puede hacer login con credenciales válidas")
    def test_login_exitoso(self, page: Page):
        with allure.step("Abrir página de login"):
            page.goto("https://www.saucedemo.com/")
        
        with allure.step("Ingresar credenciales"):
            page.fill("#user-name", "standard_user")
            page.fill("#password", "secret_sauce")
        
        with allure.step("Click en Login"):
            page.click("#login-button")
        
        with allure.step("Verificar redirección"):
            assert "inventory.html" in page.url
    
    @allure.feature("Autenticación")
    @allure.story("Login Fallido")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Usuario bloqueado no puede hacer login")
    def test_login_usuario_bloqueado(self, page: Page):
        with allure.step("Abrir página de login"):
            page.goto("https://www.saucedemo.com/")
        
        with allure.step("Ingresar usuario bloqueado"):
            page.fill("#user-name", "locked_out_user")
            page.fill("#password", "secret_sauce")
        
        with allure.step("Click en Login"):
            page.click("#login-button")
        
        with allure.step("Verificar mensaje de error"):
            error = page.locator(".error-message-container")
            assert error.is_visible()
            assert "locked out" in error.inner_text().lower()

class TestCarrito:
    """Suite de tests del carrito de compras"""
    
    @allure.feature("Carrito")
    @allure.story("Agregar Producto")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_agregar_producto(self, page: Page):
        # Login primero
        with allure.step("Login"):
            page.goto("https://www.saucedemo.com/")
            page.fill("#user-name", "standard_user")
            page.fill("#password", "secret_sauce")
            page.click("#login-button")
        
        with allure.step("Agregar primer producto al carrito"):
            page.click("button[data-test='add-to-cart-sauce-labs-backpack']")
        
        with allure.step("Verificar badge del carrito"):
            badge = page.locator(".shopping_cart_badge")
            assert badge.inner_text() == "1"
```

### Ejecutar
```bash
pytest tests/test_suite_completa.py -v
./generate_report.sh
```

### Output Esperado
```
✅ Reporte organizado por:

Behaviors → Features:
  📁 Autenticación
    📖 Login Exitoso
      ├─ test_login_exitoso (BLOCKER) ✓
    📖 Login Fallido
      └─ test_login_usuario_bloqueado (CRITICAL) ✓
  
  📁 Carrito
    📖 Agregar Producto
      └─ test_agregar_producto (CRITICAL) ✓

Suites:
  📁 test_suite_completa.py
    📁 TestAutenticacion
      ├─ test_login_exitoso
      └─ test_login_usuario_bloqueado
    📁 TestCarrito
      └─ test_agregar_producto
```

---

## Ejemplo 7: Agregar Links a Tickets

### Código
```python
# tests/test_con_links.py
import allure
from playwright.sync_api import Page

@allure.feature("Checkout")
@allure.story("Proceso de Compra")
@allure.link("https://jira.example.com/browse/PROJ-123", name="JIRA Ticket")
@allure.issue("PROJ-123", url="https://jira.example.com/browse/PROJ-123")
@allure.testcase("TC-456", url="https://testcase.example.com/TC-456")
def test_con_links(page: Page):
    with allure.step("Realizar checkout"):
        # Test code
        pass
```

### Output Esperado
```
✅ Reporte muestra:
  - Test: test_con_links
  - Links section:
      🔗 JIRA Ticket → https://jira.example.com/browse/PROJ-123
      🔗 PROJ-123 → https://jira.example.com/browse/PROJ-123
      🔗 TC-456 → https://testcase.example.com/TC-456
```

---

## Ejemplo 8: Debugging un Test que Falla

### Escenario
Un test falla y necesitas debugearlo.

### Paso 1: Ejecutar con verbose
```bash
pytest tests/test_login.py::test_login_correcto -vv
```

### Paso 2: Inspeccionar el reporte
```bash
./generate_report.sh
# Navegador abre automáticamente
```

### Paso 3: En el reporte, buscar:
1. **Status** - ¿Pasó o falló?
2. **Steps** - ¿Qué paso falló?
3. **Screenshot** - Ver captura del momento del fallo
4. **Error Message** - Leer la excepción completa

### Paso 4: Inspeccionar JSON
```bash
cat allure-results/*-result.json | jq '.steps'

# Ver solo el step que falló
cat allure-results/*-result.json | jq '.steps[] | select(.status=="failed")'
```

### Paso 5: Fix y re-ejecutar
```python
# Corregir el test
# Re-ejecutar
pytest tests/test_login.py::test_login_correcto
./generate_report.sh
```

---

## Resumen de Comandos Útiles

```bash
# Test individual
pytest tests/test_file.py::test_name -v

# Test con historial
./run_tests_with_history.sh

# Ver reporte simple
./generate_report.sh

# Ver reporte histórico
./view_history.sh

# Ver tendencias
./view_historical_trends.sh

# Inspeccionar JSON
cat allure-results/*-result.json | python3 -m json.tool

# Buscar feature específico
grep -r "@allure.feature" tests/

# Ver solo nombres de tests
pytest --collect-only

# Ejecutar con marker
pytest -m smoke
```

---

## Template de Test Completo

```python
# tests/test_template.py
"""
Template completo de test con Allure
"""
import allure
import pytest
from playwright.sync_api import Page

@allure.feature("Nombre de Feature")
@allure.story("Historia de Usuario")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Descripción corta del test")
@allure.description("""
Descripción detallada del test.
Qué hace, por qué, y qué se espera.
""")
@allure.link("https://jira.com/ISSUE-123", name="Ticket")
@pytest.mark.smoke
def test_template(page: Page):
    """Docstring del test"""
    
    with allure.step("Paso 1: Navegar"):
        page.goto("https://example.com")
        allure.attach(
            page.url,
            name="Current URL",
            attachment_type=allure.attachment_type.TEXT
        )
    
    with allure.step("Paso 2: Interactuar"):
        page.click("#button")
    
    with allure.step("Paso 3: Verificar"):
        assert page.locator("#result").is_visible()
        
        # Adjuntar dato verificado
        result_text = page.locator("#result").inner_text()
        allure.attach(
            result_text,
            name="Result Text",
            attachment_type=allure.attachment_type.TEXT
        )
```

---

¡Con estos ejemplos ya puedes crear tests completos con reportes profesionales! 📊✨
