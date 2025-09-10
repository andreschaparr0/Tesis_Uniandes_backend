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
            "technical_skills": [],
            "soft_skills": [],
            "certifications": [],
            "languages": []
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
            extraction_type (str): Tipo de extracción ("personal", "education", "experience", "technical_skills", "soft_skills", "certifications", "languages")
            
        Returns:
            dict: Diccionario con la información extraída
        """
        try:
            # Definir prompts específicos según la estructura JSON definida
            prompts = {
                "personal": """Extrae únicamente la información personal básica del siguiente CV. 
                Responde en formato JSON con esta estructura exacta:
                {{
                    "name": "nombre completo",
                    "email": "correo electrónico",
                    "phone": "número de teléfono",
                    "location": "ubicación/ciudad"
                }}
                Si no encuentras alguna información, deja el campo como DESCONOCIDO ("DESCONOCIDO").""",
                
                "education": """Extrae únicamente la información educativa del siguiente CV.
                Responde en formato JSON como un array de objetos con esta estructura:
                [
                    {{
                        "degree": "título obtenido",
                        "institution": "nombre de la institución",
                        "year": "año de graduación",
                        "field": "campo de estudio"
                    }}
                ]
                Si no hay información educativa, devuelve un array vacío [].""",
                
                "experience": """Extrae únicamente la experiencia laboral del siguiente CV.
                Responde en formato JSON como un array de objetos con esta estructura:
                [
                    {{
                        "position": "cargo o puesto",
                        "company": "nombre de la empresa",
                        "duration": "duración del trabajo",
                        "description": "descripción breve de responsabilidades"
                    }}
                ]
                Si no hay experiencia laboral, devuelve un array vacío [].""",
                
                "technical_skills": """Extrae únicamente las habilidades técnicas (technical_skills) del siguiente CV.
                Responde en formato array [] de strings:
                ["habilidad1", "habilidad2", "habilidad3"]
                Si no hay habilidades técnicas, devuelve un array con un array vacío [].""",
                
                "soft_skills": """Extrae únicamente las habilidades blandas (soft_skills) del siguiente CV.
                Responde en formato array [] de strings:
                ["habilidad1", "habilidad2", "habilidad3"]
                Si no hay habilidades blandas, devuelve un array con un array vacío [].""",
                
                "certifications": """Extrae únicamente las certificaciones del siguiente CV.
                Responde en formato JSON como un array de objetos con esta estructura:
                [
                    {{
                        "name": "nombre de la certificación",
                        "issuer": "institución que la emitió",
                        "year": "año de obtención"
                    }}
                ]
                Si no hay certificaciones, devuelve un array vacío [].""",
                
                "languages": """Extrae únicamente los idiomas del siguiente CV.
                Responde en formato JSON como un array de objetos con esta estructura:
                [
                    {{
                        "language": "nombre del idioma",
                        "level": "nivel (básico, intermedio, avanzado, nativo)"
                    }}
                ]
                Si no hay idiomas, devuelve un array vacío []."""
            }
            
            # Crear el prompt
            prompt = ChatPromptTemplate.from_messages([
                ("system", "Eres un experto en extraer información estructurada de hojas de vida. IMPORTANTE: Responde ÚNICAMENTE con la estructura que se te pide, sin texto adicional, sin explicaciones, sin bloques de código markdown (```json)."),
                ("human", f"{prompts.get(extraction_type)}, Texto del CV:{{text}}")
            ])
            
            # Crear la cadena
            chain = prompt | self.llm
            
            # Ejecutar la cadena
            response = chain.invoke({"text": text})
            
            # Parsear el JSON usando el método de limpieza
            result = self._clean_json_response(response.content)
            return result
            
        except Exception as e:
            print(f"Error en extracción simple con LangChain: {e}")
            return {}
    
    def _clean_json_response(self, response_content: str) -> dict:
        """
        Limpia y valida la respuesta JSON del modelo.
        
        Args:
            response_content (str): Contenido de la respuesta del modelo
            
        Returns:
            dict: JSON limpio y validado
        """
        try:
            # Limpiar la respuesta removiendo posibles bloques de código markdown
            cleaned_content = response_content.strip()
            
            # Remover bloques de código markdown si existen
            if cleaned_content.startswith("```json"):
                cleaned_content = cleaned_content[7:]  # Remover ```json
            if cleaned_content.startswith("```"):
                cleaned_content = cleaned_content[3:]   # Remover ```
            if cleaned_content.endswith("```"):
                cleaned_content = cleaned_content[:-3]  # Remover ```
            
            cleaned_content = cleaned_content.strip()
            
            # Intentar parsear el JSON
            result = json.loads(cleaned_content)
            return result
            
        except json.JSONDecodeError as e:
            print(f"Error al parsear JSON: {e}")
            print(f"Contenido problemático: {response_content[:200]}...")
            return {}
        except Exception as e:
            print(f"Error inesperado al limpiar JSON: {e}")
            return {}

    def extract_full_cv_simple(self, text: str) -> dict:
        """
        Extrae todo el CV usando extract_with_simple_chain y devuelve el JSON completo.
        
        Args:
            text (str): Texto extraído del CV
            
        Returns:
            dict: JSON completo del CV estructurado según la estructura definida
        """
        
        # Extraer información personal
        personal_info = self.extract_with_simple_chain(text, "personal")

        # Extraer educación
        education = self.extract_with_simple_chain(text, "education")
        
        # Extraer experiencia laboral
        experience = self.extract_with_simple_chain(text, "experience")
        
        # Extraer habilidades técnicas
        technical_skills = self.extract_with_simple_chain(text, "technical_skills")
        # Extraer habilidades blandas
        soft_skills = self.extract_with_simple_chain(text, "soft_skills")
        # Extraer certificaciones
        certifications = self.extract_with_simple_chain(text, "certifications")
        
        # Extraer idiomas
        languages = self.extract_with_simple_chain(text, "languages")
        
        # Crear estructura final según la estructura definida en create_cv_structure
        cv_final = {
            "personal": personal_info if personal_info else {
                "name": "",
                "email": "",
                "phone": "",
                "location": ""
            },
            "education": education if education else [],
            "experience": experience if experience else [],
            "technical_skills": technical_skills if technical_skills else [],
            "soft_skills": soft_skills if soft_skills else [],
            "certifications": certifications if certifications else [],
            "languages": languages if languages else []
        }
        
        
        # Validar estructura final
        validated_cv = self._validate_cv_structure(cv_final)
        return validated_cv
    
    def _validate_cv_structure(self, cv_data: dict) -> dict:
        """
        Valida y asegura que la estructura del CV sea correcta.
        
        Args:
            cv_data (dict): Datos del CV a validar
            
        Returns:
            dict: CV con estructura validada
        """
        # Estructura esperada
        expected_structure = {
            "personal": {
                "name": "",
                "email": "",
                "phone": "",
                "location": ""
            },
            "education": [],
            "experience": [],
            "technical_skills": [],
            "soft_skills": [],
            "certifications": [],
            "languages": []
        }
        
        # Validar que todas las llaves principales existan
        for key in expected_structure.keys():
            if key not in cv_data:
                cv_data[key] = expected_structure[key]
        
        # Validar estructura de información personal
        if isinstance(cv_data.get("personal"), dict):
            for field in ["name", "email", "phone", "location"]:
                if field not in cv_data["personal"]:
                    cv_data["personal"][field] = ""
        else:
            cv_data["personal"] = expected_structure["personal"]

        # Validar que las listas sean realmente listas
        list_fields = ["education", "experience", "certifications", "languages"]
        for field in list_fields:
            if not isinstance(cv_data.get(field), list):
                cv_data[field] = []
        
        return cv_data
    
    def extract_cv_from_text(self, text: str, output_path: str = None) -> dict:
        """
        Método principal para extraer CV completo desde texto y opcionalmente guardarlo.
        
        Args:
            text (str): Texto del CV a procesar
            output_path (str, optional): Ruta donde guardar el JSON resultante
            
        Returns:
            dict: CV estructurado completo
        """
        try:
            # Extraer CV completo
            cv_data = self.extract_full_cv_simple(text)
            
            # Guardar si se especifica una ruta
            if output_path:
                self.save_to_json(cv_data, output_path)
            
            return cv_data
            
        except Exception as e:
            print(f"Error en extracción completa: {e}")
            return self.create_cv_structure()  # Retornar estructura vacía en caso de error
