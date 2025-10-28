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

def _compare_certifications_with_technical_skills(cv_certifications: list, job_technical_skills: list) -> dict:
    """
    Compara las certificaciones del CV con las habilidades técnicas requeridas del trabajo.
    Esta función se usa como fallback cuando no hay certificaciones específicas requeridas.
    
    Args:
        cv_certifications (list): Certificaciones del CV
        job_technical_skills (list): Habilidades técnicas requeridas en el trabajo
        
    Returns:
        dict: Resultado de la comparación
    """
    try:
        # Preparar texto de certificaciones del CV
        cv_text = ""
        for cert in cv_certifications:
            cv_text += f"- {cert.get('name', '')} ({cert.get('issuer', '')})\n"
       
        # Preparar texto de habilidades técnicas
        job_text = "\n".join([f"- {skill}" for skill in job_technical_skills])
        
        prompt_text = f"""Eres un experto en evaluar certificaciones técnicas. Responde ÚNICAMENTE con JSON válido que contenga: 'score' IMPORTANTE QUE SEA UN NUMERO ENTRE 0 Y 1, 'reason' (string).

Compara estas certificaciones del CV con las habilidades técnicas requeridas en el trabajo:

Certificaciones del CV:
{cv_text}

Habilidades técnicas requeridas:
{job_text}

Evalúa si las certificaciones del CV son relevantes para las habilidades técnicas requeridas. 
- Si las certificaciones demuestran expertise directamente relacionado con las habilidades técnicas, score debe ser 0.6-1.0
- Si las certificaciones son parcialmente relevantes o demuestran habilidades transferibles, score debe ser 0.3-0.6
- Si las certificaciones no son relevantes, score debe ser 0.0-0.3

La razón debe explicar qué certificaciones son relevantes para las habilidades técnicas y por qué.

Responde en JSON sin bloques de código markdown (```json).: {{"score": numero entre 0.0-1.0, "reason": "explicación detallada"}}"""

        response = llm.invoke(prompt_text)
        try:
            result = json.loads(response.content)
            return {
                "score": result.get("score", 0),
                "reason": f"[Comparado con habilidades técnicas] {result.get('reason', '')}"
            }
        except json.JSONDecodeError:
            # Fallback simple
            return {
                "score": 0.0,
                "reason": "[Comparado con habilidades técnicas] Error en respuesta de IA"
            }
            
    except Exception as e:
        print(f"Error al comparar certificaciones con habilidades técnicas: {e}")
        return {"score": 0.0, "reason": "[Comparado con habilidades técnicas] Error en comparación"}

def compare_certifications(cv_certifications: list, job_certifications: list, job_technical_skills: list = None) -> dict:
    """
    Compara las certificaciones del CV con las requeridas en la descripción de trabajo.
    Si no hay certificaciones requeridas, compara con las habilidades técnicas del trabajo.
    
    Args:
        cv_certifications (list): Certificaciones del CV [{"name": "...", "issuer": "...", "year": "..."}]
        job_certifications (list): Certificaciones requeridas ["certificados aws", "certificados google cloud"]
        job_technical_skills (list, optional): Habilidades técnicas del trabajo (fallback cuando no hay certificaciones)
        
    Returns:
        dict: Resultado de la comparación
    """
    # Si el CV no tiene certificaciones
    if not cv_certifications:
        if not job_certifications:
            return {"score": -1.0, "reason": "No hay certificaciones requeridas ni certificaciones en el CV"}
        return {"score": 0.0, "reason": "CV no especifica certificaciones pero el trabajo las requiere"}
    
    # Si el trabajo no requiere certificaciones específicas
    if not job_certifications:
        # Intentar comparar con habilidades técnicas como fallback
        if job_technical_skills and len(job_technical_skills) > 0:
            return _compare_certifications_with_technical_skills(cv_certifications, job_technical_skills)
        else:
            return {"score": -1.0, "reason": "No hay certificaciones requeridas ni habilidades técnicas para comparar"}
    
    try:
        # Preparar texto de certificaciones del CV
        cv_text = ""
        for cert in cv_certifications:
            cv_text += f"- {cert.get('name', '')} ({cert.get('issuer', '')})\n"
       
        # Preparar texto de certificaciones requeridas
        job_text = "\n".join([f"- {cert}" for cert in job_certifications])
        prompt_text = f"""Eres un experto en evaluar relevancia de certificaciones técnicas. Responde ÚNICAMENTE con JSON válido que contenga: 'score' IMPORTANTE QUE SEA UN NUMERO ENTRE 0 Y 1, 'reason' (string).

            Compara estas certificaciones del CV con las requeridas:

            CV:
            {cv_text}
            Requeridas:
            {job_text}

            Evalúa si las certificaciones del CV cumplen con los requerimientos. Si es directamente relevante, score debe ser 1.0. Si es parcialmente relevante, score debe ser 0.1-0.7. Si no es relevante, score debe ser 0.0.
            La razón debe explicar qué certificaciones cumplen con los requerimientos y cuáles faltan.

            Responde en JSON  sin bloques de código markdown (```json).: {{"score": numero entre 0.0-1.0, "reason": "explicación detallada"}}"""

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
        print(f"Error en comparación de certificaciones: {e}")
        return {"score": 0.0, "reason": "Error en comparación"}