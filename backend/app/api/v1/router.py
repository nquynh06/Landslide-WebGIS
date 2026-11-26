from fastapi import APIRouter

from app.api.v1.endpoints import alerts, health, landslide_events, layers, rainfall, study_areas, susceptibility_maps

router = APIRouter()
for module in (health, study_areas, layers, susceptibility_maps, landslide_events, rainfall, alerts):
    router.include_router(module.router)
