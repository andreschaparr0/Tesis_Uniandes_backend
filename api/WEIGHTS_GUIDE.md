# Guía de Uso de Pesos (Weights) en el Análisis

## 📊 ¿Qué son los pesos?

Los pesos son valores numéricos entre 0 y 1 que determinan la importancia de cada aspecto en el análisis de compatibilidad entre un CV y una descripción de trabajo.

## 🎯 Pesos Predeterminados

Si no envías pesos personalizados, el sistema usa estos valores por defecto:

```json
{
  "experience": 0.30,           // 30% - Experiencia laboral
  "technical_skills": 0.15,     // 15% - Habilidades técnicas
  "education": 0.15,            // 15% - Educación
  "responsibilities": 0.15,     // 15% - Responsabilidades
  "certifications": 0.10,       // 10% - Certificaciones
  "soft_skills": 0.08,          // 8%  - Habilidades blandas
  "languages": 0.04,            // 4%  - Idiomas
  "location": 0.03              // 3%  - Ubicación
}
```

**Nota:** La suma de todos los pesos debe ser 1.0 (100%)

## 🔧 Cómo Usar Pesos Personalizados

### Opción 1: Sin pesos (usar predeterminados)

**Request:**
```bash
POST /analyze/1/1
```

**Nota:** No envíes un body, o envía `null`

### Opción 2: Pesos personalizados completos

**Request:**
```bash
POST /analyze/1/1
Content-Type: application/json

{
  "experience": 0.40,
  "technical_skills": 0.25,
  "education": 0.10,
  "responsibilities": 0.10,
  "certifications": 0.05,
  "soft_skills": 0.05,
  "languages": 0.03,
  "location": 0.02
}
```

### Opción 3: Pesos parciales (el resto usa predeterminados)

Si solo envías algunos pesos, el sistema **normalizará automáticamente**:

**Request:**
```bash
POST /analyze/1/1
Content-Type: application/json

{
  "experience": 0.50,
  "technical_skills": 0.30
}
```

El sistema ajustará automáticamente todos los pesos para que sumen 1.0.

## ✅ Ejemplos Prácticos

### Ejemplo 1: Enfoque en Experiencia Técnica
```json
{
  "experience": 0.35,
  "technical_skills": 0.35,
  "certifications": 0.15,
  "education": 0.10,
  "soft_skills": 0.05
}
```

### Ejemplo 2: Perfil Junior (más educación, menos experiencia)
```json
{
  "education": 0.35,
  "technical_skills": 0.25,
  "experience": 0.15,
  "certifications": 0.15,
  "soft_skills": 0.10
}
```

### Ejemplo 3: Puesto Gerencial (más soft skills y experiencia)
```json
{
  "experience": 0.40,
  "soft_skills": 0.25,
  "responsibilities": 0.20,
  "education": 0.10,
  "technical_skills": 0.05
}
```

## 🚫 Errores Comunes

### ❌ Error 1: Pesos fuera de rango
```json
{
  "experience": 1.5  // ❌ Debe ser entre 0 y 1
}
```

### ❌ Error 2: Nombres incorrectos
```json
{
  "experiencia": 0.30  // ❌ Debe ser "experience"
}
```

### ✅ Correcto:
```json
{
  "experience": 0.30
}
```

## 📝 Respuesta del Endpoint

El endpoint retorna los pesos que fueron efectivamente usados:

```json
{
  "success": true,
  "analysis_id": 1,
  "cv_id": 1,
  "job_id": 1,
  "candidato": "Juan Pérez",
  "trabajo": "Desarrollador Senior",
  "score": 0.823,
  "score_porcentaje": 82.3,
  "score_breakdown": { ... },
  "weights_used": {
    "experience": 0.30,
    "technical_skills": 0.15,
    // ... resto de pesos
  },
  "processing_time": 2.45
}
```

## 🧪 Probar en Swagger UI

1. Ve a `http://localhost:8000/docs`
2. Encuentra el endpoint `POST /analyze/{cv_id}/{job_id}`
3. Click en "Try it out"
4. Ingresa los IDs del CV y Job
5. En el body, puedes:
   - Dejarlo vacío para usar predeterminados
   - Modificar el ejemplo para usar pesos personalizados
6. Click en "Execute"

## 💡 Recomendaciones

1. **Empieza con los predeterminados**: Son balanceados para la mayoría de casos
2. **Ajusta según el tipo de puesto**: 
   - Técnico: Mayor peso en `technical_skills` y `experience`
   - Gerencial: Mayor peso en `soft_skills` y `responsibilities`
   - Junior: Mayor peso en `education` y `certifications`
3. **Normalización automática**: Si tus pesos no suman 1.0, el sistema los ajustará
4. **Valida los resultados**: Revisa `weights_used` en la respuesta para confirmar qué pesos se usaron

