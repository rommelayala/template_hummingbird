# 🚀 CI/CD con GitHub Actions - Documentación

Documentación completa del sistema de CI/CD con GitHub Actions y publicación automática de reportes Allure.

---

## 📚 Índice de Documentación

### 🏗️ [01. Configuración Inicial](./01-setup.md)
Configuración paso a paso del workflow de GitHub Actions.

### 🔄 [02. Uso del Workflow](./02-usage.md)
Cómo ejecutar tests desde GitHub Actions.

### 📊 [03. GitHub Pages](./03-github-pages.md)
Configuración y acceso a reportes en GitHub Pages.

### 🔧 [04. Personalización](./04-customization.md)
Cómo personalizar el workflow para tus necesidades.

### 🐛 [05. Troubleshooting](./05-troubleshooting.md)
Problemas comunes y soluciones.

---

## 🚀 Inicio Rápido

### ¿Qué es el CI/CD Pipeline?

Sistema automatizado que ejecuta tests de Playwright en GitHub Actions, genera reportes Allure y los publica automáticamente en GitHub Pages.

### Características Principales

✅ **Ejecución manual** - Elige rama y tests específicos  
✅ **Allure Reports** - Reportes visuales automáticos  
✅ **GitHub Pages** - Acceso público a reportes  
✅ **Trending histórico** - Últimas 20 ejecuciones  
✅ **Screenshots** - Capturas automáticas en fallos  
✅ **Artifacts** - Descarga de reportes como backup  

---

## 📋 Setup en 3 Pasos

### 1. **Subir el workflow**
```bash
git add .github/workflows/playwright-tests.yml
git commit -m "feat: Add CI/CD with GitHub Actions"
git push origin main
```

### 2. **Configurar GitHub**
- Settings → Pages → Source: `gh-pages` → Save
- Settings → Actions → General → Read/write permissions → Save

### 3. **Ejecutar tests**
- Actions → Run workflow → Selecciona rama → Run workflow

---

## 🎯 Acceso al Reporte

Tu reporte estará disponible en:

```
https://<usuario>.github.io/<repo>/
```

**Ejemplo:**
```
https://rommelayala.github.io/template_hummingbird/
```

---

## 📂 Estructura de Archivos

```
template_hummingbird/
├── .github/
│   └── workflows/
│       └── playwright-tests.yml   # ← Workflow principal
├── doc/
│   └── features/
│       └── ci-cd/                 # ← Esta documentación
│           ├── README.md
│           ├── 01-setup.md
│           ├── 02-usage.md
│           ├── 03-github-pages.md
│           ├── 04-customization.md
│           └── 05-troubleshooting.md
├── tests/                         # Tests de Playwright
└── pytest.ini                     # Configuración de pytest
```

---

## 🎓 Para Comenzar

### Lee en este orden:

1. **[01-setup.md](./01-setup.md)** - Configuración inicial completa
2. **[02-usage.md](./02-usage.md)** - Cómo usar el workflow
3. **[03-github-pages.md](./03-github-pages.md)** - Setup de GitHub Pages
4. **[04-customization.md](./04-customization.md)** - Personalización avanzada
5. **[05-troubleshooting.md](./05-troubleshooting.md)** - Si algo falla

---

## 🔍 Conceptos Clave

### CI/CD
Continuous Integration / Continuous Deployment - Automatización de tests y despliegues.

### GitHub Actions
Plataforma de automatización de GitHub para ejecutar workflows.

### Workflow
Archivo YAML que define qué ejecutar y cuándo.

### GitHub Pages
Hosting gratuito de GitHub para sitios estáticos (nuestros reportes).

### Artifacts
Archivos generados que se pueden descargar desde GitHub Actions.

---

## 📞 ¿Necesitas Ayuda?

1. **Revisa** [05-troubleshooting.md](./05-troubleshooting.md)
2. **Consulta** ejemplos en [02-usage.md](./02-usage.md)
3. **Personaliza** según [04-customization.md](./04-customization.md)

---

## ✨ Última Actualización

- **Versión:** 1.0
- **Fecha:** Noviembre 2025
- **Autor:** Rommel Ayala
