import random
import time
from api_client import BrawlStarsAPIClient
from parsers import parse_player, parse_battlelog
from database import (
    insert_player, insert_event, insert_battle,
    insert_fact_battle, battle_exists  # Nova função para checar duplicidade
)
from utils import get_result_from_rank
from models import Player, BattleLog, Participant

#tag = input("Qual é sua tag?\n")

def main():
    client = BrawlStarsAPIClient(BrawlStarsAPIClient.key)
    player_tag = "GQ9LQP98"  # Tag fixa para testes
    player_tag = random.choice(client.get_top_players()["items"])["tag"] # Tag aleatória para testes

    print("🔄 Buscando Top 200 jogadores...")
    top_players = client.get_top_players()["items"]

    players_cache = {}

    for player_info in top_players:
        player_tag = player_info["tag"]

        try:
            # 🔷 Buscar e parsear Player, se ainda não tiver no cache
            if player_tag not in players_cache:
                player_data = client.get_player(player_tag)
                player_obj: Player = parse_player(player_data)
                players_cache[player_tag] = player_obj
                insert_player(player_obj)
                time.sleep(0.2)  # Rate limit segurança extra

            # 🔷 Buscar Battlelog
            battlelog_data = client.get_battlelog(player_tag)
            battlelog_obj: BattleLog = parse_battlelog(battlelog_data, player_tag)

            # 🔷 Para cada batalha
            for battle in battlelog_obj.battles:
                # 🔷 Checar duplicidade usando índice
                if battle_exists(battle.battle_time, battle.event.id):
                    print(f"⚠️ Batalha já registrada. Pulando.")
                    continue

                # 🔷 Nova batalha: processar
                insert_event(battle.event)
                battle_id = insert_battle(battle, event_id=battle.event.id)

                is_showdown = battle.mode.lower() in ["soloshowdown", "duoshowdown", "trioshowdown"]

                for participant in battle.players:

                    # 🔷 Buscar detalhes do participante
                    if participant.tag in players_cache:
                        participant_obj = players_cache[participant.tag]
                    else:
                        try:
                            participant_data = client.get_player(participant.tag)
                            participant_obj: Player = parse_player(participant_data)
                            players_cache[participant.tag] = participant_obj
                            insert_player(participant_obj)
                            time.sleep(0.2)
                        except Exception as e:
                            print(f"⚠️ Falha ao buscar participante {participant.name}: {e}")
                            continue

                    # 🔷 Procurar o brawler usado
                    brawler_details = None
                    for b in participant_obj.brawlers:
                        if b.id == participant.brawler.id:
                            brawler_details = b
                            break

                    if not brawler_details:
                        continue  # Segurança

                    # 🔷 Definir loadout
                    gadget = brawler_details.gadgets[0] if len(brawler_details.gadgets) == 1 else None
                    star_power = brawler_details.star_powers[0] if len(brawler_details.star_powers) == 1 else None
                    gears = brawler_details.gears if 0 < len(brawler_details.gears) <= 2 else None

                    # 🔷 Definir resultado
                    if is_showdown:
                        if battle.rank is None:
                            continue
                        result = get_result_from_rank(battle.mode, battle.rank)
                    else:
                        result = battle.result

                    # 🔷 Inserir fato
                    insert_fact_battle(
                        player_tag=participant.tag,
                        battle_id=battle_id,
                        battle_time=battle.battle_time,
                        mode=battle.mode,
                        map_name=battle.event.map,
                        participant=participant,
                        result=result,
                        gadget=gadget,
                        star_power=star_power,
                        gears=gears
                    )

                print(f"✅ Batalha {battle_id} processada.")

            print(f"🏁 Jogador {player_tag} concluído.\n")

        except Exception as e:
            print(f"⚠️ Erro ao processar jogador {player_tag}: {e}")
            time.sleep(1)  # Pausa extra em caso de falha

if __name__ == "__main__":
    main()