import asyncio
from sqlalchemy.orm import Session
from app.database import SessionLocal, init_db
from app.models.user import User
from app.services.riot_service import riot_service


async def setup_not_alet_user():
    """Setup inicial para el usuario Not Alet con datos básicos pero funcionales"""
    init_db()
    db: Session = SessionLocal()

    try:
        account_data = await riot_service.get_summoner_by_riot_id("Not Alet", "JCP", "las")

        if not account_data:
            return

        puuid = account_data.get("puuid")
        summoner_data = await riot_service.get_summoner_by_puuid(puuid, "las")

        rank_tier = None
        rank_division = None
        league_points = 0
        summoner_level = None

        if summoner_data:
            summoner_level = summoner_data.get("summonerLevel")
            summoner_id = summoner_data.get("id")

            rank_info = await riot_service.get_rank_info(summoner_id, "las")

            if rank_info:
                for queue in rank_info:
                    if queue.get("queueType") == "RANKED_SOLO_5x5":
                        rank_tier = queue.get("tier")
                        rank_division = queue.get("rank")
                        league_points = queue.get("leaguePoints", 0)
                        break
        else:
            # Usar datos conocidos de League of Graphs como fallback
            summoner_level = 271
            rank_tier = "PLATINUM"
            rank_division = "IV"
            league_points = 91

        recent_matches = await riot_service.get_recent_matches(puuid, 20, "las")
        matches_count = len(recent_matches) if recent_matches else 0

        existing_user = db.query(User).filter(User.riot_id == "Not Alet").first()

        if existing_user:
            existing_user.summoner_name = account_data["gameName"]
            existing_user.tag_line = account_data["tagLine"]
            existing_user.rank_tier = rank_tier
            existing_user.rank_division = rank_division
            existing_user.league_points = league_points
            existing_user.preferred_jungle_champions = '["Graves", "Kindred", "Kha\'Zix", "Nidalee", "Hecarim", "Viego"]'

            db.commit()
            user = existing_user
        else:
            user = User(
                riot_id="Not Alet",
                summoner_name=account_data["gameName"],
                tag_line=account_data["tagLine"],
                region="las",
                rank_tier=rank_tier,
                rank_division=rank_division,
                league_points=league_points,
                preferred_jungle_champions='["Graves", "Kindred", "Kha\'Zix", "Nidalee", "Hecarim", "Viego"]'
            )

            db.add(user)
            db.commit()
            db.refresh(user)

    except Exception as e:
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    asyncio.run(setup_not_alet_user())