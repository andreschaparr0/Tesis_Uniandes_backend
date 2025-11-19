"""
Services - Capa de lógica de negocio.
Conecta los endpoints con el core del sistema y los repositories.
"""

import sys
import os
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session

# Agregar paths
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main.data_cleaner import DataCleaner
from main.data_structurer import DataStructurer
from main.recommendation_engine import RecommendationEngine
from api.repositories import CVRepository, JobRepository, AnalysisRepository


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
    
    def create_cv(self, db: Session, cv_data: Dict[str, Any]) -> Any:
        """Crea un CV en la base de datos"""
        return CVRepository.create(db, cv_data)
    
    def get_cv_by_id(self, db: Session, cv_id: int) -> Optional[Any]:
        """Obtiene un CV por ID"""
        return CVRepository.get_by_id(db, cv_id)
    
    def get_all_cvs(self, db: Session, skip: int = 0, limit: int = 100) -> List[Any]:
        """Obtiene todos los CVs con paginación"""
        return CVRepository.get_all(db, skip, limit)
    
    def search_cvs_by_name(self, db: Session, name: str) -> List[Any]:
        """Busca CVs por nombre"""
        return CVRepository.search_by_name(db, name)
    
    def delete_cv(self, db: Session, cv_id: int) -> bool:
        """Elimina un CV"""
        return CVRepository.delete(db, cv_id)


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
    
    def create_job(self, db: Session, job_data: Dict[str, Any]) -> Any:
        """Crea un Job en la base de datos"""
        return JobRepository.create(db, job_data)
    
    def get_job_by_id(self, db: Session, job_id: int) -> Optional[Any]:
        """Obtiene un Job por ID"""
        return JobRepository.get_by_id(db, job_id)
    
    def get_all_jobs(self, db: Session, skip: int = 0, limit: int = 100) -> List[Any]:
        """Obtiene todos los Jobs con paginación"""
        return JobRepository.get_all(db, skip, limit)
    
    def search_jobs_by_title(self, db: Session, title: str) -> List[Any]:
        """Busca Jobs por título"""
        return JobRepository.search_by_title(db, title)
    
    def delete_job(self, db: Session, job_id: int) -> bool:
        """Elimina un Job"""
        return JobRepository.delete(db, job_id)


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


class AnalysisService:
    """Servicio para gestión de análisis"""
    
    def __init__(self):
        pass
    
    def create_analysis(
        self,
        db: Session,
        cv_id: int,
        job_id: int,
        nombre_candidato: str,
        titulo_trabajo: str,
        score: float,
        score_breakdown: dict,
        resultado_completo: dict,
        processing_time: float
    ) -> Any:
        """Crea un análisis en la base de datos"""
        return AnalysisRepository.create(
            db=db,
            cv_id=cv_id,
            job_id=job_id,
            nombre_candidato=nombre_candidato,
            titulo_trabajo=titulo_trabajo,
            score=score,
            score_breakdown=score_breakdown,
            resultado_completo=resultado_completo,
            processing_time=processing_time
        )
    
    def get_analysis_by_id(self, db: Session, analysis_id: int) -> Optional[Any]:
        """Obtiene un análisis por ID"""
        return AnalysisRepository.get_by_id(db, analysis_id)
    
    def get_all_analyses(self, db: Session, skip: int = 0, limit: int = 100) -> List[Any]:
        """Obtiene todos los análisis"""
        return AnalysisRepository.get_all(db, skip, limit)
    
    def get_analyses_by_cv(self, db: Session, cv_id: int) -> List[Any]:
        """Obtiene todos los análisis de un CV"""
        return AnalysisRepository.get_by_cv(db, cv_id)
    
    def get_analyses_by_job(self, db: Session, job_id: int) -> List[Any]:
        """Obtiene todos los análisis de un Job"""
        return AnalysisRepository.get_by_job(db, job_id)
    
    def get_top_candidates(self, db: Session, job_id: int, limit: int = 10) -> List[Any]:
        """Obtiene los mejores candidatos para un Job"""
        return AnalysisRepository.get_top_candidates(db, job_id, limit)
    
    def get_statistics(self, db: Session) -> Dict[str, Any]:
        """Obtiene estadísticas generales del sistema"""
        return AnalysisRepository.get_statistics(db)
    
    def delete_analysis(self, db: Session, analysis_id: int) -> bool:
        """Elimina un análisis"""
        return AnalysisRepository.delete(db, analysis_id)

