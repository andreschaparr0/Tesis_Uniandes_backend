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

def compare_responsibilities(cv_experience: list, job_responsibilities: list) -> dict:
    """
    Compara la experiencia del CV con las responsabilidades requeridas en la descripción de trabajo.
    
    Args:
        cv_experience (list): Experiencia del CV [{"position": "...", "company": "...", "duration": "...", "description": "..."}]
        job_responsibilities (list): Responsabilidades requeridas ["supervisar las actividades de planificación...", "monitorear y reportar..."]
        
    Returns:
        dict: Resultado de la comparación
    """
    if not job_responsibilities:
        return {"score": -1.0, "reason": "No hay responsabilidades requeridas"}
    
    if not cv_experience:
        return {"score": -1.0, "reason": "CV no especifica experiencia"}
    
    try:
        # Preparar texto de experiencia del CV
        cv_text = ""
        for exp in cv_experience:
            cv_text += f"- {exp.get('position', '')} en {exp.get('company', '')} ({exp.get('duration', '')})\n"
            cv_text += f"  Descripción: {exp.get('description', '')}\n\n"
        
        # Preparar texto de responsabilidades requeridas
        job_text = "\n".join([f"- {resp}" for resp in job_responsibilities])
        
        prompt_text = f"""Eres un experto en evaluar compatibilidad entre responsabilidades laborales y experiencia previa. Responde ÚNICAMENTE con JSON válido que contenga: 'score' IMPORTANTE QUE SEA UN NUMERO ENTRE 0 Y 1, 'reason' (string).

Compara la experiencia del CV con las responsabilidades requeridas:

CV:
{cv_text}
Responsabilidades requeridas:
{job_text}

Evalúa si la experiencia del CV demuestra capacidad para cumplir las responsabilidades. Si la experiencia es directamente relevante, score debe ser 1.0. Si es parcialmente relevante, score debe ser 0.1-0.7. Si no es relevante, score debe ser 0.0.
La razón debe explicar qué responsabilidades puede cumplir basándose en la experiencia y cuáles faltan.

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
        print(f"Error en comparación de responsabilidades: {e}")
        return {"score": 0.0, "reason": "Error en comparación"}
