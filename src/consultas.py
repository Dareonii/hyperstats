from database import get_connection

def top_winrate(limit: int = 10):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT
            brawler_name,
            COUNT(*) AS partidas_jogadas,
            ROUND(100.0 * SUM(CASE WHEN result = 'victory' THEN 1 ELSE 0 END) / COUNT(*), 2) AS winrate_percentual
        FROM fact_battles
        WHERE brawler_power = 11
        GROUP BY brawler_name
        HAVING COUNT(*) > 20  -- opcional: evitar estatísticas com poucos jogos
        ORDER BY winrate_percentual DESC
        LIMIT {limit};
    """)

    resultados = cursor.fetchall()
    cursor.close()
    conn.close()

    print(f"\n🏆 Top {limit} Brawlers por Winrate:")
    for brawler_name, partidas, winrate in resultados:
        print(f"{brawler_name}: {winrate}% (em {partidas} partidas)")

def top_userate(limit: int = 10):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT
            brawler_name,
            COUNT(*) AS partidas_jogadas,
            ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM fact_battles WHERE brawler_power = 11), 2) AS userate_percentual
        FROM fact_battles
        WHERE brawler_power = 11
        GROUP BY brawler_name
        ORDER BY userate_percentual DESC
        LIMIT {limit};
    """)

    resultados = cursor.fetchall()
    cursor.close()
    conn.close()

    print(f"\n🔥 Top {limit} Brawlers por Uso:")
    for brawler_name, partidas, userate in resultados:
        print(f"{brawler_name}: {userate}% de uso ({partidas} partidas)")

def top_wins(limit: int = 10):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
            SELECT
                brawler_name AS brawler,
                COUNT(*) AS partidas_jogadas,
                SUM(CASE WHEN result = 'victory' THEN 1 ELSE 0 END) AS wins
            FROM fact_battles
            GROUP BY brawler
            HAVING COUNT(*) > 20  -- opcional: evitar estatísticas com poucos jogos
            ORDER BY wins DESC
            LIMIT {limit};
        """)

    resultados = cursor.fetchall()
    cursor.close()
    conn.close()

    print(f"\n🔥 Top {limit} Brawlers por Uso:")
    for brawler_name, partidas, userate in resultados:
        print(f"{brawler_name}: {userate}% de uso ({partidas} partidas)")

def consultas_menu():
    while True:
        print("\n📊 Consultas disponíveis:")
        print("1 - Top Brawlers por Winrate")
        print("2 - Top Brawlers por Uso")
        print("3 - Top Brawlers por Vitória")
        print("4 - Voltar ao Menu Principal")

        escolha = input("\nDigite o número da consulta desejada: ").strip()

        if escolha == "1":
            limite = input("Quantos resultados deseja listar? (Padrão 10): ").strip()
            limite = int(limite) if limite else 10
            top_winrate(limite)
        elif escolha == "2":
            limite = input("Quantos resultados deseja listar? (Padrão 10): ").strip()
            limite = int(limite) if limite else 10
            top_userate(limite)
        elif escolha == "3":
            limite = input("Quantos resultados deseja listar? (Padrão 10): ").strip()
            limite = int(limite) if limite else 10
            top_wins(limite)
        elif escolha == "4":
            break
        else:
            print("Opção inválida.")
