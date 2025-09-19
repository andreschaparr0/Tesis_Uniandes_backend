import json
import os
from dotenv import load_dotenv
from openai import AzureOpenAI
from langchain_openai import AzureChatOpenAI
from langchain.prompts import ChatPromptTemplate

# Cargar variables de entorno
load_dotenv()

# Configuración de Azure OpenAI
endpoint = "https://invuniandesai-2.openai.azure.com/"
model_name = "gpt-4o-mini"
deployment = "gpt-4o-mini"
subscription_key = os.getenv("API_TOKEN")
api_version = "2024-12-01-preview"

# Inicializar LangChain con Azure OpenAI
llm = AzureChatOpenAI(
    azure_deployment=deployment,
    azure_endpoint=endpoint,
    api_key=subscription_key,
    api_version=api_version,
    temperature=0.1,
    max_tokens=500
)

def compare_experience(cv_experience: list, job_experience: str) -> dict:
    """
    Compara la experiencia del CV con la requerida en la descripción de trabajo.
    
    Args:
        cv_experience (list): Experiencia del CV [{"position": "...", "company": "...", "duration": "...", "description": "..."}]
        job_experience (str): Experiencia requerida "contar con mínimo 4 años trabajando en posiciones similares..."
        
    Returns:
        dict: Resultado de la comparación
    """
    if not job_experience:
        return {"score": 1.0, "reason": "No hay experiencia requerida"}
    
    if not cv_experience:
        return {"score": 0.0, "reason": "CV no especifica experiencia"}
    
    try:
        # Preparar texto de experiencia del CV
        cv_text = ""
        for exp in cv_experience:
            cv_text += f"- {exp.get('position', '')} en {exp.get('company', '')} ({exp.get('duration', '')})\n"
            cv_text += f"  Descripción: {exp.get('description', '')}\n\n"
        
        prompt_text = f"""Eres un experto en evaluar experiencia laboral. Responde ÚNICAMENTE con JSON válido que contenga: 'score' IMPORTANTE QUE SEA UN NUMERO ENTRE 0 Y 1, 'reason' (string).

Compara la experiencia del CV con la requerida:

CV:
{cv_text}
Requerida:
{job_experience}

Evalúa si la experiencia del CV cumple con los requerimientos. Considera años de experiencia, posiciones similares, tecnologías, y habilidades mencionadas. Si cumple completamente, score debe ser 1.0. Si cumple parcialmente, score debe ser 0.1-0.7. Si no cumple, score debe ser 0.0.
La razón debe explicar qué aspectos de la experiencia cumplen con los requerimientos y cuáles faltan.

Responde en JSON sin bloques de código markdown (```json).: {{"score": numero entre 0.0-1.0, "reason": "explicación detallada"}}"""

        response = llm.invoke(prompt_text)
        
        try:
            result = json.loads(response.content)
            return {
                "score": result.get("score", 0),
                "reason": result.get("reason", "")
            }
        except json.JSONDecodeError:
            # Fallback simple
            return {
                "score": 0.0,
                "reason": "Error en respuesta de IA"
            }
            
    except Exception as e:
        print(f"Error en comparación de experiencia: {e}")
        return {"score": 0.0, "reason": "Error en comparación"}
