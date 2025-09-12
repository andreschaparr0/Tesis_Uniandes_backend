"""
Módulo de estructuración de datos para el sistema de recomendación de CVs.
Convierte texto limpio a JSON estructurado usando los extractores existentes.
"""

import sys
import os

# Agregar el directorio src al path para importar los extractores
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))
from estructuracion_CV.cv_simple_extractor import SimpleCVExtractor
from estructuracion_Descripcion.job_description_extractor import JobDescriptionExtractor


class DataStructurer:
    """
    Clase para estructurar datos de CVs y descripciones de trabajo.
    """
    
    def __init__(self):
        """
        Inicializa el estructurador de datos.
        """
        self.cv_extractor = SimpleCVExtractor()
        self.job_extractor = JobDescriptionExtractor()
    
    def structure_cv(self, cv_text: str) -> dict:
        """
        Estructura el texto limpio del CV a JSON.
        
        Args:
            cv_text (str): Texto limpio del CV
            
        Returns:
            dict: CV estructurado en JSON
        """
        try:
            # Usar el extractor existente para estructurar el CV
            cv_structured = self.cv_extractor.extract_cv_from_text(cv_text)
            return cv_structured
            
        except Exception as e:
            print(f"Error al estructurar CV: {e}")
            return {}
    
    def structure_job_description(self, description_text: str) -> dict:
        """
        Estructura el texto limpio de la descripción de trabajo a JSON.
        
        Args:
            description_text (str): Texto limpio de la descripción
            
        Returns:
            dict: Descripción estructurada en JSON
        """
        try:
            # Usar el extractor existente para estructurar la descripción
            job_structured = self.job_extractor.extract_full_job_description(description_text)
            return job_structured
            
        except Exception as e:
            print(f"Error al estructurar descripción: {e}")
            return {}
    
    def structure_both(self, cv_text: str, description_text: str) -> tuple:
        """
        Estructura tanto el CV como la descripción de trabajo.
        
        Args:
            cv_text (str): Texto limpio del CV
            description_text (str): Texto limpio de la descripción
            
        Returns:
            tuple: (cv_structured, job_structured)
        """
        try:
            # Estructurar CV
            cv_structured = self.structure_cv(cv_text)
            
            # Estructurar descripción
            job_structured = self.structure_job_description(description_text)
            
            return cv_structured, job_structured
            
        except Exception as e:
            print(f"Error al estructurar datos: {e}")
            return {}, {}


def main():
    """
    Función principal para probar el módulo de estructuración.
    """
    structurer = DataStructurer()
    
    # Ejemplo de uso
    try:
        cv_text = "ejemplo de texto de cv limpio"
        description_text = "ejemplo de texto de descripción limpia"
        
        print("Iniciando estructuración de datos...")
        
        # Estructurar ambos
        cv_structured, job_structured = structurer.structure_both(cv_text, description_text)
        
        print("Estructuración completada exitosamente!")
        print(f"CV estructurado: {len(str(cv_structured))} caracteres")
        print(f"Descripción estructurada: {len(str(job_structured))} caracteres")
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
