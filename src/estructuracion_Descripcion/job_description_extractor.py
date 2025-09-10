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
            "basic_info": {
                "job_title": "",
                "company_name": "",
                "work_modality": "",
                "contract_type": "",
                "salary": "",
                "summary": ""
            },
            "responsibilities": [],
            "location": "",
            "education": "",
            "experience": "",
            "technical_skills": [],
            "soft_skills": [],
            "certifications": "",
            "languages": {},
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
    
    def extract_with_simple_chain(self, text: str, extraction_type: str = "basic_info") -> dict:
        """
        Método sencillo usando LangChain sin Pydantic.
        
        Args:
            text (str): Texto de la descripción de trabajo
            extraction_type (str): Tipo de extracción ("basic_info", "responsibilities", "location", "education", "experience", "technical_skills", "soft_skills", "certifications", "languages", "benefits")
            
        Returns:
            dict: Diccionario con la información extraída
        """
        try:
            # Definir prompts específicos según la estructura JSON definida
            prompts = {
                "basic_info": """Extrae únicamente la información básica del trabajo del siguiente texto.
                Responde en formato JSON con esta estructura exacta:
                {{
                    "job_title": "título del puesto",
                    "company_name": "nombre de la empresa",
                    "work_modality": "modalidad de trabajo (presencial, remoto, híbrido)",
                    "contract_type": "tipo de contrato (tiempo completo, medio tiempo, etc.)",
                    "salary": "información salarial",
                    "summary": "resumen breve del puesto"
                }}
                Si no encuentras alguna información, deja el campo como DESCONOCIDO ("DESCONOCIDO").""",
                
                "responsibilities": """Extrae únicamente las responsabilidades y funciones del cargo del siguiente texto.
                Responde en formato array [] de strings:
                ["responsabilidad1", "responsabilidad2", "responsabilidad3"]
                Si no hay responsabilidades, devuelve un array vacío [].""",
                
                "location": """Extrae únicamente la ubicación del trabajo del siguiente texto.
                Responde en formato JSON con esta estructura:
                {{"location": "ubicación del trabajo"}}
                Si no encuentras la ubicación, devuelve {{"location": "DESCONOCIDO"}}.""",
                
                "education": """Extrae únicamente los requisitos educativos del siguiente texto.
                Responde en formato JSON con esta estructura:
                {{"education": "requisitos educativos"}}
                Si no encuentras requisitos educativos, devuelve {{"education": "DESCONOCIDO"}}.""",
                
                "experience": """Extrae únicamente los requisitos de experiencia del siguiente texto.
                Responde en formato JSON con esta estructura:
                {{"experience": "requisitos de experiencia"}}
                Si no encuentras requisitos de experiencia, devuelve {{"experience": "DESCONOCIDO"}}.""",
                
                "technical_skills": """Extrae únicamente las habilidades técnicas requeridas del siguiente texto.
                Responde en formato array [] de strings
                ["habilidad1", "habilidad2", "habilidad3"]
                Si no hay habilidades técnicas, devuelve un array vacío [].""",
                
                "soft_skills": """Extrae únicamente las habilidades blandas requeridas del siguiente texto.
                Responde en formato array [] de strings:
                ["habilidad1", "habilidad2", "habilidad3"]
                Si no hay habilidades blandas, devuelve un array vacío [].""",
                
                "certifications": """Extrae únicamente las certificaciones requeridas del siguiente texto.
                Responde en formato JSON con esta estructura:
                {{"certifications": "certificaciones requeridas"}}
                Si no encuentras certificaciones, devuelve {{"certifications": "DESCONOCIDO"}}.""",
                
                "languages": """Extrae únicamente los requisitos de idiomas del siguiente texto.
                Responde en formato JSON como un objeto donde las llaves son los idiomas y los valores son los niveles:
                {{"idioma1": "nivel1", "idioma2": "nivel2"}}
                Si no hay requisitos de idiomas, devuelve un objeto vacío {{}}.""",
                
                "benefits": """Extrae únicamente los beneficios ofrecidos del siguiente texto.
                Responde en formato array [] de strings:
                ["beneficio1", "beneficio2", "beneficio3"]
                Si no hay beneficios, devuelve un array vacío []."""
            }
            
            # Crear el prompt
            prompt = ChatPromptTemplate.from_messages([
                ("system", "Eres un experto en extraer información estructurada de descripciones de trabajo. IMPORTANTE: Responde ÚNICAMENTE con la estructura que se te pide, sin texto adicional, sin explicaciones, sin bloques de código markdown (```json)."),
                ("human", f"{prompts.get(extraction_type)}, Texto de la descripción:{{text}}")
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
    
    def extract_full_job_description(self, text: str) -> dict:
        """
        Extrae toda la descripción de trabajo usando extract_with_simple_chain y devuelve el JSON completo.
        
        Args:
            text (str): Texto de la descripción de trabajo
            
        Returns:
            dict: JSON completo de la descripción de trabajo estructurada según la nueva estructura
        """
        # Extraer información básica
        basic_info = self.extract_with_simple_chain(text, "basic_info")
        
        # Extraer responsabilidades
        responsibilities = self.extract_with_simple_chain(text, "responsibilities")
        
        # Extraer ubicación
        location = self.extract_with_simple_chain(text, "location")
        
        # Extraer educación
        education = self.extract_with_simple_chain(text, "education")
        
        # Extraer experiencia
        experience = self.extract_with_simple_chain(text, "experience")
        
        # Extraer habilidades técnicas
        technical_skills = self.extract_with_simple_chain(text, "technical_skills")
        
        # Extraer habilidades blandas
        soft_skills = self.extract_with_simple_chain(text, "soft_skills")

        # Extraer certificaciones
        certifications = self.extract_with_simple_chain(text, "certifications")
        
        # Extraer idiomas
        languages = self.extract_with_simple_chain(text, "languages")
        
        # Extraer beneficios
        benefits = self.extract_with_simple_chain(text, "benefits")
        # Crear estructura final según la nueva estructura definida
        job_final = {
            "basic_info": basic_info if basic_info else {
                "job_title": "DESCONOCIDO",
                "company_name": "DESCONOCIDO",
                "work_modality": "DESCONOCIDO",
                "contract_type": "DESCONOCIDO",
                "salary": "DESCONOCIDO",
                "summary": "DESCONOCIDO"
            },
            "responsibilities": responsibilities if responsibilities else [],
            "location": location.get("location", "DESCONOCIDO") if location else "DESCONOCIDO",
            "education": education.get("education", "DESCONOCIDO") if education else "DESCONOCIDO",
            "experience": experience.get("experience", "DESCONOCIDO") if experience else "DESCONOCIDO",
            "technical_skills": technical_skills if technical_skills else [],
            "soft_skills": soft_skills if soft_skills else [],
            "certifications": certifications.get("certifications", "DESCONOCIDO") if certifications else "DESCONOCIDO",
            "languages": languages if languages else {},
            "benefits": benefits if benefits else []
        }
        
        # Validar estructura final
        validated_job = self._validate_job_structure(job_final)
        return validated_job
    
    def _validate_job_structure(self, job_data: dict) -> dict:
        """
        Valida y asegura que la estructura de la descripción de trabajo sea correcta.
        
        Args:
            job_data (dict): Datos de la descripción de trabajo a validar
            
        Returns:
            dict: Descripción de trabajo con estructura validada
        """
        # Estructura esperada
        expected_structure = {
            "basic_info": {
                "job_title": "DESCONOCIDO",
                "company_name": "DESCONOCIDO",
                "work_modality": "DESCONOCIDO",
                "contract_type": "DESCONOCIDO",
                "salary": "DESCONOCIDO",
                "summary": "DESCONOCIDO"
            },
            "responsibilities": [],
            "location": "DESCONOCIDO",
            "education": "DESCONOCIDO",
            "experience": "DESCONOCIDO",
            "technical_skills": [],
            "soft_skills": [],
            "certifications": "DESCONOCIDO",
            "languages": {},
            "benefits": []
        }
        
        # Validar que todas las llaves principales existan
        for key in expected_structure.keys():
            if key not in job_data:
                job_data[key] = expected_structure[key]
        
        # Validar estructura de información básica
        if isinstance(job_data.get("basic_info"), dict):
            for field in ["job_title", "company_name", "work_modality", "contract_type", "salary", "summary"]:
                if field not in job_data["basic_info"]:
                    job_data["basic_info"][field] = "DESCONOCIDO"
        else:
            job_data["basic_info"] = expected_structure["basic_info"]
        
        # Validar que las listas sean realmente listas
        list_fields = ["responsibilities", "technical_skills", "soft_skills", "benefits"]
        for field in list_fields:
            if not isinstance(job_data.get(field), list):
                job_data[field] = []
        
        # Validar que los strings sean strings
        string_fields = ["location", "education", "experience", "certifications"]
        for field in string_fields:
            if not isinstance(job_data.get(field), str):
                job_data[field] = "DESCONOCIDO"
        
        # Validar que languages sea un diccionario
        if not isinstance(job_data.get("languages"), dict):
            job_data["languages"] = {}
        
        return job_data
    
    def extract_job_from_text(self, text: str, output_path: str = None) -> dict:
        """
        Método principal para extraer descripción de trabajo completa desde texto y opcionalmente guardarla.
        
        Args:
            text (str): Texto de la descripción de trabajo a procesar
            output_path (str, optional): Ruta donde guardar el JSON resultante
            
        Returns:
            dict: Descripción de trabajo estructurada completa
        """
        try:
            # Extraer descripción completa
            job_data = self.extract_full_job_description(text)
            
            # Guardar si se especifica una ruta
            if output_path:
                self.save_to_json(job_data, output_path)
            
            return job_data
            
        except Exception as e:
            print(f"Error en extracción completa: {e}")
            return self.create_job_structure()  # Retornar estructura vacía en caso de error