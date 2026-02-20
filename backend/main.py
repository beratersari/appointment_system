from fastapi import FastAPI

from backend.api.controllers.appointment_controller import router as appointment_router
from backend.api.controllers.auth_controller import router as auth_router
from backend.api.controllers.offering_controller import router as offering_router
from backend.business.services.auth_service import AuthService
from backend.data_access.db_context import initialize_database

app = FastAPI(
    title="Appointment System API",
    description="A multi-tenant appointment management system with role-based access",
    version="1.0.0",
)

app.include_router(auth_router)
app.include_router(offering_router)
app.include_router(appointment_router)


@app.on_event("startup")
def on_startup() -> None:
    initialize_database()
    auth_service = AuthService()
    auth_service.seed_default_admin()


@app.get("/health")
def health_check() -> dict:
    return {"status": "healthy"}
