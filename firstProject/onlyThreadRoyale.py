import threading
import time
import random


class Personagem(threading.Thread):
    lista_personagens: list['Personagem'] = []

    def __init__(
            self,
            nome: str,
            vida: int,
            dano: int,
            velocidade: int,
            accuracy: int,
            habilidade: str
    ):
        super().__init__()
        if habilidade == "veloz":
            velocidade += 1
        elif habilidade == "forte":
            dano *= 1.2
        elif habilidade == "tanque":
            vida *= 1.1

        self.nome = nome
        self.vida = round(vida, 2)
        self.dano = round(dano, 2)
        self.velocidade = velocidade
        self.accuracy = accuracy
        self.habilidade = habilidade
        self.vivo = True

        if dano <= 12:
            self.arma = "socou"
        elif dano < 15:
            self.arma = "esfaqueou"
        elif dano <= 18:
            self.arma = "atirou em"
        else:
            self.arma = "bazucou"

    def receber_dano(self, dano: float):
        self.vida = round(self.vida - dano, 2)
        if self.vida <= 0:
            self.vivo = False
            Personagem.lista_personagens.remove(self)

    def aplicar_modificador(self, outro_personagem: 'Personagem'):
        if self.habilidade == "encegamento":
            outro_personagem.accuracy -= 1
        elif self.habilidade == "vampirismo":
            self.vida += self.dano * 0.25
        elif self.habilidade == "ladino":
            self.dano += 1
            outro_personagem.dano -= 1

    def atacar(self, outro_personagem: 'Personagem'):
        aim = random.randint(0, 100)
        if aim >= self.accuracy:
            print(f"{self.nome} errou o tiro em {outro_personagem.nome}!")

        elif outro_personagem.vivo and self.vivo:
            if aim <= 10:
                self.aplicar_modificador(outro_personagem)
                outro_personagem.receber_dano(round(self.dano * 1.5))
                print(f"{self.nome} deu um CRITICO em {outro_personagem.nome} "
                      f"causando {round(self.dano * 1.5, 2)} de dano.")
            else:
                self.aplicar_modificador(outro_personagem)
                outro_personagem.receber_dano(round(self.dano))
                print(f"{self.nome} {self.arma} {outro_personagem.nome} causando {round(self.dano, 2)} de dano.")

            if outro_personagem.vivo:
                print(f"{outro_personagem.nome} tem {outro_personagem.vida} de vida restante.")
            else:
                print(f"{outro_personagem.nome} morreu.")

    def imprimir_status(self):
        print(f"Nome: {self.nome}, "
              f"Vida: {self.vida}, "
              f"Dano: {self.dano}, "
              f"Velocidade: {self.velocidade}, "
              f"Precisão: {self.accuracy}, "
              f"Habilidade: {self.habilidade}")
        print("===================")

    def run(self):
        while self.vivo:
            time.sleep(5-self.velocidade)

            outro_personagem = random.choice(Personagem.lista_personagens)
            if outro_personagem is not self:
                self.atacar(outro_personagem)

            if len(Personagem.lista_personagens) == 1:
                if Personagem.lista_personagens[0] == self:
                    print(f"{Personagem.lista_personagens[0].nome} é o último sobrevivente e "
                          f"venceu o Battle Royale com {Personagem.lista_personagens[0].vida} de vida!")
                break


# Criando os personagens
personagens = []
nomes = [
    "Alice de Lorenzo Coelho",
    "Álisson Feliciano Pontes Morais",
    "Álvaro Lúcio Almeida Ribeiro",
    "Arthur Bueno Silva",
    "Augusto Teixeira Roberto",
    "Bárbara Martins Barbieri",
    "Breno Carvalho do Nascimento",
    "Bruno Vinícius Santos",
    "Davi Rosa Gomes",
    "Diogo Antonio Castro dos Santos",
    "Eduardo Karpfenstein",
    "Ewel Fernandes Pereira",
    "Fabio Augusto Gandra Cruvinel",
    "Felipe da Silva Inácio",
    "Felipe Henrique Conrado",
    "Fernanda Ellen de Souza",
    "Francisco Pereira Guimarães",
    "Frederico Flauzino Wlassow",
    "Gabriel Almeida Dias",
    "Gabriel Alves Fernandes",
    "Gabriel de Souza Siqueira",
    "Gabriel Filhagosa Guimarães",
    "Giovani Furigo Finazzi",
    "Guilherme Muniz de Oliveira Reis",
    "Humberto Gomes Fernandes Santos",
    "Jéssica Guerzoni Figueiredo Silva",
    "João Marcos Coutinho Nunes",
    "João Pedro Maciel de Souza",
    "Laura Pivoto Ambrósio",
    "Lucas Belino Da Silva",
    "Lucas Mendes Ribeiro do Couto",
    "Luiz Matheus Rodrigues Cândido",
    "Marcos Guerra Soares",
    "Marcos Henrique Barbosa Pereira",
    "Marcos Vinicius Correia Sanches",
    "Matheus Henrique Fonseca Afonso",
    "Matheus Lima Pereira",
    "Natacha Calixto Garcia Ribeiro",
    "Nicholas do Vale Siécola",
    "Pedro Guilherme Fernandes Oliveira",
    "Pedro Henrique Passos Carreira",
    "Pedro Luis Dionísio Fraga",
    "Raissa Beatriz Carlucio",
    "Raíssa Rodrigues de Souza",
    "Samuel Freitas Macedo Soares",
    "Sarah Alves Chagas",
    "Thomas Ceccon Guimarães",
    "Victor Boaventura Souza Muniz",
    "Vitor André Brochado Wogel da Costa",
    "Vitor Oliveira Juliano de Almeida",
    "Vitor Pestalozi de Oliveira Chagas",
    "Ygor Silva Costa",
    "Yves Antonio Guimarães Ribeiro"
]
habilidades = ["vampirismo", "comum", "encegamento", "ladino", "veloz", "tanque", "forte"]
for nome in nomes:
    vida = random.randint(80, 125)
    dano = random.randint(10, 20)
    velocidade = random.randint(1, 2) if vida > 100 else random.randint(2, 3)
    precisao_max = min(90, 100 - dano)
    precisao = random.randint(70, precisao_max)

    # Criando e retornando o personagem
    personagem = Personagem(nome=nome,
                            vida=vida,
                            dano=dano,
                            velocidade=velocidade,
                            accuracy=precisao,
                            habilidade=random.choice(habilidades))
    personagens.append(personagem)

Personagem.lista_personagens = personagens

for personagem in personagens:
    personagem.imprimir_status()

# Iniciando a batalha
for personagem in personagens:
    personagem.start()

# Esperando até que todos os personagens terminem a batalha
for personagem in personagens:
    personagem.join()

print("Battle Royale encerrado.")