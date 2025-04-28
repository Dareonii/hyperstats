
def get_result_from_rank(mode: str, rank: int) -> str:
    """
    Determina o resultado (victory, draw, defeat) baseado no modo e no rank final no Showdown.

    Parâmetros:
        mode (str): Modo da batalha ('soloShowdown', 'duoShowdown', 'trioShowdown', etc.).
        rank (int): Posição final do jogador (1 a 10).

    Retorna:
        str: 'victory', 'draw', ou 'defeat'
    """
    mode = mode.lower()

    if mode == "soloshowdown":
        if rank in [1, 2, 3, 4]:
            return "victory"
        elif rank == 5:
            return "draw"
        else:
            return "defeat"

    elif mode in ["duoshowdown", "trioshowdown"]:
        if rank in [1, 2]:
            return "victory"
        elif rank == 3:
            return "draw"
        else:
            return "defeat"

    # Para modos normais (não showdown), o resultado já virá da API
    return "unknown"


def is_gadget_determinable(gadgets: list[str]) -> bool:
    """
    Checa se é seguro considerar o gadget para a análise.
    Só se o jogador tiver desbloqueado UM único gadget.

    Parâmetros:
        gadgets (list): Lista de nomes de gadgets desbloqueados.

    Retorna:
        bool: True se houver exatamente 1 gadget, False caso contrário.
    """
    return len(gadgets) == 1


def is_star_power_determinable(star_powers: list[str]) -> bool:
    """
    Checa se é seguro considerar o star power para a análise.
    Só se o jogador tiver desbloqueado UM único star power.

    Parâmetros:
        star_powers (list): Lista de nomes de star powers desbloqueados.

    Retorna:
        bool: True se houver exatamente 1 star power, False caso contrário.
    """
    return len(star_powers) == 1


def is_gears_determinable(gears: list[str]) -> bool:
    """
    Checa se é seguro considerar as gears para a análise.
    Só se o jogador tiver no máximo duas gears desbloqueadas.

    Parâmetros:
        gears (list): Lista de nomes de gears desbloqueadas.

    Retorna:
        bool: True se houver 1 ou 2 gears, False caso contrário.
    """
    return 0 < len(gears) <= 2
