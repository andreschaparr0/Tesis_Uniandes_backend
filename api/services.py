"""
Services - Capa de lógica de negocio.
Conecta los endpoints con el core del sistema y los repositories.
"""

import sys
import os
from typing import Dict, Any

# Agregar paths
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main.data_cleaner import DataCleaner
from main.data_structurer import DataStructurer
from main.recommendation_engine import RecommendationEngine


class CVService:
    """Servicio para procesamiento de CVs"""
    
    def __init__(self):
        self.cleaner = DataCleaner()
        self.structurer = DataStructurer()
    
    def process_cv_from_file(self, file_path: str) -> Dict[str, Any]:
        """
        Procesa un CV desde un archivo PDF.
        Retorna el CV estructurado.
        """
        # Limpiar y extraer texto
        cv_text = self.cleaner.clean_cv_from_image(file_path)
        
        # Estructurar con IA
        cv_structured = self.structurer.structure_cv(cv_text)
        
        return cv_structured
    
    def extract_summary(self, cv_data: Dict[str, Any]) -> Dict[str, str]:
        """Extrae resumen del CV"""
        personal = cv_data.get("personal", {})
        return {
            "nombre": personal.get("name", "N/A"),
            "email": personal.get("email", "N/A"),
            "telefono": personal.get("phone", "N/A"),
            "ubicacion": personal.get("location", "N/A")
        }


class JobService:
    """Servicio para procesamiento de Jobs"""
    
    def __init__(self):
        self.structurer = DataStructurer()
    
    def process_job_from_text(self, description: str) -> Dict[str, Any]:
        """
        Procesa una descripción de trabajo.
        Retorna el job estructurado.
        """
        # Estructurar con IA
        job_structured = self.structurer.structure_job_description(description)
        
        return job_structured
    
    def extract_summary(self, job_data: Dict[str, Any]) -> Dict[str, str]:
        """Extrae resumen del Job"""
        basic_info = job_data.get("basic_info", {})
        return {
            "titulo": basic_info.get("job_title", "N/A"),
            "empresa": basic_info.get("company_name", "N/A"),
            "ubicacion": job_data.get("location", "N/A"),
            "modalidad": basic_info.get("work_modality", "N/A")
        }


class RecommendationService:
    """Servicio para análisis y recomendaciones"""
    
    def __init__(self):
        self.engine = RecommendationEngine()
    
    def analyze(
        self,
        cv_data: Dict[str, Any],
        job_data: Dict[str, Any],
        weights: Dict[str, float] = None
    ) -> Dict[str, Any]:
        """
        Ejecuta el análisis completo CV vs Job.
        Retorna el resultado con score y detalles.
        
        Args:
            cv_data: Datos estructurados del CV
            job_data: Datos estructurados del Job
            weights: Pesos personalizados (opcional). Si es None o dict vacío, usa predeterminados.
        
        Returns:
            dict con score, score_breakdown y resultado_completo
        """
        # Si weights es None o dict vacío, el motor usará los predeterminados
        if weights is not None and len(weights) == 0:
            weights = None
        
        # Generar recomendación usando el motor existente
        recommendation = self.engine.generate_recommendation(
            cv_data=cv_data,
            job_data=job_data,
            weights=weights
        )
        
        # Extraer información clave
        score_final = self.engine.get_final_score(recommendation)
        score_breakdown = self.engine.get_score_breakdown(recommendation)
        
        return {
            "score": score_final,
            "score_breakdown": score_breakdown,
            "resultado_completo": recommendation
        }

