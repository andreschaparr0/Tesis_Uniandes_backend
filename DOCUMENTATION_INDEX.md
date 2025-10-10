# 📚 Índice de Documentación - CV Recommendation API

## 🎯 Para empezar rápido

### 🚀 [QUICK_START_FRONTEND.md](QUICK_START_FRONTEND.md)
**Guía de inicio rápido para desarrolladores frontend**

- Resumen ejecutivo de la API
- Flujo principal (3 pasos)
- Endpoints esenciales
- Código de ejemplo mínimo
- Testing rápido
- Prioridad de implementación

**👉 Empieza aquí si quieres una visión general rápida**

---

## 📖 Documentación Completa

### 📚 [API_DOCUMENTATION_FOR_FRONTEND.md](API_DOCUMENTATION_FOR_FRONTEND.md)
**Documentación técnica completa de la API**

- Todos los endpoints detallados
- Modelos de datos completos
- Flujos de trabajo típicos
- Ejemplos de requests/responses
- Manejo de errores
- Sistema de pesos explicado
- Recomendaciones de arquitectura frontend
- Estructura de base de datos
- Checklist de implementación

**👉 Consulta este documento para detalles técnicos completos**

---

## 💻 Ejemplos de Código

### 🎨 [FRONTEND_INTEGRATION_EXAMPLES.md](FRONTEND_INTEGRATION_EXAMPLES.md)
**Ejemplos prácticos de integración**

**Contenido:**
- API Client completo en TypeScript
- Ejemplos React/Next.js:
  - CVUploader component
  - CVAnalyzer con pesos
  - TopCandidates component
  - Dashboard component
- Ejemplos Vue.js:
  - Composable para API
  - Componentes Vue
- State Management (Zustand, Pinia)
- Visualización con gráficos
- Checklist de implementación

**👉 Usa este documento para implementación práctica**

---

## ⚖️ Sistema de Pesos

### 📊 [api/WEIGHTS_GUIDE.md](api/WEIGHTS_GUIDE.md)
**Guía completa del sistema de pesos**

**Contenido:**
- ¿Qué son los pesos?
- Pesos predeterminados
- Cómo usar pesos personalizados
- Ejemplos prácticos por perfil:
  - Junior
  - Senior Técnico
  - Gerencial
- Errores comunes
- Interpretación del score
- Testing en Swagger UI

**👉 Referencia obligatoria para configurar análisis**

---

## 🛠️ Documentación Backend

### 📝 [README.md](README.md)
**Guía general del proyecto backend**

**Contenido:**
- Descripción del proyecto
- Instalación y configuración
- Estructura del proyecto
- Cómo ejecutar la API
- Variables de entorno
- Tecnologías utilizadas

**👉 Para configurar y ejecutar el backend**

---

## 🌐 Documentación Interactiva

### 📡 Swagger UI
**URL:** `http://localhost:8000/docs`

- Documentación interactiva autogenerada
- Probar endpoints en vivo
- Ver esquemas de datos
- Ejemplos de requests/responses

**👉 Para testing y exploración interactiva**

### 📄 ReDoc
**URL:** `http://localhost:8000/redoc`

- Documentación alternativa (más legible)
- Mejor para lectura
- Esquema OpenAPI completo

**👉 Para lectura detallada de la API**

### 🔧 OpenAPI Schema
**URL:** `http://localhost:8000/openapi.json`

- Esquema JSON de la API
- Para generar clientes automáticamente
- Para integración con herramientas

---

## 📊 Arquitectura y Estructura

### 🏗️ Estructura del Backend

```
Tesis_Uniandes_backend/
├── api/                        # API FastAPI
│   ├── main.py                # Endpoints principales
│   ├── database.py            # Modelos SQLAlchemy
│   ├── repositories.py        # Capa de datos
│   ├── services.py            # Lógica de negocio
│   └── WEIGHTS_GUIDE.md       # Guía de pesos
│
├── main/                      # Core del sistema
│   ├── data_cleaner.py        # Limpieza de PDFs
│   ├── data_structurer.py     # Estructuración con IA
│   └── recommendation_engine.py # Motor de recomendación
│
├── algoritmo_recomendacion/   # Comparadores
│   ├── comparator_main.py     # Orquestador
│   └── comparators/           # Comparadores individuales
│
├── src/                       # Utilidades
│   ├── estructuracion_CV/     # Extracción de CVs
│   ├── estructuracion_Descripcion/ # Extracción de Jobs
│   └── limpieza/              # Limpieza de texto
│
└── DOCUMENTATION/             # Documentación
    ├── QUICK_START_FRONTEND.md
    ├── API_DOCUMENTATION_FOR_FRONTEND.md
    ├── FRONTEND_INTEGRATION_EXAMPLES.md
    └── DOCUMENTATION_INDEX.md (este archivo)
```

