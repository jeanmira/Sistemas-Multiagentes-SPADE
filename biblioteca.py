# ------------------------------- /usr/bin/g++-7 ------------------------------#
# ------------------------------- coding: utf-8 -------------------------------#
# Criado por:   Jean Marcelo Mira Junior
#               Victor Philos Donato Luiz da Silva
# Versão: 2.0
# Criado em: 08/03/2021
# Sistema operacional: Linux - Ubuntu 20.04.1 LTS
# Python 3
# ------------------------------ Pacotes --------------------------------------#
import random
import math
import time
from spade.agent import Agent
from spade.template import Template
from spade.behaviour import CyclicBehaviour
from spade.behaviour import OneShotBehaviour
from spade.message import Message

# -----------------------------------------------------------------------------#

# ----------------
def inicializar(agente1, senha1, agente2, senha2):
    solucionar = Resolvedor(agente1, senha1)
    problema = Gerador(agente2, senha2)

    # problema.web.start(hostname="127.0.0.1", port="10000")

    problema.start()
    time.sleep(10)
    solucionar.start()
    espera()


def espera():
    print("Espere até que o usuário interrompa com ctrl + Z")
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break


class Resolvedor(Agent):
    class recebeFuncao(OneShotBehaviour):
        async def run(self):
            msg = Message(to="jeanmu@jix.im")
            msg.set_metadata("performative", "request")
            msg.body = "Qual o grau da função?"
            await self.send(msg)
            print("Pediu para " + "vphilos2@jix.im" + ": " + msg.body)

    class encontraRaiz(CyclicBehaviour):
        async def run(self):
            global x_chute
            global comparar
            global a
            global b
            res = await self.receive(timeout=5)
            # print("Resposta:", res.body)
            # time.sleep(2)
            # print("Entrou")
            if res:
                if res.body != "1grau" and res.body != "2grau" and res.body != "3grau":
                    # x = random.randint(-1000, 1000)
                    # --------------------------------------
                    fx = int(res.body)
                    # bissecta o intervalo
                    if fx > 0:
                        a = x_chute
                    else:
                        b = x_chute
                else:
                    a = -1000
                    b = 1000
                    x_chute = 0
                    comparar = 0

                x_chute = (a + b) / 2

                if comparar == x_chute:
                    x_chute *= -1

                comparar = x_chute

                # --------------------------------------
                msg = Message(to=str(res.sender))
                msg.set_metadata("performative", "subscribe")
                msg.body = str(int(x_chute))

                await self.send(msg)
                print(
                    "Transmitiu para " + str(res.sender) + " x = " + str(int(x_chute))
                )

    async def setup(self):
        self.add_behaviour(self.recebeFuncao())
        self.add_behaviour(self.encontraRaiz())


