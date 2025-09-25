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

def compare_location_compatibility(cv_location: str, required_location: str) -> dict:
    """
    Compara dos ubicaciones usando IA para determinar compatibilidad.
    
    Args:
        cv_location (str): Ubicación del CV (ej: "bogota colombia")
        required_location (str): Ubicación requerida (ej: "bogota colombia")
        
    Returns:
        dict: Resultado de la comparación
    """
    try:
        prompt = ChatPromptTemplate.from_messages([
            ("system", "Eres un experto en evaluar compatibilidad de ubicaciones geográficas. Responde ÚNICAMENTE con JSON válido que contenga: 'score' (0-1), 'reason' (string). Considera ciudades, países, regiones y proximidad geográfica."),
            ("human", f"Compara estas ubicaciones y determina si la ubicación del CV es compatible con la requerida:\nCV: {cv_location}\nRequerida: {required_location}\n\nSi las ubicaciones son la misma ciudad/país o están muy cerca geográficamente, score debe ser 1.0. Si están en diferentes países lejanos, score debe ser 0.0. Para ubicaciones en el mismo país pero diferentes ciudades, usa un score intermedio (0.3-0.7). Para mismas ciudades y paises pero en escritas en diferente formato es 1. La razón debe explicar el nivel de compatibilidad. Responde en formato JSON.")
        ])
        
        chain = prompt | llm
        response = chain.invoke({"cv_location": cv_location, "required_location": required_location})
        
        try:
            result = json.loads(response.content)
            return {
                "score": result.get("score", 0),
                "reason": result.get("reason", "")
            }
        except json.JSONDecodeError:
            # Fallback simple - comparación básica de texto
            cv_lower = cv_location.lower().strip()
            req_lower = required_location.lower().strip()
            
            # Si son exactamente iguales
            if cv_lower == req_lower:
                return {
                    "score": 1.0,
                    "reason": "Ubicaciones idénticas"
                }
            
            # Si contienen palabras comunes (ciudad o país)
            cv_words = set(cv_lower.split())
            req_words = set(req_lower.split())
            common_words = cv_words.intersection(req_words)
            
            if common_words:
                return {
                    "score": 0.7,
                    "reason": f"Ubicaciones con elementos comunes: {', '.join(common_words)}"
                }
            
            return {
                "score": 0.0,
                "reason": "Ubicaciones diferentes"
            }
            
    except Exception as e:
        print(f"Error en comparación de ubicación: {e}")
        return {"score": 0.0, "reason": "Error en comparación"}

def compare_locations(cv_location: dict, job_location: dict) -> dict:
    """
    Compara la ubicación del CV con la requerida en la descripción de trabajo.
    
    Args:
        cv_location (dict): Ubicación del CV {"location": "bogota colombia"}
        job_location (dict): Ubicación requerida {"location": "bogota colombia"}
        
    Returns:
        dict: Resultado de la comparación
    """
    if not job_location or not job_location.get("location"):
        return {"score": -1.0, "reason": "No hay ubicación requerida"}
    
    if not cv_location or not cv_location.get("location"):
        return {"score": -1.0, "reason": "CV no especifica ubicación"}
    
    cv_loc = cv_location.get("location", "")
    job_loc = job_location.get("location", "")
    
    # Comparar ubicaciones usando IA
    comparison = compare_location_compatibility(cv_loc, job_loc)
    
    return {
        "score": comparison["score"],
        "reason": comparison["reason"]
    }
