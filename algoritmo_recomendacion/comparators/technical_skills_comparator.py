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

def compare_technical_skill(cv_skill: str, required_skill: str) -> dict:
    """
    Compara una habilidad técnica del CV con una requerida usando IA.
    
    Args:
        cv_skill (str): Habilidad técnica del CV
        required_skill (str): Habilidad técnica requerida
        
    Returns:
        dict: Resultado de la comparación
    """
    try:
        prompt = ChatPromptTemplate.from_messages([
            ("system", "Eres un experto en evaluar compatibilidad de habilidades técnicas. Responde ÚNICAMENTE con JSON válido que contenga: 'compatible' (boolean), 'score' (0-1), 'reason' (string)."),
            ("human", f"Compara estas habilidades técnicas y determina si la habilidad del CV cumple con la requerida:\nCV: {cv_skill}\nRequerida: {required_skill}\n\nSi el CV cumple o supera el requerido, score debe ser 1.0. Si no cumple, score debe ser 0.0. Responde en formato JSON.")
        ])
        
        chain = prompt | llm
        response = chain.invoke({"cv_skill": cv_skill, "required_skill": required_skill})
        
        try:
            result = json.loads(response.content)
            return {
                "compatible": result.get("compatible", False),
                "score": result.get("score", 0),
                "reason": result.get("reason", "")
            }
        except json.JSONDecodeError:
            # Fallback simple
            compatible = cv_skill.lower() in required_skill.lower() if cv_skill and required_skill else False
            return {
                "compatible": compatible,
                "score": 1.0 if compatible else 0.0,
                "reason": "Comparación simple por texto"
            }
            
    except Exception as e:
        print(f"Error en comparación: {e}")
        return {"compatible": False, "score": 0.0, "reason": "Error en comparación"}

def compare_technical_skills(cv_skills: list, job_skills: list) -> dict:
    """
    Compara las habilidades técnicas del CV con las requeridas en la descripción de trabajo.
    
    Args:
        cv_skills (list): Lista de habilidades técnicas del CV
        job_skills (list): Lista de habilidades técnicas requeridas
        
    Returns:
        dict: Resultado de la comparación
    """
    if not job_skills:
        return {"score": 1.0, "matched": [], "missing": []}
    
    if not cv_skills:
        return {"score": 0.0, "matched": [], "missing": job_skills}
    
    matched_skills = []
    missing_skills = []
    total_score = 0
    
    # Comparar cada habilidad requerida
    for required_skill in job_skills:
        found_match = False
        
        for cv_skill in cv_skills:
            # Comparar habilidades usando IA
            comparison = compare_technical_skill(cv_skill, required_skill)
            
            if comparison["compatible"]:
                matched_skills.append(required_skill)
                total_score += comparison["score"]
                found_match = True
                break
        
        if not found_match:
            missing_skills.append(required_skill)
    
    # Calcular puntaje promedio
    avg_score = total_score / len(job_skills) if job_skills else 0
    
    return {
        "score": round(avg_score, 2),
        "matched": matched_skills,
        "missing": missing_skills
    }

def get_technical_skills_score(comparison_result: dict) -> float:
    """
    Calcula un puntaje numérico basado en los resultados de la comparación.
    
    Args:
        comparison_result (dict): Resultado de compare_technical_skills
        
    Returns:
        float: Puntaje entre 0 y 1
    """
    return comparison_result.get("score", 0.0)
