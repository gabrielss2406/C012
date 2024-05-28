import sys
import threading
import time
import random
from queue import Queue


# Classe que representa cada personagem do jogo
class Personagem(threading.Thread):
    lista_personagens: list['Personagem'] = []  # Lista compartilhada de todos os personagens
    pausar_threads = False  # Flag para pausar os threads

    def __init__(
            self,
            nome: str,
            vida: int,
            dano: int,
            velocidade: int,
            accuracy: int,
            habilidade: str,
            turno: int
    ):
        super().__init__()
        # Ajusta os atributos baseados na habilidade do personagem
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
        self.turno = turno
        self.tempo_espera = 0  # Tempo de espera do personagem

        # Define o tipo de arma baseado no dano
        if dano <= 12:
            self.arma = "socou"
        elif dano < 15:
            self.arma = "esfaqueou"
        elif dano <= 18:
            self.arma = "atirou em"
        else:
            self.arma = "bazucou"

    # Método para o personagem receber dano
    def receber_dano(self, dano: float):
        self.vida = round(self.vida - dano, 2)
        if self.vida <= 0:
            self.vivo = False
            Personagem.lista_personagens.remove(self)  # Remove o personagem da lista

    # Aplica modificadores baseados na habilidade do personagem
    def aplicar_modificador(self, outro_personagem: 'Personagem'):
        if self.habilidade == "encegamento":
            outro_personagem.accuracy -= 1
        elif self.habilidade == "vampirismo":
            self.vida += self.dano * 0.20
        elif self.habilidade == "ladino":
            self.dano += 1
            outro_personagem.dano -= 1

    # Método para o personagem atacar outro personagem
    def atacar(self, outro_personagem: 'Personagem'):
        aim = random.randint(0, 100)  # Gera um valor aleatório para a precisão do ataque

        if aim >= self.accuracy:
            print(f"{self.nome} errou o tiro em {outro_personagem.nome}!")
            return

        elif outro_personagem.vivo and self.vivo:
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

    # Imprime o status atual do personagem
    def imprimir_status(self):
        print(f"Nome: {self.nome}, "
              f"Vida: {self.vida}, "
              f"Dano: {self.dano}, "
              f"Velocidade: {self.velocidade}, "
              f"Precisão: {self.accuracy}, "
              f"Habilidade: {self.habilidade}, "
              f"Arma: {self.arma}, "
              f"Tempo de Espera: {self.tempo_espera}")
        print("===================")

    # Método run que define o comportamento do thread do personagem
    def run(self):
        while self.vivo:
            if Personagem.pausar_threads:
                time.sleep(10)  # Pausa de 10 segundos
            time.sleep(5 - self.velocidade)  # Espera baseada na velocidade do personagem

            global fila_personagens
            with lock:
                fila_personagens.put(self)  # Adiciona o personagem à fila de execução
            time.sleep(0.1)  # Pequena espera para permitir a adição de todos os personagens


# Inicializa a fila de personagens e a trava para sincronização
fila_personagens = Queue()
lock = threading.Lock()  # Executar uma thread por vez 


# Função que implementa o escalonador SJF
def sjf_scheduler():
    sjf_start_time = time.time()
    global fila_personagens
    start_time = time.time()  # Marca o início da execução do escalonador
    while True:
        with lock:
            if not fila_personagens.empty():
                personagens_vivos = [p for p in Personagem.lista_personagens if p.vivo]
                if not personagens_vivos:
                    break
                personagem = min(personagens_vivos,
                                 key=lambda p: p.velocidade)  # Seleciona o personagem com menor velocidade
                try:
                    fila_personagens.queue.remove(personagem)  # Remove o personagem da fila
                except ValueError:
                    continue
                outro_personagem = random.choice([p for p in personagens_vivos if p != personagem])
                personagem.atacar(outro_personagem)

                personagem.tempo_espera += time.time() - start_time  # Calcula o tempo de espera do personagem
                start_time = time.time()  # Reinicia o tempo de início para o próximo personagem

        vivos = [personagem for personagem in Personagem.lista_personagens if personagem.vivo]
        if len(vivos) == 1:
            print(f"{vivos[0].nome} é o último sobrevivente e venceu o Battle Royale!")
            break

        time.sleep(1)
    sjf_end_time = time.time()

    # Cálculo da média de tempo de espera
    total_espera = sum(p.tempo_espera for p in Personagem.lista_personagens)
    media_espera = total_espera / len(Personagem.lista_personagens)
    print(f"Média de Tempo de Espera: {media_espera:.2f} unidades de tempo")
    print(f"Tempo de execução do SJF: {round(sjf_end_time - sjf_start_time, 3)} segundos")


# Cria os personagens
personagens = []
nomes = ["Personagem 1", "Personagem 2", "Personagem 3"]
habilidades = ["vampirismo", "comum", "encegamento", "ladino", "veloz", "tanque", "forte"]
for i, nome in enumerate(nomes):
    vida = random.randint(80, 125)
    dano = random.randint(10, 20)
    velocidade = random.randint(1, 2) if vida > 100 else random.randint(2, 3)
    precisao_max = min(90, 100 - dano)
    precisao = random.randint(70, precisao_max)

    personagem = Personagem(nome=nome,
                            vida=vida,
                            dano=dano,
                            velocidade=velocidade,
                            accuracy=precisao,
                            habilidade=random.choice(habilidades),
                            turno=i)
    personagens.append(personagem)

Personagem.lista_personagens = personagens

# Imprime o status inicial de todos os personagens
for personagem in personagens:
    personagem.imprimir_status()

# Inicia os threads dos personagens
for personagem in personagens:
    personagem.start()

# Inicia o thread do escalonador
thread_escalonador = threading.Thread(target=sjf_scheduler, daemon=True)
thread_escalonador.start()

# Espera pelo término de todos os threads de personagens
for personagem in personagens:
    personagem.join()

thread_escalonador.join()

print("Battle Royale encerrado.")
