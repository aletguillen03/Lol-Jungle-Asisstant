from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, List, Optional
from pydantic import BaseModel
from datetime import datetime, timedelta
from app.database import get_db
from app.services.riot_service import riot_service
from app.services.claude_service import claude_service
from app.models.user import User
from app.models.game_session import GameSession
from app.models.jungle_timer import JungleTimer

router = APIRouter()

# Schemas específicos para junglers
class ObjectiveTimer(BaseModel):
    objective_type: str  # "dragon", "baron", "herald", "gromp", etc.
    objective_name: str  # "Ocean Dragon", "Baron Nashor", etc.
    spawn_time: datetime
    respawn_seconds: int
    team_side: str  # "blue", "red", "neutral"

class JunglePathSuggestion(BaseModel):
    champion: str
    enemy_jungle: Optional[str] = None
    game_time: int  # minutes
    team_state: str  # "ahead", "behind", "even"

class LiveGameTracking(BaseModel):
    summoner_id: str
    region: str = "las"

@router.get("/objectives-timers")
async def get_objective_timers(db: Session = Depends(get_db)):
    """Get standard jungle objective timers"""
    
    # Timers estándar de League of Legends (Season 14)
    standard_timers = {
        "dragons": {
            "first_spawn": 300,  # 5:00
            "respawn_time": 300,  # 5 minutes
            "types": ["Ocean", "Mountain", "Cloud", "Infernal", "Hextech", "Chemtech"]
        },
        "baron": {
            "first_spawn": 1200,  # 20:00
            "respawn_time": 360   # 6 minutes
        },
        "herald": {
            "first_spawn": 480,   # 8:00
            "despawn_time": 1140, # 19:00 (despawns when Baron spawns)
            "respawn_time": 360   # 6 minutes
        },
        "jungle_camps": {
            "krugs": {"respawn": 135},      # 2:15
            "gromp": {"respawn": 135},      # 2:15
            "wolves": {"respawn": 135},     # 2:15
            "raptors": {"respawn": 135},    # 2:15
            "red_buff": {"respawn": 300},   # 5:00
            "blue_buff": {"respawn": 300},  # 5:00
            "scuttle": {"respawn": 150}     # 2:30
        }
    }
    
    return {
        "timers": standard_timers,
        "season": "14",
        "patch": "14.24",
        "last_updated": datetime.now().isoformat()
    }

@router.post("/start-timer")
async def start_objective_timer(
    timer_data: ObjectiveTimer,
    session_id: int,
    db: Session = Depends(get_db)
):
    """Start a new objective timer"""
    
    # Verificar que la sesión existe
    game_session = db.query(GameSession).filter(GameSession.id == session_id).first()
    if not game_session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game session not found"
        )
    
    # Calcular tiempo de respawn
    respawn_time = timer_data.spawn_time + timedelta(seconds=timer_data.respawn_seconds)
    
    # Crear nuevo timer
    new_timer = JungleTimer(
        game_session_id=session_id,
        objective_type=timer_data.objective_type,
        objective_name=timer_data.objective_name,
        spawn_time=timer_data.spawn_time,
        respawn_time=respawn_time,
        game_time_minutes=int((timer_data.spawn_time.timestamp() - game_session.started_at.timestamp()) / 60),
        is_active=True
    )
    
    db.add(new_timer)
    db.commit()
    db.refresh(new_timer)
    
    return {
        "timer": new_timer,
        "message": f"Timer iniciado para {timer_data.objective_name}",
        "respawn_at": respawn_time.isoformat()
    }

@router.get("/jungle-path-suggestions")
async def get_jungle_path_suggestions(
    champion: str,
    game_time: int = 0,
    enemy_jungle: Optional[str] = None,
    team_state: str = "even",
    db: Session = Depends(get_db)
):
    """Get AI-powered jungle pathing suggestions"""
    
    try:
        # Preparar contexto para Claude
        path_context = {
            "champion": champion,
            "enemyJungle": enemy_jungle,
            "gameTime": game_time,
            "teamState": team_state
        }
        
        # Obtener sugerencias de Claude
        suggestions = await claude_service.get_jungle_suggestions(path_context)
        
        # Pathing básico por defecto si Claude no está disponible
        if not suggestions:
            basic_suggestions = get_basic_jungle_path(champion, game_time)
            return {
                "suggestions": basic_suggestions,
                "source": "basic_algorithm",
                "context": path_context
            }
        
        return {
            "suggestions": suggestions,
            "source": "claude_ai",
            "context": path_context,
            "generated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting jungle suggestions: {str(e)}"
        )

