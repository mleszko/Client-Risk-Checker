from fastapi import FastAPI

from app.api.routes.risk import router as risk_router

app = FastAPI(title="AI Risk Assessment Microservice")
app.include_router(risk_router)