class Gerador(Agent):
    grau = random.randint(1, 3)  # Gera nuemro aleatorio de 1 a 3
    x = random.randint(-1000, 1000)  # Gera o valor de x

    # Para a equacao do primeiro grau
    if grau == 1:
        a = 0
        while a == 0:
            a = random.randint(-100, 100)
        y = (a * x) * (-1)

    # Para a equacao do segundo grau
    if grau == 2:
        a = b = 0
        while a == 0:
            a = random.randint(-100, 100)
        while b == 0:
            b = random.randint(-100, 100)
        y = ((a * x * x) + (b * x)) * (-1)

    # Para a equacao do terceiro grau
    if grau == 3:
        a = b = c = 0
        while a == 0:
            a = random.randint(-100, 100)
        while b == 0:
            b = random.randint(-100, 100)
        while c == 0:
            c = random.randint(-100, 100)
        y = ((a * x * x * x) + (b * x * x) + (c * x)) * (-1)

        class primeiroGrau(CyclicBehaviour):
            async def run(self):
                res = await self.receive(timeout=5)
                if res:
                    x = float(res.body)
                    x = float(Gerador.a * x + Gerador.y)
                    print(
                        "Transmitiu para " + str(res.sender) + " f(",
                        res.body,
                        ") = ",
                        x,
                        "=>",
                        int(x),
                    )
                    msg = Message(to=str(res.sender))
                    msg.set_metadata("performative", "inform")
                    msg.body = str(int(x))
                    if float(x) == 0:
                        await self.agent.stop()
                        print(
                            "A função",
                            Gerador.a,
                            "x + (",
                            Gerador.y,
                            ") tem raiz: ",
                            str(float(res.body)),
                        )
                    else:
                        await self.send(msg)

    class segundoGrau(CyclicBehaviour):
        async def run(self):
            res = await self.receive(timeout=5)
            if res:
                x = float(res.body)
                x = float(Gerador.a * x * x + Gerador.b * x + Gerador.y)
                print(
                    "Transmitiu para " + str(res.sender) + " f(",
                    res.body,
                    ") = ",
                    x,
                    "=>",
                    int(x),
                )
                msg = Message(to=str(res.sender))
                msg.set_metadata("performative", "inform")
                msg.body = str(int(x))
                if float(x) == 0:
                    await self.agent.stop()
                    print(
                        "A função",
                        Gerador.a,
                        "x^2 + (",
                        Gerador.b,
                        ")x + (",
                        Gerador.y,
                        ") tem raiz: ",
                        str(float(res.body)),
                    )
                else:
                    await self.send(msg)

    class terceiroGrau(CyclicBehaviour):
        async def run(self):
            res = await self.receive(timeout=5)
            if res:
                x = float(res.body)
                x = float(
                    Gerador.a * x * x * x
                    + Gerador.b * x * x
                    + Gerador.c * x
                    + Gerador.y
                )
                print(
                    "Transmitiu para " + str(res.sender) + " f(",
                    res.body,
                    ") = ",
                    x,
                    "=>",
                    int(x),
                )
                msg = Message(to=str(res.sender))
                msg.set_metadata("performative", "inform")
                msg.body = str(int(x))
                if float(x) == 0:
                    await self.agent.stop()
                    print(
                        "A função",
                        Gerador.a,
                        "x^3 + (",
                        Gerador.b,
                        ")x^2 + (",
                        Gerador.c,
                        ")x + (",
                        Gerador.y,
                        ") tem raiz: ",
                        str(float(res.body)),
                    )
                else:
                    await self.send(msg)

    class grauFuncao(CyclicBehaviour):
        async def run(self):
            res = await self.receive(timeout=5)
            if res:
                msg = Message(to=str(res.sender))
                msg.set_metadata("performative", "inform")

                if Gerador.grau == 1:
                    msg.body = "1grau"

                if Gerador.grau == 2:
                    msg.body = "2grau"

                if Gerador.grau == 3:
                    msg.body = "3grau"

                await self.send(msg)
                print("Respondeu para " + str(res.sender) + " com: " + msg.body)

    async def setup(self):
        t = Template()
        t.set_metadata("performative", "subscribe")

        if Gerador.grau == 1:
            print("Gerou função de primeiro grau com x: ", Gerador.x)
            print("Função: ", Gerador.a, "x + (", Gerador.y, ")")
            tf1 = self.primeiroGrau()
            self.add_behaviour(tf1, t)

        if Gerador.grau == 2:
            print("Gerou função de segundo grau com x: ", Gerador.x)
            print("Função: ", Gerador.a, "x^2 + (", Gerador.b, ")x + (", Gerador.y, ")")
            tf2 = self.segundoGrau()
            self.add_behaviour(tf2, t)

        if Gerador.grau == 3:
            print("Gerou função de terceiro grau com x: ", Gerador.x)
            print(
                "Função: ",
                Gerador.a,
                "x^3 + (",
                Gerador.b,
                ")x^2 + (",
                Gerador.c,
                ")x + (",
                Gerador.y,
                ")",
            )
            tf3 = self.terceiroGrau()
            self.add_behaviour(tf3, t)

        ft = self.grauFuncao()
        template = Template()
        template.set_metadata("performative", "request")
        self.add_behaviour(ft, template)
