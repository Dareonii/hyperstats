from dataclasses import dataclass, field

@dataclass
class Brawler:
    id: int
    name: str
    power: int
    trophies: int
    # not always
    gadgets: list[str] = field(default_factory=list)
    gears: list[str] = field(default_factory=list)
    star_powers: list[str] = field(default_factory=list)

@dataclass
class Participant:
    tag: str
    name: str
    brawler: Brawler

@dataclass
class Event:
    id: int
    mode: str
    map: str

@dataclass
class Battle:
    battle_time: str
    event: Event
    #battle
    mode: str
    type: str
    rank: int | None # Used only in Showdown
    result: str
    # may be extracted from ["teams"] if not in showdown
    players: list[Participant]
    is_showdown: bool = False


@dataclass
class BattleLog:
    player_tag: str
    battles: list[Battle]

@dataclass
class Player:
    tag: str
    name: str
    trophies: int
    brawlers: list[Brawler] = field(default_factory=list)