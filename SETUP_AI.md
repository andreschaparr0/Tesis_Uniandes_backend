# Configuración para usar LangChain en la extracción de CVs

## Pasos para configurar

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Configurar API Key
Crea un archivo `.env` en la raíz del proyecto con tu API key:

```bash
# .env
HUGGINGFACEHUB_API_TOKEN=tu_api_key_aqui
```

### 3. Probar la funcionalidad
```bash
cd Tesis_Uniandes/src/estructuracion
python test_cv_extractor.py
```

**Nota:** Si no tienes un PDF de ejemplo, el test también funcionará con texto de ejemplo.

## ¿Qué hace ahora el sistema?

### Antes (solo regex):
- Extraía información personal usando patrones regex
- Limitado a formatos específicos
- Menos preciso con variaciones en el formato

### Ahora (con LangChain):
- Usa LangChain + OpenAI para extracción más inteligente
- Modelos Pydantic para validación de datos
- Extrae: nombre, email, teléfono, ubicación
- Arquitectura más robusta y escalable
- Solo IA, sin métodos de respaldo

## Próximos pasos

Una vez que confirmes que funciona la extracción de información personal, podemos agregar:

1. **Extracción de experiencia laboral** con IA
2. **Extracción de habilidades** con IA  
3. **Extracción de educación** con IA
4. **Algoritmo de matching** con descripciones de trabajo

## Estructura del JSON generado

```json
{
  "personal_info": {
    "name": "Juan Pérez",
    "email": "juan@email.com", 
    "phone": "3001234567",
    "location": "Bogotá, Colombia"
  },
  "education": [],
  "experience": [],
  "skills": {
    "programming_languages": [],
    "frameworks": [],
    "databases": [],
    "soft_skills": []
  },
  "languages": []
}
```
