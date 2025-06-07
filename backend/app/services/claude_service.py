import httpx
import json
from typing import Dict, List, Optional
from app.core.config import settings


class ClaudeAPIService:
    def __init__(self):
        self.api_key = settings.CLAUDE_API_KEY
        self.base_url = settings.CLAUDE_BASE_URL
        self.headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }

    async def _make_request(self, messages: List[Dict], system_prompt: str = None) -> Optional[str]:
        """Make request to Claude API"""
        data = {
            "model": "claude-3-5-sonnet-20241022",
            "max_tokens": 1000,
            "messages": messages
        }

        if system_prompt:
            data["system"] = system_prompt

        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/v1/messages",
                    headers=self.headers,
                    json=data
                )
                response.raise_for_status()
                result = response.json()
                return result["content"][0]["text"]
            except httpx.HTTPStatusError as e:
                return None
            except Exception as e:
                return None

    async def analyze_jungle_performance(self, match_data: Dict, user_puuid: str) -> Optional[str]:
        """Analyze jungle performance from match data"""
        player_data = None
        for participant in match_data.get("info", {}).get("participants", []):
            if participant.get("puuid") == user_puuid:
                player_data = participant
                break

        if not player_data:
            return None

        system_prompt = """Eres un coach experto de League of Legends especializado en jungla. 
        Analiza el rendimiento del jungler basándote en los datos de la partida y proporciona 
        consejos específicos y constructivos en español."""

        match_summary = {
            "champion": player_data.get("championName"),
            "position": player_data.get("teamPosition"),
            "gameResult": "Victoria" if player_data.get("win") else "Derrota",
            "kda": f"{player_data.get('kills', 0)}/{player_data.get('deaths', 0)}/{player_data.get('assists', 0)}",
            "cs": player_data.get("totalMinionsKilled", 0),
            "jungleCS": player_data.get("neutralMinionsKilled", 0),
            "visionScore": player_data.get("visionScore", 0),
            "gameDuration": match_data.get("info", {}).get("gameDuration", 0) // 60,
            "dragons": player_data.get("dragonKills", 0),
            "barons": player_data.get("baronKills", 0),
            "objectives": player_data.get("objectivesStolen", 0),
        }

        messages = [
            {
                "role": "user",
                "content": f"""Analiza esta partida de jungla:

Champion: {match_summary['champion']}
Resultado: {match_summary['gameResult']}
KDA: {match_summary['kda']}
CS Total: {match_summary['cs']}
CS de Jungla: {match_summary['jungleCS']}
Vision Score: {match_summary['visionScore']}
Duración: {match_summary['gameDuration']} minutos
Dragones: {match_summary['dragons']}
Barones: {match_summary['barons']}

Proporciona un análisis detallado con:
1. Aspectos positivos del rendimiento
2. Áreas de mejora específicas
3. Consejos prácticos para la próxima partida
4. Una calificación del 1-10 y por qué

Mantén el análisis constructivo y enfocado en mejorar."""
            }
        ]

        return await self._make_request(messages, system_prompt)

    async def get_jungle_suggestions(self, game_state: Dict) -> Optional[str]:
        """Get real-time jungle suggestions based on game state"""
        system_prompt = """Eres un asistente de jungla experto que da consejos en tiempo real. 
        Proporciona sugerencias específicas y accionables basadas en el estado actual del juego."""

        messages = [
            {
                "role": "user",
                "content": f"""Estado actual del juego:

Tiempo de juego: {game_state.get('gameTime', 0)} minutos
Champion: {game_state.get('champion', 'Desconocido')}
Nivel: {game_state.get('level', 1)}
Oro: {game_state.get('gold', 0)}
Objetivos disponibles: {', '.join(game_state.get('availableObjectives', []))}
Estado del equipo: {game_state.get('teamState', 'Neutro')}

Dame 3 sugerencias específicas para los próximos 2-3 minutos de juego. 
Sé conciso y enfócate en acciones concretas."""
            }
        ]

        return await self._make_request(messages, system_prompt)

    async def recommend_jungle_champions(self, user_preferences: Dict, enemy_team: List[str] = None) -> Optional[str]:
        """Recommend jungle champions based on user preferences and enemy team"""
        system_prompt = """Eres un experto en meta de League of Legends y selección de campeones. 
        Recomienda campeones de jungla basándote en las preferencias del usuario y la composición enemiga."""

        enemy_info = f"\nEquipo enemigo: {', '.join(enemy_team)}" if enemy_team else ""

        messages = [
            {
                "role": "user",
                "content": f"""Preferencias del usuario:

Estilo de juego preferido: {user_preferences.get('playstyle', 'Balanceado')}
Campeones favoritos: {user_preferences.get('favoriteChampions', 'Ninguno especificado')}
Rango actual: {user_preferences.get('rank', 'No especificado')}
Objetivo: {user_preferences.get('goal', 'Mejorar en general')}{enemy_info}

Recomienda 3 campeones de jungla con:
1. Por qué es una buena elección
2. Estilo de juego sugerido
3. Objetivo principal en early/mid/late game

Mantén las recomendaciones actualizadas con el meta actual."""
            }
        ]

        return await self._make_request(messages, system_prompt)

    async def analyze_jungle_pathing(self, match_data: Dict, user_puuid: str) -> Optional[str]:
        """Analyze jungle pathing efficiency"""
        system_prompt = """Eres un coach experto en pathing de jungla. Analiza la eficiencia 
        del recorrido de jungla y proporciona consejos específicos para optimizar el claro."""

        player_data = None
        for participant in match_data.get("info", {}).get("participants", []):
            if participant.get("puuid") == user_puuid:
                player_data = participant
                break

        if not player_data:
            return None

        cs_per_min = player_data.get("neutralMinionsKilled", 0) / (
                    match_data.get("info", {}).get("gameDuration", 1) / 60)

        messages = [
            {
                "role": "user",
                "content": f"""Analiza la eficiencia de jungla:

Champion: {player_data.get('championName')}
CS de jungla: {player_data.get('neutralMinionsKilled', 0)}
CS por minuto: {cs_per_min:.1f}
Duración de partida: {match_data.get("info", {}).get("gameDuration", 0) // 60} minutos
Nivel final: {player_data.get('champLevel', 0)}

Proporciona consejos específicos sobre:
1. Eficiencia del claro de jungla
2. Pathing recomendado para este campeón
3. Timing óptimo para objetivos
4. Balance entre farmeo y gankeo"""
            }
        ]

        return await self._make_request(messages, system_prompt)


# Singleton instance
claude_service = ClaudeAPIService()