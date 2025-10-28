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
                "reason": f"{result.get('reason', '')}"
            }
        except json.JSONDecodeError:
            # Fallback simple
            return {
                "score": 0.0,
                "reason": "Error en respuesta de IA"
            }
            
    except Exception as e:
        print(f"Error al comparar certificaciones con habilidades técnicas: {e}")
        return {"score": 0.0, "reason": "Error en comparación"}

def compare_certifications(cv_certifications: list, job_certifications: list, job_technical_skills: list = None, cv_technical_skills: list = None) -> dict:
    """
    Compara las certificaciones del CV con las requeridas en la descripción de trabajo.
    Si no hay certificaciones requeridas, compara con las habilidades técnicas del trabajo.
    Si hay certificaciones requeridas, también considera las habilidades técnicas del CV como alternativa (con penalización).
    
    Args:
        cv_certifications (list): Certificaciones del CV [{"name": "...", "issuer": "...", "year": "..."}]
        job_certifications (list): Certificaciones requeridas ["certificados aws", "certificados google cloud"]
        job_technical_skills (list, optional): Habilidades técnicas del trabajo (fallback cuando no hay certificaciones)
        cv_technical_skills (list, optional): Habilidades técnicas del CV (alternativa a certificaciones con penalización)
        
    Returns:
        dict: Resultado de la comparación
    """
    # Si el trabajo no requiere certificaciones específicas
    if not job_certifications:
        # Si el CV no tiene certificaciones tampoco
        if not cv_certifications:
            return {"score": -1.0, "reason": "No hay certificaciones requeridas ni certificaciones en el CV"}
        # Intentar comparar certificaciones del CV con habilidades técnicas del trabajo
        if job_technical_skills and len(job_technical_skills) > 0:
            return _compare_certifications_with_technical_skills(cv_certifications, job_technical_skills)
        else:
            return {"score": -1.0, "reason": "No hay certificaciones requeridas ni habilidades técnicas para comparar"}
    
    # Si el trabajo SÍ requiere certificaciones
    # Intentar comparación con certificaciones del CV primero
    if cv_certifications:
        cert_result = _compare_certifications_direct(cv_certifications, job_certifications)
    else:
        cert_result = None
    
    # También intentar comparar las certificaciones requeridas con las technical skills del CV (con penalización)
    if cv_technical_skills and len(cv_technical_skills) > 0:
        skills_result = _compare_required_certifications_with_cv_technical_skills(job_certifications, cv_technical_skills)
    else:
        skills_result = None
    
    # Combinar resultados
    return _combine_certification_results(cert_result, skills_result)

def _compare_certifications_direct(cv_certifications: list, job_certifications: list) -> dict:
    """
    Comparación directa entre certificaciones del CV y certificaciones requeridas.
    
    Args:
        cv_certifications (list): Certificaciones del CV
        job_certifications (list): Certificaciones requeridas
        
    Returns:
        dict: Resultado de la comparación
    """
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

