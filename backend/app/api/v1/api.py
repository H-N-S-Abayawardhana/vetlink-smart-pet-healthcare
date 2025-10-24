from fastapi import APIRouter
from app.api.v1.endpoints import auth, appointments, users, veterinarians, profile

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(appointments.router, prefix="/appointments", tags=["appointments"])
api_router.include_router(users.router, prefix="/admin/users", tags=["admin"])
api_router.include_router(veterinarians.router, prefix="/veterinarians", tags=["veterinarians"])
api_router.include_router(profile.router, prefix="/profile", tags=["profile"])

