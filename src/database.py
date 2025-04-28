import psycopg2
from psycopg2.extras import execute_values
from models import Player, Brawler, Event, Battle, Participant
from typing import Optional

# 🔷 Função para criar conexão
def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="hyperstats",
        user="postgres",
        password="N@tang0s/os0"
    )

# 🔷 Função genérica para inserir um Player
def insert_player(player: Player):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO players (tag, name, trophies)
        VALUES (%s, %s, %s)
        ON CONFLICT (tag) DO NOTHING;
    """, (player.tag, player.name, player.trophies))

    conn.commit()
    cursor.close()
    conn.close()

# 🔷 Função genérica para inserir um Event
def insert_event(event: Event):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO events (id, mode, map)
        VALUES (%s, %s, %s)
        ON CONFLICT (id) DO NOTHING;
    """, (event.id, event.mode, event.map))

    conn.commit()
    cursor.close()
    conn.close()

# 🔷 Função para inserir Battle básica
def insert_battle(battle: Battle, event_id: int) -> Optional[int]:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO battles (battle_time, result, duration, event_id)
        VALUES (%s, %s, %s, %s)
        RETURNING id;
    """, (
        battle.battle_time,
        battle.result,
        None,  # Pode substituir depois por duração, se for útil
        event_id
    ))

    battle_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return battle_id

# 🔷 Função para inserir fatos para análise (fact_battles)
def insert_fact_battle(
    player_tag: str,
    battle_id: int,
    battle_time: str,
    mode: str,
    map_name: str,
    participant: Participant,
    result: str,
    gadget: Optional[str] = None,
    star_power: Optional[str] = None,
    gears: Optional[list[str]] = None
):
    conn = get_connection()
    cursor = conn.cursor()

    # Transforma lista de gears em string separada por vírgula
    gears_string = ", ".join(gears) if gears else None

    cursor.execute("""
        INSERT INTO fact_battles (
            player_tag, battle_id, battle_time, mode, map, brawler_name,
            brawler_power, result, gadget, star_power, gears
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """, (
        player_tag,
        battle_id,
        battle_time,
        mode,
        map_name,
        participant.brawler.name,
        participant.brawler.power,
        result,
        gadget,
        star_power,
        gears_string
    ))

    conn.commit()
    cursor.close()
    conn.close()

def battle_exists(battle_time: str, event_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 1
        FROM battles
        WHERE battle_time = %s AND event_id = %s
        LIMIT 1;
    """, (battle_time, event_id))
    exists = cursor.fetchone() is not None
    cursor.close()
    conn.close()
    return exists