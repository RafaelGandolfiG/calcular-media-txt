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
