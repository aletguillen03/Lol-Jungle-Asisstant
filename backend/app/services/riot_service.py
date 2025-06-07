import httpx
from typing import Dict, Optional
from app.core.config import settings

class RiotAPIService:
    def __init__(self):
        self.api_key = settings.RIOT_API_KEY
        self.base_url = settings.RIOT_BASE_URL
        self.headers = {
            "X-Riot-Token": self.api_key
        }
    
    async def get_summoner_by_riot_id(self, riot_id: str, tag_line: str, region: str = "americas") -> Optional[Dict]:
        """Get summoner information by Riot ID"""
        url = f"{self.base_url}/riot/account/v1/accounts/by-riot-id/{riot_id}/{tag_line}"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=self.headers)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                print(f"Error getting summoner: {e}")
                return None
    
    async def get_summoner_by_puuid(self, puuid: str, region: str = "na1") -> Optional[Dict]:
        """Get summoner details by PUUID"""
        region_url = f"https://{region}.api.riotgames.com"
        url = f"{region_url}/lol/summoner/v4/summoners/by-puuid/{puuid}"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=self.headers)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                print(f"Error getting summoner by PUUID: {e}")
                return None
    
    async def get_rank_info(self, summoner_id: str, region: str = "na1") -> Optional[Dict]:
        """Get ranked information for a summoner"""
        region_url = f"https://{region}.api.riotgames.com"
        url = f"{region_url}/lol/league/v4/entries/by-summoner/{summoner_id}"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=self.headers)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                print(f"Error getting rank info: {e}")
                return None
    
    async def get_recent_matches(self, puuid: str, count: int = 10, region: str = "americas") -> Optional[list]:
        """Get recent match IDs for a player"""
        url = f"{self.base_url}/lol/match/v5/matches/by-puuid/{puuid}/ids"
        params = {"count": count}
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=self.headers, params=params)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                print(f"Error getting recent matches: {e}")
                return None
    
    async def get_match_details(self, match_id: str, region: str = "americas") -> Optional[Dict]:
        """Get detailed match information"""
        url = f"{self.base_url}/lol/match/v5/matches/{match_id}"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=self.headers)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                print(f"Error getting match details: {e}")
                return None

# Singleton instance
riot_service = RiotAPIService() 