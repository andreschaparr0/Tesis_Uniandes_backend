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

def compare_education(cv_education: list, job_education: str) -> dict:
    """
    Compara la educación del CV con los requisitos educativos del trabajo.
    Optimizado para hacer toda la comparación en un solo prompt de IA.
    
    Args:
        cv_education (list): Lista de objetos de educación del CV
                              [{"degree": "...", "institution": "...", "year": "...", "field": "..."}]
        job_education (str): Requisitos educativos del trabajo
        
    Returns:
        dict: Resultado de la comparación
    """
    if not job_education or not job_education.strip():
        return {"score": 1.0, "reason": "No hay requisitos educativos"}
    
    if not cv_education:
        return {"score": 0.0, "reason": "CV sin información educativa"}
    
    try:
        # Crear el prompt para comparar toda la educación de una vez
        cv_education_str = "\n".join([
            f"- Título: {edu.get('degree', 'N/A')}, Institución: {edu.get('institution', 'N/A')}, "
            f"Año: {edu.get('year', 'N/A')}, Campo: {edu.get('field', 'N/A')}"
            for edu in cv_education
        ])
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """Eres un experto en evaluar compatibilidad educativa. 
            Analiza la educación del CV y determina si cumple con los requisitos educativos del trabajo.
            No Descartes de una analiza si tienen relacion, no tienen que ser exactamente igual para que se relacionen.
            Considera títulos equivalentes, campos relacionados, niveles educativos similares y especializaciones afines.
            
            Responde ÚNICAMENTE con JSON válido que contenga:
            - "score": puntaje entre 0-1
            - "reason": explicación detallada de la compatibilidad"""),
            
            ("human", f"""Compara esta educación:

EDUCACIÓN DEL CV:
{cv_education_str}

REQUISITOS EDUCATIVOS DEL TRABAJO:
{job_education}

Analiza si la educación del CV cumple con los requisitos del trabajo.
Score debe ser 1.0 para cumplimiento exacto, 0.8-0.9 para muy relacionado, 0.3-0.7 para parcialmente relacionado, 0.0-0.2 para no relacionado.
La razón debe explicar qué aspectos educativos cumplen con los requisitos y cuáles faltan.

Responde en formato JSON. sin bloques de código markdown (```json).""")
        ])
        
        chain = prompt | llm
        response = chain.invoke({
            "cv_education": cv_education_str, 
            "job_education": job_education
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
            return _fallback_comparison(cv_education, job_education)
            
    except Exception as e:
        print(f"Error en comparación con IA: {e}")
        return _fallback_comparison(cv_education, job_education)

def _fallback_comparison(cv_education: list, job_education: str) -> dict:
    """
    Comparación simple de fallback cuando falla la IA.
    """
    if not cv_education:
        return {
            "score": 0.0,
            "reason": "CV sin información educativa"
        }
    
    # Buscar coincidencias simples por palabras clave
    job_lower = job_education.lower()
    total_score = 0
    matched_count = 0
    matched_details = []
    
    # Palabras clave comunes en educación técnica/universitaria
    technical_keywords = ["ingeniería", "sistemas", "computación", "informática", "técnico", "universitario", "egresado"]
    
    for edu in cv_education:
        degree_lower = edu.get("degree", "").lower()
        field_lower = edu.get("field", "").lower()
        
        # Verificar si el título o campo contiene palabras clave relacionadas
        score = 0
        
        for keyword in technical_keywords:
            if keyword in degree_lower or keyword in field_lower:
                if keyword in job_lower:
                    score = 1.0
                    matched_details.append(f"{edu.get('degree', 'N/A')} coincide exactamente con '{keyword}'")
                    break
                else:
                    score = 0.7
                    matched_details.append(f"{edu.get('degree', 'N/A')} es relacionado con '{keyword}'")
        
        if score > 0:
            matched_count += 1
            total_score += score
    
    avg_score = total_score / len(cv_education) if cv_education else 0
    
    # Crear razón explicativa
    if matched_count == 0:
        reason = f"No se encontraron coincidencias entre las {len(cv_education)} educaciones del CV y los requisitos."
    elif matched_count == len(cv_education):
        reason = f"Todas las educaciones del CV cumplen con los requisitos. {', '.join(matched_details[:3])}."
    else:
        reason = f"{matched_count} de {len(cv_education)} educaciones cumplen con los requisitos. {', '.join(matched_details[:3])}."
    
    return {
        "score": round(avg_score, 2),
        "reason": reason
    }
