import threading
import time
import random
from queue import Queue

class ArmaUnica:
    def __init__(self):
        self.semaphore = threading.Semaphore(1)  # Inicializa o semáforo com valor inicial de 1 (disponível)

    def tentar_pegar_arma(self) -> bool:
        return self.semaphore.acquire(blocking=False)  # Tenta adquirir o semáforo sem bloquear

    def soltar_arma(self):
        self.semaphore.release()  # Libera o semáforo


class Personagem(threading.Thread):
    lista_personagens: list['Personagem'] = []
    pausar_threads = False

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
        self.arma_unica = False  # Indica se o personagem possui a arma única
        self.turno = turno

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
            if self.arma_unica:
                arma_unica.soltar_arma()  # Solta a arma única se o personagem morrer
            Personagem.lista_personagens.remove(self)

    def aplicar_modificador(self, outro_personagem: 'Personagem'):
        if self.habilidade == "encegamento":
            outro_personagem.accuracy -= 1
        elif self.habilidade == "vampirismo":
            self.vida += self.dano * 0.20
        elif self.habilidade == "ladino":
            self.dano += 1
            outro_personagem.dano -= 1

    def atacar(self, outro_personagem: 'Personagem'):
        aim = random.randint(0, 100)

        if aim >= self.accuracy:
            print(f"{self.nome} errou o tiro em {outro_personagem.nome}!")
            return

        elif outro_personagem.vivo and self.vivo:
            if aim <= 15:
                # Tenta adquirir a arma única
                if arma_unica.tentar_pegar_arma():  # Verifica se o personagem já possui a arma única
                    self.dano += 5  # Aumenta o dano do personagem em 5 pontos
                    self.aplicar_modificador(outro_personagem)
                    outro_personagem.receber_dano(round(self.dano))  # Dano dobrado com a arma única
                    print(f"{self.nome} PEGOU a arma única e deu um ataque em {outro_personagem.nome}, "
                          f"causando {self.dano} de dano.")
                    if outro_personagem.vivo:
                        print(f"{outro_personagem.nome} tem {outro_personagem.vida} de vida restante.")
                    else:
                        print(f"{outro_personagem.nome} foi nocauteado(a).")
                else:
                    # Se não pegar a arma única ou já possuir, ataca normalmente
                    self.aplicar_modificador(outro_personagem)
                    outro_personagem.receber_dano(round(self.dano))
                    print(f"{self.nome} {self.arma} {outro_personagem.nome} causando {round(self.dano, 2)} de dano.")
                    if outro_personagem.vivo:
                        print(f"{outro_personagem.nome} tem {outro_personagem.vida} de vida restante.")
                    else:
                        print(f"{outro_personagem.nome} foi nocauteado(a).")
            else:
                # Ataque normal se não for um ataque crítico
                self.aplicar_modificador(outro_personagem)
                outro_personagem.receber_dano(round(self.dano))
                print(f"{self.nome} {self.arma} {outro_personagem.nome} causando {round(self.dano, 2)} de dano.")
                if outro_personagem.vivo:
                    print(f"{outro_personagem.nome} tem {outro_personagem.vida} de vida restante.")
                else:
                    print(f"{outro_personagem.nome} foi nocauteado(a).")

    def imprimir_status(self):
        print(f"Nome: {self.nome}, "
              f"Vida: {self.vida}, "
              f"Dano: {self.dano}, "
              f"Velocidade: {self.velocidade}, "
              f"Precisão: {self.accuracy}, "
              f"Habilidade: {self.habilidade}, "
              f"Arma Única: {'Sim' if self.arma_unica else 'Não'}")
        print("===================")

    def run(self):
        while self.vivo:
            if Personagem.pausar_threads:
                time.sleep(10)
            time.sleep(5-self.velocidade)

            # Agora vamos usar uma fila para o escalonamento
            global fila_personagens
            fila_personagens.put(self)
            time.sleep(0.1)  # Garantir que todos os personagens sejam adicionados à fila


# Inicialize a fila de personagens
fila_personagens = Queue()

# Função que executa o escalonamento
def round_robin():
    global fila_personagens
    while True:
        if not fila_personagens.empty():
            personagem = fila_personagens.get()
            outro_personagem = random.choice(Personagem.lista_personagens)
            if outro_personagem is not personagem and personagem.vivo:
                personagem.atacar(outro_personagem)
        time.sleep(2)

# Inicialize a arma única
arma_unica = ArmaUnica()

# Criando os personagens
personagens = []
nomes = ["Personagem 1", "Personagem 2", "Personagem 3"]  # Adicione mais nomes conforme necessário
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

# Iniciar threads para personagens e escalonador
for personagem in personagens:
    personagem.start()

thread_escalonador = threading.Thread(target=round_robin)
thread_escalonador.start()

while True:
    if len(Personagem.lista_personagens) == 1:
        break

    comando = input("Digite '%' para pausar por 10 segundos e imprimir informações dos personagens ou 'd' para encerrar': ")
    if comando == "%":
        Personagem.pausar_threads = True
        time.sleep(4) # esperando todas pausarem
        for personagem in personagens:
            personagem.imprimir_status()
        time.sleep(8)  # Pausa por 8 segundos
        Personagem.pausar_threads = False

# Aguardando o término de todas as threads
for personagem in personagens:
    personagem.join()

thread_escalonador.join()

print("Battle Royale encerrado.")
