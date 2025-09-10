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

def compare_soft_skills(cv_skills: list, job_skills: list) -> dict:
    """
    Compara las habilidades blandas del CV con las requeridas en la descripción de trabajo.
    Optimizado para hacer toda la comparación en un solo prompt de IA.
    
    Args:
        cv_skills (list): Lista de habilidades blandas del CV
        job_skills (list): Lista de habilidades blandas requeridas
        
    Returns:
        dict: Resultado de la comparación
    """
    if not job_skills:
        return {"score": 1.0, "matched": [], "missing": []}
    
    if not cv_skills:
        return {"score": 0.0, "matched": [], "missing": job_skills}
    
    try:
        # Crear el prompt para comparar todas las habilidades de una vez
        cv_skills_str = "\n".join([f"- {skill}" for skill in cv_skills])
        job_skills_str = "\n".join([f"- {skill}" for skill in job_skills])
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """Eres un experto en evaluar compatibilidad de habilidades blandas. 
            Analiza las habilidades blandas del CV y determina cuáles cumplen con los requerimientos del trabajo.
            No Descartes de una analiza si tienen relacion, no tienen que ser exactamente igual para que se relacionen.
            
            Responde ÚNICAMENTE con JSON válido que contenga:
            - "matches": array de objetos con "cv_skill", "required_skill", "score" (0-1), "reason"
            - "missing": array de habilidades requeridas que no tienen coincidencia
            - "total_score": puntaje promedio (0-1)"""),
            
            ("human", f"""Compara estas habilidades blandas:

HABILIDADES BLANDAS DEL CV:
{cv_skills_str}

HABILIDADES BLANDAS REQUERIDAS:
{job_skills_str}

Para cada habilidad requerida, encuentra la mejor coincidencia en el CV (si existe).
Score debe ser 1.0 para coincidencias exactas, 0.8-0.9 para muy relacionadas, 0.3-0.7 para parcialmente relacionadas.
Si no hay coincidencia (Trata de que siempre allá una relacion), inclúyela en "missing".

Responde en formato JSON. sin bloques de código markdown (```json).""")
        ])
        
        chain = prompt | llm
        response = chain.invoke({
            "cv_skills": cv_skills_str, 
            "job_skills": job_skills_str
        })
        
        try:
            result = json.loads(response.content)
            
            # Procesar los resultados
            matched_skills = result.get("matches", [])
            missing_skills = result.get("missing", [])
            total_score = result.get("total_score", 0)
            
            return {
                "score": round(total_score, 2),
                "matched": matched_skills,
                "missing": missing_skills
            }
            
        except json.JSONDecodeError:
            print("Error al parsear JSON de IA, usando fallback simple")
            return _fallback_comparison(cv_skills, job_skills)
            
    except Exception as e:
        print(f"Error en comparación con IA: {e}")
        return _fallback_comparison(cv_skills, job_skills)

def _fallback_comparison(cv_skills: list, job_skills: list) -> dict:
    """
    Comparación simple de fallback cuando falla la IA.
    """
    matched_skills = []
    missing_skills = []
    total_score = 0
    
    for required_skill in job_skills:
        best_match = None
        best_score = 0
        
        for cv_skill in cv_skills:
            cv_lower = cv_skill.lower().strip()
            required_lower = required_skill.lower().strip()
            
            # Comparación simple por texto
            if cv_lower == required_lower:
                score = 1.0
            elif cv_lower in required_lower or required_lower in cv_lower:
                score = 0.7
            else:
                score = 0.0
            
            if score > best_score:
                best_score = score
                best_match = {
                    "cv_skill": cv_skill,
                    "required_skill": required_skill,
                    "score": score,
                    "reason": "Comparación simple por texto"
                }
        
        if best_match and best_match["score"] > 0.5:
            matched_skills.append(best_match)
            total_score += best_match["score"]
        else:
            missing_skills.append(required_skill)
    
    avg_score = total_score / len(job_skills) if job_skills else 0
    
    return {
        "score": round(avg_score, 2),
        "matched": matched_skills,
        "missing": missing_skills
    }
