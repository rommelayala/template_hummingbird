# Arquitectura del Proyecto

Esta sección describe la estructura de carpetas y componentes principales del framework Hummingbird.

## Estructura de Carpetas

```
template_hummingbird/
├── lib/                        # Utilidades y helpers
│   ├── config.py              # Configuración (URLs, credenciales)
│   ├── utilities.py           # Funciones auxiliares (legacy)
│   └── pages/                 # Page Object Model
│       └── login_page.py      # Página de login
│
├── tests/                     # Tests (pytest)
│   ├── features/             # Archivos Gherkin (.feature)
│   ├── test_login.py         # Pruebas de login estándar
│   └── test_login_bdd.py     # Pruebas de login BDD
│
├── integrations/              # Integraciones externas
│   └── elastic.py            # Elasticsearch (legacy)
│
├── reporting/                 # Funcionalidad de reportes
│   └── __init__.py           # Placeholder para reportes custom
│
├── doc/                       # Documentación del proyecto
│   ├── architecture/         # Arquitectura y diseño
│   ├── features/             # Documentación de features específicas
│   └── guides/               # Guías de uso y configuración
│
├── allure-history/            # Historial de ejecuciones (últimas 20)
│   ├── YYYYMMDD_HHMMSS/      # Cada ejecución con timestamp
│   │   ├── allure-results/   # Resultados completos
│   │   └── metadata.txt      # Info (fecha, branch, commit, etc.)
│   └── ...
│
├── conftest.py                # Fixtures de pytest + Allure hooks
├── pytest.ini                 # Configuración de pytest
├── requirements.txt           # Dependencias Python
├── generate_report.sh         # Script simple para reportes
├── run_tests_with_history.sh  # Ejecutar con historial
├── view_history.sh            # Ver reportes históricos
└── view_historical_trends.sh  # Ver tendencias consolidadas
```

## Componentes Principales

### Page Object Model (POM)
Los objetos de página se encuentran en `lib/pages/`. Cada clase representa una página web y encapsula la interacción con sus elementos.

### Tests
Los tests se ubican en `tests/`. Se pueden escribir como funciones de pytest estándar (`test_*.py`) o usando Gherkin (`features/*.feature`).

### Reporting
El sistema utiliza Allure para generar reportes. Los scripts en la raíz (`*.sh`) facilitan la generación y visualización de historial.
