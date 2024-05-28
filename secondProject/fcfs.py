import queue
import threading
import time
import random


class Personagem:
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
        self.tempo_espera = 0

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


q = queue.Queue()


def fcfs_scheduler() -> None:
    start_time = time.time()

    while True:
        time.sleep(1)
        personagem = q.get()

        # verifica se o personagem está vivo
        if not personagem.vivo:
            q.task_done()
        else:
            # selecionando os inimigos vivos
            queue_copy = list(q.queue).copy()
            inimigos_vivos = []

            for elemento in queue_copy:
                if elemento.vivo:
                    inimigos_vivos.append(elemento)
            # caso exista algum inimigo, vivo ele será atacado
            if len(inimigos_vivos) > 0:
                outro_personagem = random.choice(inimigos_vivos)
                time.sleep(5 - personagem.velocidade)
                personagem.atacar(outro_personagem)

            # termina o turno e coloca o personagem no fim da fila
            q.task_done()
            personagem.tempo_espera += time.time() - start_time
            start_time = time.time()
            q.put(personagem)

            # caso a fila tenha apenas um personagem o jogo acaba
            if q.qsize() == 1:
                print(f"{personagem.nome} é o último sobrevivente e "
                      f"venceu o Battle Royale com {personagem.nome} de vida!")
                q.task_done()
                break

    total_espera = sum(p.tempo_espera for p in Personagem.lista_personagens)
    media_espera = total_espera / len(Personagem.lista_personagens)
    print(f"Média de Tempo de Espera: {media_espera:.2f} unidades de tempo")

    return None


# Criando os personagens
personagens = []
nomes = ["Personagem 1", "Personagem 2", "Personagem 3"]
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

# mostrando os dados dos personagens
for personagem in personagens:
    personagem.imprimir_status()

fcfs_start_time = time.time()

threading.Thread(target=fcfs_scheduler).start()

for personagem in Personagem.lista_personagens:
    q.put(personagem)

# esperando as threads terminarem
q.join()
print("Battle Royale encerrado.")

fcfs_end_time = time.time()

print(f"Tempo de execução do FCFS: {round(fcfs_end_time - fcfs_start_time, 3)} segundos")
