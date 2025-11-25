# 🚀 GitHub Actions - Guía de Uso

## Configuración Completa de GitHub Actions para Tests con Allure

Esta guía te muestra paso a paso cómo configurar y usar GitHub Actions para ejecutar tests automáticamente.

---

## 📋 Paso 1: Verificar Archivos Necesarios

Asegúrate de tener estos archivos en tu repo:

```
template_hummingbird/
├── .github/
│   └── workflows/
│       └── playwright-tests.yml   # ✅ Workflow creado
├── requirements.txt                # ✅ Con allure-pytest
├── pytest.ini                      # ✅ Con --alluredir
├── conftest.py                     # ✅ Con hooks
└── tests/                          # ✅ Tus tests
```

---

## 📋 Paso 2: Habilitar GitHub Pages

### 2.1 Ir a Settings del Repositorio
1. Abre tu repositorio en GitHub
2. Click en **Settings** (Configuración)
3. En el menú lateral, click en **Pages**

### 2.2 Configurar Source
```
Source: Deploy from a branch
Branch: gh-pages / (root)
```

### 2.3 Guardar
Click en **Save**

**Nota:** La rama `gh-pages` se creará automáticamente en la primera ejecución.

---

## 📋 Paso 3: Dar Permisos al Workflow

### 3.1 Ir a Settings → Actions → General
1. Settings
2. Actions → General
3. Scroll hasta **Workflow permissions**

### 3.2 Seleccionar Permisos
Marcar:
- ✅ **Read and write permissions**
- ✅ **Allow GitHub Actions to create and approve pull requests**

### 3.3 Guardar
Click en **Save**

---

## 📋 Paso 4: Ejecutar Tests Manualmente

### 4.1 Ir a Actions
1. En tu repositorio, click en **Actions** (arriba)
2. En el menú lateral, click en **🧪 Playwright Tests con Allure**

### 4.2 Ejecutar Workflow
1. Click en **Run workflow** (botón a la derecha)
2. Se abre un formulario:

```
Branch: [main ▼]                  ← Selecciona la rama
Test path: tests/                 ← (Opcional) path específico
```

### 4.3 Configurar Ejecución

**Ejemplos:**

#### Ejecutar TODOS los tests en rama `main`
```
Branch: main
Test path: tests/
```

#### Ejecutar solo test_login.py en rama `develop`
```
Branch: develop
Test path: tests/test_login.py
```

#### Ejecutar tests con marker smoke en rama `feature/new-feature`
```
Branch: feature/new-feature
Test path: tests/ -m smoke
```

### 4.4 Iniciar
Click en **Run workflow** (botón verde)

---

## 📋 Paso 5: Ver Progreso de Ejecución

### 5.1 Monitorear
- Verás el workflow en la lista (amarillo = ejecutando)
- Click en el nombre para ver detalles
- Verás cada paso ejecutándose en tiempo real

### 5.2 Estados
- 🟡 **Amarillo** - Ejecutando
- 🟢 **Verde** - Exitoso
- 🔴 **Rojo** - Falló

---

## 📋 Paso 6: Ver el Reporte Allure

### Opción 1: GitHub Pages (Recomendado)

Una vez que el workflow termina:

1. **URL del reporte:**
   ```
   https://<tu-usuario>.github.io/<nombre-repo>/
   ```

2. **Ejemplo:**
   ```
   https://rommelayala.github.io/template_hummingbird/
   ```

3. Abre esa URL en tu navegador
4. ✅ Verás el reporte Allure completo con trending

### Opción 2: Artifacts

1. En la página del workflow ejecutado
2. Scroll hasta **Artifacts**
3. Click en `allure-results-<número>`
4. Se descarga un ZIP
5. Descomprimir y abrir `allure-history/index.html`

---

## 📋 Paso 7: Ver Historial de Ejecuciones

### En GitHub Pages
- El reporte muestra trending de las últimas 20 ejecuciones
- Gráficos de evolución automáticos

### En Actions
1. Actions → Workflow
2. Verás lista de todas las ejecuciones
3. Click en cualquiera para ver logs y reportes

---

## 🎯 Casos de Uso Comunes

### Ejecutar Tests Antes de Merge

**Escenario:** Tienes un PR y quieres verificar tests antes de mergear

```
1. Ve a Actions
2. Run workflow
3. Branch: <tu-rama-de-feature>
4. Run workflow
5. Espera resultados
6. Revisa reporte en GitHub Pages
```

### Ejecutar Solo Tests Smoke

