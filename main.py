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
        else:
            print("Essa materia ja esta adicionada")

    def adicionar_nota(self, materia, nota):
        if materia not in self.materias:
            self.matricular(materia)
        if materia not in self.notas:
            self.notas[materia.nome] = []
        self.notas[materia.nome].append(nota)
        if len(self.notas[materia.nome]) > 3:
            self.remover_nota(materia)

    def remover_nota(self, materia):
        print(f"Limite de 3 notas excedido em {materia.nome}")
        print(f"Notas atuais: {self.notas[materia.nome]}")
        while len(self.notas[materia.nome]) > 3:
            nota = float(input("Digite a nota que deseja remover: "))
            if nota in self.notas[materia.nome]:
                self.notas[materia.nome].remove(nota)
                print("Nota removida com sucesso!")
            else:
                print("Essa nota não existe!")

    def media_por_materia(self, materia):
        if materia.nome not in self.notas:
            return 0.0
        notas = self.notas[materia.nome]
        if not notas:
            return 0.0
        return sum(notas) / len(notas)

    def media_geral(self):
        medias_por_disciplina = []
        for i in self.disciplinas:
            media = self.media_por_materia(i)
            medias_por_disciplina.append(media)
        if not medias_por_disciplina:
            return 0.0
        return sum(medias_por_disciplina) / len(medias_por_disciplina)



def matricular():
    turma = input("Quer adicionar aluno em qual turma? ")
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


def adicionar_nota():
    turma = input("De qual turma é o aluno? ")
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
    materia = input("Qual materia deseja adicionar a nota? ")
    if materia not in materias:
        print("Essa materia nao existe")
        return
    materia = materias[materia]
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
            "[1] Adicionar aluno\n[2] remover aluno\n[3] adicionar nota\n[4] remover nota\n[5] matricular materia"
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
                ...
            case "5":
                ...
            case _:
                print("valor invalido")
                continue


menu()
