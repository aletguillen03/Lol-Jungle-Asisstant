import asyncio
import sys
import os
from pathlib import Path

current_dir = Path(__file__).parent
backend_path = current_dir / "backend"
sys.path.append(str(backend_path))

env_path = current_dir / "backend" / ".env"
if env_path.exists():
    with open(env_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key] = value

try:
    from app.database import init_db, SessionLocal
    from app.models.user import User

    DB_AVAILABLE = True
except Exception as e:
    DB_AVAILABLE = False


async def test_riot_api():
    print("🔍 Probando Riot Games API...")

    riot_key = os.getenv('RIOT_API_KEY')
    if not riot_key:
        print("❌ RIOT_API_KEY no configurada")
        return False

    print(f"🔑 Usando API Key: {riot_key[:10]}...")

    try:
        import httpx
        headers = {"X-Riot-Token": riot_key}
        url = "https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/Not%20Alet/JCP"

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)

            if response.status_code == 200:
                summoner_data = response.json()
                print(f"✅ Riot API conectada correctamente")
                print(f"   📋 Summoner: {summoner_data.get('gameName')}#{summoner_data.get('tagLine')}")
                print(f"   🆔 PUUID: {summoner_data.get('puuid')[:20]}...")

                puuid = summoner_data.get('puuid')
                platform_url = f"https://la1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}"

                response = await client.get(platform_url, headers=headers)
                if response.status_code == 200:
                    summoner_details = response.json()
                    print(f"   📊 Nivel: {summoner_details.get('summonerLevel')}")

                    matches_url = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?count=3"
                    response = await client.get(matches_url, headers=headers)
                    if response.status_code == 200:
                        recent_matches = response.json()
                        print(f"   🎮 Últimas partidas encontradas: {len(recent_matches)}")
                    else:
                        print("   ⚠️  No se encontraron partidas recientes")
                else:
                    print("   ⚠️  No se pudieron obtener detalles del summoner")

                return True
            else:
                print(f"❌ Error {response.status_code}: {response.text}")
                return False

    except Exception as e:
        print(f"❌ Error conectando con Riot API: {e}")
        return False


async def test_claude_api():
    print("\n🤖 Probando Claude API...")

    claude_key = os.getenv('CLAUDE_API_KEY')
    if not claude_key:
        print("❌ CLAUDE_API_KEY no configurada")
        return False

    print(f"🔑 Usando API Key: {claude_key[:20]}...")

    try:
        import httpx

        headers = {
            "x-api-key": claude_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }

        data = {
            "model": "claude-3-5-sonnet-20241022",
            "max_tokens": 50,
            "messages": [{"role": "user", "content": "Responde solo 'OK' si me puedes escuchar."}]
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=data
            )

            if response.status_code == 200:
                result = response.json()
                response_text = result.get('content', [{}])[0].get('text', 'Sin respuesta')
                print(f"✅ Claude API conectada correctamente")
                print(f"   📝 Respuesta de prueba: {response_text}")
                return True
            else:
                print(f"❌ Error Claude API: {response.status_code}")
                try:
                    error_detail = response.json()
                    print(f"   📋 Detalle: {error_detail}")
                except:
                    print(f"   📋 Texto: {response.text}")
                return False

    except Exception as e:
        print(f"❌ Error conectando con Claude API: {e}")
        return False


async def test_database():
    print("\n🗄️  Probando base de datos...")

    if not DB_AVAILABLE:
        print("❌ Módulos de base de datos no disponibles")
        return False

    try:
        init_db()
        db = SessionLocal()
        user_count = db.query(User).count()
        print(f"✅ Base de datos conectada")
        print(f"   👤 Usuarios en BD: {user_count}")
        db.close()
        return True
    except Exception as e:
        print(f"❌ Error con la base de datos: {e}")
        return False


async def main():
    print("🚀 LoL Jungle Assistant - Test de Conectividad")
    print("=" * 50)

    current_dir = Path(__file__).parent
    env_path = current_dir / "backend" / ".env"

    print(f"🔍 Buscando .env en: {env_path}")
    print(f"📁 Directorio actual: {current_dir}")

    if not env_path.exists():
        print("❌ Archivo backend/.env no encontrado")
        return
    else:
        print("✅ Archivo .env encontrado")

    riot_ok = await test_riot_api()
    claude_ok = await test_claude_api()
    db_ok = await test_database()

    print("\n" + "=" * 50)
    print("📊 RESUMEN DE CONECTIVIDAD")
    print("=" * 50)
    print(f"🎮 Riot Games API: {'✅ OK' if riot_ok else '❌ ERROR'}")
    print(f"🤖 Claude API:     {'✅ OK' if claude_ok else '❌ ERROR'}")
    print(f"🗄️  Base de Datos:  {'✅ OK' if db_ok else '❌ ERROR'}")

    if all([riot_ok, claude_ok, db_ok]):
        print("\n🎉 ¡Todas las APIs están configuradas correctamente!")
        print("🚀 Ya puedes iniciar el servidor con: python backend/main.py")


if __name__ == "__main__":
    asyncio.run(main())