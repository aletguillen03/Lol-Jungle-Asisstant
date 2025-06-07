from fastapi import APIRouter, HTTPException, status
from typing import Dict, List, Optional
from app.services.riot_service import riot_service

router = APIRouter()

@router.get("/summoner/{riot_id}/{tag_line}")
async def get_summoner(riot_id: str, tag_line: str, region: str = "americas") -> Dict:
    """Get summoner information by Riot ID"""
    summoner_data = await riot_service.get_summoner_by_riot_id(riot_id, tag_line, region)
    
    if not summoner_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Summoner not found"
        )
    
    return summoner_data

@router.get("/summoner/puuid/{puuid}")
async def get_summoner_by_puuid(puuid: str, region: str = "na1") -> Dict:
    """Get summoner details by PUUID"""
    summoner_data = await riot_service.get_summoner_by_puuid(puuid, region)
    
    if not summoner_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Summoner not found"
        )
    
    return summoner_data

@router.get("/rank/{summoner_id}")
async def get_rank_info(summoner_id: str, region: str = "na1") -> List[Dict]:
    """Get ranked information for a summoner"""
    rank_data = await riot_service.get_rank_info(summoner_id, region)
    
    if not rank_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rank information not found"
        )
    
    return rank_data

@router.get("/matches/{puuid}")
async def get_recent_matches(puuid: str, count: int = 10, region: str = "americas") -> List[str]:
    """Get recent match IDs for a player"""
    matches = await riot_service.get_recent_matches(puuid, count, region)
    
    if not matches:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No matches found"
        )
    
    return matches

@router.get("/match/{match_id}")
async def get_match_details(match_id: str, region: str = "americas") -> Dict:
    """Get detailed match information"""
    match_data = await riot_service.get_match_details(match_id, region)
    
    if not match_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Match not found"
        )
    
    return match_data 