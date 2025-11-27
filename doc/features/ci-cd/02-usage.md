# 🔄 Uso del Workflow de GitHub Actions

Cómo ejecutar tests desde GitHub Actions con diferentes configuraciones.

---

## Ejecución Manual Básica

### Paso 1: Ir a Actions

1. Abre tu repositorio en GitHub
2. Click en la pestaña **Actions** (arriba)
3. En el menú lateral, click en **🧪 Playwright Tests con Allure**

### Paso 2: Iniciar Workflow

1. Click en **Run workflow** (botón a la derecha)
2. Se abre un formulario con opciones

### Paso 3: Configurar Ejecución

```
Branch: [main ▼]                  ← Selecciona rama
Test path: tests/                 ← Path de tests
```

### Paso 4: Ejecutar

Click en **Run workflow** (botón verde)

---

## Opciones de Configuración

### Selector de Rama

**Propósito:** Elegir desde qué rama ejecutar los tests

**Opciones comunes:**
- `main` - Rama principal
- `develop` - Rama de desarrollo
- `staging` - Rama de staging
- `feature/nombre` - Rama de feature específica

**Ejemplo:**
```
Branch: feature/new-login
```

### Test Path

**Propósito:** Especificar qué tests ejecutar

**Opciones:**

#### Todos los tests
```
Test path: tests/
```

#### Test específico
```
Test path: tests/test_login.py
```

#### Múltiples archivos
```
Test path: tests/test_login.py tests/test_checkout.py
```

#### Con markers
```
Test path: tests/ -m smoke
```

#### Con verbose
```
Test path: tests/ -v
```

---

## Casos de Uso Comunes

### Caso 1: Ejecutar Todos los Tests en Main

**Cuándo:** Antes de release, verificación general

**Configuración:**
```
Branch: main
Test path: tests/
```

**Resultado esperado:**
- Ejecuta TODOS los tests
- Genera reporte completo
- Publica en GitHub Pages

---

### Caso 2: Ejecutar Tests de una Feature

**Cuándo:** Verificar feature antes de merge

**Configuración:**
```
Branch: feature/new-checkout
Test path: tests/test_checkout.py
```

**Resultado esperado:**
- Ejecuta solo tests de checkout
- Verifica funcionalidad específica
- Reporte enfocado en esa feature

---

### Caso 3: Smoke Tests en Develop

**Cuándo:** Verificación rápida después de cambios

**Configuración:**
```
Branch: develop
Test path: tests/ -m smoke
```

**Resultado esperado:**
- Ejecuta solo tests críticos
- Rápido (~2-5 min)
- Verifica funcionalidad básica

---

### Caso 4: Tests Específicos en PR

**Cuándo:** Pull Request abierto, verificar cambios

**Configuración:**
```
Branch: feature/fix-bug-123
Test path: tests/test_login.py tests/test_auth.py
```

**Resultado esperado:**
- Tests relacionados con el cambio
- Comentario automático en PR con link al reporte

---

## Monitorear Ejecución

### Ver Progreso en Tiempo Real

1. Después de iniciar el workflow
2. Click en el nombre del workflow que aparece en la lista
3. Verás cada paso ejecutándose:
   ```
   📥 Checkout código          ✅
   🐍 Configurar Python        ✅
   📦 Instalar dependencias    🟡 (ejecutando...)
   🌐 Instalar browsers        ⏸️ (pendiente)
   🧪 Ejecutar tests           ⏸️
   📊 Generar reporte          ⏸️
   🚀 Publicar a Pages         ⏸️
   ```

### Estados

- 🟡 **Amarillo** - En progreso
- ✅ **Verde** - Completado exitosamente
- ❌ **Rojo** - Falló
- ⏸️ **Gris** - Pendiente

### Ver Logs

1. Click en cualquier paso
2. Se expande mostrando logs detallados
3. Útil para debugging si algo falla

---

## Después de la Ejecución

### Si Todos los Tests Pasaron (✅)

1. Workflow muestra **✅ verde**
2. Espera 1-2 minutos
3. Reporte disponible en GitHub Pages:
   ```
   https://<usuario>.github.io/<repo>/
   ```

