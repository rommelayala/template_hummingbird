# 📊 GitHub Pages para Reportes Allure

Configuración y acceso a los reportes publicados en GitHub Pages.

---

## ¿Qué es GitHub Pages?

GitHub Pages es un servicio de hosting gratuito de GitHub que permite publicar sitios web estáticos directamente desde un repositorio.

**En nuestro caso:**
- Publicamos los reportes Allure generados
- Acceso público vía URL
- Actualización automática con cada ejecución

---

## URL del Reporte

Tu reporte estará en:

```
https://<usuario>.github.io/<nombre-repo>/
```

### Ejemplos Reales

```
Usuario: rommelayala
Repo: template_hummingbird
URL: https://rommelayala.github.io/template_hummingbird/

Usuario: johndoe  
Repo: my-tests
URL: https://johndoe.github.io/my-tests/

Usuario: acme-corp
Repo: qa-automation
URL: https://acme-corp.github.io/qa-automation/
```

---

## Configuración de GitHub Pages

### Método 1: Via Settings (Recomendado)

1. Ve a tu repositorio en GitHub
2. **Settings** → **Pages**
3. En **Source**:
   ```
   Deploy from a branch
   Branch: gh-pages
   Folder: / (root)
   ```
4. Click **Save**

### Método 2: Configuración Automática

El workflow intentará crear y configurar `gh-pages` automáticamente, pero necesita permisos:

- Settings → Actions → General
- Workflow permissions: "Read and write"

---

## Estructura de gh-pages

La rama `gh-pages` contiene:

```
gh-pages (branch)
├── index.html              # Página principal del reporte
├── data/                   # Datos de tests
├── widgets/                # Componentes visuales
├── history/                # Trending data
└── allure-history/         # Histórico de ejecuciones
```

**No edites esta rama manualmente** - Se actualiza automáticamente.

---

## Acceder al Reporte

### Primera Vez

Después de la primera ejecución del workflow:

1. Workflow termina exitosamente (✅)
2. **Espera 1-2 minutos** para que Pages procese
3. Abre la URL en tu navegador
4. Verás el reporte Allure

### Veces Subsiguientes

El reporte se actualiza automáticamente:

1. Ejecutas workflow
2. Workflow termina
3. Espera ~30 segundos
4. Refresca la URL (F5)
5. Verás el reporte actualizado

---

## Contenido del Reporte

### Overview (Dashboard Principal)

El primer pantalse muestra:

- 📊 **Estadísticas generales**
  - Total de tests
  - Pasados / Fallidos
  - Duración total
  
- 🎯 **Distribución por severidad**
  - Blocker
  - Critical
  - Normal
  - Minor
  
- 📈 **Gráfico de tendencias**
  - Evolución en el tiempo (a partir de 2da ejecución)

### Suites

Organización por archivos:

```
📁 tests/
  └── 📄 test_login.py
      ├── ✅ test_login_correcto
      └── ✅ test_login_incorrecto
```

### Behaviors

Organización por Features/Stories:

```
📁 Autenticación
  └── 📖 Login Exitoso
      └── ✅ test_login_correcto
```

### Graphs

Visualizaciones:

- **Trend** - Histórico de ejecuciones
- **Duration** - Duración en el tiempo
- **Retry** - Tests que fallaron y volvieron a ejecutarse

### Timeline

Vista cronológica de ejecución de tests en paralelo.

### Test Details

Click en cualquier test para ver:

- ✅ Status (Passed/Failed)
- ⏱️ Duración
- 📝 Steps ejecutados
- 📸 Screenshots (si falló)
- 📄 Logs
- 🔗 Links a tickets (si se configuraron)

---

## Screenshots en Fallos

### Cómo Funcionan

1. Test falla
2. Hook en `conftest.py` captura screenshot automáticamente
3. Se adjunta al reporte Allure
4. Aparece en la sección "Attachments"

### Ver Screenshots

1. En el reporte, click en un test fallido (❌ rojo)
2. Scroll hasta **Attachments**
3. Click en la imagen
4. Se abre en modal (pantalla completa)
5. Útil para ver exactamente qué salió mal

---

## Trending Histórico

### ¿Qué es?

Gráfico que muestra evolución de tests en el tiempo:

```
Ejecución 1: ✅✅✅ (3 passed)
Ejecución 2: ✅✅❌ (2 passed, 1 failed)
Ejecución 3: ✅✅✅ (3 passed)
```

### Cómo Habilitarlo

El workflow **ya lo incluye** automáticamente:

- Se guarda historial de últimas 20 ejecuciones
- Aparece en:
  - Overview → Gráfico superior
  - Graphs → Trend

### Cuándo Aparece

- **Primera ejecución:** No trend (solo 1 punto)
- **Segunda ejecución:** Empieza a mostrarse
- **Tercera en adelante:** Trending completo

