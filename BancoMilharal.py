from datetime import datetime, timedelta

# Decorador para registrar data, hora e tipo de transação
def registrar_transacao(func):
    def wrapper(self, conta):
        self.data_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        tipo_transacao = type(self).__name__
        print(f"{self.data_hora} - {tipo_transacao}")
        result = func(self, conta)
        return result
    return wrapper

class Transacao:
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    @registrar_transacao
    def registrar(self, conta):
        conta.saldo += self.valor
        conta.historico.adicionar_transacao(self)

class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    @registrar_transacao
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

    def __iter__(self):
        return iter(self.transacoes)

    def transacoes_de_hoje(self):
        hoje = datetime.now().date()
        return [t for t in self.transacoes if datetime.strptime(t.data_hora, '%Y-%m-%d %H:%M:%S').date() == hoje]

class Conta:
    def __init__(self, cliente, numero):
        self.saldo = 0.0
        self.numero = numero
        self.cliente = cliente
        self.historico = Historico()

    def sacar(self, valor):
        if self.transacoes_diarias() < 10:
            saque = Saque(valor)
            if saque.registrar(self):
                return True
        else:
            print("Limite de transações diárias excedido.")
        return False

    def depositar(self, valor):
        if self.transacoes_diarias() < 10:
            deposito = Deposito(valor)
            deposito.registrar(self)
        else:
            print("Limite de transações diárias excedido.")

    def transacoes_diarias(self):
        return len(self.historico.transacoes_de_hoje())

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
        else:
            print("Número de saques diários excedido.")
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

class Contalterador:
    def __init__(self, contas):
        self._contas = contas
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self._contas):
            conta = self._contas[self._index]
            self._index += 1
            return conta
        raise StopIteration

menu = '''
MENU DE OPÇÕES:

Escolha uma operação para seguir:
[1] Depósito
[2] Saque
[3] Extrato
[4] Cadastrar nova conta
[5] Mudar de conta
[6] Sair
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
    for transacao in conta.historico:
        if isinstance(transacao, Deposito):
            print(f"{transacao.data_hora} - Depósito: R$ {transacao.valor:.2f}")
        elif isinstance(transacao, Saque):
            print(f"{transacao.data_hora} - Saque: R$ {transacao.valor:.2f}")
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
        contas = cadastrar_conta(contas, cliente_atual)
        conta_atual = selecionar_conta(contas, cliente_atual.cpf)

    elif opcao == "5":
        conta_atual = selecionar_conta(contas, cliente_atual.cpf)

    elif opcao == "6":
        print("Obrigado por usar o Banco Milharal. Até logo!")
        break

    else:
        print("Opção inválida, por favor selecione novamente a opção desejada.")
