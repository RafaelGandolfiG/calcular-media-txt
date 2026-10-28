class Materia:
    def __init__(self, nome, professor):
        self.nome = nome
        self.professor = professor

    def mostrar_infos(self):
        print(f"{'Nome':<15} | {'Professor':<15}")
        print(f"{self.nome:<15} | {self.professor:<15}")
