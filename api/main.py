"""
CV Recommendation API
Arquitectura limpia con Services y Repositories
"""

from fastapi import FastAPI, File, UploadFile, Form, Depends, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional, Dict
from pydantic import BaseModel, Field
import os
import time

from api.database import init_db, get_db
from api.repositories import CVRepository, JobRepository, AnalysisRepository
from api.services import CVService, JobService, RecommendationService


# ==================== MODELOS PYDANTIC ====================

class WeightsRequest(BaseModel):
    """Modelo para los pesos del análisis"""
    experience: Optional[float] = Field(None, ge=0, le=1, description="Peso para experiencia (0-1)")
    technical_skills: Optional[float] = Field(None, ge=0, le=1, description="Peso para habilidades técnicas (0-1)")
    education: Optional[float] = Field(None, ge=0, le=1, description="Peso para educación (0-1)")
    responsibilities: Optional[float] = Field(None, ge=0, le=1, description="Peso para responsabilidades (0-1)")
    certifications: Optional[float] = Field(None, ge=0, le=1, description="Peso para certificaciones (0-1)")
    soft_skills: Optional[float] = Field(None, ge=0, le=1, description="Peso para habilidades blandas (0-1)")
    languages: Optional[float] = Field(None, ge=0, le=1, description="Peso para idiomas (0-1)")
    location: Optional[float] = Field(None, ge=0, le=1, description="Peso para ubicación (0-1)")
    
    class Config:
        schema_extra = {
            "example": {
                "experience": 0.30,
                "technical_skills": 0.15,
                "education": 0.15,
                "responsibilities": 0.15,
                "certifications": 0.10,
                "soft_skills": 0.08,
                "languages": 0.04,
                "location": 0.03
            }
        }
    
    def to_dict(self) -> Optional[Dict[str, float]]:
        """Convierte a dict, eliminando valores None"""
        weights = {
            k: v for k, v in self.dict().items() 
            if v is not None
        }
        # Si está vacío, retornar None para usar pesos predeterminados
        return weights if weights else None