---

## Compartir el Reporte

### URL Pública

La URL es pública y se puede compartir:

```
https://rommelayala.github.io/template_hummingbird/
```

Cualquier persona con el link puede:
- ✅ Ver el reporte
- ✅ Navegar por tests
- ✅ Ver screenshots
- ❌ No puede modificar nada

### Embed en Documentación

Puedes agregar el link en:

**README.md:**
```markdown
## 📊 Test Reports

[Ver Último Reporte](https://rommelayala.github.io/template_hummingbird/)
```

**Confluence/Notion:**
```
[Test Reports](https://rommelayala.github.io/template_hummingbird/)
```

**Slack:**
```
Reporte de tests actualizado:
https://rommelayala.github.io/template_hummingbird/
```

---

## Personalizar GitHub Pages

### Cambiar Tema (Opcional)

Si quieres un tema personalizado:

1. Crea `_config.yml` en raíz de `gh-pages`
2. Agrega:
   ```yaml
   theme: jekyll-theme-minimal
   ```

**Nota:** El reporte Allure tiene su propio estilo, esto solo afecta páginas adicionales que agregues.

### Agregar Landing Page

Crear `index_custom.html` que redirija al reporte:

```html
<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="refresh" content="0;url=./index.html">
    <title>Redirecting...</title>
</head>
<body>
    <p>Cargando reporte...</p>
</body>
</html>
```

---

## Dominio Personalizado (Opcional)

### Usar Tu Propio Dominio

Si tienes un dominio (ej: `reports.miempresa.com`):

1. Settings → Pages → Custom domain
2. Agrega tu dominio
3. Configura DNS (CNAME record):
   ```
   reports.miempresa.com → <usuario>.github.io
   ```
4. Espera propagación DNS (15-30 min)

**Resultado:** Reporte en `https://reports.miempresa.com/`

---

## Limitar Acceso (Repositorios Privados)

### GitHub Pro / Enterprise

Si tienes GitHub Pro o Enterprise:

1. Settings → Pages → Visibility
2. Selecciona "Private"
3. Solo colaboradores del repo pueden ver el reporte

### Alternativa: Proteger con Password

Usa GitHub Actions para agregar autenticación:
- Cloudflare Access
- Netlify con password protection
- Custom auth middleware

---

## Mantenimiento del Historial

### Límite de Ejecuciones

El workflow guarda las últimas **20 ejecuciones**.

**¿Por qué 20?**
- Balance entre trending útil y tamaño del repositorio
- ~100-200 MB típicamente

### Cambiar Límite

En `.github/workflows/playwright-tests.yml`:

```yaml
- name: 📈 Generar reporte Allure
  uses: simple-eld/allure-report-action@master
  with:
    allure_results: allure-results
    allure_history: allure-history
    keep_reports: 20  # ← Cambiar aquí (1-50)
```

### Limpiar Historial Manual

Si quieres borrar todo el historial:

```bash
# Borrar rama gh-pages
git push origin --delete gh-pages

# Próxima ejecución creará nueva rama limpia
```

---

## Troubleshooting

### 404 - Page Not Found

**Causas:**
- GitHub Pages aún no procesó
- Rama gh-pages no existe
- Workflow no terminó exitosamente

**Solución:**
1. Espera 2-3 minutos
2. Verifica que gh-pages branch exista
3. Refresca navegador (Ctrl+F5)

### Reporte No Se Actualiza

**Causas:**
- Cache del navegador
- Pages no actualizó

**Solución:**
```
1. Ctrl+Shift+R (hard refresh)
2. Abre en incógnito
3. Espera 1 minuto más
```

### "Refused to Connect"

**Causa:**
- HTTPS forzado pero certificado no listo

**Solución:**
1. Settings → Pages
2. Desmarcar "Enforce HTTPS" temporalmente
3. Esperar 10 minutos
4. Volver a marcar

---

## Métricas y Analytics

### GitHub Insights

Ver tráfico del sitio:

1. Settings → Pages
2. Verás estadísticas básicas:
   - Visitantes únicos
   - Views
   - Países

### Google Analytics (Opcional)

Agregar tracking:

1. Crea propiedad en Google Analytics
2. Obtén tracking ID
3. Agrega a custom layout de Allure

---

## Resumen

| Aspecto | Detalle |
|---------|---------|
| **URL** | `https://<user>.github.io/<repo>/` |
| **Actualización** | Automática en cada workflow |
| **Historial** | Últimas 20 ejecuciones |
| **Acceso** | Público (configurable) |
| **Costo** | Gratis |
| **Screenshot** | Incluido en fallos |
| **Trending** | Desde 2da ejecución |

---

**Siguiente:** [04-customization.md](./04-customization.md) - Personalización del workflow
