import time
import pandas


class Turma:
    def __init__(self, nome):
        self.nome = nome
        self.alunos = []
        self.total = 0

    def adicionar_aluno(self, aluno):
        self.total += 1
        aluno.id = self.total
        self.alunos.append(aluno)

    def remover_aluno(self, id, nome):
        for i in self.alunos:
            if i.id == id and i.nome.strip().lower() == nome.strip().lower():
                self.alunos.remove(i)
                print("Aluno removido")
                break
        else:
            print("Não existe esse aluno")

    def listar_alunos(self):
        print(f"\nTurma: {self.nome}")
        print("-" * 30)
        print(f"{'ID':<5} | {'Nome':<20}")
        print("-" * 30)
        for aluno in self.alunos:
            print(f"{aluno.id:<5} | {aluno.nome:<20}")
        print("-" * 30)


class Materia:
    def __init__(self, nome, professor):
        self.nome = nome
        self.professor = professor

    def mostrar_infos(self):
        print(f"{'Nome':<15} | {'Professor':<15}")
        print(f"{self.nome:<15} | {self.professor:<15}")


class Aluno:
    def __init__(self, nome):
        self.nome = nome
        self.id = None
        self.materias = []
        self.notas = {}

    def matricular(self, materia):
        if materia not in self.materias:
            self.materias.append(materia)
            return True
        else:
            print("Essa materia ja esta adicionada")
            return False

    def adicionar_nota(self, materia, nota):
        if materia not in self.materias:
            self.matricular(materia)
        if materia.nome not in self.notas:
            self.notas[materia.nome] = []
        self.notas[materia.nome].append(nota)
        if len(self.notas[materia.nome]) > 3:
            self.remover_excedido(materia)

    def remover_excedido(self, materia):
        print(f"Limite de 3 notas excedido em {materia.nome}")
        print(f"Notas atuais: {self.notas[materia.nome]}")
        while len(self.notas[materia.nome]) > 3:
            nota = input("Digite a nota que deseja remover: ")
            try:
                nota = float(nota)
            except ValueError:
                print("Digite apenas numeros")
                continue
            if nota in self.notas[materia.nome]:
                self.notas[materia.nome].remove(nota)
                print("Nota removida com sucesso!")
            else:
                print("Essa nota não existe!")

    def remover_nota(self, materia, nota):
        for n in self.notas[materia.nome]:
            if n == nota:
                self.notas[materia.nome].remove(nota)
                break

    def media_por_materia(self, materia):
        if materia.nome not in self.notas:
            return 0.0
        notas = self.notas[materia.nome]
        if not notas:
            return 0.0
        return sum(notas) / len(notas)

    def media_geral(self):
        medias_por_disciplina = []
        for i in self.materias:
            media = self.media_por_materia(i)
            medias_por_disciplina.append(media)
        if not medias_por_disciplina:
            return 0.0
        return sum(medias_por_disciplina) / len(medias_por_disciplina)


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


materias = {
    "dsa": Materia("Data Structures", "Erick"),
    "cs": Materia("Computer Science", "Mauricio"),
    "mlpam": Materia("Modelagem Linear", "Rodolfo"),
    "mmc": Materia("Modelagem Matematica", "Roberto"),
    "pcap": Materia("Python", "Russi"),
}

turmas = {
    "1CCPH": Turma("1CCPH"),
    "1CCPI": Turma("1CCPI"),
    "1CCPJ": Turma("1CCPJ"),
    "1CCPK": Turma("1CCPK"),
    "1CCPL": Turma("1CCPL"),
}


def menu():
    while True:
        print(
            "[1] Adicionar aluno\n[2] remover aluno\n[3] adicionar nota\n[4] remover nota\n[5] matricular materia\n[6] salvar txt\n[0] Sair"
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
            case "0":
                salvar_txt()
                print("Saindo...")
                return
            case _:
                print("valor invalido")
                continue


carregar_txt()
menu()
