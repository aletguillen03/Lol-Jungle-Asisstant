from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, List, Optional
from pydantic import BaseModel
from app.database import get_db
from app.services.claude_service import claude_service
from app.services.riot_service import riot_service

router = APIRouter()

# Schemas para requests
class GameAnalysisRequest(BaseModel):
    match_id: str
    user_puuid: str
    region: str = "las"

class JungleSuggestionsRequest(BaseModel):
    game_time: int  # in minutes
    champion: str
    level: int
    gold: int
    available_objectives: List[str]
    team_state: str  # "ahead", "behind", "even"

class ChampionRecommendationRequest(BaseModel):
    playstyle: str  # "aggressive", "supportive", "farming", "balanced"
    favorite_champions: List[str]
    rank: str
    goal: str
    enemy_team: Optional[List[str]] = None

class PathingAnalysisRequest(BaseModel):
    match_id: str
    user_puuid: str
    region: str = "las"

@router.post("/analyze-game")
async def analyze_game_performance(
    request: GameAnalysisRequest,
    db: Session = Depends(get_db)
):
    """Analyze game performance using Claude AI"""
    try:
        # Get match details from Riot API
        match_data = await riot_service.get_match_details(request.match_id, request.region)
        
        if not match_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Match not found"
            )
        
        # Analyze with Claude
        analysis = await claude_service.analyze_jungle_performance(match_data, request.user_puuid)
        
        if not analysis:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to generate analysis"
            )
        
        return {
            "match_id": request.match_id,
            "analysis": analysis,
            "timestamp": match_data.get("info", {}).get("gameCreation")
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing game: {str(e)}"
        )

@router.post("/jungle-suggestions")
async def get_jungle_suggestions(
    request: JungleSuggestionsRequest,
    db: Session = Depends(get_db)
):
    """Get AI-powered real-time jungle suggestions"""
    try:
        game_state = {
            "gameTime": request.game_time,
            "champion": request.champion,
            "level": request.level,
            "gold": request.gold,
            "availableObjectives": request.available_objectives,
            "teamState": request.team_state
        }
        
        suggestions = await claude_service.get_jungle_suggestions(game_state)
        
        if not suggestions:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to generate suggestions"
            )
        
        return {
            "suggestions": suggestions,
            "game_state": game_state,
            "generated_at": request.game_time
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting suggestions: {str(e)}"
        )

@router.post("/champion-recommendations")
async def get_champion_recommendations(
    request: ChampionRecommendationRequest,
    db: Session = Depends(get_db)
):
    """Get AI champion recommendations"""
    try:
        user_preferences = {
            "playstyle": request.playstyle,
            "favoriteChampions": request.favorite_champions,
            "rank": request.rank,
            "goal": request.goal
        }
        
        recommendations = await claude_service.recommend_jungle_champions(
            user_preferences, 
            request.enemy_team
        )
        
        if not recommendations:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to generate recommendations"
            )
        
        return {
            "recommendations": recommendations,
            "user_preferences": user_preferences,
            "enemy_team": request.enemy_team
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting recommendations: {str(e)}"
        )

@router.post("/analyze-pathing")
async def analyze_jungle_pathing(
    request: PathingAnalysisRequest,
    db: Session = Depends(get_db)
):
    """Analyze jungle pathing efficiency"""
    try:
        # Get match details from Riot API
        match_data = await riot_service.get_match_details(request.match_id, request.region)
        
        if not match_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Match not found"
            )
        
        # Analyze pathing with Claude
        analysis = await claude_service.analyze_jungle_pathing(match_data, request.user_puuid)
        
        if not analysis:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to generate pathing analysis"
            )
        
        return {
            "match_id": request.match_id,
            "pathing_analysis": analysis,
            "timestamp": match_data.get("info", {}).get("gameCreation")
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing pathing: {str(e)}"
        )

@router.get("/health")
async def check_ai_service_health():
    """Check if AI services are working"""
    try:
        # Test basic Claude API connectivity
        test_messages = [{"role": "user", "content": "Responde solo 'OK' para confirmar conectividad."}]
        response = await claude_service._make_request(test_messages)
        
        return {
            "claude_api": "connected" if response else "error",
            "status": "healthy" if response else "degraded"
        }
    except Exception as e:
        return {
            "claude_api": "error", 
            "status": "error",
            "error": str(e)
        }