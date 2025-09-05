import json
import os
from dotenv import load_dotenv
from openai import AzureOpenAI
from langchain_openai import AzureChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.prompts import ChatPromptTemplate

# Cargar variables de entorno
load_dotenv()

class JobDescriptionExtractor:
    """
    Extractor de descripciones de trabajo usando Azure OpenAI y LangChain.
    """
    
    def __init__(self):
        """
        Inicializa el extractor con Azure OpenAI y LangChain.
        """
        # Configuración de Azure OpenAI
        self.endpoint = "https://invuniandesai-2.openai.azure.com/"
        self.model_name = "gpt-4o-mini"
        self.deployment = "gpt-4o-mini"
        self.subscription_key = os.getenv("API_TOKEN")
        self.api_version = "2024-12-01-preview"
        
        # Inicializar cliente de Azure OpenAI
        self.client = AzureOpenAI(
            api_version=self.api_version,
            azure_endpoint=self.endpoint,
            api_key=self.subscription_key,
        )
        
        # Inicializar LangChain con Azure OpenAI
        self.llm = AzureChatOpenAI(
            azure_deployment=self.deployment,
            azure_endpoint=self.endpoint,
            api_key=self.subscription_key,
            api_version=self.api_version,
            temperature=0.1,
            max_tokens=2000
        )
    
    def create_job_structure(self) -> dict:
        """
        Crea la estructura inicial del JSON para la descripción de trabajo.
        
        Returns:
            dict: Estructura JSON inicial vacía
        """
        return {
        "job_title": "",
        "company_name": "",
        "location": "",
        "work_modality": "",
        "contract_type": "",
        "salary": "",
        "summary": "",
        "responsibilities": [],
        "qualifications": {
            "requirements": {
            "education": "",
            "experience": "",
            "technical_skills": [],
            "soft_skills": [],
            "certifications": "",
            "languages": {}
            }
        },
        "benefits": []
        }
    
    def save_to_json(self, job_data: dict, output_path: str) -> None:
        """
        Guarda la descripción de trabajo en un archivo JSON.
        
        Args:
            job_data (dict): Datos de la descripción de trabajo
            output_path (str): Ruta donde guardar el archivo JSON
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(job_data, f, ensure_ascii=False, indent=2)
            print(f"Descripción de trabajo guardada exitosamente en: {output_path}")
        except Exception as e:
            print(f"Error al guardar el JSON: {e}")
    
    def extract_with_simple_chain(self, text: str, extraction_type: str = "basic") -> dict:
        """
        Método sencillo usando LangChain sin Pydantic.
        
        Args:
            text (str): Texto de la descripción de trabajo
            extraction_type (str): Tipo de extracción ("basic", "responsibilities", "qualifications", "benefits")
            
        Returns:
            dict: Diccionario con la información extraída
        """
        try:
            # Definir prompts según el tipo
            prompts = {
                "basic": "Extrae únicamente la información básica del trabajo (título, empresa, ubicación, modalidad, tipo de contrato, salario, resumen) del siguiente texto. Responde en formato JSON.",
                "responsibilities": "Extrae únicamente las responsabilidades y funciones del cargo del siguiente texto. Responde en formato JSON con una lista llamada 'responsibilities'.",
                "qualifications": "Extrae únicamente los requisitos y calificaciones (educación, experiencia, habilidades técnicas y blandas, certificaciones y idiomas) del siguiente texto. Responde en formato JSON y pon las llaves en ingles.",
                "benefits": "Extrae únicamente los beneficios ofrecidos del siguiente texto. Responde en formato JSON con una lista llamada 'benefits'."
            }
            
            # Crear el prompt
            prompt = ChatPromptTemplate.from_messages([
                ("system", "Eres un experto en extraer información estructurada de descripciones de trabajo. IMPORTANTE: Responde ÚNICAMENTE con JSON válido, sin texto adicional, sin explicaciones, sin bloques de código markdown (```json). Solo el JSON puro."),
                ("human", f"{prompts.get(extraction_type)}\n\nTexto de la descripción:\n{{text}}")
            ])
            
            # Crear la cadena
            chain = prompt | self.llm
            
            # Ejecutar la cadena
            response = chain.invoke({"text": text})
            
            # Parsear el JSON
            try:
                result = json.loads(response.content)
                return result
            except json.JSONDecodeError:
                print(f"Error al parsear JSON: {response.content}")
                return {}
            
        except Exception as e:
            print(f"Error en extracción simple con LangChain: {e}")
            return {}
    
    def extract_full_job_description(self, text: str) -> dict:
        """
        Extrae toda la descripción de trabajo usando extract_with_simple_chain y devuelve el JSON completo.
        
        Args:
            text (str): Texto de la descripción de trabajo
            
        Returns:
            dict: JSON completo de la descripción de trabajo estructurada
        """
        # Extraer información básica
        basic_info = self.extract_with_simple_chain(text, "basic")
        
        # Extraer responsabilidades
        responsibilities = self.extract_with_simple_chain(text, "responsibilities")
        
        # Extraer calificaciones
        qualifications = self.extract_with_simple_chain(text, "qualifications")
        
        # Extraer beneficios
        benefits = self.extract_with_simple_chain(text, "benefits")
        
        # Crear estructura final
        job_final = {
            "job_title": basic_info.get("titulo", ""),
            "company_name": basic_info.get("empresa", ""),
            "location": basic_info.get("ubicacion", ""),
            "work_modality": basic_info.get("modalidad", ""),
            "contract_type": basic_info.get("tipo_contrato", ""),
            "salary": basic_info.get("salario", {}),
            "summary": basic_info.get("resumen", ""),
            "responsibilities": responsibilities.get("responsibilities", []),
            "qualifications": qualifications,
            "benefits": benefits.get("benefits", [])
        }
        
        return job_final