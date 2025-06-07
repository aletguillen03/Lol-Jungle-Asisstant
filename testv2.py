#!/usr/bin/env python3
"""
Script para probar diferentes variaciones del usuario de Riot
"""

import asyncio
import httpx
import os
from pathlib import Path

# Cargar .env
env_path = Path("backend/.env")
if env_path.exists():
    with open(env_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                # Quitar comillas si las hay
                value = value.strip('"').strip("'")
                os.environ[key] = value


async def test_riot_user_variations():
    """Probar diferentes variaciones del usuario"""
    riot_key = os.getenv('RIOT_API_KEY')
    if not riot_key:
        print("❌ RIOT_API_KEY no encontrada")
        return

    print(f"🔑 Usando API Key: {riot_key[:10]}...")

    # Diferentes variaciones para probar
    users_to_test = [
        ("Not Alet", "JCP"),  # El correcto según League of Graphs
        ("NotAlet", "JCP"),
        ("Not Alet", "LAS"),
        ("NotAlet", "LAS"),
    ]

    headers = {"X-Riot-Token": riot_key}

    async with httpx.AsyncClient() as client:
        for riot_id, tag_line in users_to_test:
            try:
                # URL encode del riot_id
                encoded_riot_id = riot_id.replace(" ", "%20")
                url = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{encoded_riot_id}/{tag_line}"

                print(f"\n🔍 Probando: {riot_id}#{tag_line}")
                print(f"URL: {url}")

                response = await client.get(url, headers=headers)

                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ ¡ENCONTRADO! {data.get('gameName')}#{data.get('tagLine')}")
                    print(f"   PUUID: {data.get('puuid')}")
                    return data
                elif response.status_code == 404:
                    print(f"❌ No encontrado: {riot_id}#{tag_line}")
                else:
                    print(f"⚠️  Error {response.status_code}: {response.text}")

            except Exception as e:
                print(f"❌ Error: {e}")

    print(f"\n🤔 No se encontró ninguna variación. Posibles problemas:")
    print(f"   1. El usuario no existe en LAS")
    print(f"   2. La API key no es válida")
    print(f"   3. El formato del nombre es diferente")

    # Probar la API key con un endpoint básico
    print(f"\n🔬 Probando validez de la API key...")
    try:
        # Endpoint para verificar que la key funciona
        test_url = "https://la1.api.riotgames.com/lol/status/v4/platform-data"
        response = await client.get(test_url, headers=headers)
        if response.status_code == 200:
            print("✅ API key es válida")
        else:
            print(f"❌ API key inválida: {response.status_code}")
    except Exception as e:
        print(f"❌ Error probando API key: {e}")


if __name__ == "__main__":
    asyncio.run(test_riot_user_variations())