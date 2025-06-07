from fastapi import APIRouter
from app.api.endpoints import users, game_sessions, jungle_timers, riot_api, ai_assistant

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(game_sessions.router, prefix="/game-sessions", tags=["game-sessions"])
api_router.include_router(jungle_timers.router, prefix="/jungle-timers", tags=["jungle-timers"])
api_router.include_router(riot_api.router, prefix="/riot", tags=["riot-api"])
api_router.include_router(ai_assistant.router, prefix="/ai", tags=["ai-assistant"]) 