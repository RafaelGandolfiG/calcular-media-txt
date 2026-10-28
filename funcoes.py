import pandas
from aluno import Aluno
from dados import materias, turmas


def carregar_txt():
    try:
        with open("notas.txt", "r", encoding="utf-8") as arquivo:
            linhas = arquivo.readlines()
    except FileNotFoundError:
        print("Arquivo não encontrado")
        return
    for linha in linhas:
        if not linha.strip():
            continue
        dados = linha.strip().split(";")
        nome_turma = dados[0]
        id = int(dados[1])
        nome_aluno = dados[2]
        nome_materia = dados[3]
        professor = dados[4]
        notas = dados[5:]
        notas = list(map(float, notas))
        turma = turmas[nome_turma]
        for aluno in turma.alunos:
            if aluno.id == id:
                aluno_encontrado = aluno
                break
        else:
            aluno_encontrado = Aluno(nome_aluno)
            aluno_encontrado.id = id
            turma.alunos.append(aluno_encontrado)
        if id > turma.total:
            turma.total = id
        if nome_materia:
            for materia in materias.values():
                if materia.nome == nome_materia:
                    aluno_encontrado.matricular(materia)
                    aluno_encontrado.notas[materia.nome] = notas
                    break


def salvar_txt():
    with open("notas.txt", "w", encoding="utf-8") as arquivo:
        for turma in turmas.values():
            for aluno in turma.alunos:
                if not aluno.materias:
                    dados = [turma.nome, str(aluno.id), aluno.nome, "", ""]
                    arquivo.write(";".join(dados) + "\n")
                else:
                    for materia in aluno.materias:
                        dados = [
                            turma.nome,
                            str(aluno.id),
                            aluno.nome,
                            materia.nome,
                            materia.professor,
                        ]
                        for chave, notas in aluno.notas.items():
                            if chave == materia.nome:
                                for nota in notas:
                                    dados.append(str(nota))
                        arquivo.write(";".join(dados) + "\n")
    print("Dados salvos com sucesso!")


def matricular():
    turma = input("Quer adicionar aluno em qual turma? ").strip().upper()
    if turma not in turmas:
        print("Não existe essa turma")
        return
    nome = input("nome do aluno: ")
    aluno = Aluno(nome)
    turmas[turma].adicionar_aluno(aluno)
    print(f"Aluno {aluno.nome} cadastrado com ID {aluno.id}")


def remover():
    turma = input("De qual turma é o aluno que será removido? ")
    if turma not in turmas:
        print("Não tem essa turma")
        return
    nome = input("nome do aluno: ")
    id = input("Id do aluno: ")
    try:
        id = int(id)
    except:
        print("Digite um numero")
        return
    turmas[turma].remover_aluno(id, nome)


def verificar_dados():
    turma = input("De qual turma é o aluno? ").strip().upper()
    if turma not in turmas:
        print("Não tem essa turma")
        return
    nome = input("Nome do aluno: ")
    id = input("Id do aluno: ")
    try:
        id = int(id)
    except:
        print("Digite um numero")
        return
    materia = input("Qual matéria deseja selecionar? ").strip().lower()
    if materia not in materias:
        print("Essa materia nao existe")
        return
    materia = materias[materia]
    return turma, nome, id, materia


def adicionar_nota():
    dados = verificar_dados()
    if dados is None:
        return
    turma, nome, id, materia = dados
    for i in turmas[turma].alunos:
        if i.id == id and i.nome.strip().lower() == nome.strip().lower():
            nota = input(f"Digite a nota de {materia.nome}: ")
            try:
                nota = float(nota)
            except:
                print("Digite apenas numeros")
                return
            i.adicionar_nota(materia, nota)
            break
    else:
        print("Aluno não encontrado")


def remover_nota():
    dados = verificar_dados()
    if dados is None:
        return
    turma, nome, id, materia = dados
    for i in turmas[turma].alunos:
        if i.id == id and i.nome.strip().lower() == nome.strip().lower():
            if materia.nome not in i.notas or not i.notas[materia.nome]:
                print("O aluno não possui notas nessa matéria")
                return
            print(f"Notas de {materia.nome} disponiveis")
            for num, j in enumerate(i.notas[materia.nome]):
                print(f"Nota {num}: {j}")
            nota = input("Qual nota deseja remover? ")
            try:
                nota = float(nota)
            except:
                print("Digite apenas numeros")
                return
            for n in i.notas[materia.nome]:
                if nota == n:
                    i.remover_nota(materia, nota)
                    break
            else:
                print("nota não encontrada")
            break
    else:
        print("Aluno não encontrado")


def matricular_materia():
    dados = verificar_dados()
    if dados is None:
        return
    turma, nome, id, materia = dados
    for i in turmas[turma].alunos:
        if i.id == id and i.nome.strip().lower() == nome.strip().lower():
            if i.matricular(materia):
                print(f"Aluno matriculado em {materia.nome}")
            break
    else:
        print("Aluno não encontrado")


def area_turma():
    print("Bem vindo à área das turma")
    turma = input("Qual turma deseja consultar? ").strip().upper()
    for i in turmas:
        if i == turma:
            menu_turma()
            break
    else:
        print("Essa turma não existe")
        return


