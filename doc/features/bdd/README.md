# Implementación de BDD con Gherkin

Hummingbird utiliza `pytest-bdd` para implementar Behavior Driven Development (BDD). Esto permite escribir especificaciones de prueba en lenguaje Gherkin (formato `.feature`) y vincularlas a código Python.

## Estructura de Archivos

La implementación de BDD sigue esta estructura:

```
tests/
├── features/           # Archivos .feature (Gherkin)
│   └── login.feature
└── test_login_bdd.py   # Step definitions y test runner
```

## 1. Escribir Features (.feature)

Los archivos `.feature` describen el comportamiento esperado utilizando sintaxis Gherkin (`Given`, `When`, `Then`).

**Ejemplo (`tests/features/login.feature`):**

```gherkin
Feature: Autenticación de Usuarios
    Como usuario registrado
    Quiero poder iniciar sesión
    Para acceder a mi cuenta

    Scenario: Login exitoso con credenciales válidas
        Given que estoy en la página de login
        When ingreso el usuario "standard_user" y password "secret_sauce"
        Then debería ver la página de inventario
```

## 2. Implementar Step Definitions

Los pasos definidos en el archivo `.feature` se mapean a funciones de Python usando decoradores.

**Ejemplo (`tests/test_login_bdd.py`):**

```python
import pytest
from pytest_bdd import scenario, given, when, then, parsers
from pages.login_page import LoginPage

# Enlace al scenario del feature
@scenario('features/login.feature', 'Login exitoso con credenciales válidas')
def test_login_exitoso():
    pass

# Fixtures compartidos
@pytest.fixture
def login_page(page):
    return LoginPage(page)

# Steps
@given('que estoy en la página de login')
def navegar_al_login(login_page):
    login_page.navigate()

@when(parsers.parse('ingreso el usuario "{user}" y password "{password}"'))
def ingresar_credenciales(login_page, user, password):
    login_page.login(user, password)

@then('debería ver la página de inventario')
def verificar_inventario(page):
    assert "inventory.html" in page.url
```

## Ejecución

Los tests BDD se ejecutan igual que cualquier otro test de pytest:

```bash
# Ejecutar todos los tests (incluyendo BDD)
pytest

# Ejecutar solo tests BDD (filtrando por archivo)
pytest tests/test_login_bdd.py
```

## Mantenimiento y Escalabilidad

### Reutilización de Steps
Los steps son reutilizables entre diferentes escenarios de un mismo archivo feature. Para compartir steps entre diferentes features, se recomienda definirlos en `tests/conftest.py` o en un archivo de steps compartido (`tests/step_defs/shared_steps.py`).

### Page Object Model (POM)
Es crucial mantener la lógica de interacción con la UI separada de los steps definitions. Los steps deben llamar a métodos de los Page Objects, manteniendo el código de prueba limpio y legible.
