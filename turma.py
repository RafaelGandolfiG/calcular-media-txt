import pandas as pd


class Turma:
    def __init__(self, nome):
        self.nome = nome
        self.alunos = []
        self.total = 0
        self.situacoes = {"aprovados": [], "exame": [], "reprovados": []}

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

    def classificar_alunos(self):
        self.situacoes = {"aprovados": [], "exame": [], "reprovados": []}
        for aluno in self.alunos:
            if not aluno.notas:
                continue
            media = aluno.media_geral()
            if media >= 6:
                self.situacoes["aprovados"].append(aluno)
            elif media >= 4:
                self.situacoes["exame"].append(aluno)
            else:
                self.situacoes["reprovados"].append(aluno)

    def listar_alunos(self):
        self.classificar_alunos()
        dados = []
        for situacao, alunos in self.situacoes.items():
            for aluno in alunos:
                dados.append(
                    {
                        "Turma": self.nome,
                        "ID": aluno.id,
                        "Nome": aluno.nome,
                        "Média": round(aluno.media_geral(), 2),
                        "Situação": situacao.capitalize(),
                    }
                )
        tabela = pd.DataFrame(dados)
        if tabela.empty:
            print("Nenhum aluno classificado")
        else:
            print(tabela.to_string(index=False))

    def mostrar_resumo(self):
        self.classificar_alunos()
        dados = []
        for situacao, alunos in self.situacoes.items():
            dados.append({"Situação": situacao.capitalize(), "Quantidade": len(alunos)})
        tabela = pd.DataFrame(dados)
        print(f"\nResumo da turma {self.nome}")
        print(tabela.to_string(index=False))
