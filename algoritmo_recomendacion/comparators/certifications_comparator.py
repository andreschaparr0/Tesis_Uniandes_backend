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

def compare_certifications(cv_certifications: list, job_certifications: list) -> dict:
    """
    Compara las certificaciones del CV con las requeridas en la descripción de trabajo.
    
    Args:
        cv_certifications (list): Certificaciones del CV [{"name": "...", "issuer": "...", "year": "..."}]
        job_certifications (list): Certificaciones requeridas ["certificados aws", "certificados google cloud"]
        
    Returns:
        dict: Resultado de la comparación
    """
    if not job_certifications:
        return {"score": 1.0, "matched": [], "missing": []}
    
    if not cv_certifications:
        return {"score": 0.0, "matched": [], "missing": job_certifications}
    
    try:
        # Preparar texto de certificaciones del CV
        cv_text = ""
        for cert in cv_certifications:
            cv_text += f"- {cert.get('name', '')} ({cert.get('issuer', '')})\n"
       
        # Preparar texto de certificaciones requeridas
        job_text = "\n".join([f"- {cert}" for cert in job_certifications])
        prompt_text = f"""Eres un experto en evaluar relevancia de certificaciones técnicas. Responde ÚNICAMENTE con JSON válido que contenga: 'score' IMPORTANTE QUE SEA UN NUMERO ENTRE 0 Y 1, 'matched' (array de strings), 'missing' (array de strings).

            Compara estas certificaciones del CV con las requeridas:

            CV:
            {cv_text}
            Requeridas:
            {job_text}

            Para cada requerimiento, determina si hay una certificación relevante en el CV. Si es directamente relevante, score debe ser 1.0. Si es parcialmente relevante, score debe ser 0.1-0.7. 

            Responde en JSON  sin bloques de código markdown (```json).: {{"score": numero entre 0.0-1.0, "matched": ["requerimiento1", "requerimiento2"], "missing": ["requerimiento3"]}}"""

        response = llm.invoke(prompt_text)
        try:
            result = json.loads(response.content)
            return {
                "score": result.get("score", 0),
                "matched": result.get("matched", []),
                "missing": result.get("missing", [])
            }
        except json.JSONDecodeError:
            # Fallback simple
            return {
                "score": 0.0,
                "matched": [],
                "missing": job_certifications
            }
            
    except Exception as e:
        print(f"Error en comparación de certificaciones: {e}")
        return {"score": 0.0, "matched": [], "missing": job_certifications}