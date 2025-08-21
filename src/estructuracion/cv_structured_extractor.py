import re
import json
from typing import Dict, List, Optional
from pdf_text_extractor import extract_text_from_pdf
from limpieza import clean_text
import os

class CVStructuredExtractor:
    """
    Clase para extraer y estructurar información de hojas de vida en formato JSON.
    """
    
    def __init__(self):
        """
        Inicializa el extractor de CV estructurado.
        """
        # Patrones regex para información personal
        self.email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        self.phone_pattern = r'(\+?57\s?)?[0-9]{3}[\s-]?[0-9]{3}[\s-]?[0-9]{4}'
        
        # Palabras clave para identificar secciones
        self.section_keywords = {
            'education': ['educación', 'education', 'estudios', 'académico', 'academic'],
            'experience': ['experiencia', 'experience', 'laboral', 'work', 'trabajo'],
            'skills': ['habilidades', 'skills', 'competencias', 'tecnologías', 'technologies'],
            'languages': ['idiomas', 'languages', 'idioma', 'language']
        }
    
    def extract_personal_info(self, text: str) -> Dict[str, str]:
        """
        Extrae información personal básica del texto del CV.
        
        Args:
            text (str): Texto extraído del CV
            
        Returns:
            Dict[str, str]: Diccionario con información personal extraída
        """
        personal_info = {
            'name': '',
            'email': '',
            'phone': '',
            'location': ''
        }
        
        # Extraer email
        email_match = re.search(self.email_pattern, text)
        if email_match:
            personal_info['email'] = email_match.group(0)
        
        # Extraer teléfono
        phone_match = re.search(self.phone_pattern, text)
        if phone_match:
            personal_info['phone'] = phone_match.group(0)
        
        # Extraer nombre (heurística simple: primera línea que no sea email ni teléfono)
        lines = text.split('\n')
        for line in lines[:10]:  # Revisar solo las primeras 10 líneas
            line = line.strip()
            if (line and 
                not re.search(self.email_pattern, line) and 
                not re.search(self.phone_pattern, line) and
                len(line.split()) <= 4 and  # Nombre típicamente tiene 1-4 palabras
                not any(keyword in line.lower() for keywords in self.section_keywords.values() for keyword in keywords)):
                personal_info['name'] = line
                break
        
        # Extraer ubicación (heurística: buscar después de "Ubicación:", "Location:", etc.)
        location_patterns = [
            r'ubicación[:\s]+([^\n]+)',
            r'location[:\s]+([^\n]+)',
            r'dirección[:\s]+([^\n]+)',
            r'address[:\s]+([^\n]+)'
        ]
        
        for pattern in location_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                personal_info['location'] = match.group(1).strip()
                break
        
        return personal_info
    
    def create_initial_structure(self) -> Dict:
        """
        Crea la estructura inicial del JSON para el CV.
        
        Returns:
            Dict: Estructura JSON inicial vacía
        """
        return {
            "personal_info": {
                "name": "",
                "email": "",
                "phone": "",
                "location": ""
            },
            "education": [],
            "experience": [],
            "skills": {
                "programming_languages": [],
                "frameworks": [],
                "databases": [],
                "soft_skills": []
            },
            "languages": []
        }
    
    def extract_from_pdf(self, pdf_path: str) -> Dict:
        """
        Extrae y estructura información de un CV en PDF.
        
        Args:
            pdf_path (str): Ruta al archivo PDF
            
        Returns:
            Dict: CV estructurado en formato JSON
        """
        try:
            # Extraer texto del PDF
            raw_text = extract_text_from_pdf(pdf_path)
            
            # Crear estructura inicial
            cv_structure = self.create_initial_structure()
            
            # Extraer información personal
            personal_info = self.extract_personal_info(raw_text)
            cv_structure['personal_info'] = personal_info
            
            # Por ahora solo retornamos la información personal
            # En los siguientes pasos agregaremos las demás secciones
            
            return cv_structure
            
        except Exception as e:
            raise Exception(f"Error al procesar el PDF {pdf_path}: {str(e)}")
    
    def save_to_json(self, cv_data: Dict, output_path: str) -> None:
        """
        Guarda el CV estructurado en un archivo JSON.
        
        Args:
            cv_data (Dict): Datos del CV estructurado
            output_path (str): Ruta donde guardar el archivo JSON
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(cv_data, f, ensure_ascii=False, indent=2)
            print(f"CV guardado exitosamente en: {output_path}")
        except Exception as e:
            raise Exception(f"Error al guardar el JSON: {str(e)}")

# Función de conveniencia para uso directo
def extract_cv_to_json(pdf_path: str, output_path: Optional[str] = None) -> Dict:
    """
    Función de conveniencia para extraer CV a JSON.
    
    Args:
        pdf_path (str): Ruta al archivo PDF
        output_path (str, optional): Ruta donde guardar el JSON
        
    Returns:
        Dict: CV estructurado en formato JSON
    """
    extractor = CVStructuredExtractor()
    cv_data = extractor.extract_from_pdf(pdf_path)
    
    if output_path:
        extractor.save_to_json(cv_data, output_path)
    
    return cv_data

