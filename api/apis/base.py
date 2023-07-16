from fastapi import APIRouter

from apis.v1 import (
    route_character,
    route_encounter,
    route_gear,
    route_monster,
    route_power,
    route_store,
    route_user,
    route_weapon,
)

api_router = APIRouter()
api_router.include_router(route_character.router, prefix="/api", tags=["characters"])
api_router.include_router(route_encounter.router, prefix="/api", tags=["encounter"])
api_router.include_router(route_gear.router, prefix="/api", tags=["gear"])
api_router.include_router(route_monster.router, prefix="/api", tags=["monster"])
api_router.include_router(route_power.router, prefix="/api", tags=["powers"])
api_router.include_router(route_store.router, prefix="/api", tags=["store"])
api_router.include_router(route_user.router, prefix="/api", tags=["users"])
api_router.include_router(route_weapon.router, prefix="/api", tags=["weapons"])
