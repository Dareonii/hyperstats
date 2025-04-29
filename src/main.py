from colector import coletar_dados
from cleaner import clean_old
from consultas import consultas_menu

def menu():
    while True:
        print("\n🔵 Comandos disponíveis:")
        print("1 - Atualizar Banco de Dados")
        print("2 - Limpar dados antigos")
        print("3 - Consultas")
        print("4 - Sair")

        escolha = input("\nDigite o número da opção desejada: ").strip()

        if escolha == "1":
            coletar_dados()
        elif escolha == "2":
            dias = input("Quantos dias deseja manter no banco? (Padrão 7): ").strip()
            dias = int(dias) if dias else 7
            clean_old(dias)
        elif escolha == "3":
            consultas_menu()
        elif escolha == "4":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()