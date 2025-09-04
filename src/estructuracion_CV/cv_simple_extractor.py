import json
import os
from dotenv import load_dotenv
from openai import AzureOpenAI
from langchain_openai import AzureChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List, Optional

# Cargar variables de entorno
load_dotenv()

class SimpleCVExtractor:
    """
    Extractor de CV que soporta tanto Azure OpenAI directo como LangChain.
    """
    
    def __init__(self):
        """
        Inicializa el extractor con ambas opciones: OpenAI directo y LangChain.
        """
        # Configuración de Azure OpenAI (igual que tu plantilla.py)
        self.endpoint = "https://invuniandesai-2.openai.azure.com/"
        self.model_name = "gpt-4o-mini"
        self.deployment = "gpt-4o-mini"
        self.subscription_key = os.getenv("API_TOKEN")
        self.api_version = "2024-12-01-preview"
        
        # Inicializar cliente de Azure OpenAI (método original)
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
        
    
    
    def create_cv_structure(self) -> dict:
        """
        Crea la estructura inicial del JSON para el CV.
        
        Returns:
            dict: Estructura JSON inicial vacía
        """
        return {
            "personal": {
                "name": "",
                "email": "",
                "phone": "",
                "location": ""
            },
            "education": [],
            "experience": [],
            "languages": [],
            "skills": {
                "technical": [],
                "methodologies_and_practices": [],
                "standards_and_frameworks": [],
                "soft_skills": [],
                "certifications": []
            }
            
        }
    
    def save_to_json(self, cv_data: dict, output_path: str) -> None:
        """
        Guarda el CV estructurado en un archivo JSON.
        
        Args:
            cv_data (dict): Datos del CV estructurado
            output_path (str): Ruta donde guardar el archivo JSON
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(cv_data, f, ensure_ascii=False, indent=2)
            print(f"CV guardado exitosamente en: {output_path}")
        except Exception as e:
            print(f"Error al guardar el JSON: {e}")
    
    
    def extract_with_simple_chain(self, text: str, extraction_type: str = "personal") -> dict:
        """
        Método sencillo usando LangChain sin Pydantic (más simple).
        
        Args:
            text (str): Texto extraído del CV
            extraction_type (str): Tipo de extracción ("personal", "education", "experience", "skills")
            
        Returns:
            dict: Diccionario con la información extraída
        """
        try:
            # Definir prompts según el tipo
            prompts = {
                "personal": "Extrae únicamente la información personal básica (nombre, email, teléfono, ubicación) del siguiente CV. Responde en formato JSON (pon las llaves en ingles).",
                "education": "Extrae únicamente la información educativa (títulos, instituciones, años) del siguiente CV. Responde en formato JSON (pon las llaves en ingles).",
                "experience": "Extrae únicamente la experiencia laboral (cargos, empresas, duración) del siguiente CV. Responde en formato JSON (pon las llaves en ingles).",
                "languages": "Extrae únicamente los idiomas (idioma, nivel) del siguiente CV. Responde en formato JSON donde la llave es el lenguaje y el valor el nivel (pon las llaves en ingles).",
                "skills": "Extrae únicamente las skills (technical habilities, methodologies_and_practices, standards_and_frameworks, soft_skills y certifications) del siguiente CV. Responde en formato JSON (pon las llaves en ingles)."
            }
            
            # Crear el prompt
            prompt = ChatPromptTemplate.from_messages([
                ("system", "Eres un experto en extraer información estructurada de hojas de vida. IMPORTANTE: Responde ÚNICAMENTE con JSON válido, sin texto adicional, sin explicaciones, sin bloques de código markdown (```json). Solo el JSON puro."),
                ("human", f"{prompts.get(extraction_type)}\n\nTexto del CV:\n{{text}}")
            ])
            
            # Crear la cadena
            chain = prompt | self.llm
            
            # Ejecutar la cadena
            response = chain.invoke({"text": text[:2000]})
            
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

    def extract_full_cv_simple(self, text: str) -> dict:
        """
        Extrae todo el CV usando extract_with_simple_chain y devuelve el JSON completo.
        
        Args:
            text (str): Texto extraído del CV
            
        Returns:
            dict: JSON completo del CV estructurado
        """
        # Extraer información personal
        personal_info = self.extract_with_simple_chain(text, "personal")

        # Extraer educación
        education = self.extract_with_simple_chain(text, "education")
        
        # Extraer experiencia laboral
        experience = self.extract_with_simple_chain(text, "experience")
        
        # Extraer habilidades
        skills = self.extract_with_simple_chain(text, "skills")
        
        # Extraer idiomas
        languages = self.extract_with_simple_chain(text, "languages")
        
        # Crear estructura final
        cv_final = {
            "personal": personal_info,
            "education": education,
            "experience": experience,
            "languages": languages,
            "skills": skills
        }
        
        return cv_final
