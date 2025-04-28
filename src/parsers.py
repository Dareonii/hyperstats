from models import Brawler, Player, Event, Participant, BattleLog, Battle

def parse_brawler(data: dict) -> Brawler:
    return Brawler(
        id=data["id"],
        name=data["name"],
        power=data["power"],
        trophies=data["trophies"],
        gears=[gear["name"] for gear in data.get("gears", [])],
        star_powers=[sp["name"] for sp in data.get("starPowers", [])],
        gadgets=[g["name"] for g in data.get("gadgets", [])],
    )

def parse_player(data: dict) -> Player:
    return Player(
        tag=data["tag"],
        name=data["name"],
        trophies=data["trophies"],
        brawlers=[parse_brawler(b) for b in data.get("brawlers", [])]
    )

def parse_participant(data: dict) -> Participant:
    return Participant(
        tag=data["tag"],
        name=data["name"],
        brawler=parse_brawler(data["brawler"]),
    )

def parse_battle(data: dict) -> Battle:
    battle_time = data["battleTime"]

    event = Event(
        id=data["event"]["id"],
        mode=data["event"]["mode"],
        map=data["event"]["map"]
    )

    mode = data["battle"].get("mode")
    type_ = data["battle"].get("type")
    result = data["battle"].get("result")
    rank = data["battle"].get("rank")  # rank geral do jogador (aparece só para quem consulta seu próprio histórico)

    participants: list[Participant] = []

    if "teams" in data["battle"]:
        teams = data["battle"]["teams"]
        for team in teams:
            for participant in team:
                participants.append(parse_participant(participant))

    elif "players" in data["battle"]:
        players = data["battle"]["players"]
        for participant in players:
            participants.append(parse_participant(participant))

    else:
        raise ValueError(f"Batalha sem 'teams' nem 'players': {data}")

    is_showdown = "players" in data["battle"]

    return Battle(
        battle_time=battle_time,
        event=event,
        mode=mode,
        type=type_,
        rank=rank,
        result=result,
        players=participants,
        is_showdown=is_showdown
    )


def parse_battlelog(data: dict, player_tag: str) -> BattleLog:
    """Retorna um BattleLog (lista de batalhas) associado a um player."""
    battles: list[Battle] = []

    for battle_entry in data.get("items", []):
        battles.append(parse_battle(battle_entry))

    return BattleLog(player_tag=player_tag, battles=battles)