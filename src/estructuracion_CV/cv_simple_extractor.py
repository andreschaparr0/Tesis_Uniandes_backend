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
                "nombre": "",
                "email": "",
                "telefono": "",
                "ubicacion": ""
            },
            "educacion": [],
            "experiencia_laboral": [],
            "skills": {
                "habilidades_tecnicas": [],
                "habilidades_blandas": [],
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
                "personal": "Extrae únicamente la información personal básica (nombre, email, teléfono, ubicación) del siguiente CV. Responde en formato JSON.",
                "education": "Extrae únicamente la información educativa (títulos, instituciones, años) del siguiente CV. Responde en formato JSON.",
                "experience": "Extrae únicamente la experiencia laboral (cargos, empresas, duración) del siguiente CV. Responde en formato JSON.",
                "skills": "Extrae únicamente las habilidades técnicas y blandas del siguiente CV. Responde en formato JSON."
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
        
        # Crear estructura final
        cv_final = {
            "personal": personal_info,
            "educacion": education,
            "experiencia_laboral": experience,
            "skills": skills
        }
        
        return cv_final

# ===== EJEMPLO DE USO =====
if __name__ == "__main__":
    # Texto de ejemplo de un CV
    sample_cv_text = """
    Juan Pérez
    juan.perez@email.com
    +57 300 123 4567
    Bogotá, Colombia
    
    EXPERIENCIA PROFESIONAL
    Desarrollador Full Stack - TechCorp (2022-2024)
    - Desarrollo de aplicaciones web con React y Node.js
    - Manejo de bases de datos PostgreSQL y MongoDB
    
    Desarrollador Junior - StartupXYZ (2020-2022)
    - Desarrollo frontend con JavaScript y CSS
    - Colaboración en equipo ágil
    
    EDUCACIÓN
    Ingeniería de Sistemas - Universidad de los Andes (2016-2020)
    Bachillerato - Colegio San Patricio (2010-2016)
    
    HABILIDADES
    Lenguajes: Python, JavaScript, Java, SQL
    Frameworks: React, Node.js, Django, Spring Boot
    Bases de datos: PostgreSQL, MongoDB, MySQL
    Habilidades blandas: Trabajo en equipo, Comunicación, Liderazgo
    
    IDIOMAS
    Español (nativo), Inglés (avanzado), Francés (básico)
    """
    
    # Crear instancia del extractor
    extractor = SimpleCVExtractor()
    
    print("=== EJEMPLO DE USO DEL EXTRACTOR DE CV ===\n")
    
    # 1. Método original (OpenAI directo)
    print("1. EXTRACCIÓN CON OPENAI DIRECTO:")
    personal_info_original = extractor.extract_personal_info(sample_cv_text)
    print(f"Información personal: {personal_info_original}\n")
    
    # 2. Método con LangChain + Pydantic (información personal)
    print("2. EXTRACCIÓN CON LANGCHAIN + PYDANTIC (Personal):")
    personal_info_langchain = extractor.extract_personal_info_langchain(sample_cv_text)
    print(f"Información personal: {personal_info_langchain}\n")
    
    # 3. Método con LangChain + Pydantic (CV completo)
    print("3. EXTRACCIÓN CON LANGCHAIN + PYDANTIC (CV Completo):")
    full_cv_langchain = extractor.extract_full_cv_langchain(sample_cv_text)
    print(f"CV completo extraído:")
    print(f"- Nombre: {full_cv_langchain.personal_info.name}")
    print(f"- Email: {full_cv_langchain.personal_info.email}")
    print(f"- Experiencias: {len(full_cv_langchain.experience)}")
    print(f"- Educación: {len(full_cv_langchain.education)}")
    print(f"- Habilidades técnicas: {len(full_cv_langchain.skills.programming_languages)}")
    print()
    
    # 4. Método simple con LangChain (sin Pydantic)
    print("4. EXTRACCIÓN SIMPLE CON LANGCHAIN:")
    simple_personal = extractor.extract_with_simple_chain(sample_cv_text, "personal")
    print(f"Información personal simple: {simple_personal}\n")
    
    simple_skills = extractor.extract_with_simple_chain(sample_cv_text, "skills")
    print(f"Habilidades extraídas: {simple_skills}\n")
    
    # 5. Guardar resultado en JSON
    print("5. GUARDANDO RESULTADO EN JSON:")
    cv_structure = extractor.create_cv_structure()
    cv_structure["personal_info"] = personal_info_original
    extractor.save_to_json(cv_structure, "cv_extracted.json")
    
    print("\n=== FIN DEL EJEMPLO ===")
