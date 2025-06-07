import httpx
from typing import Dict, Optional, List
from app.core.config import settings


class RiotAPIService:
    def __init__(self):
        self.api_key = settings.RIOT_API_KEY
        self.region_config = {
            "las": {
                "platform": "la1",
                "regional": "americas"
            }
        }
        self.headers = {
            "X-Riot-Token": self.api_key
        }

    def get_platform_url(self, region: str = "las") -> str:
        platform = self.region_config.get(region, {}).get("platform", "la1")
        return f"https://{platform}.api.riotgames.com"

    def get_regional_url(self, region: str = "las") -> str:
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
        # Ensure PUUID is properly formatted (no extra characters)
        clean_puuid = puuid.strip()
        url = f"{self.get_platform_url(region)}/lol/summoner/v4/summoners/by-puuid/{clean_puuid}"

        print(f"🔍 Requesting summoner data from: {url}")
        print(f"🆔 PUUID length: {len(clean_puuid)}")

        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.get(url, headers=self.headers)
                print(f"📊 Response status: {response.status_code}")

                if response.status_code == 404:
                    print("⚠️ 404 Error - This might be due to:")
                    print("   1. PUUID format issue")
                    print("   2. Account not found on LAS platform")
                    print("   3. API rate limiting")
                    print(f"   4. PUUID: {clean_puuid}")
                    return None

                response.raise_for_status()
                data = response.json()
                print(f"✅ Summoner data retrieved successfully")
                return data

            except httpx.HTTPStatusError as e:
                print(f"❌ HTTP Error getting summoner by PUUID: {e}")
                print(f"📋 Response text: {e.response.text if e.response else 'No response'}")
                return None
            except Exception as e:
                print(f"❌ Unexpected error: {e}")
                return None

    async def get_rank_info(self, summoner_id: str, region: str = "las") -> Optional[List[Dict]]:
        """Get ranked information for a summoner in LAS"""
        url = f"{self.get_platform_url(region)}/lol/league/v4/entries/by-summoner/{summoner_id}"

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=self.headers)
                response.raise_for_status()
                rank_data = response.json()
                print(f"✅ Rank data retrieved: {rank_data}")  # Debug
                return rank_data
            except httpx.HTTPStatusError as e:
                print(f"Error getting rank info: {e}")
                return None

    async def get_recent_matches(self, puuid: str, count: int = 20, region: str = "las") -> Optional[List[str]]:
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
                matches = response.json()
                print(f"✅ Found {len(matches)} recent matches")  # Debug
                return matches
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
                    return None
                print(f"Error getting current game: {e}")
                return None

    async def get_complete_summoner_info(self, riot_id: str, tag_line: str, region: str = "las") -> Optional[Dict]:
        """Get complete summoner information including rank"""
        try:
            # 1. Get account info (PUUID)
            account_data = await self.get_summoner_by_riot_id(riot_id, tag_line, region)
            if not account_data:
                return None

            puuid = account_data.get("puuid")

            # 2. Get summoner details (ID, level, etc.)
            summoner_data = await self.get_summoner_by_puuid(puuid, region)
            if not summoner_data:
                return None

            summoner_id = summoner_data.get("id")

            # 3. Get rank information
            rank_data = await self.get_rank_info(summoner_id, region)

            # 4. Get recent matches
            recent_matches = await self.get_recent_matches(puuid, 20, region)

            # 5. Combine all data
            complete_info = {
                "account": account_data,
                "summoner": summoner_data,
                "rank": rank_data,
                "recent_matches": recent_matches or []
            }

            return complete_info

        except Exception as e:
            print(f"Error getting complete summoner info: {e}")
            return None


# Singleton instance
riot_service = RiotAPIService()