menu = """
====Menu====
[1] Depositar valor
[2] Sacar valor
[3] Extrato
[0] Sair
============
"""
saldo = 0.00
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3
valor = 0.00

while True:
    opcao = input(menu)

    if opcao == "1":
        valor = float(input("Digite o valor que deseja depositar: R$"))
        if valor > 0:
            saldo += valor
            extrato += f"Deposito: R${valor:.2f}\n"
            print(f" Você depositou: R${valor:.2f}\nSaldo disponível: R${saldo:.2f}")
        else:
            print("Não foi possível depositar, tente novamente")

    elif opcao == "2":
        print(f"""
 Saldo disponível: R${saldo:.2f} 
 Limite de saque: R${limite:.2f} 
 Saques disponíveis: {LIMITE_SAQUES - numero_saques}\n""")
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

    elif opcao == "3":
        if extrato == "":
            print("Não foram realizadas movimentações")
        else:
            print("========== EXTRATO =========")
            print(extrato)
            print(f"Saldo atual: R${saldo:.2f}")
            print("============================")

    elif opcao == "0":
        print("Saindo do sistema...")
        break
    else:
        print("Operação inválida, tente novamente")
print("Obrigado por utilizar nosso banco")
