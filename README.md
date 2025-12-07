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
```bash
# ❌ NO USAR SOLAMENTE
pytest

# ✅ USAR SIEMPRE
./run_suite.sh --env=DEV
```

# Generar reporte con historial (Recomendado)
# Generar reporte con historial (Recomendado)
# Ejecución Maestra (Recomendada) 🚀
# Ejecuta tests, guarda historial y genera reportes Allure + Cluecumber
```bash
./run_suite.sh --env=DEV --open=all
```
# Opciones de apertura:
# --open=allure      (Solo Allure)
# --open=cluecumber  (Solo Cucumber HTML)
# --open=all         (Ambos)


# Ejecutar en entorno específico (DEV, QA, STAG, PP)
pytest --env=QA
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