Responde en JSON sin bloques de código markdown (```json).: {{"score": numero entre 0.0-1.0, "reason": "explicación detallada"}}"""

        response = llm.invoke(prompt_text)
        try:
            result = json.loads(response.content)
            return {
                "score": result.get("score", 0),
                "reason": result.get("reason", "")
            }
        except json.JSONDecodeError:
            return {
                "score": 0.0,
                "reason": "Error en respuesta de IA"
            }
            
    except Exception as e:
        print(f"Error en comparación de certificaciones: {e}")
        return {"score": 0.0, "reason": "Error en comparación"}

def _compare_required_certifications_with_cv_technical_skills(job_certifications: list, cv_technical_skills: list) -> dict:
    """
    Compara las certificaciones requeridas del trabajo con las habilidades técnicas del CV.
    Esta es una comparación con penalización (las skills no son tan buenas como certificaciones).
    
    Args:
        job_certifications (list): Certificaciones requeridas en el trabajo
        cv_technical_skills (list): Habilidades técnicas del CV
        
    Returns:
        dict: Resultado de la comparación (con score penalizado)
    """
    try:
        # Preparar texto de certificaciones requeridas
        job_text = "\n".join([f"- {cert}" for cert in job_certifications])
        
        # Preparar texto de habilidades técnicas del CV
        cv_text = "\n".join([f"- {skill}" for skill in cv_technical_skills])
        
        prompt_text = f"""Eres un experto en evaluar habilidades técnicas. Responde ÚNICAMENTE con JSON válido que contenga: 'score' IMPORTANTE QUE SEA UN NUMERO ENTRE 0 Y 1, 'reason' (string).

Compara las habilidades técnicas del CV con las certificaciones requeridas:

Certificaciones requeridas:
{job_text}

Habilidades técnicas del CV:
{cv_text}

Evalúa si las habilidades técnicas del CV demuestran conocimiento relacionado con las certificaciones requeridas.
IMPORTANTE: Las habilidades técnicas NO son equivalentes a certificaciones, así que el score debe ser más conservador.
- Si las habilidades cubren las áreas de las certificaciones requeridas, score debe ser 0.4-0.7 (NO más alto)
- Si las habilidades cubren parcialmente, score debe ser 0.2-0.4
- Si no hay relación, score debe ser 0.0-0.2

La razón debe explicar qué habilidades técnicas son relevantes para las certificaciones requeridas.

Responde en JSON sin bloques de código markdown (```json).: {{"score": numero entre 0.0-1.0, "reason": "explicación detallada"}}"""

        response = llm.invoke(prompt_text)
        try:
            result = json.loads(response.content)
            # Aplicar penalización adicional del 50% porque son skills, no certificaciones
            penalized_score = result.get("score", 0) * 0.5
            return {
                "score": penalized_score,
                "reason": f"[Skills del CV vs certificaciones requeridas - penalizado 50%] {result.get('reason', '')}"
            }
        except json.JSONDecodeError:
            return {
                "score": 0.0,
                "reason": "[Skills del CV vs certificaciones requeridas] Error en respuesta de IA"
            }
            
    except Exception as e:
        print(f"Error al comparar certificaciones requeridas con skills del CV: {e}")
        return {"score": 0.0, "reason": "[Skills del CV vs certificaciones requeridas] Error en comparación"}

def _combine_certification_results(cert_result: dict, skills_result: dict) -> dict:
    """
    Combina los resultados de certificaciones y habilidades técnicas.
    Prioriza las certificaciones, pero considera las skills como alternativa.
    
    Args:
        cert_result (dict): Resultado de comparación con certificaciones
        skills_result (dict): Resultado de comparación con skills (penalizado)
        
    Returns:
        dict: Resultado combinado
    """
    # Si no hay ningún resultado
    if not cert_result and not skills_result:
        return {"score": 0.0, "reason": "CV no tiene certificaciones ni habilidades técnicas relevantes"}
    
    # Si solo hay resultado de certificaciones
    if cert_result and not skills_result:
        return cert_result
    
    # Si solo hay resultado de skills
    if skills_result and not cert_result:
        return skills_result
    
    # Si hay ambos, tomar el mejor score y combinar razones
    cert_score = cert_result.get("score", 0)
    skills_score = skills_result.get("score", 0)
    
    if cert_score >= skills_score:
        # Las certificaciones ganaron
        if skills_score > 0:
            combined_reason = f"{cert_result.get('reason', '')} | Adicionalmente: {skills_result.get('reason', '')}"
        else:
            combined_reason = cert_result.get('reason', '')
        return {
            "score": cert_score,
            "reason": combined_reason
        }
    else:
        # Las skills (penalizadas) ganaron, lo que significa que no había buenas certificaciones
        return {
            "score": skills_score,
            "reason": f"No hay certificaciones adecuadas. {skills_result.get('reason', '')}"
        }