---

## 🔄 Flujo de Datos

```
1. Frontend sube CV (PDF)
   ↓
2. API extrae texto del PDF (PyMuPDF)
   ↓
3. API estructura CV con IA (Azure OpenAI)
   ↓
4. API guarda en SQLite
   ↓
5. Frontend crea Job (texto)
   ↓
6. API estructura Job con IA
   ↓
7. API guarda en SQLite
   ↓
8. Frontend solicita análisis
   ↓
9. API compara CV vs Job (8 aspectos)
   ↓
10. API calcula score ponderado
    ↓
11. API guarda resultado
    ↓
12. Frontend muestra resultados
```

---

## 🎯 Casos de Uso

### Caso 1: Análisis Individual
1. Subir 1 CV
2. Crear 1 Job
3. Analizar
4. Ver resultados

**Documentos relevantes:**
- [QUICK_START_FRONTEND.md](QUICK_START_FRONTEND.md) - Flujo principal
- [API_DOCUMENTATION_FOR_FRONTEND.md](API_DOCUMENTATION_FOR_FRONTEND.md) - Endpoints

### Caso 2: Ranking de Candidatos
1. Crear 1 Job
2. Subir múltiples CVs
3. Analizar cada CV vs Job
4. Ver ranking de top candidatos

**Documentos relevantes:**
- [API_DOCUMENTATION_FOR_FRONTEND.md](API_DOCUMENTATION_FOR_FRONTEND.md) - Endpoint `/jobs/{id}/top-candidatos`
- [FRONTEND_INTEGRATION_EXAMPLES.md](FRONTEND_INTEGRATION_EXAMPLES.md) - TopCandidates component

### Caso 3: Análisis con Pesos Personalizados
1. Configurar pesos según perfil
2. Ejecutar análisis
3. Comparar con análisis default

**Documentos relevantes:**
- [api/WEIGHTS_GUIDE.md](api/WEIGHTS_GUIDE.md) - Guía completa de pesos
- [FRONTEND_INTEGRATION_EXAMPLES.md](FRONTEND_INTEGRATION_EXAMPLES.md) - WeightConfigurator

---

## 📋 Checklist de Implementación

### Backend (✅ Completado)
- [x] API con FastAPI
- [x] Base de datos SQLite
- [x] Procesamiento de CVs con IA
- [x] Procesamiento de Jobs con IA
- [x] Motor de recomendación
- [x] Sistema de pesos configurables
- [x] Endpoints completos
- [x] Documentación Swagger
- [x] CORS configurado

### Frontend (📝 Por implementar)
- [ ] Setup del proyecto
- [ ] API Client
- [ ] Dashboard con estadísticas
- [ ] Upload de CVs
- [ ] Creación de Jobs
- [ ] Módulo de análisis
- [ ] Configurador de pesos
- [ ] Visualización de scores
- [ ] Gráficos de breakdown
- [ ] Top candidatos
- [ ] Listas con búsqueda
- [ ] Historial de análisis

---

## 🚀 Orden de Lectura Recomendado

### Para un LLM que implementará el frontend:

1. **Primero** → [QUICK_START_FRONTEND.md](QUICK_START_FRONTEND.md)
   - Entender el flujo básico
   - Ver ejemplos mínimos
   - Conocer endpoints esenciales

2. **Segundo** → [API_DOCUMENTATION_FOR_FRONTEND.md](API_DOCUMENTATION_FOR_FRONTEND.md)
   - Detalles técnicos completos
   - Todos los endpoints
   - Modelos de datos
   - Flujos de trabajo

3. **Tercero** → [FRONTEND_INTEGRATION_EXAMPLES.md](FRONTEND_INTEGRATION_EXAMPLES.md)
   - Implementación práctica
   - Componentes completos
   - API Client robusto