```
Branch: main
Test path: tests/ -m smoke
```

### Ejecutar Tests en Múltiples Ramas

Ejecuta el workflow varias veces con diferentes ramas:
```
1. Branch: main → Run
2. Branch: develop → Run
3. Branch: staging → Run
```

Cada uno genera su propio artifact.

---

## 🔧 Personalización del Workflow

### Cambiar Python Version

En `.github/workflows/playwright-tests.yml`:
```yaml
- name: 🐍 Configurar Python 3.11
  uses: actions/setup-python@v5
  with:
    python-version: '3.11'  # ← Cambiar aquí
```

### Cambiar Browser

En el workflow:
```yaml
- name: 🌐 Instalar browsers
  run: |
    playwright install chromium  # ← chrome, firefox, webkit
```

### Cambiar Retención de Artifacts

```yaml
- name: 📎 Subir artifacts
  uses: actions/upload-artifact@v4
  with:
    retention-days: 30  # ← Cambiar días (1-90)
```

### Agregar Notificaciones Slack

Agregar al final del workflow:
```yaml
- name: 📢 Notificar a Slack
  if: always()
  uses: slackapi/slack-github-action@v1
  with:
    webhook-url: ${{ secrets.SLACK_WEBHOOK }}
    payload: |
      {
        "text": "Tests finished on ${{ github.event.inputs.branch }}"
      }
```

---

## 🐛 Troubleshooting

### Problema: "Permission denied" al publicar a gh-pages

**Solución:**
1. Settings → Actions → General
2. Workflow permissions → **Read and write permissions**
3. Save

### Problema: GitHub Pages no muestra el reporte

**Solución:**
1. Settings → Pages
2. Verificar que Source = **gh-pages** branch
3. Esperar 1-2 minutos para que se publique
4. Refrescar navegador

### Problema: Tests fallan en CI pero pasan local

**Causas comunes:**
- Timeout muy corto
- Headless mode issues
- Dependencias diferentes

**Solución:**
```python
# En conftest.py, aumentar timeout para CI
import os
if os.getenv('CI'):
    page.set_default_timeout(30000)  # 30s en CI
```

### Problema: No se ve trending en el reporte

**Solución:**
- El trending aparece a partir de la **segunda** ejecución
- Ejecuta el workflow al menos 2 veces

---

## 📊 Ver Métricas

### En el Reporte Allure (GitHub Pages)

- **Overview** → Estadísticas generales
- **Graphs** → Trending de ejecuciones
- **Timeline** → Duración de tests
- **Behaviors** → Organización por Features

### En GitHub Actions

- Actions → Insights → Ver estadísticas de workflows
- Duración promedio
- Tasa de éxito/fallo

---

## ✨ Mejoras Opcionales

### 1. Ejecutar en Schedule (Cron)

Agregar al workflow:
```yaml
on:
  workflow_dispatch:
    # ... inputs actuales
  
  schedule:
    - cron: '0 2 * * *'  # Diario a las 2 AM UTC
```

### 2. Ejecutar en Push Automático

```yaml
on:
  workflow_dispatch:
    # ... inputs actuales
  
  push:
    branches: [ main, develop ]
```

### 3. Matrix Strategy (Múltiples Versiones)

```yaml
jobs:
  test:
    strategy:
      matrix:
        python-version: ['3.10', '3.11', '3.12']
    steps:
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
```

---

## 🎓 Resumen

### Para Ejecutar Tests:
1. Actions → Workflow → Run workflow
2. Seleccionar rama
3. Run workflow
4. Esperar resultados

### Para Ver Reporte:
- **Mejor:** `https://<usuario>.github.io/<repo>/`
- **Alternativa:** Descargar artifact

### Para Ver Trending:
- Ejecutar workflow múltiples veces
- Ver Overview → Graphs en el reporte

---

## 📞 Preguntas Frecuentes

**P: ¿Puedo ejecutar tests en rama privada?**
R: Sí, selecciona cualquier rama en el selector.

**P: ¿Cuántos reportes se guardan?**
R: 20 en GitHub Pages (configurable en workflow).

**P: ¿Puedo ver screenshots de fallos?**
R: Sí, están en el reporte bajo "Attachments".

**P: ¿Costo de GitHub Actions?**
R: Gratis para repos públicos. 2000 min/mes gratis para privados.

**P: ¿Puedo cancelar una ejecución?**
R: Sí, click en el workflow ejecutando → "Cancel workflow".

---

¡Ahora tienes CI/CD completo para tus tests! 🚀
