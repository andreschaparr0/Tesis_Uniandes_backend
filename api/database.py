"""
Configuración de base de datos y modelos.
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Configuración SQLite
DATABASE_URL = "sqlite:///./cv_system.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# ==================== MODELOS ====================

class CV(Base):
    """Modelo para CVs procesados"""
    __tablename__ = "cvs"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    email = Column(String)
    telefono = Column(String)
    ubicacion = Column(String)
    cv_data = Column(JSON)  # CV completo estructurado
    created_at = Column(DateTime, default=datetime.utcnow)


class JobDescription(Base):
    """Modelo para descripciones de trabajo"""
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True)
    empresa = Column(String)
    ubicacion = Column(String)
    job_data = Column(JSON)  # Job completo estructurado
    created_at = Column(DateTime, default=datetime.utcnow)


class Analysis(Base):
    """Modelo para análisis/comparaciones"""
    __tablename__ = "analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    cv_id = Column(Integer, index=True)
    job_id = Column(Integer, index=True)
    nombre_candidato = Column(String)
    titulo_trabajo = Column(String)
    score = Column(Float)
    score_breakdown = Column(JSON)  # Desglose del score
    resultado_completo = Column(JSON)  # Resultado detallado
    processing_time = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)


# ==================== FUNCIONES AUXILIARES ====================

def init_db():
    """Inicializa la base de datos"""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Dependency para obtener sesión de BD"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

