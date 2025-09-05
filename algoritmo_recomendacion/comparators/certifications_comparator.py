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

def compare_certification(cv_certification: str, required_certification: str) -> dict:
    """
    Compara una certificación del CV con una requerida usando IA.
    
    Args:
        cv_certification (str): Certificación del CV
        required_certification (str): Certificación requerida
        
    Returns:
        dict: Resultado de la comparación
    """
    try:
        prompt = ChatPromptTemplate.from_messages([
            ("system", "Eres un experto en evaluar compatibilidad de certificaciones. Responde ÚNICAMENTE con JSON válido que contenga: 'compatible' (boolean), 'score' (0-1), 'reason' (string)."),
            ("human", f"Compara estas certificaciones y determina si la certificación del CV cumple con la requerida:\nCV: {cv_certification}\nRequerida: {required_certification}\n\nSi el CV cumple o supera el requerido, score debe ser 1.0. Si no cumple, score debe ser 0.0. Responde en formato JSON.")
        ])
        
        chain = prompt | llm
        response = chain.invoke({"cv_certification": cv_certification, "required_certification": required_certification})
        
        try:
            result = json.loads(response.content)
            return {
                "compatible": result.get("compatible", False),
                "score": result.get("score", 0),
                "reason": result.get("reason", "")
            }
        except json.JSONDecodeError:
            # Fallback simple
            compatible = cv_certification.lower() in required_certification.lower() if cv_certification and required_certification else False
            return {
                "compatible": compatible,
                "score": 1.0 if compatible else 0.0,
                "reason": "Comparación simple por texto"
            }
            
    except Exception as e:
        print(f"Error en comparación: {e}")
        return {"compatible": False, "score": 0.0, "reason": "Error en comparación"}

def compare_certifications(cv_certifications: list, job_certifications: list) -> dict:
    """
    Compara las certificaciones del CV con las requeridas en la descripción de trabajo.
    
    Args:
        cv_certifications (list): Lista de certificaciones del CV
        job_certifications (list): Lista de certificaciones requeridas
        
    Returns:
        dict: Resultado de la comparación
    """
    if not job_certifications:
        return {"score": 1.0, "matched": [], "missing": []}
    
    if not cv_certifications:
        return {"score": 0.0, "matched": [], "missing": job_certifications}
    
    matched_certifications = []
    missing_certifications = []
    total_score = 0
    
    # Comparar cada certificación requerida
    for required_cert in job_certifications:
        found_match = False
        
        for cv_cert in cv_certifications:
            # Comparar certificaciones usando IA
            comparison = compare_certification(cv_cert, required_cert)
            
            if comparison["compatible"]:
                matched_certifications.append(required_cert)
                total_score += comparison["score"]
                found_match = True
                break
        
        if not found_match:
            missing_certifications.append(required_cert)
    
    # Calcular puntaje promedio
    avg_score = total_score / len(job_certifications) if job_certifications else 0
    
    return {
        "score": round(avg_score, 2),
        "matched": matched_certifications,
        "missing": missing_certifications
    }

def get_certification_score(comparison_result: dict) -> float:
    """
    Calcula un puntaje numérico basado en los resultados de la comparación.
    
    Args:
        comparison_result (dict): Resultado de compare_certifications
        
    Returns:
        float: Puntaje entre 0 y 1
    """
    return comparison_result.get("score", 0.0)
