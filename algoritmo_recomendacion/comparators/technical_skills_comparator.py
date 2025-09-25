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

def compare_technical_skills(cv_skills: list, job_skills: list) -> dict:
    """
    Compara las habilidades técnicas del CV con las requeridas en la descripción de trabajo.
    Optimizado para hacer toda la comparación en un solo prompt de IA.
    
    Args:
        cv_skills (list): Lista de habilidades técnicas del CV
        job_skills (list): Lista de habilidades técnicas requeridas
        
    Returns:
        dict: Resultado de la comparación
    """
    if not job_skills:
        return {"score": -1.0, "matched": [], "missing": []}
    
    if not cv_skills:
        return {"score": -1.0, "matched": [], "missing": job_skills}
    
    try:
        # Crear el prompt para comparar todas las habilidades de una vez
        cv_skills_str = "\n".join([f"- {skill}" for skill in cv_skills])
        job_skills_str = "\n".join([f"- {skill}" for skill in job_skills])
        prompt = ChatPromptTemplate.from_messages([
            ("system", """Eres un experto en evaluar compatibilidad de habilidades técnicas. 
            Analiza las habilidades del CV y determina cuáles cumplen con los requerimientos del trabajo.
            No Descartes de una analiza si tienen relacion, no tienen que ser exactamente igual para que se relacionen.
            
            Responde ÚNICAMENTE con JSON válido que contenga:
            - "score": puntaje entre 0-1
            - "reason": explicación detallada de la compatibilidad"""),
            
            ("human", f"""Compara estas habilidades técnicas:

HABILIDADES DEL CV:
{cv_skills_str}

HABILIDADES REQUERIDAS:
{job_skills_str}

Evalúa la compatibilidad general entre las habilidades del CV y las requeridas.
Score debe ser 1.0 para compatibilidad perfecta, 0.8-0.9 para muy buena, 0.3-0.7 para regular, 0.0-0.2 para baja.
La razón debe explicar qué habilidades coinciden, cuáles faltan y por qué.

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
            score = result.get("score", 0)
            reason = result.get("reason", "")
            
            return {
                "score": round(score, 2),
                "reason": reason
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
    matched_count = 0
    total_score = 0
    matched_details = []
    
    for required_skill in job_skills:
        best_score = 0
        best_match = ""
        
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
                best_match = cv_skill
        
        if best_score > 0.5:
            matched_count += 1
            matched_details.append(f"{best_match} coincide con {required_skill}")
        
        total_score += best_score
    
    avg_score = total_score / len(job_skills) if job_skills else 0
    
    # Crear razón explicativa
    if matched_count == 0:
        reason = f"No se encontraron coincidencias entre las {len(cv_skills)} habilidades del CV y las {len(job_skills)} requeridas."
    elif matched_count == len(job_skills):
        reason = f"Todas las {len(job_skills)} habilidades requeridas tienen coincidencias en el CV. {', '.join(matched_details[:3])}."
    else:
        reason = f"{matched_count} de {len(job_skills)} habilidades requeridas tienen coincidencias. {', '.join(matched_details[:3])}."
    
    return {
        "score": round(avg_score, 2),
        "reason": reason
    }
