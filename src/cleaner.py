from database import get_connection

def clean_old(dias: int = 7):
    print(f"\n🧹 Limpando dados com mais de {dias} dias...")
    conn = get_connection()
    cursor = conn.cursor()

    # Deletar primeiro os fatos
    cursor.execute(f"""
        DELETE FROM fact_battles
        WHERE battle_time < NOW() - INTERVAL '{dias} days';
    """)

    # Deletar depois as batalhas
    cursor.execute(f"""
        DELETE FROM battles
        WHERE battle_time < NOW() - INTERVAL '{dias} days';
    """)

    conn.commit()
    cursor.close()
    conn.close()

    print("✅ Limpeza concluída.")
