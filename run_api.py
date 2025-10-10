"""
Script para ejecutar la API.
"""

import uvicorn

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 CV Recommendation API")
    print("=" * 60)
    print("\n📐 Arquitectura: Services + Repositories + Database")
    print("📚 Documentación: http://localhost:8000/docs")
    print("💡 Presiona Ctrl+C para detener\n")
    print("=" * 60)
    
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