@router.get("/live-game/{riot_id}/{tag_line}")
async def track_live_game(
    riot_id: str,
    tag_line: str,
    region: str = "las",
    db: Session = Depends(get_db)
):
    """Track live game for jungle analysis"""
    
    try:
        # Obtener información del summoner
        summoner_data = await riot_service.get_summoner_by_riot_id(riot_id, tag_line, region)
        if not summoner_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Summoner not found"
            )
        
        # Obtener detalles del summoner para tener el ID
        puuid = summoner_data.get("puuid")
        summoner_details = await riot_service.get_summoner_by_puuid(puuid, region)
        
        if not summoner_details:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Summoner details not found"
            )
        
        summoner_id = summoner_details.get("id")
        
        # Verificar si hay una partida activa
        current_game = await riot_service.get_current_game(summoner_id, region)
        
        if not current_game:
            return {
                "in_game": False,
                "message": "No hay partida activa",
                "summoner": summoner_data
            }
        
        # Extraer información relevante de la partida
        game_info = {
            "gameId": current_game.get("gameId"),
            "gameMode": current_game.get("gameMode"),
            "gameLength": current_game.get("gameLength"),  # en segundos
            "participants": []
        }
        
        # Encontrar al jugador y extraer información relevante
        player_info = None
        for participant in current_game.get("participants", []):
            if participant.get("puuid") == puuid:
                player_info = {
                    "championId": participant.get("championId"),
                    "spell1Id": participant.get("spell1Id"),
                    "spell2Id": participant.get("spell2Id"),
                    "teamId": participant.get("teamId")
                }
            
            game_info["participants"].append({
                "championId": participant.get("championId"),
                "teamId": participant.get("teamId"),
                "puuid": participant.get("puuid") == puuid  # Mark if it's our player
            })
        
        return {
            "in_game": True,
            "game_info": game_info,
            "player_info": player_info,
            "game_time_minutes": current_game.get("gameLength", 0) // 60,
            "tracking_started": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error tracking live game: {str(e)}"
        )

@router.get("/champion-stats/{champion_name}")
async def get_jungle_champion_stats(
    champion_name: str,
    region: str = "las",
    db: Session = Depends(get_db)
):
    """Get jungle-specific stats for a champion"""
    
    # Stats básicos de jungla por campeón (podrías expandir esto con una API de stats)
    jungle_stats = {
        "graves": {
            "clear_speed": "A+",
            "gank_potential": "B",
            "scaling": "A",
            "difficulty": "Medium",
            "recommended_build": ["Warrior", "Berserker's Greaves", "The Collector"],
            "optimal_runes": "Fleet Footwork"
        },
        "kindred": {
            "clear_speed": "B+",
            "gank_potential": "A",
            "scaling": "S",
            "difficulty": "Hard",
            "recommended_build": ["Kraken Slayer", "Berserker's Greaves", "Runaan's Hurricane"],
            "optimal_runes": "Press the Attack"
        },
        "kha'zix": {
            "clear_speed": "B",
            "gank_potential": "A+",
            "scaling": "A",
            "difficulty": "Medium",
            "recommended_build": ["Duskblade", "Ionian Boots", "Youmuu's Ghostblade"],
            "optimal_runes": "Dark Harvest"
        }
    }
    
    champion_key = champion_name.lower().replace("'", "").replace(" ", "")
    stats = jungle_stats.get(champion_key, {
        "clear_speed": "Unknown",
        "gank_potential": "Unknown", 
        "scaling": "Unknown",
        "difficulty": "Unknown",
        "recommended_build": [],
        "optimal_runes": "Unknown"
    })
    
    return {
        "champion": champion_name,
        "jungle_stats": stats,
        "region": region,
        "meta_tier": "A",  # Podrías conectar esto con APIs de meta
        "last_updated": datetime.now().isoformat()
    }

def get_basic_jungle_path(champion: str, game_time: int) -> str:
    """Fallback basic jungle pathing algorithm"""
    
    if game_time <= 5:
        return f"Early game con {champion}: Inicia en el buff de tu lado → campamentos pequeños → Scuttle crab a los 3:15"
    elif game_time <= 15:
        return f"Mid game: Prioriza objetivos y gankeos. Con {champion} busca oportunidades de counterjungle"
    else:
        return f"Late game: Acompaña al equipo y controla visión alrededor de Baron/Dragon"