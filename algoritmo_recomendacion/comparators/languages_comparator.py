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

def compare_language_levels(cv_level: str, required_level: str) -> dict:
    """
    Compara dos niveles de idioma usando IA.
    
    Args:
        cv_level (str): Nivel de idioma del CV
        required_level (str): Nivel de idioma requerido
        
    Returns:
        dict: Resultado de la comparación
    """
    try:
        prompt = ChatPromptTemplate.from_messages([
            ("system", "Eres un experto en evaluar compatibilidad de niveles de idioma. Responde ÚNICAMENTE con JSON válido que contenga: 'compatible' (boolean), 'score' (0-1), 'reason' (string)."),
            ("human", f"Compara estos niveles de idioma y determina si el nivel del CV cumple con el requerido:\nCV: {cv_level}\nRequerido: {required_level}\n\nSi el CV cumple o supera el requerido, score debe ser 1.0. Si no cumple, score debe ser 0.0. Responde en formato JSON.")
        ])
        
        chain = prompt | llm
        response = chain.invoke({"cv_level": cv_level, "required_level": required_level})
        
        try:
            result = json.loads(response.content)
            return {
                "compatible": result.get("compatible", False),
                "score": result.get("score", 0),
                "reason": result.get("reason", "")
            }
        except json.JSONDecodeError:
            # Fallback simple
            compatible = cv_level.upper() >= required_level.upper() if cv_level and required_level else False
            return {
                "compatible": compatible,
                "score": 1.0 if compatible else 0.0,
                "reason": "Comparación simple por texto"
            }
            
    except Exception as e:
        print(f"Error en comparación: {e}")
        return {"compatible": False, "score": 0.0, "reason": "Error en comparación"}

def compare_languages(cv_languages: dict, job_languages: dict) -> dict:
    """
    Compara los idiomas del CV con los requeridos en la descripción de trabajo.
    
    Args:
        cv_languages (dict): Idiomas del CV {"idioma": "nivel"}
        job_languages (dict): Idiomas requeridos {"idioma": "nivel"}
        
    Returns:
        dict: Resultado de la comparación
    """
    if not job_languages:
        return {"score": 1.0, "matched": [], "missing": []}
    
    if not cv_languages:
        return {"score": 0.0, "matched": [], "missing": list(job_languages.keys())}
    
    matched_languages = []
    missing_languages = []
    total_score = 0
    
    # Comparar cada idioma requerido
    for language, required_level in job_languages.items():
        cv_level = cv_languages.get(language, "")
        
        if cv_level:
            # Comparar niveles usando IA
            comparison = compare_language_levels(cv_level, required_level)
            
            if comparison["compatible"]:
                matched_languages.append(language)
                total_score += comparison["score"]
            else:
                missing_languages.append(language)
        else:
            missing_languages.append(language)
    
    # Calcular puntaje promedio
    avg_score = total_score / len(job_languages) if job_languages else 0
    
    return {
        "score": round(avg_score, 2),
        "matched": matched_languages,
        "missing": missing_languages
    }

def get_language_score(comparison_result: dict) -> float:
    """
    Calcula un puntaje numérico basado en los resultados de la comparación.
    
    Args:
        comparison_result (dict): Resultado de compare_languages
        
    Returns:
        float: Puntaje entre 0 y 1
    """
    return comparison_result.get("score", 0.0)
