menu = '''
BEM-VINDO AO BANCO MILHARAL

Escolha uma operação para seguir:
[1] Depósito
[2] Saque
[3] Extrato
[4] Sair
=> '''

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
limite_saques = 3

while True:
    opcao = input(menu)

    if opcao == "1":
        deposito = float(input("DIGITE O VALOR PARA REALIZAR O DEPÓSITO:\nR$: "))
        if deposito > 0:
            saldo += deposito
            extrato += f"Depósito: R$ {deposito:.2f}\n"
            print(f"Depósito realizado com sucesso! \n Novo saldo: R$ {saldo:.2f}")
        else:
            print("Digite um valor válido.")

    elif opcao == "2":
        if numero_saques >= limite_saques:
            print("Você atingiu seu limite de saques diário.")
            continue

        saque = float(input("DIGITE O VALOR PARA REALIZAR O SAQUE:\nR$: "))
        
        if saque > saldo:
            print("Saldo insuficiente! \n Operação cancelada.")
        elif saque > limite:
            print("Valor do saque excede o limite permitido.")
        elif saque > 0:
            saldo -= saque
            extrato += f"Saque: R$ {saque:.2f}\n"
            numero_saques += 1
            print(f"Saque realizado com sucesso! \n Novo saldo: R$ {saldo:.2f}")
        else:
            print("Digite um valor válido.")

    elif opcao == "3":
        print("HISTÓRICO DE TRANSAÇÕES:")
        print(extrato if extrato else "Não foram realizadas movimentações.")
        print(f"Saldo atual: R$ {saldo:.2f}")

    elif opcao == "4":
        print("Obrigado por usar o Banco Milharal. Até logo!")
        break

    else:
        print("Opção inválida, por favor selecione novamente a opção desejada.")
