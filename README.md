# 🐦 Hummingbird

Framework de automatización de pruebas E2E basado en **Playwright + Python** con capacidades de **Gherkin/BDD** y reportes profesionales **Allure**.

---

## 🚀 Quick Start

### 1. Instalación
```bash
# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
playwright install chromium
```

### 2. Ejecutar Tests
```bash
# Ejecutar todos los tests
pytest

# Generar reporte con historial (Recomendado)
./run_tests_with_history.sh
```

---

## 📚 Documentación

La documentación detallada se encuentra en la carpeta `doc/`:

### 🏗️ Arquitectura
- [Estructura del Proyecto](./doc/architecture/structure.md) - Organización de carpetas y componentes.

### 📖 Guías de Uso
- [Ejecución y Reportes](./doc/guides/execution.md) - Comandos avanzados, filtros, paralelo y gestión de reportes Allure.
- [Configuración](./doc/guides/configuration.md) - Variables de entorno y modo headless.

### 🥒 Features
- [Gherkin / BDD](./doc/features/bdd/README.md) - Guía para implementar tests con sintaxis Gherkin (`.feature`).
- [Sistema de Reportes](./doc/features/reporting/README.md) - Detalles sobre la personalización de reportes.
- [CI/CD](./doc/features/ci-cd/README.md) - Integración continua con GitHub Actions.

---

## Contribuir
Este proyecto sigue el flujo de GitHub Flow. Por favor, crea una rama para cada nueva funcionalidad o corrección.

## Licencia
Licencia MIT - ver [LICENSE](LICENSE).

## Autor
**Rommel Ayala**
