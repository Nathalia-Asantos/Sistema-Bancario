from abc import ABC, abstractmethod, abstractproperty, abstractclassmethod
from datetime import datetime

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento,endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0.00
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = saldo < valor
        if excedeu_saldo:
            print("Você tentou sacar um valor maior do que o saldo disponível, tente novamente")
        elif saldo > 0:
            self._saldo -= valor
            print(f" Você sacou: R${valor:.2f}\n Saldo disponível: R${saldo:.2f}")
            return True
        else:
            print("Não foi possível completar a operação, tente novamente")
        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print(f" Você depositou: R${valor:.2f}\nSaldo disponível: R${self._saldo:.2f}")
        else:
            print("Não foi possível depositar, tente novamente")
            return False
        return True

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, LIMITE_SAQUE=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.LIMITE_SAQUE = LIMITE_SAQUE

    def sacar(self, valor):
        numero_saque = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )
        excedeu_limite = valor > self.limite
        excedeu_saque = numero_saque >= self.LIMITE_SAQUE

        if excedeu_limite:
            print("Você tentou sacar mais do que o limite de saque, tente novamente")
        elif excedeu_saque:
            print("Você atingiu o numero limite de saques diário, tente novamente amanhã")
        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
        Agência :\t {self.agencia}
        Conta Corrente:\t\t {self.numero}
        Titular:\t {self.cliente.nome}"""

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacao.append(
            {
                "Tipo" : transacao.__class__.__name__,
                "Valor" : transacao.valor,
                "Data" : datetime.now().strftime("%d/%m/%Y")
            }
        )

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self._valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Depositar(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self._valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)