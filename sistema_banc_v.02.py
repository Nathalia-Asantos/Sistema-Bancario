def depositar(valor, saldo, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Deposito: R${valor:.2f}\n"
        print(f" Você depositou: R${valor:.2f}\nSaldo disponível: R${saldo:.2f}")
    else:
        print("Não foi possível depositar, tente novamente")
    return saldo, extrato


def sacar(*, saldo, limite, extrato, numero_saques, LIMITE_SAQUES):
    if numero_saques < LIMITE_SAQUES and saldo > 0:
        valor = float(input("Digite o valor que deseja sacar: R$"))
        if 0 < valor <= limite and valor <= saldo:
            saldo -= valor
            numero_saques += 1
            extrato += f"Saque: R${valor:.2f}\n"
            print(f" Você sacou: R${valor:.2f}\n Saldo disponível: R${saldo:.2f}")
        elif valor > limite:
            print("Você tentou sacar mais do que o limite de saque, tente novamente")
        elif valor > saldo:
            print("Você tentou sacar um valor maior do que o saldo disponível, tente novamente")
        else:
            print("Não foi possível sacar, tente novamente")
    elif saldo == 0:
        print(f"O saldo disponível é de {saldo:.2f}, faça um deposito para poder sacar")
    elif numero_saques >= LIMITE_SAQUES:
        print("Você atingiu o numero limite de saque diário, tente novamente amanhã")
    else:
        print("Não foi possível completar a operação, tente novamente")
    return saldo, extrato, numero_saques


def f_extrato(saldo, /, *, extrato):
    if extrato == "":
        print("Não foram realizadas movimentações")
    else:
        print("========== EXTRATO =========")
        print(extrato)
        print(f"Saldo atual: R${saldo:.2f}")
        print("============================")

def criar_usuario(usuarios):
    cpf = input("Digite seu CPF (somente números): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("Esse CPF já está cadastrado no sistema!")
        return

    nome = input("Digite seu nome: ")
    print("Digite sua data de nascimento")
    data_nascimento = data()
    endereco = input("Digite seu endereço (logradouro, num - bairro - cidade/silga estado):")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "CPF": cpf,"endereco": endereco})
    print("usuário criado com sucesso!")


def filtrar_usuario(cpf, usuarios):
    usuarios_filtados= [usuario for usuario in usuarios if usuario["CPF"] == cpf]
    return usuarios_filtados[0] if usuarios_filtados else None

def criar_conta(AGENCIA, numero_conta, usuarios):
    cpf = input("Digite seu CPF: ")
    usuario = filtrar_usuario(cpf,usuarios)

    if usuario:
        print("=========================")
        print("Conta Criada com sucesso!")
        return {"Agência" : AGENCIA, "numero_conta": numero_conta, "usuario" : usuario}

    print("CPF não encontrado, digite um CPF já cadastrado como usuário")
    return None

def info_conta(contas):
    cpf = input("Digite seu CPF: ")
    conta = next((conta for conta in contas if conta["usuario"]["CPF"] == cpf), None)
    if conta:
        print("================")
        print(f"Agência: {conta['Agência']}")
        print(f"Número da conta: {conta['numero_conta']}")
        print(f"Titular: {conta['usuario']['nome']}")
        print("================")
    else:
        print("Conta não encontrada para o CPF informado")

def data():
    dia = int(input("Dia:"))
    mes = int(input("Mês:"))
    ano = int(input("Ano:"))
    data_nasc = f"{dia}/{mes}/{ano}"
    return data_nasc

def main():
    menu = """
    ====Menu====
    [1] Depositar valor
    [2] Sacar valor
    [3] Extrato
    [4] Cadastrar Usuário
    [5] Criar Conta
    [6] Informações de Conta
    [0] Sair
    ============
    """
    saldo = 0.00
    limite = 500
    extrato = ""
    numero_saques = 0
    LIMITE_SAQUES = 3
    AGENCIA = "0001"
    valor = 0.00
    usuarios = []
    contas = []
    numero_conta = 0


    while True:
        opcao = input(menu)

        if opcao == "1":
            valor = float(input("Digite o valor que deseja depositar: R$"))
            saldo, extrato = depositar(valor, saldo, extrato)

        elif opcao == "2":
            print(f"""
     Saldo disponível: R${saldo:.2f} 
     Limite de saque: R${limite:.2f} 
     Saques disponíveis: {LIMITE_SAQUES - numero_saques}\n""")
            saldo, extrato, numero_saques = sacar(saldo=saldo, limite=limite, extrato=extrato, numero_saques=numero_saques, LIMITE_SAQUES=LIMITE_SAQUES)

        elif opcao == "3":
            f_extrato(saldo, extrato=extrato)

        elif opcao == "4":
            criar_usuario(usuarios)

        elif opcao == "5":
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)
                numero_conta += 1

        elif opcao == "6":
            info_conta(contas)

        elif opcao == "0":
            print("Saindo do sistema...")
            break
        else:
            print("Operação inválida, tente novamente")
    print("Obrigado por utilizar nosso banco")

main()