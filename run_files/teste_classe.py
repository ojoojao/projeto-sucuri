from datetime import datetime

class TesteCriaArquivo():
    def __init__(self):
        self.data = datetime.strftime(datetime.today(), "%d%m%Y %H%M%S")

    def cria_arquivo(self, nome: str):
        nome = nome + self.data + ".txt"
        with open(nome, "w", encoding='utf-8') as arquivo:
            arquivo.write("Olá mundo do arquivo criado pela classezinha sucuri")
        arquivo.close()

        return nome

if __name__ == "__main__":

    pasta = "C:/Users/jluca/Documents/python/sucuri/"
        
    teste = TesteCriaArquivo()
    nome = teste.cria_arquivo(pasta+"testeSucuri ")

    print(nome)

 
        