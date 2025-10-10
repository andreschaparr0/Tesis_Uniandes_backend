# 🎯 CV Recommendation API

Sistema de análisis de CVs con arquitectura en capas (Services + Repositories + Database).

## 🏗️ Arquitectura

```
┌─────────────────────────────────────┐
│         Endpoints (main.py)         │  ← FastAPI Routes
├─────────────────────────────────────┤
│      Services (services.py)         │  ← Lógica de negocio
├─────────────────────────────────────┤
│   Repositories (repositories.py)    │  ← Acceso a datos (CRUD)
├─────────────────────────────────────┤
│      Database (database.py)         │  ← SQLAlchemy + SQLite
└─────────────────────────────────────┘
```

## 📁 Estructura

```
api/
├── database.py       # Modelos BD (CV, Job, Analysis)
├── repositories.py   # CRUD operations
├── services.py       # Lógica de negocio
└── main.py           # Endpoints FastAPI

main/                 # Tu código core existente
algoritmo_recomendacion/
src/

run_api.py            # Script de inicio
requirements.txt      # Dependencias
```

## ⚡ Inicio Rápido

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Ejecutar
python run_api.py
```

**API corriendo en:** http://localhost:8000  
**Documentación:** http://localhost:8000/docs

---

## 📋 Endpoints

### **CVs** (5 endpoints)
- `POST /cvs` - Procesar y guardar CV
- `GET /cvs` - Listar CVs
- `GET /cvs/{cv_id}` - Obtener CV por ID
- `GET /cvs/search/{nombre}` - Buscar CV
- `DELETE /cvs/{cv_id}` - Eliminar CV

### **Jobs** (5 endpoints)
- `POST /jobs` - Procesar y guardar Job
- `GET /jobs` - Listar Jobs
- `GET /jobs/{job_id}` - Obtener Job por ID
- `GET /jobs/search/{titulo}` - Buscar Job
- `DELETE /jobs/{job_id}` - Eliminar Job

### **Análisis** (6 endpoints)
- `POST /analyze/{cv_id}/{job_id}` - ⭐ Analizar CV vs Job
- `GET /analyses` - Listar análisis
- `GET /analyses/{analysis_id}` - Obtener análisis por ID
- `GET /cvs/{cv_id}/analyses` - Análisis de un CV
- `GET /jobs/{job_id}/analyses` - Análisis de un Job
- `GET /jobs/{job_id}/top-candidatos` - 🏆 Ranking candidatos

### **Utilidades** (3 endpoints)
- `GET /` - Info de la API
- `GET /health` - Health check
- `GET /stats` - Estadísticas

---

## 💡 Ejemplos

### Ejemplo 1: Flujo Completo

```python
import requests

base = "http://localhost:8000"

# 1. Procesar CV
cv = requests.post(f"{base}/cvs", files={'cv_file': open('cv.pdf', 'rb')})
cv_id = cv.json()['cv_id']

# 2. Procesar Job
job = requests.post(f"{base}/jobs", data={'description': 'Buscamos...'})
job_id = job.json()['job_id']

# 3. Analizar
result = requests.post(f"{base}/analyze/{cv_id}/{job_id}").json()
print(f"Score: {result['score_porcentaje']}%")
```

### Ejemplo 2: Ver Top Candidatos

```python
# Ver mejores candidatos para un trabajo
top = requests.get(f"{base}/jobs/1/top-candidatos?limit=5").json()

for c in top:
    print(f"{c['rank']}. {c['candidato']}: {c['score_porcentaje']}%")
```

### Ejemplo 3: Estadísticas

```python
stats = requests.get(f"{base}/stats").json()
print(f"Total CVs: {stats['total_cvs']}")
print(f"Total Jobs: {stats['total_jobs']}")
print(f"Score Promedio: {stats['score_promedio_porcentaje']}%")
```

---

## 🗄️ Base de Datos

- **Archivo**: `cv_system.db` (SQLite)
- **Tablas**: 
  - `cvs` - CVs procesados
  - `jobs` - Jobs procesados
  - `analyses` - Resultados de análisis

---

## 🎯 Capas del Sistema

### 1. **Endpoints** (`main.py`)
- Reciben requests HTTP
- Validan inputs
- Llaman a Services
- Retornan responses

### 2. **Services** (`services.py`)
- `CVService` - Procesa CVs
- `JobService` - Procesa Jobs
- `RecommendationService` - Ejecuta análisis
- Conectan con tu código core (`main/`, `algoritmo_recomendacion/`)

### 3. **Repositories** (`repositories.py`)
- `CVRepository` - CRUD de CVs
- `JobRepository` - CRUD de Jobs
- `AnalysisRepository` - CRUD de análisis
- Interactúan con la BD

### 4. **Database** (`database.py`)
- Modelos SQLAlchemy
- Configuración de BD
- Sesiones

---

## ✨ Características

- ✅ Arquitectura limpia en capas
- ✅ Separación de responsabilidades
- ✅ Base de datos SQLite local
- ✅ Swagger UI incluido
- ✅ Código organizado y mantenible
- ✅ Fácil de extender

---

## 📊 Total: 19 Endpoints

Balance perfecto entre funcionalidad y simplicidad.

---

¿Listo para empezar? 

```bash
python run_api.py
```

Luego ve a **http://localhost:8000/docs** 🚀
