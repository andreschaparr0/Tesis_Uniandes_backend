# 🚀 Quick Start Guide - Frontend Integration

## 📌 Resumen Ejecutivo

API de recomendación de CVs con IA. Permite procesar CVs en PDF, descripciones de trabajo, y generar análisis de compatibilidad con scoring inteligente.

**Base URL:** `http://localhost:8000`  
**Docs:** `http://localhost:8000/docs`

---

## ⚡ Flujo Principal (3 Pasos)

```
1. POST /cvs (subir CV PDF) → cv_id
2. POST /jobs (enviar descripción texto) → job_id  
3. POST /analyze/{cv_id}/{job_id} → score + detalles
```

---

## 🔌 Endpoints Esenciales

### 1. Procesar CV
```bash
POST /cvs
Content-Type: multipart/form-data
Body: cv_file (PDF)

Response:
{
  "cv_id": 1,
  "nombre": "Juan Pérez",
  "email": "juan@email.com"
}
```

### 2. Procesar Job
```bash
POST /jobs
Content-Type: application/x-www-form-urlencoded
Body: description (texto)

Response:
{
  "job_id": 1,
  "titulo": "Desarrollador Java Senior",
  "empresa": "Vector Colombia"
}
```

### 3. Analizar (⭐ CORE)
```bash
POST /analyze/{cv_id}/{job_id}
Content-Type: application/json (opcional)

Body (OPCIONAL):
{
  "experience": 0.30,
  "technical_skills": 0.15,
  "education": 0.15
}

Response:
{
  "score_porcentaje": 82.3,
  "candidato": "Juan Pérez",
  "trabajo": "Desarrollador Java Senior",
  "score_breakdown": {
    "experience": {
      "score": 0.90,
      "weight": 0.30,
      "contribution": 0.27
    },
    ...
  }
}
```

### 4. Top Candidatos
```bash
GET /jobs/{job_id}/top-candidatos?limit=10

Response:
[
  {
    "rank": 1,
    "candidato": "María García",
    "score_porcentaje": 88.7
  },
  ...
]
```

### 5. Estadísticas
```bash
GET /stats

Response:
{
  "total_cvs": 15,
  "total_jobs": 8,
  "total_analyses": 45,
  "score_promedio_porcentaje": 78.2
}
```

---

## 💡 Pesos del Análisis

### Predeterminados (si no envías nada)
```json
{
  "experience": 0.30,          // 30%
  "technical_skills": 0.15,    // 15%
  "education": 0.15,           // 15%
  "responsibilities": 0.15,    // 15%
  "certifications": 0.10,      // 10%
  "soft_skills": 0.08,         // 8%
  "languages": 0.04,           // 4%
  "location": 0.03             // 3%
}
```

### Perfiles Sugeridos

**Junior:**
```json
{
  "education": 0.35,
  "technical_skills": 0.25,
  "experience": 0.15,
  "certifications": 0.15,
  "soft_skills": 0.10
}
```

**Senior:**
```json
{
  "experience": 0.40,
  "technical_skills": 0.30,
  "certifications": 0.15,
  "education": 0.10,
  "soft_skills": 0.05
}
```

**Gerencial:**
```json
{
  "experience": 0.35,
  "soft_skills": 0.25,
  "responsibilities": 0.20,
  "education": 0.10,
  "technical_skills": 0.10
}
```

---

## 📦 Todos los Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/` | Info de la API |
| `GET` | `/health` | Health check |
| `POST` | `/cvs` | Subir y procesar CV |
| `GET` | `/cvs` | Listar CVs |
| `GET` | `/cvs/{id}` | Obtener CV por ID |
| `GET` | `/cvs/search/{nombre}` | Buscar CVs |
| `DELETE` | `/cvs/{id}` | Eliminar CV |
| `POST` | `/jobs` | Crear Job |
| `GET` | `/jobs` | Listar Jobs |
| `GET` | `/jobs/{id}` | Obtener Job por ID |
| `GET` | `/jobs/search/{titulo}` | Buscar Jobs |
| `DELETE` | `/jobs/{id}` | Eliminar Job |
| `POST` | `/analyze/{cv_id}/{job_id}` | **Analizar CV vs Job** |
| `GET` | `/analyses` | Listar análisis |
| `GET` | `/analyses/{id}` | Obtener análisis por ID |
| `GET` | `/cvs/{id}/analyses` | Análisis de un CV |
| `GET` | `/jobs/{id}/analyses` | Análisis de un Job |
| `GET` | `/jobs/{id}/top-candidatos` | **Top candidatos** |
| `GET` | `/stats` | **Estadísticas generales** |

---

## 🎨 Componentes Sugeridos

### Must Have
1. **Dashboard** - Estadísticas generales (`/stats`)
2. **CV Uploader** - Upload de PDF (`POST /cvs`)
3. **Job Creator** - Formulario de job (`POST /jobs`)
4. **Analyzer** - Selector CV + Job + Pesos (`POST /analyze`)
5. **Results Viewer** - Score + Breakdown (gráficos)
6. **Top Candidates** - Ranking (`/jobs/{id}/top-candidatos`)

### Nice to Have
7. **CV List** - Tabla con CVs (`GET /cvs`)
8. **Job List** - Tabla con Jobs (`GET /jobs`)
9. **Analysis History** - Historial de análisis
10. **Comparison Tool** - Comparar candidatos

---

## 💻 Código de Ejemplo (TypeScript)

### API Client Mínimo

