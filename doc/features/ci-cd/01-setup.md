# 🏗️ Configuración Inicial de CI/CD

## Prerequisitos

Antes de comenzar, asegúrate de tener:

- ✅ Repositorio en GitHub
- ✅ Workflow file en `.github/workflows/playwright-tests.yml`
- ✅ Tests de Playwright funcionando localmente
- ✅ `requirements.txt` con `allure-pytest`
- ✅ `pytest.ini` configurado con `--alluredir`

---

## Paso 1: Verificar Archivos del Proyecto

### 1.1 Estructura Necesaria

Tu proyecto debe tener:

```
template_hummingbird/
├── .github/
│   └── workflows/
│       └── playwright-tests.yml   ✅
├── requirements.txt                ✅
├── pytest.ini                      ✅
├── conftest.py                     ✅
└── tests/                          ✅
    └── test_*.py
```

### 1.2 Verificar requirements.txt

Debe contener:
```txt
pytest==8.4.2
pytest-playwright==0.7.1
playwright==1.56.0
allure-pytest==2.15.0
```

### 1.3 Verificar pytest.ini

Debe tener:
```ini
[pytest]
addopts = --alluredir=allure-results --clean-alluredir
```

---

## Paso 2: Subir Workflow a GitHub

### 2.1 Commit y Push

```bash
# Agregar archivo del workflow
git add .github/workflows/playwright-tests.yml

# Commit
git commit -m "feat: Add GitHub Actions workflow for Playwright tests"

# Push a main (o tu rama principal)
git push origin main
```

### 2.2 Verificar en GitHub

1. Ve a tu repositorio en GitHub
2. Navega a `.github/workflows/playwright-tests.yml`
3. Verifica que el archivo esté ahí

---

## Paso 3: Configurar GitHub Pages

### 3.1 Acceder a Settings

1. En tu repositorio, click en **Settings** (⚙️)
2. En el menú lateral izquierdo, busca **Pages**
3. Click en **Pages**

### 3.2 Configurar Source

En la sección **Build and deployment**:

```
Source: Deploy from a branch
Branch: gh-pages
Folder: / (root)
```

### 3.3 Guardar

1. Click en **Save**
2. Verás un mensaje: "GitHub Pages source saved"

**Nota:** La rama `gh-pages` se creará automáticamente en la primera ejecución del workflow.

---

## Paso 4: Dar Permisos al Workflow

### 4.1 Acceder a Actions Settings

1. Todavía en **Settings**
2. En el menú lateral, click en **Actions**
3. Click en **General**

### 4.2 Configurar Workflow Permissions

Scroll hasta encontrar **Workflow permissions**

Selecciona:
- ✅ **Read and write permissions**
- ✅ **Allow GitHub Actions to create and approve pull requests**

### 4.3 Guardar

Click en **Save** al final de la página

**¿Por qué necesitamos esto?**
- El workflow necesita permisos para crear/actualizar la rama `gh-pages`
- También para publicar en GitHub Pages

---

## Paso 5: Verificar Configuración

### 5.1 Checklist de Verificación

Marca cada item:

- [ ] Workflow file existe en `.github/workflows/playwright-tests.yml`
- [ ] GitHub Pages configurado con source `gh-pages`
- [ ] Workflow permissions en "Read and write"
- [ ] `requirements.txt` tiene `allure-pytest`
- [ ] `pytest.ini` tiene `--alluredir=allure-results`

### 5.2 Ver Workflows Disponibles

1. Ve a la pestaña **Actions** en tu repo
2. Deberías ver **🧪 Playwright Tests con Allure** en el menú lateral
3. Si lo ves, ¡configuración correcta! ✅

---

## Paso 6: Primera Ejecución (Opcional)

### 6.1 Ejecutar Manualmente

1. En **Actions**, click en **🧪 Playwright Tests con Allure**
2. Click en **Run workflow** (botón derecho)
3. Formulario:
   ```
   Branch: main
   Test path: tests/
   ```
4. Click en **Run workflow** (botón verde)

### 6.2 Monitorear Ejecución

- Verás el workflow en la lista con estado 🟡 (ejecutando)
- Click en él para ver detalles
- Cada paso se ejecuta en orden
- Espera a que termine (✅ verde o ❌ rojo)

### 6.3 Verificar gh-pages

1. Después de la primera ejecución exitosa
2. Click en el selector de ramas (arriba izquierda)
3. Deberías ver la rama `gh-pages` creada ✅

---

## Paso 7: Acceder al Reporte

### 7.1 Esperar Publicación

Después de que el workflow termine:
- Espera 1-2 minutos adicionales
- GitHub Pages necesita tiempo para procesar

### 7.2 Obtener URL

Tu reporte estará en:

```
https://<tu-usuario>.github.io/<nombre-repo>/
```

**Ejemplos:**
```
https://rommelayala.github.io/template_hummingbird/
https://johndoe.github.io/my-project/
```

### 7.3 Verificar URL en Settings

1. Settings → Pages
2. En la parte superior verás:
   ```
   Your site is live at https://...
   ```
3. Copia esa URL

### 7.4 Abrir en Navegador

1. Pega la URL en tu navegador
2. Deberías ver el reporte Allure ✅
3. Si ves error 404, espera 1-2 minutos más

---

## Configuración Completada ✅

Si llegaste aquí, tu CI/CD está listo:

- ✅ Workflow configurado
- ✅ GitHub Pages habilitado
- ✅ Permisos otorgados
- ✅ Primera ejecución exitosa
- ✅ Reporte visible en GitHub Pages

---

## Siguiente Paso

Continúa con [02-usage.md](./02-usage.md) para aprender a usar el workflow.

---

## Troubleshooting Rápido

### Si workflow no aparece en Actions
- Verifica que el archivo esté en `.github/workflows/`
- Haz push del archivo a GitHub

### Si falla con "Permission denied"
- Settings → Actions → General
- Workflow permissions → Read and write
- Save

### Si GitHub Pages muestra 404
- Espera 2-3 minutos después de la primera ejecución
- Refresca navegador
- Verifica que gh-pages branch existe

### Si no se crea gh-pages
- Verifica que workflow termine exitosamente
- Revisa permisos (paso 4)
- Ejecuta workflow nuevamente

---

**Siguiente:** [02-usage.md](./02-usage.md) - Uso del workflow
