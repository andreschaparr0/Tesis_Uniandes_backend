# 🎓 CV Recommendation API - Tesis Universidad de los Andes

Sistema de análisis y recomendación de CVs usando Inteligencia Artificial. Permite procesar CVs en PDF, descripciones de trabajo, y generar análisis de compatibilidad con scoring inteligente basado en múltiples aspectos.

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Tecnologías](#-tecnologías)
- [Instalación](#-instalación)
- [Configuración](#-configuración)
- [Uso](#-uso)
- [Documentación API](#-documentación-api)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Testing](#-testing)
- [FAQ](#-faq)

---

## ✨ Características

- ✅ **Procesamiento de CVs**: Extrae y estructura información de PDFs usando Azure OpenAI
- ✅ **Procesamiento de Jobs**: Estructura descripciones de trabajo con IA
- ✅ **Análisis Inteligente**: Compara CVs vs Jobs en 8 aspectos diferentes
- ✅ **Sistema de Pesos Configurable**: Personaliza la importancia de cada aspecto
- ✅ **Persistencia de Datos**: Base de datos SQLite local
- ✅ **API RESTful**: FastAPI con documentación automática
- ✅ **Ranking de Candidatos**: Ordena candidatos por compatibilidad
- ✅ **Estadísticas**: Métricas generales del sistema

---

## 🛠️ Tecnologías

### Backend
- **FastAPI** - Framework web moderno y rápido
- **SQLAlchemy** - ORM para manejo de base de datos
- **SQLite** - Base de datos local
- **Pydantic** - Validación de datos

### Procesamiento IA
- **Azure OpenAI** (GPT-4o-mini) - Estructuración de CVs y Jobs
- **LangChain** - Orquestación de prompts
- **PyMuPDF** - Extracción de texto de PDFs
- **NLTK** - Procesamiento de lenguaje natural

### Otros
- **Python 3.11+**
- **Uvicorn** - Servidor ASGI

---

## 📥 Instalación

### 1. Clonar el repositorio

```bash
git clone <url-del-repo>
cd Tesis_Uniandes_backend
```

### 2. Crear entorno virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Descargar recursos NLTK (solo primera vez)

```python
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

---

## ⚙️ Configuración

### Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
# Azure OpenAI
AZURE_OPENAI_API_KEY=tu-api-key-aqui
AZURE_OPENAI_ENDPOINT=https://tu-endpoint.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o-mini
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

### Obtener Azure OpenAI API Key

1. Ir a [Azure Portal](https://portal.azure.com/)
2. Crear recurso de Azure OpenAI
3. Copiar el endpoint y API key
4. Crear deployment de `gpt-4o-mini`

---

## 🚀 Uso

### Iniciar el servidor

```bash
python run_api.py
```

La API estará disponible en: `http://localhost:8000`

### Documentación Interactiva

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Flujo Básico

```bash
# 1. Subir un CV
curl -X POST "http://localhost:8000/cvs" -F "cv_file=@cv.pdf"
# Response: { "cv_id": 1, "nombre": "Juan Pérez", ... }

# 2. Crear un Job
curl -X POST "http://localhost:8000/jobs" -F "description=Buscamos desarrollador..."
# Response: { "job_id": 1, "titulo": "Desarrollador Senior", ... }

# 3. Analizar
curl -X POST "http://localhost:8000/analyze/1/1" -H "Content-Type: application/json"
# Response: { "score_porcentaje": 82.3, ... }

# 4. Ver top candidatos
curl "http://localhost:8000/jobs/1/top-candidatos?limit=5"
```

---

## 📚 Documentación API

Ver [API_DOCUMENTATION.md](API_DOCUMENTATION.md) para documentación completa.

### Endpoints Principales

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/cvs` | Procesar y guardar CV |
| `GET` | `/cvs` | Listar CVs |
| `GET` | `/cvs/{id}` | Obtener CV por ID |
| `DELETE` | `/cvs/{id}` | Eliminar CV |
| `POST` | `/jobs` | Procesar y guardar Job |
| `GET` | `/jobs` | Listar Jobs |
| `GET` | `/jobs/{id}` | Obtener Job por ID |
| `DELETE` | `/jobs/{id}` | Eliminar Job |
| `POST` | `/analyze/{cv_id}/{job_id}` | Analizar CV vs Job |
| `GET` | `/analyses` | Listar análisis |
| `GET` | `/analyses/{id}` | Obtener análisis por ID |
| `DELETE` | `/analyses/{id}` | Eliminar análisis |
| `GET` | `/jobs/{id}/top-candidatos` | Ranking de candidatos |
| `GET` | `/stats` | Estadísticas generales |

---

## 📁 Estructura del Proyecto

```
Tesis_Uniandes_backend/
│
├── api/                        # API FastAPI
│   ├── main.py                # Endpoints principales
│   ├── database.py            # Modelos SQLAlchemy
│   ├── repositories.py        # Capa de datos (CRUD)
│   └── services.py            # Lógica de negocio
│
├── main/                      # Core del sistema
│   ├── data_cleaner.py        # Limpieza de PDFs
│   ├── data_structurer.py     # Estructuración con IA
│   ├── recommendation_engine.py # Motor de recomendación
│   └── main_executor.py       # Orquestador (legacy)
│
├── algoritmo_recomendacion/   # Algoritmos de comparación
│   ├── comparator_main.py     # Orquestador principal
│   └── comparators/           # Comparadores individuales
│       ├── technical_skills_comparator.py
│       ├── experience_comparator.py
│       ├── education_comparator.py
│       ├── certifications_comparator.py
│       ├── languages_comparator.py
│       ├── location_comparator.py
│       ├── responsibilities_comparator.py
│       └── soft_skills_comparator.py
│
├── src/                       # Utilidades
│   ├── estructuracion_CV/     # Extracción de CVs
│   ├── estructuracion_Descripcion/ # Extracción de Jobs
│   └── limpieza/              # Limpieza de texto
│
├── temp_uploads/              # Archivos temporales
├── cv_system.db              # Base de datos SQLite
├── requirements.txt          # Dependencias
├── run_api.py               # Script de inicio
├── README.md                # Este archivo
└── API_DOCUMENTATION.md     # Documentación de la API
```

---

## 🧪 Testing

### Testing Manual con Swagger UI

1. Ir a http://localhost:8000/docs
2. Probar cada endpoint interactivamente

### Testing con cURL

```bash
# Health check
curl http://localhost:8000/health

# Stats
curl http://localhost:8000/stats
```

### Testing Automatizado (Opcional)

```bash
# Ejecutar tests de comparadores
python -m pytest algoritmo_recomendacion/test_comparators/
```

---

## 🔄 Mantenimiento

### Reiniciar la Base de Datos

```bash
# 1. Detener la API (Ctrl+C)

# 2. Eliminar la base de datos
# Windows
del cv_system.db

# Linux/Mac
rm cv_system.db

# 3. Reiniciar la API
python run_api.py
```

### Limpiar archivos temporales

```bash
# Windows
rd /s /q temp_uploads
mkdir temp_uploads

# Linux/Mac
rm -rf temp_uploads
mkdir temp_uploads
```

### Actualizar dependencias

```bash
pip install --upgrade -r requirements.txt
```

---

## 🎯 Sistema de Scoring

### Aspectos Evaluados

El sistema evalúa 8 aspectos:

1. **Experiencia** (30%) - Años y relevancia de experiencia laboral
2. **Habilidades Técnicas** (15%) - Tecnologías y herramientas
3. **Educación** (15%) - Nivel educativo y títulos
4. **Responsabilidades** (15%) - Match con responsabilidades del puesto
5. **Certificaciones** (10%) - Certificaciones relevantes
6. **Habilidades Blandas** (8%) - Soft skills
7. **Idiomas** (4%) - Nivel de idiomas requeridos
8. **Ubicación** (3%) - Compatibilidad geográfica

### Pesos Personalizables

Puedes personalizar los pesos según el tipo de puesto:

**Perfil Junior:**
```json
{
  "education": 0.35,
  "technical_skills": 0.25,
  "experience": 0.15,
  "certifications": 0.15,
  "soft_skills": 0.10
}
```

**Perfil Senior:**
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

---

## 📊 Ejemplo de Respuesta

### Análisis Completo

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
      "contribution": 0.27
    },
    "technical_skills": {
      "score": 0.85,
      "weight": 0.15,
      "contribution": 0.127
    }
    // ... otros aspectos
  },
  "processing_time": 2.45
}
```

---

## ❓ FAQ

### ¿Cuánto tarda en procesar un CV?
Entre 2-5 segundos, dependiendo del tamaño del PDF y la respuesta de Azure OpenAI.

### ¿Qué formato de CV acepta?
Solo archivos PDF.

### ¿Puedo cambiar los pesos después de crear un análisis?
No, pero puedes crear un nuevo análisis con diferentes pesos.

### ¿Los datos persisten al reiniciar?
Sí, se guardan en `cv_system.db` (SQLite).

### ¿Puedo usar otro modelo de IA?
Sí, modificando `data_structurer.py` para usar otro modelo de Azure OpenAI o incluso otro proveedor.

### ¿Cómo interpreto el score?
- **90-100%**: Candidato excepcional
- **80-89%**: Candidato muy bueno
- **70-79%**: Candidato bueno
- **60-69%**: Candidato aceptable
- **< 60%**: No recomendado

### ¿Qué pasa si subo el mismo CV dos veces?
El sistema no tiene detección de duplicados actualmente, creará dos registros separados.

### ¿Puedo exportar los resultados?
Actualmente no, pero puedes implementar un endpoint de exportación en el frontend.

---

## 🔐 Seguridad

- ⚠️ **CORS**: Configurado para `localhost:*` (desarrollo)
- ⚠️ **API Keys**: Mantén tu `.env` fuera de Git (ya está en `.gitignore`)
- ⚠️ **Producción**: Para producción, configura CORS específico y HTTPS

---

## 🤝 Contribuciones

Este es un proyecto de tesis. Para sugerencias o mejoras:

1. Fork del repositorio
2. Crear rama (`git checkout -b feature/mejora`)
3. Commit cambios (`git commit -am 'Agregar mejora'`)
4. Push a la rama (`git push origin feature/mejora`)
5. Crear Pull Request

---

## 📝 Licencia

Proyecto de Tesis - Universidad de los Andes

---

## 👤 Autor

**Proyecto de Tesis**  
Universidad de los Andes  
2024

---

## 🆘 Soporte

- **Documentación API**: [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🚀 Roadmap

- [ ] Autenticación y autorización
- [ ] Detección de CVs duplicados
- [ ] Exportación a PDF/Excel
- [ ] Análisis batch (múltiples CVs a la vez)
- [ ] Caché de estructuración IA
- [ ] Dashboard de métricas
- [ ] Soporte para más formatos (DOCX, TXT)
- [ ] API de webhooks para notificaciones

---

**¡Gracias por usar CV Recommendation API! 🎓**