def listar_alunos():
    turma = input("Qual turma deseja consultar? ").strip().upper()
    if turma not in turmas:
        print("Turma não encontrada")
        return
    turmas[turma].listar_alunos()


def mostrar_resumo():
    turma = input("Qual turma deseja consultar? ").strip().upper()
    if turma not in turmas:
        print("Turma não encontrada")
        return
    turmas[turma].mostrar_resumo()


def menu_turma():
    while True:
        print("[1] Listar alunos\n[2] Resumo da turma")
        escolha = input("Escolha: ")
        match escolha:
            case "1":
                listar_alunos()
            case "2":
                mostrar_resumo()
            case "0":
                print("Saindo da área das turmas")
                return
            case _:
                print("Valor inválido")
                continue


def mostrar_medias(aluno):
    dados = []
    for materia in aluno.materias:
        media = aluno.media_por_materia(materia)
        if media >= 6:
            situacao = "Aprovado"
        elif media >= 4:
            situacao = "Exame"
        else:
            situacao = "Reprovado"
        dados.append(
            {
                "Matéria": materia.nome,
                "Professor": materia.professor,
                "Média": round(media, 2),
                "Situação": situacao,
            }
        )
    if not dados:
        print("Aluno não possui matérias")
        return
    tabela = pandas.DataFrame(dados)
    print(tabela.to_string(index=False))


def mostrar_media_geral(aluno):
    media = aluno.media_geral()
    if media >= 6:
        situacao = "Aprovado"
    elif media >= 4:
        situacao = "Exame"
    else:
        situacao = "Reprovado"
    dados = [
        {
            "ID": aluno.id,
            "Nome": aluno.nome,
            "Média Geral": round(media, 2),
            "Situação": situacao,
        }
    ]
    tabela = pandas.DataFrame(dados)
    print(tabela.to_string(index=False))


def menu_aluno(aluno):
    while True:
        print("\n[1] Médias por matéria\n" "[2] Média geral e situação\n" "[0] Sair")
        escolha = input("Escolha: ")
        match escolha:
            case "1":
                mostrar_medias(aluno)
            case "2":
                mostrar_media_geral(aluno)
            case "0":
                print("Saindo da área do aluno")
                return
            case _:
                print("Valor inválido")
                continue


def area_aluno():
    print("Bem vindo à área dos alunos")
    turma = input("Qual turma é o aluno? ").strip().upper()
    if turma not in turmas:
        print("Essa turma não existe")
        return
    nome = input("Nome do aluno: ").strip().lower()
    try:
        id = int(input("ID do aluno: "))
    except ValueError:
        print("Digite um ID válido")
        return
    for aluno in turmas[turma].alunos:
        if aluno.id == id and aluno.nome.strip().lower() == nome:
            print(f"Bem vindo, {aluno.nome}!")
            menu_aluno(aluno)
            break
    else:
        print("Aluno não encontrado")


def menu():
    while True:
        print(
            "[1] Adicionar aluno\n[2] remover aluno\n[3] adicionar nota\n[4] remover nota\n[5] matricular materia\n[6] salvar txt\n[7] Area da turma\n[8] Area do aluno\n[0] Sair"
        )
        escolha = input("Escolha: ")
        match escolha:
            case "1":
                matricular()
            case "2":
                remover()
            case "3":
                adicionar_nota()
            case "4":
                remover_nota()
            case "5":
                matricular_materia()
            case "6":
                salvar_txt()
            case "7":
                area_turma()
            case "8":
                area_aluno()
            case "0":
                salvar_txt()
                print("Saindo...")
                return
            case _:
                print("valor invalido")
                continue


def criar():
    while True:
        print("Vamos criar sua conta")
        try:
            with open("logins.txt", "r", encoding="utf-8") as arquivo:
                linhas = arquivo.readlines()
        except FileNotFoundError:
            print("Arquivo não existe")
            linhas = []
        email = input("Digite seu email: ")
        senha = input("Digite sua senha: ")
        confirma = input("Confirme sua senha: ")
        if senha.strip() != confirma.strip():
            print("Senhas não coincidem")
            continue
        for linha in linhas:
            dados = linha.split(";")
            if dados[0] == email:
                print("Ja tem uma conta com esse email")
                break
        else:
            with open("logins.txt", "a", encoding="utf-8") as arquivo:
                arquivo.write(f"{email};{senha}\n")
            print("Conta criada com sucesso")
            menu()
            return


def logar():
    while True:
        print("Vamos entrar na sua conta")
        try:
            with open("logins.txt", "r", encoding="utf-8") as arquivo:
                linhas = arquivo.readlines()
            if len(linhas) == 0:
                print("Nenhuma conta cadastrada")
                return
        except FileNotFoundError:
            print("Nenhuma conta cadastrada")
            return
        email = input("Digite seu email: ")
        senha = input("Digite sua senha: ")
        for linha in linhas:
            dados = linha.strip().split(";")
            if dados[0] == email and dados[1] == senha:
                print("Login realizado com sucesso!")
                menu()
                return
        else:
            print("Email ou senha incorretos")
