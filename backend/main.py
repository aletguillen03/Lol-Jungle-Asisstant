from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
from app.database import init_db
from app.api.routes import api_router
from app.core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_db()
    yield
    # Shutdown
    pass

app = FastAPI(
    title="LoL Jungle Assistant API",
    description="API para asistir a junglers de League of Legends en tiempo real",
    version="1.0.0",
    lifespan=lifespan
)

# Configurar CORS - usar la propiedad corregida
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,  # Usar la nueva propiedad
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "LoL Jungle Assistant API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )