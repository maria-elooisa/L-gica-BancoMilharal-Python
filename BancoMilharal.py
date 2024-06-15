menu = '''
MENU DE OPÇÕES:

Escolha uma operação para seguir:
[1] Depósito
[2] Saque
[3] Extrato
[4] Sair
=> '''

home = '''
BEM-VINDO AO BANCO MILHARAL

Por favor digite o número do seu CPF para acessar sua conta:
'''
saldo = 0
limite = 500
extrato = ""
numero_saques = 0
limite_saques = 3
usuarios = []
contas = []
numero_conta_sequencial = 1

def op_deposito(saldo, extrato,/):
    deposito = float(input("DIGITE O VALOR PARA REALIZAR O DEPÓSITO:\nR$: "))
    if deposito > 0:
        saldo += deposito
        extrato += f"Depósito: R$ {deposito:.2f}\n"
        print(f"Depósito realizado com sucesso! \n Novo saldo: R$ {saldo:.2f}")
    else:
        print("Digite um valor válido.")
    return saldo, extrato

def op_saque(*,saldo, extrato, numero_saques, limite, limite_saques):
    if numero_saques >= limite_saques:
        print("Você atingiu seu limite de saques diário.")
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
    return saldo, extrato, numero_saques

def op_extrato(saldo, /, *, extrato):
    print("HISTÓRICO DE TRANSAÇÕES:")
    print(extrato if extrato else "Não foram realizadas movimentações.")
    print(f"Saldo atual: R$ {saldo:.2f}")
    return extrato

def cadastrar_usuario(usuarios):
    nome = input("Digite o nome do usuário: ")
    data_nascimento = input("Digite a data de nascimento (DD/MM/AAAA): ")
    cpf = input("Digite o CPF (somente números): ")

    if any(usuario['cpf'] == cpf for usuario in usuarios):
        print("Já existe um usuário cadastrado com este CPF.")
        return usuarios

    endereco = input("Digite o endereço (formato: logradouro, número - bairro - cidade/sigla estado): ")
    
    usuario = {
        'nome': nome,
        'data_nascimento': data_nascimento,
        'cpf': cpf,
        'endereco': endereco
    }
    usuarios.append(usuario)
    print("Usuário cadastrado com sucesso!")
    return usuarios

def listar_usuarios(usuarios):
    if not usuarios:
        print("Nenhum usuário cadastrado.")
    else:
        for usuario in usuarios:
            print(f"Nome: {usuario['nome']}, Data de Nascimento: {usuario['data_nascimento']}, CPF: {usuario['cpf']}, Endereço: {usuario['endereco']}")
    return usuarios

def encontrar_usuario_por_cpf(usuarios, cpf):
    for usuario in usuarios:
        if usuario['cpf'] == cpf:
            return usuario
    return None

def cadastrar_conta(contas, usuario):
    global numero_conta_sequencial
    agencia = "0001"
    conta = {
        'agencia': agencia,
        'numero_conta': numero_conta_sequencial,
        'usuario': usuario
    }
    contas.append(conta)
    numero_conta_sequencial += 1
    print(f"Conta cadastrada com sucesso! Número da conta: {conta['numero_conta']}")
    return contas

def selecionar_conta(contas, cpf):
    contas_do_usuario = [conta for conta in contas if conta['usuario']['cpf'] == cpf]
    if not contas_do_usuario:
        print("Nenhuma conta encontrada para este CPF.")
        return None
    print("Contas disponíveis:")
    for conta in contas_do_usuario:
        print(f"Agência: {conta['agencia']} - Número da conta: {conta['numero_conta']}")
    numero_conta = int(input("Digite o número da conta que deseja acessar: "))
    for conta in contas_do_usuario:
        if conta['numero_conta'] == numero_conta:
            return conta
    print("Número de conta inválido.")
    return None

while True:
    cpf = input(home).strip()
    usuario_atual = encontrar_usuario_por_cpf(usuarios, cpf)

    if usuario_atual is None:
        print("CPF não encontrado. Você precisa se cadastrar.")
        usuarios = cadastrar_usuario(usuarios)
        usuario_atual = encontrar_usuario_por_cpf(usuarios, cpf)
        contas = cadastrar_conta(contas, usuario_atual)
    else:
        print(f"Bem-vindo, {usuario_atual['nome']}!")
        conta_atual = selecionar_conta(contas, cpf)
        if conta_atual is None:
            contas = cadastrar_conta(contas, usuario_atual)
            conta_atual = selecionar_conta(contas, cpf)
        break

while True:
    opcao = input(menu)

    if opcao == "1":
        saldo, extrato = op_deposito(saldo, extrato)

    elif opcao == "2":
        saldo, extrato, numero_saques = op_saque(saldo=saldo, extrato=extrato, numero_saques=numero_saques, limite=limite, limite_saques=limite_saques)

    elif opcao == "3":
        extrato = op_extrato(saldo, extrato=extrato)

    elif opcao == "4":
        print("Obrigado por usar o Banco Milharal. Até logo!")
        break

    else:
        print("Opção inválida, por favor selecione novamente a opção desejada.")
