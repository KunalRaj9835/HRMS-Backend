from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.employees import router as employee_router
from app.attendance import router as attendance_router
from app.config import settings


app = FastAPI(title=settings.API_TITLE, version=settings.API_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(employee_router)
app.include_router(attendance_router)

@app.get("/")
def health():
    return {"status": "OK", "message": "HRMS Lite API is running"}