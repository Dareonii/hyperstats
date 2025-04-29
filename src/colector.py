import time
import logging
import random
from tqdm import tqdm
from colorama import Fore, Style, init

from pathlib import Path
from database import battle_exists, insert_player, insert_event, insert_battle, insert_fact_battle
from api_client import BrawlStarsAPIClient
from parsers import parse_player, parse_battlelog
from utils import get_result_from_rank

# Inicializar colorama
init(autoreset=True)

# Inicializar logging
base_dir = Path(__file__).resolve().parent.parent
logs_dir = base_dir / "logs"
logs_dir.mkdir(exist_ok=True)
log_file = logs_dir / "coletor.log"

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def coletar_dados():
    print(Fore.CYAN + "\n🔄 Iniciando coleta de dados...")
    logging.info("Iniciando coleta de dados.")

    client = BrawlStarsAPIClient()
    top_players = client.get_top_players()["items"]
    random.shuffle(top_players)
    players_cache = {}

    for player_info in tqdm(top_players, desc="📈 Coletando jogadores", unit="jogador"):
        player_tag = player_info["tag"]

        try:
            if player_tag not in players_cache:
                player_data = client.get_player(player_tag)
                player_obj = parse_player(player_data)
                players_cache[player_tag] = player_obj
                insert_player(player_obj)
                time.sleep(0.2)

            battlelog_data = client.get_battlelog(player_tag)
            battlelog_obj = parse_battlelog(battlelog_data, player_tag)

            for battle in battlelog_obj.battles:
                if battle_exists(battle.battle_time, battle.event.id):
                    continue

                insert_event(battle.event)
                battle_id = insert_battle(battle, event_id=battle.event.id)

                is_showdown = battle.mode.lower() in ["soloshowdown", "duoshowdown", "trioshowdown"]

                for participant in battle.players:
                    if participant.brawler.power != 11:
                        continue

                    if participant.tag in players_cache:
                        participant_obj = players_cache[participant.tag]
                    else:
                        try:
                            participant_data = client.get_player(participant.tag)
                            participant_obj = parse_player(participant_data)
                            players_cache[participant.tag] = participant_obj
                            insert_player(participant_obj)
                            time.sleep(0.2)
                        except Exception as e:
                            print(Fore.RED + f"⚠️ Falha ao buscar participante {participant.name}: {e}")
                            logging.error(f"Erro ao buscar participante {participant.name}: {e}")
                            continue

                    brawler_details = next(
                        (b for b in participant_obj.brawlers if b.id == participant.brawler.id),
                        None
                    )

                    if not brawler_details:
                        continue

                    gadget = brawler_details.gadgets[0] if len(brawler_details.gadgets) == 1 else None
                    star_power = brawler_details.star_powers[0] if len(brawler_details.star_powers) == 1 else None
                    gears = brawler_details.gears if 0 < len(brawler_details.gears) <= 2 else None

                    result = get_result_from_rank(battle.mode, battle.rank) if is_showdown else battle.result

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

            logging.info(f"Jogador {player_tag} concluído.")
        except Exception as e:
            print(Fore.RED + f"⚠️ Erro ao processar jogador {player_tag}: {e}")
            logging.error(f"Erro ao processar jogador {player_tag}: {e}")
            time.sleep(1)

    print(Fore.GREEN + "\n🏁 Coleta concluída com sucesso!")
    logging.info("Coleta concluída com sucesso.")