4. **Cuarto** → [api/WEIGHTS_GUIDE.md](api/WEIGHTS_GUIDE.md)
   - Sistema de pesos
   - Perfiles recomendados
   - Ejemplos de uso

5. **Durante desarrollo** → Swagger UI (`http://localhost:8000/docs`)
   - Testing en vivo
   - Validación de requests

---

## 🔗 Enlaces Rápidos

| Documento | Propósito | Cuándo Usar |
|-----------|-----------|-------------|
| [QUICK_START_FRONTEND.md](QUICK_START_FRONTEND.md) | Inicio rápido | **Al comenzar** |
| [API_DOCUMENTATION_FOR_FRONTEND.md](API_DOCUMENTATION_FOR_FRONTEND.md) | Referencia completa | **Durante desarrollo** |
| [FRONTEND_INTEGRATION_EXAMPLES.md](FRONTEND_INTEGRATION_EXAMPLES.md) | Código práctico | **Al implementar** |
| [api/WEIGHTS_GUIDE.md](api/WEIGHTS_GUIDE.md) | Sistema de pesos | **Al configurar análisis** |
| [README.md](README.md) | Setup backend | **Si modificas backend** |
| Swagger UI | Testing interactivo | **Al probar endpoints** |

---

## 💡 Tips para el Desarrollo

### 1. Setup Inicial
- Leer [QUICK_START_FRONTEND.md](QUICK_START_FRONTEND.md)
- Ejecutar backend: `python run_api.py`
- Verificar: `http://localhost:8000/health`
- Explorar: `http://localhost:8000/docs`

### 2. Durante Desarrollo
- Usar [API_DOCUMENTATION_FOR_FRONTEND.md](API_DOCUMENTATION_FOR_FRONTEND.md) como referencia
- Copiar código de [FRONTEND_INTEGRATION_EXAMPLES.md](FRONTEND_INTEGRATION_EXAMPLES.md)
- Probar en Swagger UI antes de implementar

### 3. Para Análisis
- Consultar [api/WEIGHTS_GUIDE.md](api/WEIGHTS_GUIDE.md)
- Implementar presets (Junior, Senior, Manager)
- Validar pesos suman 1.0 (la API normaliza automáticamente)

### 4. Debugging
- Revisar respuestas en Swagger UI
- Verificar CORS (debe estar en `localhost:3000`, `:5173`, etc.)
- Check loading states (procesamiento tarda 2-5 segundos)

---

## 🆘 Troubleshooting

### ❌ Error: CORS
**Solución:** Verifica que tu frontend esté en un puerto permitido (3000, 5173, 8080, 4200)

### ❌ Error: 404 Not Found
**Solución:** Verifica que el CV/Job exista antes de analizar

### ❌ Error: 422 Validation Error
**Solución:** Revisa los pesos (deben estar entre 0 y 1)

### ❌ Error: Procesamiento lento
**Solución:** Normal, Azure OpenAI tarda 2-5 segundos. Implementa loading states.

---

## 📞 Contacto y Recursos

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`
- **OpenAPI Schema:** `http://localhost:8000/openapi.json`

---

## 🎓 Para LLMs

**Instrucciones para otro LLM que desarrollará el frontend:**

```
Hola! Vas a desarrollar el frontend para una API de recomendación de CVs.

1. LEE PRIMERO: QUICK_START_FRONTEND.md
   - Te dará la visión general y flujo básico
   
2. REFERENCIA PRINCIPAL: API_DOCUMENTATION_FOR_FRONTEND.md
   - Documentación técnica completa de todos los endpoints
   
3. COPIA CÓDIGO DE: FRONTEND_INTEGRATION_EXAMPLES.md
   - Implementaciones completas de componentes React/Vue
   - API Client listo para usar
   
4. PARA PESOS: api/WEIGHTS_GUIDE.md
   - Sistema de pesos detallado
   - Perfiles predefinidos
   
5. PRUEBA EN: http://localhost:8000/docs
   - Swagger UI para testing

El backend ya está 100% funcional. Solo necesitas crear el frontend
que consuma la API. Todos los ejemplos de código están listos.

¡Éxito! 🚀
```

---

**Versión:** 1.0.0  
**Última actualización:** 2024  
**Proyecto:** CV Recommendation API - Tesis Universidad de los Andes

