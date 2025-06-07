import asyncio
from sqlalchemy.orm import Session
from app.database import SessionLocal, init_db
from app.models.user import User
from app.services.riot_service import riot_service

async def setup_not_alet_user():
    """Setup inicial para el usuario Not Alet"""
    # Initialize database
    init_db()
    
    # Create database session
    db: Session = SessionLocal()
    
    try:
        # Buscar información del summoner en Riot API
        print("Buscando información de Not Alet en LAS...")
        summoner_data = await riot_service.get_summoner_by_riot_id("Not Alet", "LAS", "las")
        
        if not summoner_data:
            print("❌ No se pudo encontrar el summoner 'Not Alet' en LAS")
            print("🔧 Asegúrate de que el Riot ID y tag line sean correctos")
            return
        
        print(f"✅ Summoner encontrado: {summoner_data}")
        
        # Obtener detalles adicionales del summoner
        puuid = summoner_data.get("puuid")
        summoner_details = await riot_service.get_summoner_by_puuid(puuid, "las")
        
        if summoner_details:
            summoner_id = summoner_details.get("id")
            # Obtener información de ranked
            rank_info = await riot_service.get_rank_info(summoner_id, "las")
            
            # Extraer información de ranked si existe
            rank_tier = None
            rank_division = None
            league_points = 0
            
            if rank_info:
                for queue in rank_info:
                    if queue.get("queueType") == "RANKED_SOLO_5x5":
                        rank_tier = queue.get("tier")
                        rank_division = queue.get("rank")
                        league_points = queue.get("leaguePoints", 0)
                        break
        
        # Verificar si el usuario ya existe
        existing_user = db.query(User).filter(User.riot_id == "Not Alet").first()
        
        if existing_user:
            print("👤 Usuario ya existe, actualizando información...")
            existing_user.summoner_name = summoner_data.get("gameName", "Not Alet")
            existing_user.tag_line = summoner_data.get("tagLine", "LAS")
            existing_user.rank_tier = rank_tier
            existing_user.rank_division = rank_division
            existing_user.league_points = league_points
            db.commit()
            user = existing_user
        else:
            print("➕ Creando nuevo usuario...")
            # Crear nuevo usuario
            user = User(
                riot_id="Not Alet",
                summoner_name=summoner_data.get("gameName", "Not Alet"),
                tag_line=summoner_data.get("tagLine", "LAS"),
                region="las",
                rank_tier=rank_tier,
                rank_division=rank_division,
                league_points=league_points,
                preferred_jungle_champions='["Graves", "Kindred", "Nidalee", "Kha\'Zix"]'
            )
            
            db.add(user)
            db.commit()
            db.refresh(user)
        
        print(f"""
✅ Usuario configurado exitosamente:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👤 Riot ID: {user.riot_id}
🏷️  Tag Line: {user.tag_line}
🌎 Región: {user.region}
🏆 Rango: {user.rank_tier} {user.rank_division} ({user.league_points} LP)
🎮 ID de Usuario: {user.id}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        """)
        
        # Obtener partidas recientes para prueba
        print("🔍 Obteniendo partidas recientes...")
        recent_matches = await riot_service.get_recent_matches(puuid, 5, "las")
        
        if recent_matches:
            print(f"📊 {len(recent_matches)} partidas recientes encontradas:")
            for i, match_id in enumerate(recent_matches[:3], 1):
                print(f"   {i}. {match_id}")
        else:
            print("⚠️  No se encontraron partidas recientes")
        
    except Exception as e:
        print(f"❌ Error configurando usuario: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(setup_not_alet_user())