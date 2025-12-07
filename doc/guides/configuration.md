# Configuración del Proyecto

## Variables de Entorno

Se recomienda crear un archivo `.env` en la raíz del proyecto para gestionar la configuración local.

```bash
BASE_URL=https://www.saucedemo.com/
TEST_USERNAME=standard_user
TEST_PASSWORD=secret_sauce
HEADLESS=true
```

## Modo Headless

El modo de ejecución del navegador se configura en `conftest.py`.

```python
# Con interfaz gráfica (desarrollo/debug)
browser = playwright_instance.chromium.launch(headless=False)

# Sin interfaz gráfica (CI/CD)
browser = playwright_instance.chromium.launch(headless=True)
```

También puedes usar la variable de entorno `HEADLESS=true` si tu `conftest.py` está configurado para leerla (recomendado).