# Crear app
app = FastAPI(
    title="CV Recommendation API",
    version="2.0.0",
    description="Sistema de análisis de CVs con arquitectura en capas"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servicios
cv_service = CVService()
job_service = JobService()
recommendation_service = RecommendationService()

# Carpeta temporal
TEMP_FOLDER = "temp_uploads"
os.makedirs(TEMP_FOLDER, exist_ok=True)


@app.on_event("startup")
def startup():
    """Inicializa BD al iniciar"""
    init_db()
    print("✅ Base de datos inicializada: cv_system.db")


# ==================== ROOT & HEALTH ====================

@app.get("/")
def root():
    """Información de la API"""
    return {
        "nombre": "CV Recommendation API",
        "version": "2.0.0",
        "documentacion": "/docs",
        "arquitectura": "Services + Repositories + Database"
    }


@app.get("/health")
def health():
    """Health check"""
    return {"status": "ok", "database": "connected"}


# ==================== ENDPOINTS DE CVs ====================

@app.post("/cvs")
def crear_cv(
    cv_file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Procesa y guarda un CV.
    
    - Extrae texto del PDF
    - Estructura con IA
    - Guarda en BD
    - Retorna ID del CV guardado
    """
    file_path = None
    try:
        # Guardar archivo temporal
        file_path = os.path.join(TEMP_FOLDER, cv_file.filename)
        with open(file_path, "wb") as f:
            f.write(cv_file.file.read())
        
        # Procesar CV (Service)
        cv_data = cv_service.process_cv_from_file(file_path)
        
        # Guardar en BD (Repository)
        cv_record = CVRepository.create(db, cv_data)
        
        # Extraer resumen
        summary = cv_service.extract_summary(cv_data)
        
        return {
            "success": True,
            "cv_id": cv_record.id,
            **summary,
            "message": f"CV procesado y guardado con ID {cv_record.id}"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)


@app.get("/cvs")
def listar_cvs(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Lista todos los CVs guardados"""
    cvs = CVRepository.get_all(db, skip, limit)
    return [{
        "id": cv.id,
        "nombre": cv.nombre,
        "email": cv.email,
        "ubicacion": cv.ubicacion,
        "created_at": cv.created_at
    } for cv in cvs]


@app.get("/cvs/{cv_id}")
def obtener_cv(cv_id: int, db: Session = Depends(get_db)):
    """Obtiene un CV específico con todos sus datos"""
    cv = CVRepository.get_by_id(db, cv_id)
    if not cv:
        raise HTTPException(status_code=404, detail="CV no encontrado")
    
    return {
        "id": cv.id,
        "nombre": cv.nombre,
        "email": cv.email,
        "telefono": cv.telefono,
        "ubicacion": cv.ubicacion,
        "cv_data": cv.cv_data,
        "created_at": cv.created_at
    }


@app.get("/cvs/search/{nombre}")
def buscar_cvs(nombre: str, db: Session = Depends(get_db)):
    """Busca CVs por nombre"""
    cvs = CVRepository.search_by_name(db, nombre)
    return [{
        "id": cv.id,
        "nombre": cv.nombre,
        "email": cv.email,
        "created_at": cv.created_at
    } for cv in cvs]


@app.delete("/cvs/{cv_id}")
def eliminar_cv(cv_id: int, db: Session = Depends(get_db)):
    """Elimina un CV"""
    success = CVRepository.delete(db, cv_id)
    if not success:
        raise HTTPException(status_code=404, detail="CV no encontrado")
    return {"message": f"CV {cv_id} eliminado"}


# ==================== ENDPOINTS DE JOBS ====================

@app.post("/jobs")
def crear_job(
    description: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    Procesa y guarda un Job.
    
    - Estructura la descripción con IA
    - Guarda en BD
    - Retorna ID del Job guardado
    """
    try:
        # Procesar Job (Service)
        job_data = job_service.process_job_from_text(description)
        
        # Guardar en BD (Repository)
        job_record = JobRepository.create(db, job_data)
        
        # Extraer resumen
        summary = job_service.extract_summary(job_data)
        
        return {
            "success": True,
            "job_id": job_record.id,
            **summary,
            "message": f"Job procesado y guardado con ID {job_record.id}"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/jobs")
def listar_jobs(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Lista todos los Jobs guardados"""
    jobs = JobRepository.get_all(db, skip, limit)
    return [{
        "id": job.id,
        "titulo": job.titulo,
        "empresa": job.empresa,
        "ubicacion": job.ubicacion,
        "created_at": job.created_at
    } for job in jobs]


@app.get("/jobs/{job_id}")
def obtener_job(job_id: int, db: Session = Depends(get_db)):
    """Obtiene un Job específico con todos sus datos"""
    job = JobRepository.get_by_id(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job no encontrado")
    
    return {
        "id": job.id,
        "titulo": job.titulo,
        "empresa": job.empresa,
        "ubicacion": job.ubicacion,
        "job_data": job.job_data,
        "created_at": job.created_at
    }


@app.get("/jobs/search/{titulo}")
def buscar_jobs(titulo: str, db: Session = Depends(get_db)):
    """Busca Jobs por título"""
    jobs = JobRepository.search_by_title(db, titulo)
    return [{
        "id": job.id,
        "titulo": job.titulo,
        "empresa": job.empresa,
        "created_at": job.created_at
    } for job in jobs]


@app.delete("/jobs/{job_id}")
def eliminar_job(job_id: int, db: Session = Depends(get_db)):
    """Elimina un Job"""
    success = JobRepository.delete(db, job_id)
    if not success:
        raise HTTPException(status_code=404, detail="Job no encontrado")
    return {"message": f"Job {job_id} eliminado"}


# ==================== ENDPOINTS DE ANÁLISIS ====================

@app.post("/analyze/{cv_id}/{job_id}")
def analizar(
    cv_id: int,
    job_id: int,
    weights: Optional[WeightsRequest] = Body(None),
    db: Session = Depends(get_db)
):
    """
    Analiza un CV vs un Job usando sus IDs.
    
    - Obtiene CV y Job de la BD
    - Ejecuta análisis con IA
    - Guarda resultado en BD
    - Retorna score y detalles
    
    **Parámetros opcionales:**
    - `weights`: Pesos personalizados para cada aspecto (0-1). Si no se envían, se usan los predeterminados.
      - experience: 0.30 (predeterminado)
      - technical_skills: 0.15 (predeterminado)
      - education: 0.15 (predeterminado)
      - responsibilities: 0.15 (predeterminado)
      - certifications: 0.10 (predeterminado)
      - soft_skills: 0.08 (predeterminado)
      - languages: 0.04 (predeterminado)
      - location: 0.03 (predeterminado)
    
    **Nota:** Si envías pesos personalizados, no es necesario enviar todos. Los que no envíes usarán el valor predeterminado.
    """
    start_time = time.time()
    
    # Obtener CV (Repository)
    cv = CVRepository.get_by_id(db, cv_id)
    if not cv:
        raise HTTPException(status_code=404, detail="CV no encontrado")
    
    # Obtener Job (Repository)
    job = JobRepository.get_by_id(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job no encontrado")
    
    try:
        # Convertir weights a dict (None si está vacío)
        weights_dict = weights.to_dict() if weights else None
        
        # Ejecutar análisis (Service)
        resultado = recommendation_service.analyze(cv.cv_data, job.job_data, weights_dict)
        
        processing_time = time.time() - start_time
        
        # Guardar análisis (Repository)
        analysis = AnalysisRepository.create(
            db=db,
            cv_id=cv_id,
            job_id=job_id,
            nombre_candidato=cv.nombre,
            titulo_trabajo=job.titulo,
            score=resultado["score"],
            score_breakdown=resultado["score_breakdown"],
            resultado_completo=resultado["resultado_completo"],
            processing_time=processing_time
        )
        
        return {
            "success": True,
            "analysis_id": analysis.id,
            "cv_id": cv_id,
            "job_id": job_id,
            "candidato": cv.nombre,
            "trabajo": job.titulo,
            "score": round(resultado["score"], 3),
            "score_porcentaje": round(resultado["score"] * 100, 1),
            "score_breakdown": resultado["score_breakdown"],
            "weights_used": resultado["resultado_completo"].get("final_score_data", {}).get("weights_used", {}),
            "processing_time": round(processing_time, 2)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/analyses")
def listar_analyses(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Lista todos los análisis realizados"""
    analyses = AnalysisRepository.get_all(db, skip, limit)
    return [{
        "id": a.id,
        "cv_id": a.cv_id,
        "job_id": a.job_id,
        "candidato": a.nombre_candidato,
        "trabajo": a.titulo_trabajo,
        "score_porcentaje": round(a.score * 100, 1),
        "created_at": a.created_at
    } for a in analyses]


@app.get("/analyses/{analysis_id}")
def obtener_analysis(analysis_id: int, db: Session = Depends(get_db)):
    """Obtiene un análisis específico con todos los detalles"""
    analysis = AnalysisRepository.get_by_id(db, analysis_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Análisis no encontrado")
    
    return {
        "id": analysis.id,
        "cv_id": analysis.cv_id,
        "job_id": analysis.job_id,
        "candidato": analysis.nombre_candidato,
        "trabajo": analysis.titulo_trabajo,
        "score": round(analysis.score, 3),
        "score_porcentaje": round(analysis.score * 100, 1),
        "score_breakdown": analysis.score_breakdown,
        "resultado_completo": analysis.resultado_completo,
        "processing_time": analysis.processing_time,
        "created_at": analysis.created_at
    }


@app.get("/cvs/{cv_id}/analyses")
def analyses_por_cv(cv_id: int, db: Session = Depends(get_db)):
    """Obtiene todos los análisis de un CV específico"""
    analyses = AnalysisRepository.get_by_cv(db, cv_id)
    return [{
        "id": a.id,
        "job_id": a.job_id,
        "trabajo": a.titulo_trabajo,
        "score_porcentaje": round(a.score * 100, 1),
        "created_at": a.created_at
    } for a in analyses]


@app.get("/jobs/{job_id}/analyses")
def analyses_por_job(job_id: int, db: Session = Depends(get_db)):
    """Obtiene todos los análisis de un Job específico"""
    analyses = AnalysisRepository.get_by_job(db, job_id)
    return [{
        "id": a.id,
        "cv_id": a.cv_id,
        "candidato": a.nombre_candidato,
        "score_porcentaje": round(a.score * 100, 1),
        "created_at": a.created_at
    } for a in analyses]


@app.get("/jobs/{job_id}/top-candidatos")
def top_candidatos(
    job_id: int,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Obtiene los mejores candidatos para un Job.
    Ordenados por score (mayor a menor).
    """
    analyses = AnalysisRepository.get_top_candidates(db, job_id, limit)
    return [{
        "rank": idx + 1,
        "analysis_id": a.id,
        "cv_id": a.cv_id,
        "candidato": a.nombre_candidato,
        "score_porcentaje": round(a.score * 100, 1),
        "created_at": a.created_at
    } for idx, a in enumerate(analyses)]


@app.get("/stats")
def estadisticas(db: Session = Depends(get_db)):
    """Estadísticas generales del sistema"""
    stats = AnalysisRepository.get_statistics(db)
    return {
        "total_cvs": stats["total_cvs"],
        "total_jobs": stats["total_jobs"],
        "total_analyses": stats["total_analyses"],
        "score_promedio": stats["average_score"],
        "score_promedio_porcentaje": round(stats["average_score"] * 100, 1)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

