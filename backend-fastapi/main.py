from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pathlib import Path

from core.database import Base, engine
from auth.router import router as auth_router
from prediction.router import router as prediction_router

MEDIA_DIR = Path(__file__).resolve().parent / "media"
MEDIA_DIR.mkdir(exist_ok=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create DB tables on startup
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Stock Prediction Portal",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve media files (charts/plots)
app.mount("/media", StaticFiles(directory=str(MEDIA_DIR)), name="media")

# Routers
app.include_router(auth_router, prefix="/api/v1")
app.include_router(prediction_router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "Stock Prediction Portal API"}
