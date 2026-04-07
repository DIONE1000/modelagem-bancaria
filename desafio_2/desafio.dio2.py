from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import date, datetime
from typing import List

# ==========================================
# 1. CLASSES DE TRANSAÇÃO (INTERFACES)
# ==========================================
class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self) -> float:
        pass

    @abstractmethod
    def registrar(self, conta: Conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor: float):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta: Conta):
        sucesso = conta.depositar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)

class Saque(Transacao):
    def __init__(self, valor: float):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta: Conta):
        sucesso = conta.sacar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)

# ==========================================
# 2. CLASSE HISTÓRICO
# ==========================================
class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao: Transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )

# ==========================================
# 3. CLASSES DE CLIENTE
# ==========================================
class Cliente:
    def __init__(self, endereco: str):
        self.endereco = endereco
        self.contas: List[Conta] = []

    def realizar_transacao(self, conta: Conta, transacao: Transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta: Conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, cpf: str, nome: str, data_nascimento: date, endereco: str):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

# ==========================================
# 4. CLASSES DE CONTA
# ==========================================
class Conta:
    def __init__(self, numero: int, cliente: Cliente):
        self._saldo = 0.0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente: Cliente, numero: int):
        return cls(numero, cliente)

    @property
    def saldo(self): return self._saldo

    @property
    def numero(self): return self._numero

    @property
    def agencia(self): return self._agencia

    @property
    def cliente(self): return self._cliente

    @property
    def historico(self): return self._historico

    def sacar(self, valor: float) -> bool:
        if valor > self._saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
            return False
        
        if valor > 0:
            self._saldo -= valor
            return True
        
        return False

    def depositar(self, valor: float) -> bool:
        if valor > 0:
            self._saldo += valor
            return True
        return False

class ContaCorrente(Conta):
    def __init__(self, numero: int, cliente: Cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor: float):
        # Lógica de contagem de saques baseada no histórico
        numero_saques = len(
            [t for t in self.historico.transacoes if t["tipo"] == "Saque"]
        )

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"Agência:\t{self.agencia}\nC/C:\t\t{self.numero}\nTitular:\t{self.cliente.nome}"

# ==========================================
# 5. FUNÇÕES DO SISTEMA (OPÇÕES DO MENU)
# ==========================================
def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [c for c in clientes if c.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return None
    return cliente.contas[0]

def depositar(clientes):
    cpf = input("CPF: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("Cliente não encontrado.")
        return

    valor = float(input("Valor do depósito: "))
    transacao = Deposito(valor)
    conta = recuperar_conta_cliente(cliente)
    if conta:
        cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    cpf = input("CPF: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("Cliente não encontrado.")
        return

    valor = float(input("Valor do saque: "))
    transacao = Saque(valor)
    conta = recuperar_conta_cliente(cliente)
    if conta:
        cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    cpf = input("CPF: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("Cliente não encontrado.")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta: return

    print("\n================ EXTRATO ================")
    for t in conta.historico.transacoes:
        print(f"{t['tipo']}: R$ {t['valor']:.2f} ({t['data']})")
    print(f"\nSaldo: R$ {conta.saldo:.2f}")
    print("==========================================")

def criar_cliente(clientes):
    cpf = input("CPF: ")
    if filtrar_cliente(cpf, clientes):
        print("CPF já existe.")
        return
    nome = input("Nome: ")
    data_nascimento = input("Data (dd-mm-aaaa): ")
    endereco = input("Endereço: ")
    clientes.append(PessoaFisica(cpf, nome, data_nascimento, endereco))
    print("Cliente criado!")

def criar_conta(numero_conta, clientes, contas):
    cpf = input("CPF: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("Cliente não encontrado.")
        return
    conta = ContaCorrente.nova_conta(cliente, numero_conta)
    contas.append(conta)
    cliente.adicionar_conta(conta)
    print("Conta criada!")

# ==========================================
# 6. MENU PRINCIPAL
# ==========================================
def main():
    clientes = []
    contas = []
    while True:
        op = input("\n[d] Depósito | [s] Saque | [e] Extrato | [nc] Nova Conta | [nu] Novo Usuário | [q] Sair\n=> ").lower()
        if op == "d": depositar(clientes)
        elif op == "s": sacar(clientes)
        elif op == "e": exibir_extrato(clientes)
        elif op == "nu": criar_cliente(clientes)
        elif op == "nc": criar_conta(len(contas)+1, clientes, contas)
        elif op == "q": break

if __name__ == "__main__":
    main()