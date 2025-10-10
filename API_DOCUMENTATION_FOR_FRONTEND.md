# 📚 Documentación de CV Recommendation API para Frontend

## 🎯 Descripción General

Sistema de análisis y recomendación de CVs usando IA. La API permite procesar CVs en PDF, descripciones de trabajo, y generar análisis de compatibilidad con scoring inteligente.

**Base URL:** `http://localhost:8000`

**Swagger UI:** `http://localhost:8000/docs`

**Arquitectura:** FastAPI + SQLAlchemy + SQLite + Azure OpenAI

---

## 📋 Índice

1. [Endpoints Principales](#endpoints-principales)
2. [Modelos de Datos](#modelos-de-datos)
3. [Flujo de Trabajo Típico](#flujo-de-trabajo-típico)
4. [Ejemplos de Requests](#ejemplos-de-requests)
5. [Manejo de Errores](#manejo-de-errores)
6. [Sistema de Pesos](#sistema-de-pesos)

---

## 🔌 Endpoints Principales

### 1. Health & Info

#### `GET /`
Información básica de la API.

**Response:**
```json
{
  "nombre": "CV Recommendation API",
  "version": "2.0.0",
  "documentacion": "/docs",
  "arquitectura": "Services + Repositories + Database"
}
```

#### `GET /health`
Health check del sistema.

**Response:**
```json
{
  "status": "ok",
  "database": "connected"
}
```

---

### 2. CVs Endpoints

#### `POST /cvs` - Procesar y Guardar CV
Sube un CV en PDF, lo procesa con IA y lo guarda en la base de datos.

**Request:**
- **Content-Type:** `multipart/form-data`
- **Body:**
  - `cv_file`: File (PDF)

**Response:**
```json
{
  "success": true,
  "cv_id": 1,
  "nombre": "Juan Pérez",
  "email": "juan@email.com",
  "telefono": "+57 300 1234567",
  "ubicacion": "Bogotá, Colombia",
  "message": "CV procesado y guardado con ID 1"
}
```

#### `GET /cvs` - Listar todos los CVs
Lista todos los CVs guardados (paginado).

**Query Params:**
- `skip`: int (default: 0)
- `limit`: int (default: 100)

**Response:**
```json
[
  {
    "id": 1,
    "nombre": "Juan Pérez",
    "email": "juan@email.com",
    "ubicacion": "Bogotá, Colombia",
    "created_at": "2024-01-15T10:30:00"
  },
  {
    "id": 2,
    "nombre": "María García",
    "email": "maria@email.com",
    "ubicacion": "Medellín, Colombia",
    "created_at": "2024-01-16T14:20:00"
  }
]
```

#### `GET /cvs/{cv_id}` - Obtener CV por ID
Obtiene un CV específico con todos sus datos estructurados.

**Response:**
```json
{
  "id": 1,
  "nombre": "Juan Pérez",
  "email": "juan@email.com",
  "telefono": "+57 300 1234567",
  "ubicacion": "Bogotá, Colombia",
  "cv_data": {
    "personal": {
      "name": "Juan Pérez",
      "email": "juan@email.com",
      "phone": "+57 300 1234567",
      "location": "Bogotá, Colombia"
    },
    "experience": [...],
    "education": [...],
    "technical_skills": [...],
    "soft_skills": [...],
    "certifications": [...],
    "languages": {...}
  },
  "created_at": "2024-01-15T10:30:00"
}
```

#### `GET /cvs/search/{nombre}` - Buscar CVs por nombre
Busca CVs que contengan el nombre especificado.

**Response:**
```json
[
  {
    "id": 1,
    "nombre": "Juan Pérez",
    "email": "juan@email.com",
    "created_at": "2024-01-15T10:30:00"
  }
]
```

#### `DELETE /cvs/{cv_id}` - Eliminar CV
Elimina un CV de la base de datos.

**Response:**
```json
{
  "message": "CV 1 eliminado"
}
```

---

### 3. Jobs Endpoints

#### `POST /jobs` - Procesar y Guardar Job Description
Procesa una descripción de trabajo y la guarda en la base de datos.

**Request:**
- **Content-Type:** `application/x-www-form-urlencoded`
- **Body:**
  - `description`: string (texto de la descripción)

**Response:**
```json
{
  "success": true,
  "job_id": 1,
  "titulo": "Desarrollador Java Senior",
  "empresa": "Vector Colombia",
  "ubicacion": "Bogotá, Colombia",
  "modalidad": "Híbrido",
  "message": "Job procesado y guardado con ID 1"
}
```

#### `GET /jobs` - Listar todos los Jobs
Lista todas las descripciones de trabajo (paginado).

**Query Params:**
- `skip`: int (default: 0)
- `limit`: int (default: 100)

**Response:**
```json
[
  {
    "id": 1,
    "titulo": "Desarrollador Java Senior",
    "empresa": "Vector Colombia",
    "ubicacion": "Bogotá, Colombia",
    "created_at": "2024-01-15T11:00:00"
  }
]
```

#### `GET /jobs/{job_id}` - Obtener Job por ID
Obtiene una descripción de trabajo específica con todos sus datos.

**Response:**
```json
{
  "id": 1,
  "titulo": "Desarrollador Java Senior",
  "empresa": "Vector Colombia",
  "ubicacion": "Bogotá, Colombia",
  "job_data": {
    "basic_info": {
      "job_title": "Desarrollador Java Senior",
      "company_name": "Vector Colombia",
      "work_modality": "Híbrido"
    },
    "experience": "5+ años en Java",
    "education": "Ingeniería de Sistemas",
    "technical_skills": [...],
    "soft_skills": [...],
    "responsibilities": [...],
    "certifications": [...],
    "languages": {...},
    "location": "Bogotá, Colombia"
  },
  "created_at": "2024-01-15T11:00:00"
}
```

#### `GET /jobs/search/{titulo}` - Buscar Jobs por título
Busca jobs que contengan el título especificado.

**Response:**
```json
[
  {
    "id": 1,
    "titulo": "Desarrollador Java Senior",
    "empresa": "Vector Colombia",
    "created_at": "2024-01-15T11:00:00"
  }
]
```

#### `DELETE /jobs/{job_id}` - Eliminar Job
Elimina un Job de la base de datos.

**Response:**
```json
{
  "message": "Job 1 eliminado"
}
```

---

### 4. Análisis Endpoints (⭐ CORE)

#### `POST /analyze/{cv_id}/{job_id}` - Realizar Análisis
Analiza la compatibilidad entre un CV y un Job usando IA.

**Path Params:**
- `cv_id`: int - ID del CV
- `job_id`: int - ID del Job

**Request Body (OPCIONAL):**
```json
{
  "experience": 0.30,
  "technical_skills": 0.15,
  "education": 0.15,
  "responsibilities": 0.15,
  "certifications": 0.10,
  "soft_skills": 0.08,
  "languages": 0.04,
  "location": 0.03
}
```

**Response:**
```json
{
  "success": true,
  "analysis_id": 1,
  "cv_id": 1,
  "job_id": 1,
  "candidato": "Juan Pérez",
  "trabajo": "Desarrollador Java Senior",
  "score": 0.823,
  "score_porcentaje": 82.3,
  "score_breakdown": {
    "experience": {
      "score": 0.90,
      "weight": 0.30,
      "contribution": 0.27,
      "ignored": false
    },
    "technical_skills": {
      "score": 0.85,
      "weight": 0.15,
      "contribution": 0.127,
      "ignored": false
    },
    "education": {
      "score": 0.75,
      "weight": 0.15,
      "contribution": 0.112,
      "ignored": false
    },
    "responsibilities": {
      "score": 0.80,
      "weight": 0.15,
      "contribution": 0.12,
      "ignored": false
    },
    "certifications": {
      "score": 0.70,
      "weight": 0.10,
      "contribution": 0.07,
      "ignored": false
    },
    "soft_skills": {
      "score": 0.88,
      "weight": 0.08,
      "contribution": 0.070,
      "ignored": false
    },
    "languages": {
      "score": 1.0,
      "weight": 0.04,
      "contribution": 0.04,
      "ignored": false
    },
    "location": {
      "score": 1.0,
      "weight": 0.03,
      "contribution": 0.03,
      "ignored": false
    }
  },
  "weights_used": {
    "experience": 0.30,
    "technical_skills": 0.15,
    "education": 0.15,
    "responsibilities": 0.15,
    "certifications": 0.10,
    "soft_skills": 0.08,
    "languages": 0.04,
    "location": 0.03
  },
  "processing_time": 2.45
}
```

#### `GET /analyses` - Listar todos los Análisis
Lista todos los análisis realizados (paginado).

**Query Params:**
- `skip`: int (default: 0)
- `limit`: int (default: 100)

**Response:**
```json
[
  {
    "id": 1,
    "cv_id": 1,
    "job_id": 1,
    "candidato": "Juan Pérez",
    "trabajo": "Desarrollador Java Senior",
    "score_porcentaje": 82.3,
    "created_at": "2024-01-15T12:00:00"
  }
]
```

#### `GET /analyses/{analysis_id}` - Obtener Análisis por ID
Obtiene un análisis específico con todos los detalles.

**Response:**
```json
{
  "id": 1,
  "cv_id": 1,
  "job_id": 1,
  "candidato": "Juan Pérez",
  "trabajo": "Desarrollador Java Senior",
  "score": 0.823,
  "score_porcentaje": 82.3,
  "score_breakdown": {...},
  "resultado_completo": {...},
  "processing_time": 2.45,
  "created_at": "2024-01-15T12:00:00"
}
```

#### `GET /cvs/{cv_id}/analyses` - Análisis de un CV
Obtiene todos los análisis realizados para un CV específico.

**Response:**
```json
[
  {
    "id": 1,
    "job_id": 1,
    "trabajo": "Desarrollador Java Senior",
    "score_porcentaje": 82.3,
    "created_at": "2024-01-15T12:00:00"
  },
  {
    "id": 2,
    "job_id": 2,
    "trabajo": "Arquitecto de Software",
    "score_porcentaje": 75.5,
    "created_at": "2024-01-16T09:30:00"
  }
]
```

#### `GET /jobs/{job_id}/analyses` - Análisis de un Job
Obtiene todos los análisis realizados para un Job específico.

**Response:**
```json
[
  {
    "id": 1,
    "cv_id": 1,
    "candidato": "Juan Pérez",
    "score_porcentaje": 82.3,
    "created_at": "2024-01-15T12:00:00"
  },
  {
    "id": 3,
    "cv_id": 2,
    "candidato": "María García",
    "score_porcentaje": 88.7,
    "created_at": "2024-01-16T10:00:00"
  }
]
```

#### `GET /jobs/{job_id}/top-candidatos` - Top Candidatos para un Job
Obtiene los mejores candidatos para un Job específico (ordenados por score).

**Query Params:**
- `limit`: int (default: 10) - Número máximo de candidatos

**Response:**
```json
[
  {
    "rank": 1,
    "analysis_id": 3,
    "cv_id": 2,
    "candidato": "María García",
    "score_porcentaje": 88.7,
    "created_at": "2024-01-16T10:00:00"
  },
  {
    "rank": 2,
    "analysis_id": 1,
    "cv_id": 1,
    "candidato": "Juan Pérez",
    "score_porcentaje": 82.3,
    "created_at": "2024-01-15T12:00:00"
  },
  {
    "rank": 3,
    "analysis_id": 5,
    "cv_id": 4,
    "candidato": "Carlos Rodríguez",
    "score_porcentaje": 79.1,
    "created_at": "2024-01-17T11:20:00"
  }
]
```

#### `GET /stats` - Estadísticas Generales
Obtiene estadísticas generales del sistema.

**Response:**
```json
{
  "total_cvs": 15,
  "total_jobs": 8,
  "total_analyses": 45,
  "score_promedio": 0.782,
  "score_promedio_porcentaje": 78.2
}
```

---

## 📊 Modelos de Datos

### CV Data Structure
```json
{
  "personal": {
    "name": "string",
    "email": "string",
    "phone": "string",
    "location": "string"
  },
  "experience": [
    {
      "job_title": "string",
      "company": "string",
      "duration": "string",
      "responsibilities": ["string"]
    }
  ],
  "education": [
    {
      "degree": "string",
      "institution": "string",
      "year": "string"
    }
  ],
  "technical_skills": ["string"],
  "soft_skills": ["string"],
  "certifications": ["string"],
  "languages": {
    "language_name": "proficiency_level"
  }
}
```

### Job Data Structure
```json
{
  "basic_info": {
    "job_title": "string",
    "company_name": "string",
    "work_modality": "string"
  },
  "experience": "string",
  "education": "string",
  "technical_skills": ["string"],
  "soft_skills": ["string"],
  "responsibilities": ["string"],
  "certifications": ["string"],
  "languages": {
    "language_name": "proficiency_level"
  },
  "location": "string"
}
```

### Weights Structure (Opcional)
```json
{
  "experience": 0.30,          // 0-1, default: 0.30
  "technical_skills": 0.15,    // 0-1, default: 0.15
  "education": 0.15,           // 0-1, default: 0.15
  "responsibilities": 0.15,    // 0-1, default: 0.15
  "certifications": 0.10,      // 0-1, default: 0.10
  "soft_skills": 0.08,         // 0-1, default: 0.08
  "languages": 0.04,           // 0-1, default: 0.04
  "location": 0.03             // 0-1, default: 0.03
}
```

---

## 🔄 Flujo de Trabajo Típico

### Escenario 1: Análisis de un CV para un Job

```
1. POST /cvs (subir CV PDF)
   → Recibir cv_id

2. POST /jobs (enviar descripción de trabajo)
   → Recibir job_id

3. POST /analyze/{cv_id}/{job_id} (opcional: con weights)
   → Recibir análisis con score

4. GET /analyses/{analysis_id} (ver detalles completos)
```

### Escenario 2: Encontrar los mejores candidatos para un puesto

```
1. POST /jobs (crear el job)
   → Recibir job_id

2. POST /cvs (subir múltiples CVs)
   → Recibir cv_id para cada uno

3. POST /analyze/{cv_id}/{job_id} (para cada CV)
   → Recibir analysis_id

4. GET /jobs/{job_id}/top-candidatos?limit=10
   → Recibir ranking de mejores candidatos
```

### Escenario 3: Ver historial de un candidato

```
1. GET /cvs (listar CVs)
   → Seleccionar un cv_id

2. GET /cvs/{cv_id}/analyses
   → Ver todos los análisis de ese candidato

3. GET /analyses/{analysis_id}
   → Ver detalles de un análisis específico
```

---

## 📝 Ejemplos de Requests

### JavaScript/TypeScript (Fetch)

#### Subir CV
```javascript
const formData = new FormData();
formData.append('cv_file', fileInput.files[0]);

const response = await fetch('http://localhost:8000/cvs', {
  method: 'POST',
  body: formData
});

const result = await response.json();
console.log('CV ID:', result.cv_id);
```

#### Crear Job
```javascript
const formData = new FormData();
formData.append('description', jobDescriptionText);

const response = await fetch('http://localhost:8000/jobs', {
  method: 'POST',
  body: formData
});

const result = await response.json();
console.log('Job ID:', result.job_id);
```

#### Analizar con Pesos Personalizados
```javascript
const response = await fetch('http://localhost:8000/analyze/1/1', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    experience: 0.40,
    technical_skills: 0.25,
    education: 0.15,
    responsibilities: 0.10,
    certifications: 0.05,
    soft_skills: 0.03,
    languages: 0.01,
    location: 0.01
  })
});

const result = await response.json();
console.log('Score:', result.score_porcentaje + '%');
```

#### Analizar sin Pesos (usar predeterminados)
```javascript
const response = await fetch('http://localhost:8000/analyze/1/1', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(null)  // o simplemente no enviar body
});

const result = await response.json();
console.log('Score:', result.score_porcentaje + '%');
```

#### Obtener Top Candidatos
```javascript
const response = await fetch('http://localhost:8000/jobs/1/top-candidatos?limit=5');
const topCandidates = await response.json();

topCandidates.forEach(candidate => {
  console.log(`${candidate.rank}. ${candidate.candidato}: ${candidate.score_porcentaje}%`);
});
```

### Python (Requests)

#### Subir CV
```python
import requests

with open('cv.pdf', 'rb') as f:
    files = {'cv_file': f}
    response = requests.post('http://localhost:8000/cvs', files=files)
    result = response.json()
    print(f"CV ID: {result['cv_id']}")
```

#### Analizar
```python
import requests

weights = {
    "experience": 0.40,
    "technical_skills": 0.30,
    "education": 0.20,
    "soft_skills": 0.10
}

response = requests.post(
    'http://localhost:8000/analyze/1/1',
    json=weights
)

result = response.json()
print(f"Score: {result['score_porcentaje']}%")
```

---

## ⚠️ Manejo de Errores

### Códigos de Estado HTTP

| Código | Significado | Ejemplo |
|--------|-------------|---------|
| 200 | Success | Operación exitosa |
| 404 | Not Found | CV o Job no encontrado |
| 422 | Validation Error | Pesos inválidos (fuera de rango 0-1) |
| 500 | Internal Server Error | Error en procesamiento de IA |

### Formato de Error

```json
{
  "detail": "CV no encontrado"
}
```

### Validaciones de Pesos

- Cada peso debe estar entre 0 y 1
- Los nombres deben ser exactos: `experience`, `technical_skills`, etc.
- No es necesario enviar todos los pesos (los faltantes usan predeterminados)
- Si envías un diccionario vacío `{}`, se usan los predeterminados

---

## 🎨 Sistema de Pesos

### Pesos Predeterminados (Default)

```json
{
  "experience": 0.30,          // 30% - Experiencia laboral
  "technical_skills": 0.15,    // 15% - Habilidades técnicas
  "education": 0.15,           // 15% - Educación
  "responsibilities": 0.15,    // 15% - Responsabilidades
  "certifications": 0.10,      // 10% - Certificaciones
  "soft_skills": 0.08,         // 8%  - Habilidades blandas
  "languages": 0.04,           // 4%  - Idiomas
  "location": 0.03             // 3%  - Ubicación
}
```

### Perfiles Recomendados de Pesos

#### Perfil Junior
```json
{
  "education": 0.35,
  "technical_skills": 0.25,
  "certifications": 0.15,
  "experience": 0.15,
  "soft_skills": 0.10
}
```

#### Perfil Senior Técnico
```json
{
  "experience": 0.40,
  "technical_skills": 0.30,
  "certifications": 0.15,
  "education": 0.10,
  "soft_skills": 0.05
}
```

#### Perfil Gerencial
```json
{
  "experience": 0.35,
  "soft_skills": 0.25,
  "responsibilities": 0.20,
  "education": 0.10,
  "technical_skills": 0.10
}
```

### Interpretación del Score

- **90-100%**: Candidato excepcional, altamente recomendado
- **80-89%**: Candidato muy bueno, buen ajuste
- **70-79%**: Candidato bueno, cumple la mayoría de requisitos
- **60-69%**: Candidato aceptable, cumple requisitos básicos
- **50-59%**: Candidato por debajo del perfil
- **< 50%**: Candidato no recomendado

---

## 🚀 Recomendaciones para el Frontend

### 1. **Dashboard Principal**
- Mostrar estadísticas (`GET /stats`)
- Listar CVs y Jobs recientes
- Acceso rápido a crear análisis

### 2. **Gestión de CVs**
- Tabla con lista de CVs (`GET /cvs`)
- Upload de CV con preview (`POST /cvs`)
- Ver detalles de CV (`GET /cvs/{id}`)
- Ver análisis de un CV (`GET /cvs/{id}/analyses`)
- Búsqueda por nombre (`GET /cvs/search/{nombre}`)

### 3. **Gestión de Jobs**
- Tabla con lista de Jobs (`GET /jobs`)
- Formulario para crear Job (`POST /jobs`)
- Ver detalles de Job (`GET /jobs/{id}`)
- Ver candidatos para un Job (`GET /jobs/{id}/analyses`)
- Ranking de mejores candidatos (`GET /jobs/{id}/top-candidatos`)

### 4. **Módulo de Análisis**
- Selector de CV y Job
- Configurador de pesos (con presets: Junior, Senior, Gerencial)
- Ejecutar análisis (`POST /analyze/{cv_id}/{job_id}`)
- Visualización de resultados:
  - Score general (gauge/circular progress)
  - Breakdown por aspecto (gráfico de barras)
  - Detalles de contribución de cada aspecto

### 5. **Vista de Ranking**
- Top candidatos para un Job
- Podium visual (1°, 2°, 3°)
- Comparación lado a lado
- Filtros y ordenamiento

### 6. **Características Adicionales**
- Gráficos de score_breakdown (radar chart, bar chart)
- Exportación a PDF/Excel
- Historial de análisis
- Notificaciones de procesamiento
- Loading states (el procesamiento toma 2-5 segundos)

---

## 🔐 CORS

La API está configurada con CORS abierto (`allow_origins=["*"]`) para desarrollo. 

**Orígenes permitidos actualmente:**
- `http://localhost:3000` (React, Next.js)
- `http://localhost:5173` (Vite)
- `http://localhost:8080` (Vue)
- `http://localhost:4200` (Angular)

---

## 📌 Notas Importantes

1. **Procesamiento Asíncrono**: Los endpoints de procesamiento (CV y Job) pueden tardar 2-5 segundos. Implementar loading states.

2. **Caché de CVs**: El sistema detecta CVs duplicados por hash del archivo. Si subes el mismo PDF dos veces, retorna el existente.

3. **Normalización de Pesos**: Si los pesos no suman 1.0, el sistema los normaliza automáticamente.

4. **Score Breakdown**: Cada aspecto tiene un score (0-1), un weight (0-1), y una contribution al score final.

5. **Aspectos Ignorados**: Si un aspecto tiene score -1, significa que no había datos suficientes y fue ignorado en el cálculo.

6. **Base de Datos**: SQLite local (`cv_system.db`). Los datos persisten entre reinicios.

7. **Formato de Fechas**: Todas las fechas están en formato ISO 8601 (`2024-01-15T10:30:00`).

---

## 🛠️ Testing Rápido

### Usando cURL

```bash
# Health check
curl http://localhost:8000/health

# Subir CV
curl -X POST "http://localhost:8000/cvs" \
  -F "cv_file=@/path/to/cv.pdf"

# Crear Job
curl -X POST "http://localhost:8000/jobs" \
  -F "description=Buscamos desarrollador Python con 3+ años de experiencia..."

# Analizar (sin pesos)
curl -X POST "http://localhost:8000/analyze/1/1" \
  -H "Content-Type: application/json" \
  -d "null"

# Analizar (con pesos)
curl -X POST "http://localhost:8000/analyze/1/1" \
  -H "Content-Type: application/json" \
  -d '{"experience": 0.40, "technical_skills": 0.30}'

# Top candidatos
curl "http://localhost:8000/jobs/1/top-candidatos?limit=5"
```

---

## 📞 Soporte

- **Swagger UI**: `http://localhost:8000/docs` (documentación interactiva completa)
- **ReDoc**: `http://localhost:8000/redoc` (documentación alternativa)
- **OpenAPI Schema**: `http://localhost:8000/openapi.json`

---

## 🎯 Checklist para el Frontend

- [ ] Configurar base URL de la API
- [ ] Implementar manejo de CORS
- [ ] Crear servicio/cliente HTTP
- [ ] Implementar manejo de errores global
- [ ] Implementar loading states
- [ ] Crear componentes para upload de archivos
- [ ] Crear formularios para Jobs
- [ ] Implementar visualización de scores
- [ ] Crear gráficos de score_breakdown
- [ ] Implementar sistema de pesos personalizable
- [ ] Crear vista de ranking/top candidatos
- [ ] Implementar búsqueda y filtros
- [ ] Agregar paginación
- [ ] Implementar exportación de resultados
- [ ] Testing con datos reales

---

## 📊 Estructura de Base de Datos

### Tabla: `cvs`
- `id` (PK)
- `nombre`
- `email`
- `telefono`
- `ubicacion`
- `cv_data` (JSON)
- `created_at`

### Tabla: `jobs`
- `id` (PK)
- `titulo`
- `empresa`
- `ubicacion`
- `job_data` (JSON)
- `created_at`

### Tabla: `analyses`
- `id` (PK)
- `cv_id` (FK)
- `job_id` (FK)
- `nombre_candidato`
- `titulo_trabajo`
- `score` (float)
- `score_breakdown` (JSON)
- `resultado_completo` (JSON)
- `processing_time` (float)
- `created_at`

---

**Versión de la API:** 2.0.0  
**Última actualización:** 2024  
**Tecnologías:** FastAPI, SQLAlchemy, SQLite, Azure OpenAI, LangChain

