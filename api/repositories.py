"""
Repositories - Capa de acceso a datos.
Maneja todas las operaciones CRUD con la base de datos.
"""

from sqlalchemy.orm import Session
from typing import List, Optional
from api.database import CV, JobDescription, Analysis


class CVRepository:
    """Repository para operaciones con CVs"""
    
    @staticmethod
    def create(db: Session, cv_data: dict) -> CV:
        """Crea un nuevo CV en la BD"""
        personal = cv_data.get("personal", {})
        cv = CV(
            nombre=personal.get("name", "Unknown"),
            email=personal.get("email", ""),
            telefono=personal.get("phone", ""),
            ubicacion=personal.get("location", ""),
            cv_data=cv_data
        )
        db.add(cv)
        db.commit()
        db.refresh(cv)
        return cv
    
    @staticmethod
    def get_by_id(db: Session, cv_id: int) -> Optional[CV]:
        """Obtiene un CV por ID"""
        return db.query(CV).filter(CV.id == cv_id).first()
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[CV]:
        """Obtiene todos los CVs con paginación"""
        return db.query(CV).offset(skip).limit(limit).all()
    
    @staticmethod
    def search_by_name(db: Session, name: str) -> List[CV]:
        """Busca CVs por nombre"""
        return db.query(CV).filter(CV.nombre.ilike(f"%{name}%")).all()
    
    @staticmethod
    def delete(db: Session, cv_id: int) -> bool:
        """Elimina un CV"""
        cv = db.query(CV).filter(CV.id == cv_id).first()
        if cv:
            db.delete(cv)
            db.commit()
            return True
        return False


class JobRepository:
    """Repository para operaciones con Jobs"""
    
    @staticmethod
    def create(db: Session, job_data: dict) -> JobDescription:
        """Crea un nuevo Job en la BD"""
        basic_info = job_data.get("basic_info", {})
        job = JobDescription(
            titulo=basic_info.get("job_title", "Unknown"),
            empresa=basic_info.get("company_name", ""),
            ubicacion=job_data.get("location", ""),
            job_data=job_data
        )
        db.add(job)
        db.commit()
        db.refresh(job)
        return job
    
    @staticmethod
    def get_by_id(db: Session, job_id: int) -> Optional[JobDescription]:
        """Obtiene un Job por ID"""
        return db.query(JobDescription).filter(JobDescription.id == job_id).first()
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[JobDescription]:
        """Obtiene todos los Jobs con paginación"""
        return db.query(JobDescription).offset(skip).limit(limit).all()
    
    @staticmethod
    def search_by_title(db: Session, title: str) -> List[JobDescription]:
        """Busca Jobs por título"""
        return db.query(JobDescription).filter(JobDescription.titulo.ilike(f"%{title}%")).all()
    
    @staticmethod
    def delete(db: Session, job_id: int) -> bool:
        """Elimina un Job"""
        job = db.query(JobDescription).filter(JobDescription.id == job_id).first()
        if job:
            db.delete(job)
            db.commit()
            return True
        return False


class AnalysisRepository:
    """Repository para operaciones con Análisis"""
    
    @staticmethod
    def create(
        db: Session,
        cv_id: int,
        job_id: int,
        nombre_candidato: str,
        titulo_trabajo: str,
        score: float,
        score_breakdown: dict,
        resultado_completo: dict,
        processing_time: float
    ) -> Analysis:
        """Crea un nuevo análisis en la BD"""
        analysis = Analysis(
            cv_id=cv_id,
            job_id=job_id,
            nombre_candidato=nombre_candidato,
            titulo_trabajo=titulo_trabajo,
            score=score,
            score_breakdown=score_breakdown,
            resultado_completo=resultado_completo,
            processing_time=processing_time
        )
        db.add(analysis)
        db.commit()
        db.refresh(analysis)
        return analysis
    
    @staticmethod
    def get_by_id(db: Session, analysis_id: int) -> Optional[Analysis]:
        """Obtiene un análisis por ID"""
        return db.query(Analysis).filter(Analysis.id == analysis_id).first()
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Analysis]:
        """Obtiene todos los análisis"""
        return db.query(Analysis).order_by(Analysis.created_at.desc()).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_by_cv(db: Session, cv_id: int) -> List[Analysis]:
        """Obtiene análisis de un CV específico"""
        return db.query(Analysis).filter(Analysis.cv_id == cv_id).order_by(Analysis.created_at.desc()).all()
    
    @staticmethod
    def get_by_job(db: Session, job_id: int) -> List[Analysis]:
        """Obtiene análisis de un Job específico"""
        return db.query(Analysis).filter(Analysis.job_id == job_id).order_by(Analysis.score.desc()).all()
    
    @staticmethod
    def get_top_candidates(db: Session, job_id: int, limit: int = 10) -> List[Analysis]:
        """Obtiene los mejores candidatos para un job"""
        return (
            db.query(Analysis)
            .filter(Analysis.job_id == job_id)
            .order_by(Analysis.score.desc())
            .limit(limit)
            .all()
        )
    
    @staticmethod
    def get_statistics(db: Session) -> dict:
        """Obtiene estadísticas generales"""
        total_analyses = db.query(Analysis).count()
        total_cvs = db.query(CV).count()
        total_jobs = db.query(JobDescription).count()
        
        avg_score = db.query(Analysis).with_entities(
            db.func.avg(Analysis.score)
        ).scalar() or 0.0
        
        return {
            "total_analyses": total_analyses,
            "total_cvs": total_cvs,
            "total_jobs": total_jobs,
            "average_score": round(avg_score, 3)
        }