### Si Algún Test Falló (❌)

1. Workflow muestra **❌ rojo**
2. Click en el workflow
3. Click en paso "🧪 Ejecutar tests"
4. Revisa logs para ver qué falló
5. Reporte se genera igual con detalles del fallo
6. Accede al reporte en GitHub Pages

### Descargar Artifacts

1. Scroll hasta **Artifacts** (al final de la página)
2. Verás: `allure-results-<número>`
3. Click para descargar ZIP
4. Contiene todos los resultados y reportes

**Útil para:**
- Backup de reportes
- Análisis offline
- Compartir con el equipo

---

## Múltiples Ejecuciones

### Ejecutar en Varias Ramas

Puedes ejecutar simultáneamente en diferentes ramas:

```
1. Run workflow → Branch: main → Run
2. Run workflow → Branch: develop → Run
3. Run workflow → Branch: staging → Run
```

Cada ejecución:
- Es independiente
- Genera su propio artifact
- El último que termina actualiza GitHub Pages

### Ver Historial

1. En Actions, verás lista de todas las ejecuciones
2. Ordenadas por fecha (más reciente arriba)
3. Click en cualquiera para ver detalles

---

## Cancelar Ejecución

Si necesitas detener un workflow:

1. Ve al workflow en ejecución
2. Click en **Cancel workflow** (arriba derecha)
3. Confirma la cancelación
4. El workflow se detiene

**Útil cuando:**
- Te equivocaste de rama
- Quieres ejecutar con otros parámetros
- Algo está tardando mucho

---

## Ejemplos Avanzados

### Ejecutar Tests Paralelos

```
Test path: tests/ -n auto
```

Usa todos los CPUs disponibles para ejecutar más rápido.

### Solo Tests Fallidos

Primero ejecuta todos:
```
Test path: tests/
```

Luego solo los que fallaron:
```
Test path: tests/ --lf
```

### Con Verbose Detallado

```
Test path: tests/ -vv
```

Muestra más información en los logs.

### Excluir Tests

```
Test path: tests/ --ignore=tests/test_slow.py
```

---

## Tips y Mejores Prácticas

### ✅ Usar Nombres Descriptivos

Cuando ejecutes manualmente, GitHub usa el mensaje del commit más reciente. Haz commits descriptivos:

```bash
git commit -m "test: Run smoke tests on feature/auth"
```

### ✅ Ejecutar Antes de Merge

Siempre ejecuta el workflow en tu rama antes de crear PR:

```
1. Desarrollas en feature/...
2. Run workflow en esa rama
3. Verificas reporte
4. Si todo OK → Crear PR
```

### ✅ Smoke Tests Frecuentes

Ejecuta smoke tests regularmente en develop:

```
Branch: develop
Test path: tests/ -m smoke
```

Detecta problemas temprano.

### ✅ Revisar Trending

Después de varias ejecuciones, revisa trending en GitHub Pages:
- Identifica tests inestables (flaky)
- Ve degradación de performance
- Analiza patrones de fallos

---

## Comandos Útiles

### Ver Workflows desde CLI

```bash
# Listar workflows
gh workflow list

# Ver runs recientes
gh run list --workflow=playwright-tests.yml

# Ver detalles de un run
gh run view <run-id>
```

### Activar Workflow desde CLI

```bash
gh workflow run playwright-tests.yml \
  -f branch=main \
  -f test_path=tests/
```

---

## Resumen Rápido

| Acción | Pasos |
|--------|-------|
| Ejecutar todos los tests | Actions → Run workflow → Branch: main → Run |
| Ejecutar test específico | Test path: `tests/test_name.py` |
| Solo smoke tests | Test path: `tests/ -m smoke` |
| Ver progreso | Click en workflow ejecutando |
| Ver reporte | `https://<user>.github.io/<repo>/` |
| Descargar backup | Scroll → Artifacts → Download |
| Cancelar | Click en workflow → Cancel |

---

**Siguiente:** [03-github-pages.md](./03-github-pages.md) - Configuración de GitHub Pages
