# 📊 Sistema de Reportes Allure - Documentación

Documentación completa del sistema de reportes con Allure para el proyecto Hummingbird.

---

## 📚 Índice de Documentación

### 🏗️ [01. Arquitectura del Sistema](./01-arquitectura.md)
Explica cómo está construido el sistema de reportes, componentes principales y cómo interactúan.

### 🔄 [02. Flujo de Datos](./02-flujo-de-datos.md)
Describe el flujo completo desde que ejecutas un test hasta que ves el reporte visual.

### 📁 [03. Archivos Involucrados](./03-archivos-involucrados.md)
Lista detallada de todos los archivos relacionados con reportes y su propósito.

### 🐛 [04. Guía de Debugging](./04-debugging.md)
Cómo debugear problemas con los reportes paso a paso.

### 🔧 [05. Troubleshooting](./05-troubleshooting.md)
Problemas comunes y sus soluciones.

### 💡 [06. Ejemplos Prácticos](./06-ejemplos.md)
Casos de uso reales con código y outputs esperados.

---

## 🚀 Inicio Rápido

### ¿Qué es el Sistema de Reportes?

El sistema de reportes Allure convierte los resultados de tus tests en reportes HTML visuales e interactivos con:
- 📊 Gráficos de tendencias
- 📸 Screenshots automáticos en fallos
- 📈 Estadísticas históricas
- 🎯 Identificación de tests inestables

### Scripts Principales

```bash
# 🚀 Suite Unificada (Ejecuta, Historial, Allure + Cluecumber)
./run_suite.sh --env=DEV --open=all

# Opciones individuales:
# --open=allure      -> Abre solo Allure
# --open=cluecumber  -> Abre solo Reporte Cucumber
```



---

## 📂 Estructura de Directorios

```
template_hummingbird/
├── doc/features/reporting/     # ← Esta documentación
│   ├── README.md              # Este archivo
│   ├── 01-arquitectura.md
│   ├── 02-flujo-de-datos.md
│   ├── 03-archivos-involucrados.md
│   ├── 04-debugging.md
│   ├── 05-troubleshooting.md
│   └── 06-ejemplos.md
│
├── allure-results/            # Resultados temporales
├── allure-report/             # Reporte HTML actual
├── allure-history/            # Historial (últimas 20)
├── allure-trends/             # Tendencias consolidadas
│
├── conftest.py               # Hooks para screenshots
├── pytest.ini                # Config de Allure
├── pytest.ini                # Config de Allure
├── run_suite.sh              # 🚀 Suite Unificada
└── execution-history/        # Historial unificado
```

---

## 🎯 Para Programadores Junior

### Lee en este Orden:

1. **Empieza aquí:** [01-arquitectura.md](./01-arquitectura.md)
   - Entiende cómo funciona todo en conjunto
   
2. **Luego:** [02-flujo-de-datos.md](./02-flujo-de-datos.md)
   - Sigue el flujo desde test hasta reporte
   
3. **Después:** [03-archivos-involucrados.md](./03-archivos-involucrados.md)
   - Conoce cada archivo y su propósito
   
4. **Para practicar:** [06-ejemplos.md](./06-ejemplos.md)
   - Ejemplos reales paso a paso
   
5. **Si algo falla:** [04-debugging.md](./04-debugging.md) y [05-troubleshooting.md](./05-troubleshooting.md)
   - Guías de solución de problemas

---

## 🔍 Conceptos Clave

### Allure
Framework de reportes que convierte JSON en HTML visual.

### pytest-allure
Plugin que conecta pytest con Allure.

### Historial
Sistema que guarda las últimas 20 ejecuciones completas.

### Tendencias
Gráficos que muestran evolución de tests en el tiempo.

### Screenshots
Capturas automáticas cuando un test falla.

---

## 📞 ¿Necesitas Ayuda?

1. **Revisa la documentación** en orden
2. **Busca en** [05-troubleshooting.md](./05-troubleshooting.md)
3. **Prueba los ejemplos** en [06-ejemplos.md](./06-ejemplos.md)
4. **Debugea** siguiendo [04-debugging.md](./04-debugging.md)

---

## ✨ Última Actualización

- **Versión:** 2.0
- **Fecha:** Enero 2025
- **Autor:** Rommel Ayala
