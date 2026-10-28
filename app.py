from funcoes import carregar_txt, criar, logar


def main():
    print("Bem-vindo usuário!")
    while True:
        print("[1] Logar\n[2] Criar conta\n[0] Sair")
        escolha = input("escolha: ")

        match escolha:
            case "1":
                logar()
            case "2":
                criar()
            case "0":
                print("Encerrando...")
                exit()
            case _:
                print("Valor inválido")
                continue


if __name__ == "__main__":
    carregar_txt()
    main()
