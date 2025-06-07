import httpx
from typing import Dict, Optional, List
from app.core.config import settings

class RiotAPIService:
    def __init__(self):
        self.api_key = settings.RIOT_API_KEY
        # Configuración específica para LAS
        self.region_config = {
            "las": {
                "platform": "la1",  # Para APIs de plataforma (summoner, league, etc.)
                "regional": "americas"  # Para APIs regionales (account, match)
            }
        }
        self.headers = {
            "X-Riot-Token": self.api_key
        }
    
    def get_platform_url(self, region: str = "las") -> str:
        """Get platform URL for LAS region"""
        platform = self.region_config.get(region, {}).get("platform", "la1")
        return f"https://{platform}.api.riotgames.com"
    
    def get_regional_url(self, region: str = "las") -> str:
        """Get regional URL for LAS region"""
        regional = self.region_config.get(region, {}).get("regional", "americas")
        return f"https://{regional}.api.riotgames.com"
    
    async def get_summoner_by_riot_id(self, riot_id: str, tag_line: str, region: str = "las") -> Optional[Dict]:
        """Get summoner information by Riot ID for LAS region"""
        url = f"{self.get_regional_url(region)}/riot/account/v1/accounts/by-riot-id/{riot_id}/{tag_line}"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=self.headers)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                print(f"Error getting summoner: {e}")
                if e.response.status_code == 404:
                    return None
                raise e
    
    async def get_summoner_by_puuid(self, puuid: str, region: str = "las") -> Optional[Dict]:
        """Get summoner details by PUUID for LAS region"""
        url = f"{self.get_platform_url(region)}/lol/summoner/v4/summoners/by-puuid/{puuid}"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=self.headers)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                print(f"Error getting summoner by PUUID: {e}")
                return None
    
    async def get_rank_info(self, summoner_id: str, region: str = "las") -> Optional[List[Dict]]:
        """Get ranked information for a summoner in LAS"""
        url = f"{self.get_platform_url(region)}/lol/league/v4/entries/by-summoner/{summoner_id}"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=self.headers)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                print(f"Error getting rank info: {e}")
                return None
    
    async def get_recent_matches(self, puuid: str, count: int = 10, region: str = "las") -> Optional[List[str]]:
        """Get recent match IDs for a player in LAS"""
        url = f"{self.get_regional_url(region)}/lol/match/v5/matches/by-puuid/{puuid}/ids"
        params = {
            "count": count,
            "queue": 420  # Solo ranked solo/duo
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=self.headers, params=params)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                print(f"Error getting recent matches: {e}")
                return None
    
    async def get_match_details(self, match_id: str, region: str = "las") -> Optional[Dict]:
        """Get detailed match information for LAS"""
        url = f"{self.get_regional_url(region)}/lol/match/v5/matches/{match_id}"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=self.headers)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                print(f"Error getting match details: {e}")
                return None
    
    async def get_current_game(self, summoner_id: str, region: str = "las") -> Optional[Dict]:
        """Get current game information for active game tracking"""
        url = f"{self.get_platform_url(region)}/lol/spectator/v4/active-games/by-summoner/{summoner_id}"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=self.headers)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    return None  # No active game
                print(f"Error getting current game: {e}")
                return None

# Singleton instance
riot_service = RiotAPIService()