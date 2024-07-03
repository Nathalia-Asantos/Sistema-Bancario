import textwrap
from abc import ABC, abstractmethod
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
    def __init__(self, cpf, nome, data_nascimento, endereco):
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
            print(f" Você sacou: R${valor:.2f}\n Saldo disponível: R${self._saldo:.2f}")
            return True
        else:
            print("Não foi possível completar a operação, tente novamente")
        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print(f" Você depositou: R${valor:.2f}\n Saldo disponível: R${self._saldo:.2f}")
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
            [transacao for transacao in self.historico.transacoes if transacao["Tipo"] == Saque.__name__]
        )
        excedeu_limite = valor > self.limite
        excedeu_saque = numero_saque >= self.LIMITE_SAQUE

        if excedeu_limite:
            print("Você tentou sacar mais do que o limite de saque, tente novamente")
        elif excedeu_saque:
            print("Você atingiu o número limite de saques diário, tente novamente amanhã")
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
        self._transacoes.append(
            {
                "Tipo" : transacao.__class__.__name__,
                "Valor" : transacao.valor,
                "Data" : datetime.now().strftime("%d/%m/%Y")
            }
        )

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
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
        sucesso_transacao = conta.depositar(self._valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

def menu():
    menu = """
       ====Menu====
       [1] Depositar
       [2] Sacar
       [3] Extrato
       [4] Cadastrar Cliente
       [5] Criar Conta
       [6] Informações de Conta
       [0] Sair
       ============
       """
    return input(textwrap.dedent(menu))

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("== Cliente não possui conta! ==")
        return

    return cliente.contas[0]

def depositar(clientes):
    cpf = input("Digite o CPF: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("== Cliente não encontrado! ==")
        return
    valor = float(input("Digite o valor que deseja depositar: "))
    transacao = Depositar(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    cpf = input("Digite o CPF: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("== Cliente não encontrado! ==")
        return
    valor = float(input("Digite o valor que deseja sacar: "))
    transacao = Saque(valor)
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("== Cliente não encontrado! ==")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n============== EXTRATO ==============")

    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['Tipo']}:\n\tR$ {transacao['Valor']:.2f}"

    print(extrato)
    print(f"\nSaldo atual:\n\tR$ {conta.saldo:.2f}")
    print("=====================================")

def criar_cliente(clientes):
    cpf = input("Digite seu CPF (somente números): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("== Esse CPF já está cadastrado no sistema! ==")
        return

    nome = input("Digite seu nome: ")
    print("Digite sua data de nascimento")
    while True:
        data_nascimento = data()
        if data_nascimento == False:
            continue
        else:
            break
    endereco = input("Digite seu endereço (logradouro, num - bairro - cidade/sigla estado):")

    cliente = PessoaFisica(cpf=cpf, nome=nome, data_nascimento=data_nascimento, endereco=endereco)
    clientes.append(cliente)
    print("==== Cliente criado com sucesso! ====")

def data():
    try:
        dia = int(input("Dia: "))
        mes = int(input("Mês: "))
        ano = int(input("Ano: "))
    except ValueError:
        print("== Entrada inválida, por favor insira números inteiros. ==")
        return False

    if mes < 1 or mes > 12 or ano < 1:
        print("== Data Inválida, digite novamente! ==")
        return False
    elif dia < 1 or dia > 31:
        print("== Data Inválida, digite novamente! ==")
        return False
    elif (mes == 4 or mes == 6 or mes == 9 or mes == 11) and dia > 30:
        print("== Data Inválida, digite novamente! ==")
        return False
    elif mes == 2:
        if dia > 29 or (dia == 29 and not verificaAnoBissexto(ano)):
            print("== Data Inválida, digite novamente! ==")
            return False
    else:
        data_nasc = f"{dia}/{mes}/{ano}"
        return data_nasc

def verificaAnoBissexto(ano):
    if (ano % 4 == 0 and ano % 100 != 0) or (ano % 400 == 0):
        return True
    else:
        return False

def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado! Para criar conta o CPF precisa estar cadastrado como cliente!")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.adicionar_conta(conta)

    print("==== Conta criada com sucesso! ====")
    print("================")
    print(f"Agência: {conta.agencia}")
    print(f"Número da conta: {conta.numero}")
    print(f"Titular: {conta.cliente.nome}")
    print("================")

def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))

def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "1":
            depositar(clientes)

        elif opcao == "2":
            sacar(clientes)

        elif opcao == "3":
            exibir_extrato(clientes)

        elif opcao == "4":
            criar_cliente(clientes)

        elif opcao == "5":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "6":
            listar_contas(contas)

        elif opcao == "0":
            print("Saindo do sistema...")
            break

        else:
            print("== Operação inválida, por favor selecione novamente a operação desejada ==")

main()