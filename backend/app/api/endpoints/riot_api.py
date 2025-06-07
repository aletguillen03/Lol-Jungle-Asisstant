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
async def get_summoner_by_puuid(puuid: str, region: str = "la1") -> Dict:
    """Get summoner details by PUUID"""
    summoner_data = await riot_service.get_summoner_by_puuid(puuid, region)

    if not summoner_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Summoner not found"
        )

    return summoner_data


@router.get("/summoner/complete/{riot_id}/{tag_line}")
async def get_complete_summoner_info(
        riot_id: str,
        tag_line: str,
        region: str = "las"
) -> Dict:
    """Get complete summoner information including rank and recent matches"""

    try:
        complete_data = await riot_service.get_complete_summoner_info(riot_id, tag_line, region)

        if not complete_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Summoner not found or incomplete data"
            )

        # Procesar datos de ranked
        rank_info = None
        if complete_data.get("rank"):
            for queue in complete_data["rank"]:
                if queue.get("queueType") == "RANKED_SOLO_5x5":
                    rank_info = {
                        "tier": queue.get("tier"),
                        "rank": queue.get("rank"),
                        "leaguePoints": queue.get("leaguePoints", 0),
                        "wins": queue.get("wins", 0),
                        "losses": queue.get("losses", 0),
                        "winrate": round(
                            (queue.get("wins", 0) / max(queue.get("wins", 0) + queue.get("losses", 0), 1)) * 100, 1)
                    }
                    break

        return {
            "riot_id": riot_id,
            "tag_line": tag_line,
            "puuid": complete_data["account"]["puuid"],
            "summoner_level": complete_data["summoner"]["summonerLevel"] if complete_data.get("summoner") else None,
            "profile_icon_id": complete_data["summoner"]["profileIconId"] if complete_data.get("summoner") else None,
            "rank": rank_info,
            "recent_matches_count": len(complete_data.get("recent_matches", [])),
            "recent_match_ids": complete_data.get("recent_matches", [])[:10]
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting complete summoner info: {str(e)}"
        )


@router.get("/rank/{summoner_id}")
async def get_rank_info(summoner_id: str, region: str = "la1") -> List[Dict]:
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