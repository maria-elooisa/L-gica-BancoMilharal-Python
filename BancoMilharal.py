from datetime import date

class Transacao:
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        conta.saldo += self.valor
        conta.historico.adicionar_transacao(self)

class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if conta.saldo >= self.valor:
            conta.saldo -= self.valor
            conta.historico.adicionar_transacao(self)
            return True
        return False

class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)

class Conta:
    def __init__(self, cliente, numero):
        self.saldo = 0.0
        self.numero = numero
        self.cliente = cliente
        self.historico = Historico()

    def sacar(self, valor):
        saque = Saque(valor)
        if saque.registrar(self):
            return True
        return False

    def depositar(self, valor):
        deposito = Deposito(valor)
        deposito.registrar(self)

class ContaCorrente(Conta):
    def __init__(self, cliente, numero, limite, limite_saques):
        super().__init__(cliente, numero)
        self.limite = limite
        self.limite_saques = limite_saques
        self.numero_saques = 0

    def sacar(self, valor):
        if self.numero_saques < self.limite_saques:
            if super().sacar(valor):
                self.numero_saques += 1
                return True
        return False

class Cliente:
    def __init__(self, nome, cpf, data_nascimento, endereco):
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.endereco = endereco
        self.contas = []

    def adicionar_conta(self, conta):
        self.contas.append(conta)

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

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

clientes = []
contas = []
numero_conta_sequencial = 1

def encontrar_cliente_por_cpf(clientes, cpf):
    for cliente in clientes:
        if cliente.cpf == cpf:
            return cliente
    return None

def cadastrar_cliente(clientes):
    nome = input("Digite o nome do usuário: ")
    data_nascimento = input("Digite a data de nascimento (DD/MM/AAAA): ")
    cpf = input("Digite o CPF (somente números): ")

    if any(cliente.cpf == cpf for cliente in clientes):
        print("Já existe um cliente cadastrado com este CPF.")
        return clientes

    endereco = input("Digite o endereço (formato: logradouro, número - bairro - cidade/sigla estado): ")
    
    cliente = Cliente(nome, cpf, data_nascimento, endereco)
    clientes.append(cliente)
    print("Cliente cadastrado com sucesso!")
    return clientes

def cadastrar_conta(contas, cliente):
    global numero_conta_sequencial
    conta = ContaCorrente(cliente, numero_conta_sequencial, limite=500, limite_saques=3)
    cliente.adicionar_conta(conta)
    contas.append(conta)
    numero_conta_sequencial += 1
    print(f"Conta cadastrada com sucesso! Número da conta: {conta.numero}")
    return contas

def selecionar_conta(contas, cpf):
    contas_do_cliente = [conta for conta in contas if conta.cliente.cpf == cpf]
    if not contas_do_cliente:
        print("Nenhuma conta encontrada para este CPF.")
        return None
    print("Contas disponíveis:")
    for conta in contas_do_cliente:
        print(f"Agência: 0001 - Número da conta: {conta.numero}")
    numero_conta = int(input("Digite o número da conta que deseja acessar: "))
    for conta in contas_do_cliente:
        if conta.numero == numero_conta:
            return conta
    print("Número de conta inválido.")
    return None

def op_deposito(conta):
    valor = float(input("DIGITE O VALOR PARA REALIZAR O DEPÓSITO:\nR$: "))
    if valor > 0:
        conta.depositar(valor)
        print(f"Depósito realizado com sucesso! \n Novo saldo: R$ {conta.saldo:.2f}")
    else:
        print("Digite um valor válido.")

def op_saque(conta):
    valor = float(input("DIGITE O VALOR PARA REALIZAR O SAQUE:\nR$: "))
    if valor > conta.limite:
        print("Valor do saque excede o limite permitido.")
    elif valor > 0 and conta.sacar(valor):
        print(f"Saque realizado com sucesso! \n Novo saldo: R$ {conta.saldo:.2f}")
    else:
        print("Saldo insuficiente ou número de saques diários excedido.")

def op_extrato(conta):
    print("HISTÓRICO DE TRANSAÇÕES:")
    for transacao in conta.historico.transacoes:
        if isinstance(transacao, Deposito):
            print(f"Depósito: R$ {transacao.valor:.2f}")
        elif isinstance(transacao, Saque):
            print(f"Saque: R$ {transacao.valor:.2f}")
    print(f"Saldo atual: R$ {conta.saldo:.2f}")

while True:
    cpf = input(home).strip()
    cliente_atual = encontrar_cliente_por_cpf(clientes, cpf)

    if cliente_atual is None:
        print("CPF não encontrado. Você precisa se cadastrar.")
        clientes = cadastrar_cliente(clientes)
        cliente_atual = encontrar_cliente_por_cpf(clientes, cpf)
        contas = cadastrar_conta(contas, cliente_atual)
    else:
        print(f"Bem-vindo, {cliente_atual.nome}!")
        conta_atual = selecionar_conta(contas, cpf)
        if conta_atual is None:
            contas = cadastrar_conta(contas, cliente_atual)
            conta_atual = selecionar_conta(contas, cpf)
        break

while True:
    opcao = input(menu)

    if opcao == "1":
        op_deposito(conta_atual)

    elif opcao == "2":
        op_saque(conta_atual)

    elif opcao == "3":
        op_extrato(conta_atual)

    elif opcao == "4":
        print("Obrigado por usar o Banco Milharal. Até logo!")
        break

    else:
        print("Opção inválida, por favor selecione novamente a opção desejada.")
