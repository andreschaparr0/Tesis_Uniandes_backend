# 📡 API Documentation - CV Recommendation System

Documentación completa de la API REST para el sistema de recomendación de CVs.

**Base URL:** `http://localhost:8000`  
**Versión:** 2.0.0

---

## 📋 Tabla de Contenidos

1. [Información General](#información-general)
2. [Autenticación](#autenticación)
3. [Endpoints](#endpoints)
   - [Health & Info](#health--info)
   - [CVs](#cvs)
   - [Jobs](#jobs)
   - [Análisis](#análisis)
4. [Modelos de Datos](#modelos-de-datos)
5. [Sistema de Pesos](#sistema-de-pesos)
6. [Códigos de Error](#códigos-de-error)
7. [Ejemplos de Uso](#ejemplos-de-uso)

---

## 🌐 Información General

### Características de la API

- **Formato**: JSON (excepto uploads multipart/form-data)
- **Protocolo**: HTTP/HTTPS
- **CORS**: Habilitado para desarrollo (`localhost:*`)
- **Documentación Interactiva**: `/docs` (Swagger UI)
- **Esquema OpenAPI**: `/openapi.json`

### Headers Comunes

```
Content-Type: application/json
Accept: application/json
```

---

## 🔐 Autenticación

Actualmente la API **no requiere autenticación** (desarrollo).

---

## 📌 Endpoints

### Health & Info

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

### CVs

#### `POST /cvs`

Procesa y guarda un CV desde un archivo PDF.

**Request:**
- **Content-Type:** `multipart/form-data`
- **Body:**
  - `cv_file` (File, required): Archivo PDF del CV

**Response (200):**
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

**Errores:**
- `500`: Error en procesamiento

**Ejemplo:**
```bash
curl -X POST "http://localhost:8000/cvs" \
  -F "cv_file=@/path/to/cv.pdf"
```

---

#### `GET /cvs`

Lista todos los CVs guardados (paginado).

**Query Parameters:**
- `skip` (int, optional): Número de registros a saltar (default: 0)
- `limit` (int, optional): Número máximo de registros (default: 100)

**Response (200):**
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

**Ejemplo:**
```bash
curl "http://localhost:8000/cvs?skip=0&limit=10"
```

---

#### `GET /cvs/{cv_id}`

Obtiene un CV específico con todos sus datos estructurados.

**Path Parameters:**
- `cv_id` (int, required): ID del CV

**Response (200):**
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
    "experience": [
      {
        "job_title": "Desarrollador Senior",
        "company": "Tech Corp",
        "duration": "3 años",
        "responsibilities": ["Desarrollo backend", "Code review"]
      }
    ],
    "education": [
      {
        "degree": "Ingeniería de Sistemas",
        "institution": "Universidad de los Andes",
        "year": "2020"
      }
    ],
    "technical_skills": ["Java", "Python", "Spring Boot"],
    "soft_skills": ["Liderazgo", "Trabajo en equipo"],
    "certifications": ["AWS Certified Developer"],
    "languages": {
      "Español": "Nativo",
      "Inglés": "Avanzado"
    }
  },
  "created_at": "2024-01-15T10:30:00"
}
```

**Errores:**
- `404`: CV no encontrado

**Ejemplo:**
```bash
curl "http://localhost:8000/cvs/1"
```

---

#### `GET /cvs/search/{nombre}`

Busca CVs por nombre (búsqueda parcial, case-insensitive).

**Path Parameters:**
- `nombre` (string, required): Texto a buscar en el nombre

**Response (200):**
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

**Ejemplo:**
```bash
curl "http://localhost:8000/cvs/search/juan"
```

---

#### `DELETE /cvs/{cv_id}`

Elimina un CV de la base de datos.

**Path Parameters:**
- `cv_id` (int, required): ID del CV

**Response (200):**
```json
{
  "message": "CV 1 eliminado"
}
```

**Errores:**
- `404`: CV no encontrado

**Ejemplo:**
```bash
curl -X DELETE "http://localhost:8000/cvs/1"
```

---

### Jobs

#### `POST /jobs`

Procesa y guarda una descripción de trabajo.

**Request:**
- **Content-Type:** `application/x-www-form-urlencoded`
- **Body:**
  - `description` (string, required): Texto completo de la descripción de trabajo

**Response (200):**
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

**Errores:**
- `500`: Error en procesamiento

**Ejemplo:**
```bash
curl -X POST "http://localhost:8000/jobs" \
  -F "description=Desarrollador Java Senior con 5+ años de experiencia..."
```

---

#### `GET /jobs`

Lista todos los Jobs guardados (paginado).

**Query Parameters:**
- `skip` (int, optional): Número de registros a saltar (default: 0)
- `limit` (int, optional): Número máximo de registros (default: 100)

**Response (200):**
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

**Ejemplo:**
```bash
curl "http://localhost:8000/jobs?skip=0&limit=10"
```

---

#### `GET /jobs/{job_id}`

Obtiene un Job específico con todos sus datos estructurados.

**Path Parameters:**
- `job_id` (int, required): ID del Job

**Response (200):**
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
    "experience": "5+ años en desarrollo Java",
    "education": "Ingeniería de Sistemas o afín",
    "technical_skills": ["Java", "Spring Boot", "AWS"],
    "soft_skills": ["Liderazgo", "Comunicación"],
    "responsibilities": ["Desarrollar microservicios", "Mentorear junior"],
    "certifications": ["AWS Certified Developer"],
    "languages": {
      "Español": "Nativo",
      "Inglés": "Avanzado"
    },
    "location": "Bogotá, Colombia"
  },
  "created_at": "2024-01-15T11:00:00"
}
```

**Errores:**
- `404`: Job no encontrado

**Ejemplo:**
```bash
curl "http://localhost:8000/jobs/1"
```

---

#### `GET /jobs/search/{titulo}`

Busca Jobs por título (búsqueda parcial, case-insensitive).

**Path Parameters:**
- `titulo` (string, required): Texto a buscar en el título

**Response (200):**
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

**Ejemplo:**
```bash
curl "http://localhost:8000/jobs/search/java"
```

---

#### `DELETE /jobs/{job_id}`

Elimina un Job de la base de datos.

**Path Parameters:**
- `job_id` (int, required): ID del Job

**Response (200):**
```json
{
  "message": "Job 1 eliminado"
}
```

**Errores:**
- `404`: Job no encontrado

**Ejemplo:**
```bash
curl -X DELETE "http://localhost:8000/jobs/1"
```

---

### Análisis

#### `POST /analyze/{cv_id}/{job_id}` ⭐

Realiza un análisis de compatibilidad entre un CV y un Job.

**Path Parameters:**
- `cv_id` (int, required): ID del CV
- `job_id` (int, required): ID del Job

**Request Body (opcional):**
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

> **Nota:** Si no envías pesos, se usan los predeterminados. Puedes enviar solo algunos pesos y el resto usará los valores por defecto (se normaliza automáticamente).

**Response (200):**
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
  "summary": "Candidato muy adecuado. Destaca en Experiencia, Habilidades Técnicas y Habilidades Blandas. Requiere mejorar en Certificaciones.",
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
  "processing_time": 2.45
}
```

**Errores:**
- `404`: CV o Job no encontrado
- `422`: Pesos inválidos (fuera del rango 0-1)
- `500`: Error en procesamiento

**Ejemplos:**

```bash
# Sin pesos (usar predeterminados)
curl -X POST "http://localhost:8000/analyze/1/1" \
  -H "Content-Type: application/json"

# Con pesos personalizados
curl -X POST "http://localhost:8000/analyze/1/1" \
  -H "Content-Type: application/json" \
  -d '{
    "experience": 0.40,
    "technical_skills": 0.30,
    "education": 0.20,
    "soft_skills": 0.10
  }'
```

---

#### `GET /analyses`

Lista todos los análisis realizados (paginado).

**Query Parameters:**
- `skip` (int, optional): Número de registros a saltar (default: 0)
- `limit` (int, optional): Número máximo de registros (default: 100)

**Response (200):**
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

**Ejemplo:**
```bash
curl "http://localhost:8000/analyses?skip=0&limit=20"
```

---

#### `GET /analyses/{analysis_id}`

Obtiene un análisis específico con todos los detalles.

**Path Parameters:**
- `analysis_id` (int, required): ID del análisis

**Response (200):**
```json
{
  "id": 1,
  "cv_id": 1,
  "job_id": 1,
  "candidato": "Juan Pérez",
  "trabajo": "Desarrollador Java Senior",
  "score": 0.823,
  "score_porcentaje": 82.3,
  "score_breakdown": { ... },
  "resultado_completo": { ... },
  "processing_time": 2.45,
  "created_at": "2024-01-15T12:00:00"
}
```

**Errores:**
- `404`: Análisis no encontrado

**Ejemplo:**
```bash
curl "http://localhost:8000/analyses/1"
```

---

#### `DELETE /analyses/{analysis_id}`

Elimina un análisis de la base de datos.

**Path Parameters:**
- `analysis_id` (int, required): ID del análisis

**Response (200):**
```json
{
  "message": "Análisis 1 eliminado"
}
```

**Errores:**
- `404`: Análisis no encontrado

**Ejemplo:**
```bash
curl -X DELETE "http://localhost:8000/analyses/1"
```

---

#### `GET /cvs/{cv_id}/analyses`

Obtiene todos los análisis realizados para un CV específico.

**Path Parameters:**
- `cv_id` (int, required): ID del CV

**Response (200):**
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

**Ejemplo:**
```bash
curl "http://localhost:8000/cvs/1/analyses"
```

---

#### `GET /jobs/{job_id}/analyses`

Obtiene todos los análisis realizados para un Job específico.

**Path Parameters:**
- `job_id` (int, required): ID del Job

**Response (200):**
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

**Ejemplo:**
```bash
curl "http://localhost:8000/jobs/1/analyses"
```

---

#### `GET /jobs/{job_id}/top-candidatos` ⭐

Obtiene los mejores candidatos para un Job específico, ordenados por score.

**Path Parameters:**
- `job_id` (int, required): ID del Job

**Query Parameters:**
- `limit` (int, optional): Número máximo de candidatos (default: 10)

**Response (200):**
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

**Ejemplo:**
```bash
curl "http://localhost:8000/jobs/1/top-candidatos?limit=5"
```

---

#### `GET /stats` ⭐

Obtiene estadísticas generales del sistema.

**Response (200):**
```json
{
  "total_cvs": 15,
  "total_jobs": 8,
  "total_analyses": 45,
  "score_promedio": 0.782,
  "score_promedio_porcentaje": 78.2
}
```

**Ejemplo:**
```bash
curl "http://localhost:8000/stats"
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

### Weights Structure

```json
{
  "experience": 0.30,          // 0-1 (default: 0.30)
  "technical_skills": 0.15,    // 0-1 (default: 0.15)
  "education": 0.15,           // 0-1 (default: 0.15)
  "responsibilities": 0.15,    // 0-1 (default: 0.15)
  "certifications": 0.10,      // 0-1 (default: 0.10)
  "soft_skills": 0.08,         // 0-1 (default: 0.08)
  "languages": 0.04,           // 0-1 (default: 0.04)
  "location": 0.03             // 0-1 (default: 0.03)
}
```

---

## ⚖️ Sistema de Pesos

### Pesos Predeterminados

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

### Perfiles Sugeridos

**Perfil Junior:**
```json
{
  "education": 0.35,
  "technical_skills": 0.25,
  "certifications": 0.15,
  "experience": 0.15,
  "soft_skills": 0.10
}
```

**Perfil Senior Técnico:**
```json
{
  "experience": 0.40,
  "technical_skills": 0.30,
  "certifications": 0.15,
  "education": 0.10,
  "soft_skills": 0.05
}
```

**Perfil Gerencial:**
```json
{
  "experience": 0.35,
  "soft_skills": 0.25,
  "responsibilities": 0.20,
  "education": 0.10,
  "technical_skills": 0.10
}
```

### Normalización

Si los pesos no suman 1.0, el sistema los **normaliza automáticamente**:

```
peso_normalizado = peso_original / suma_total_pesos
```

### Aspectos Ignorados

Si un aspecto tiene score `-1.0`, significa que no había suficientes datos y fue **ignorado** en el cálculo final.

---

## ⚠️ Códigos de Error

### Códigos HTTP

| Código | Significado | Descripción |
|--------|-------------|-------------|
| `200` | OK | Operación exitosa |
| `404` | Not Found | Recurso no encontrado |
| `422` | Unprocessable Entity | Validación fallida |
| `500` | Internal Server Error | Error del servidor |

### Formato de Error

```json
{
  "detail": "Mensaje de error descriptivo"
}
```

### Ejemplos de Errores

**CV no encontrado:**
```json
{
  "detail": "CV no encontrado"
}
```

**Pesos inválidos:**
```json
{
  "detail": "value is not a valid float"
}
```

---

## 💻 Ejemplos de Uso

### JavaScript/TypeScript

```typescript
// API Client básico
class CVRecommendationAPI {
  private baseURL = 'http://localhost:8000';

  async uploadCV(file: File) {
    const formData = new FormData();
    formData.append('cv_file', file);
    
    const response = await fetch(`${this.baseURL}/cvs`, {
      method: 'POST',
      body: formData
    });
    
    return response.json();
  }

  async createJob(description: string) {
    const formData = new FormData();
    formData.append('description', description);
    
    const response = await fetch(`${this.baseURL}/jobs`, {
      method: 'POST',
      body: formData
    });
    
    return response.json();
  }

  async analyze(cvId: number, jobId: number, weights?: any) {
    const response = await fetch(`${this.baseURL}/analyze/${cvId}/${jobId}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: weights ? JSON.stringify(weights) : null
    });
    
    return response.json();
  }

  async getTopCandidates(jobId: number, limit = 10) {
    const response = await fetch(
      `${this.baseURL}/jobs/${jobId}/top-candidatos?limit=${limit}`
    );
    
    return response.json();
  }

  async getStats() {
    const response = await fetch(`${this.baseURL}/stats`);
    return response.json();
  }
}

// Uso
const api = new CVRecommendationAPI();

// Subir CV
const cvResult = await api.uploadCV(pdfFile);
console.log('CV ID:', cvResult.cv_id);

// Crear Job
const jobResult = await api.createJob(jobDescription);
console.log('Job ID:', jobResult.job_id);

// Analizar con pesos personalizados
const analysis = await api.analyze(1, 1, {
  experience: 0.40,
  technical_skills: 0.30
});
console.log('Score:', analysis.score_porcentaje + '%');

// Top 5 candidatos
const topCandidates = await api.getTopCandidates(1, 5);
topCandidates.forEach(c => {
  console.log(`${c.rank}. ${c.candidato}: ${c.score_porcentaje}%`);
});
```

### Python

```python
import requests

BASE_URL = 'http://localhost:8000'

# Subir CV
with open('cv.pdf', 'rb') as f:
    files = {'cv_file': f}
    response = requests.post(f'{BASE_URL}/cvs', files=files)
    cv_data = response.json()
    print(f"CV ID: {cv_data['cv_id']}")

# Crear Job
data = {'description': 'Buscamos desarrollador Python...'}
response = requests.post(f'{BASE_URL}/jobs', data=data)
job_data = response.json()
print(f"Job ID: {job_data['job_id']}")

# Analizar con pesos
weights = {
    "experience": 0.40,
    "technical_skills": 0.30,
    "education": 0.20,
    "soft_skills": 0.10
}
response = requests.post(
    f'{BASE_URL}/analyze/1/1',
    json=weights
)
analysis = response.json()
print(f"Score: {analysis['score_porcentaje']}%")

# Top candidatos
response = requests.get(f'{BASE_URL}/jobs/1/top-candidatos?limit=5')
top_candidates = response.json()
for candidate in top_candidates:
    print(f"{candidate['rank']}. {candidate['candidato']}: {candidate['score_porcentaje']}%")
```

### cURL

```bash
# Subir CV
curl -X POST "http://localhost:8000/cvs" \
  -F "cv_file=@cv.pdf"

# Crear Job
curl -X POST "http://localhost:8000/jobs" \
  -F "description=Buscamos desarrollador..."

# Analizar (sin pesos)
curl -X POST "http://localhost:8000/analyze/1/1" \
  -H "Content-Type: application/json"

# Analizar (con pesos)
curl -X POST "http://localhost:8000/analyze/1/1" \
  -H "Content-Type: application/json" \
  -d '{
    "experience": 0.40,
    "technical_skills": 0.30,
    "education": 0.20,
    "soft_skills": 0.10
  }'

# Top candidatos
curl "http://localhost:8000/jobs/1/top-candidatos?limit=5"

# Estadísticas
curl "http://localhost:8000/stats"

# Eliminar análisis
curl -X DELETE "http://localhost:8000/analyses/1"
```

---

## 🔄 Flujos de Trabajo

### Flujo 1: Análisis Individual

```
1. POST /cvs (subir CV PDF)
   → Recibir cv_id
   
2. POST /jobs (enviar descripción)
   → Recibir job_id
   
3. POST /analyze/{cv_id}/{job_id}
   → Recibir análisis con score
   
4. GET /analyses/{analysis_id}
   → Ver detalles completos
```

### Flujo 2: Ranking de Candidatos

```
1. POST /jobs (crear job)
   → Recibir job_id
   
2. POST /cvs (subir múltiples CVs)
   → Recibir cv_id para cada uno
   
3. POST /analyze/{cv_id}/{job_id} (para cada CV)
   → Recibir analysis_id
   
4. GET /jobs/{job_id}/top-candidatos?limit=10
   → Recibir ranking ordenado
```

### Flujo 3: Análisis con Pesos Personalizados

```
1. Definir pesos según perfil (Junior/Senior/Manager)

2. POST /analyze/{cv_id}/{job_id} (con weights)
   → Recibir análisis

3. Comparar con análisis usando pesos default
   → Ver diferencias en score
```

---

## 📈 Interpretación de Resultados

### Score Ranges

- **90-100%**: Candidato excepcional, altamente recomendado
- **80-89%**: Candidato muy bueno, buen ajuste
- **70-79%**: Candidato bueno, cumple la mayoría de requisitos
- **60-69%**: Candidato aceptable, cumple requisitos básicos
- **50-59%**: Candidato por debajo del perfil
- **< 50%**: Candidato no recomendado

### Summary (Resumen)

El campo `summary` proporciona un **resumen automático en lenguaje natural** del resultado del análisis:

- **Calificación general**: Categoriza al candidato según su score
- **Fortalezas**: Menciona los aspectos donde el candidato destaca (score ≥ 0.7)
- **Debilidades**: Indica áreas de mejora (score < 0.5)
- **Aspectos no evaluados**: Lista aspectos ignorados por falta de datos

**Ejemplos de resúmenes generados:**

| Score | Resumen |
|-------|---------|
| 88% | "Candidato muy adecuado. Destaca en Experiencia, Habilidades Técnicas y Educación." |
| 68% | "Candidato adecuado. Destaca en Educación. Requiere mejorar en Experiencia y Certificaciones." |
| 45% | "Candidato con baja compatibilidad. Requiere mejorar en varios aspectos clave." |

### Score Breakdown

Cada aspecto tiene:
- **score**: Compatibilidad del aspecto (0-1)
- **weight**: Peso del aspecto en el cálculo (0-1)
- **contribution**: Contribución al score final (score × weight)
- **ignored**: Si es `true`, el aspecto fue ignorado por falta de datos

### Cálculo del Score Final

```
score_final = Σ (score_aspecto × peso_aspecto) / Σ pesos_usados
```

---

## 🎯 Mejores Prácticas

### 1. Manejo de Errores

```typescript
try {
  const analysis = await api.analyze(cvId, jobId);
  // Usar análisis
} catch (error) {
  if (error.status === 404) {
    console.error('CV o Job no encontrado');
  } else if (error.status === 422) {
    console.error('Pesos inválidos');
  } else {
    console.error('Error del servidor');
  }
}
```

### 2. Loading States

```typescript
const [loading, setLoading] = useState(false);

const handleAnalyze = async () => {
  setLoading(true);
  try {
    const result = await api.analyze(cvId, jobId);
    // Mostrar resultado
  } finally {
    setLoading(false);
  }
};
```

### 3. Validación de Pesos

```typescript
const validateWeights = (weights: any) => {
  for (const [key, value] of Object.entries(weights)) {
    if (typeof value !== 'number' || value < 0 || value > 1) {
      throw new Error(`Peso ${key} inválido: debe estar entre 0 y 1`);
    }
  }
};
```

### 4. Caché

```typescript
// Cachear resultados para evitar re-procesamiento
const cache = new Map();

const analyzeWithCache = async (cvId, jobId, weights) => {
  const key = `${cvId}-${jobId}-${JSON.stringify(weights)}`;
  
  if (cache.has(key)) {
    return cache.get(key);
  }
  
  const result = await api.analyze(cvId, jobId, weights);
  cache.set(key, result);
  
  return result;
};
```

---

## 📞 Soporte

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

---

**Versión:** 2.0.0  
**Última actualización:** 2024  
**Proyecto:** CV Recommendation API - Universidad de los Andes