```typescript
const API = 'http://localhost:8000';

export const api = {
  // CVs
  uploadCV: async (file: File) => {
    const formData = new FormData();
    formData.append('cv_file', file);
    const res = await fetch(`${API}/cvs`, { method: 'POST', body: formData });
    return res.json();
  },

  // Jobs
  createJob: async (description: string) => {
    const formData = new FormData();
    formData.append('description', description);
    const res = await fetch(`${API}/jobs`, { method: 'POST', body: formData });
    return res.json();
  },

  // Análisis
  analyze: async (cvId: number, jobId: number, weights?: any) => {
    const res = await fetch(`${API}/analyze/${cvId}/${jobId}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: weights ? JSON.stringify(weights) : null
    });
    return res.json();
  },

  // Top Candidatos
  getTopCandidates: async (jobId: number, limit = 10) => {
    const res = await fetch(`${API}/jobs/${jobId}/top-candidatos?limit=${limit}`);
    return res.json();
  },

  // Stats
  getStats: async () => {
    const res = await fetch(`${API}/stats`);
    return res.json();
  }
};
```

### Ejemplo de Uso

```typescript
// 1. Subir CV
const cvResult = await api.uploadCV(pdfFile);
console.log('CV ID:', cvResult.cv_id);

// 2. Crear Job
const jobResult = await api.createJob(jobText);
console.log('Job ID:', jobResult.job_id);

// 3. Analizar con pesos senior
const analysis = await api.analyze(cvResult.cv_id, jobResult.job_id, {
  experience: 0.40,
  technical_skills: 0.30
});

console.log('Score:', analysis.score_porcentaje + '%');

// 4. Top 5 candidatos
const topCandidates = await api.getTopCandidates(jobResult.job_id, 5);
topCandidates.forEach(c => {
  console.log(`${c.rank}. ${c.candidato}: ${c.score_porcentaje}%`);
});
```

---

## 🎯 Visualizaciones Recomendadas

### Score Principal
- **Gauge circular** (0-100%)
- Colores: Verde (>80%), Amarillo (60-80%), Rojo (<60%)

### Score Breakdown
- **Gráfico de Radar** (8 ejes, uno por aspecto)
- **Barras horizontales** con % de cada aspecto

### Top Candidatos
- **Podium** visual (1°, 2°, 3°)
- **Lista ordenada** con scores

### Dashboard
- **Cards** con totales (CVs, Jobs, Análisis)
- **Score promedio** destacado
- **Últimos análisis** (timeline)

---

## ⚠️ Puntos Importantes

1. **Tiempo de procesamiento**: CV y Job tardan 2-5 segundos → Mostrar loading
2. **Pesos opcionales**: Si no envías body en `/analyze`, usa predeterminados
3. **Score breakdown**: Cada aspecto tiene `score`, `weight`, `contribution`
4. **Normalización**: Los pesos se normalizan automáticamente si no suman 1.0
5. **CORS**: Configurado para `localhost:3000`, `:5173`, `:8080`, `:4200`

---

## 📚 Documentación Completa

- **API Completa**: Ver `API_DOCUMENTATION_FOR_FRONTEND.md`
- **Ejemplos de Código**: Ver `FRONTEND_INTEGRATION_EXAMPLES.md`
- **Pesos Detallados**: Ver `api/WEIGHTS_GUIDE.md`
- **Swagger UI**: `http://localhost:8000/docs`

---

## 🧪 Testing Rápido

### cURL
```bash
# Health check
curl http://localhost:8000/health

# Upload CV
curl -X POST http://localhost:8000/cvs -F "cv_file=@cv.pdf"

# Create Job
curl -X POST http://localhost:8000/jobs -F "description=Buscamos desarrollador Python..."

# Analyze (default weights)
curl -X POST http://localhost:8000/analyze/1/1 -H "Content-Type: application/json" -d "null"

# Top candidates
curl http://localhost:8000/jobs/1/top-candidatos?limit=5
```

### JavaScript (Browser Console)
```javascript
// Test rápido
fetch('http://localhost:8000/stats')
  .then(r => r.json())
  .then(console.log);
```

---

## 🚦 Prioridad de Implementación

### Sprint 1 (MVP)
1. ✅ Setup API client
2. ✅ Dashboard con stats
3. ✅ Upload CV
4. ✅ Create Job
5. ✅ Analyzer básico (sin pesos)

### Sprint 2
6. ✅ Configurador de pesos
7. ✅ Visualización de score (gauge)
8. ✅ Score breakdown (gráficos)
9. ✅ Top candidatos

### Sprint 3
10. ✅ CV/Job lists con búsqueda
11. ✅ Historial de análisis
12. ✅ Comparación de candidatos
13. ✅ Exportación a PDF

---

## 🎨 UI/UX Tips

- **Colores por Score**:
  - 90-100%: Verde (#10B981)
  - 80-89%: Azul (#3B82F6)
  - 70-79%: Amarillo (#F59E0B)
  - <70%: Rojo (#EF4444)

- **Animaciones**:
  - Fade in en resultados
  - Progress bar durante análisis
  - Confetti en score >90%

- **Feedback**:
  - Toast notifications
  - Confirmaciones antes de eliminar
  - Indicadores de procesamiento

---

**¡Listo para empezar! 🚀**

Cualquier duda, revisa:
- Swagger UI: `http://localhost:8000/docs`
- Documentación completa: `API_DOCUMENTATION_FOR_FRONTEND.md`
- Ejemplos de código: `FRONTEND_INTEGRATION_EXAMPLES.md`

