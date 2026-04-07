# Sistema Bancário com Programação Orientada a Objetos (POO) 🏦

Este projeto implementa a lógica de um sistema bancário robusto, seguindo uma modelagem UML profissional. O objetivo é demonstrar a aplicação de conceitos avançados de **Programação Orientada a Objetos (POO)** em Python.

## 🚀 Funcionalidades

- **Cadastro de Clientes:** Suporte a Pessoa Física (CPF).
- **Contas Múltiplas:** Um cliente pode possuir uma ou mais contas.
- **Conta Corrente Especial:** Inclui limites de saque e limite de valor por transação.
- **Histórico de Transações:** Registro detalhado de depósitos e saques com data e hora.
- **Lógica de Negócio Protegida:** Validações de saldo, limite e quantidade de saques.

## 🛠️ Tecnologias Utilizadas

* **Python 3.10+**
* **Conceitos de POO:** Herança, Polimorfismo, Encapsulamento e Abstração.
* **Módulos Nativos:** `abc` (Abstract Base Classes) e `datetime`.

## 📐 Modelagem do Sistema

O sistema foi construído com base no seguinte diagrama de classes:

- **Cliente / PessoaFisica:** Gerencia os dados do usuário e suas contas.
- **Conta / ContaCorrente:** Gerencia o saldo e as regras de saque/depósito.
- **Histórico / Transacao:** Interface polimórfica para registrar movimentações.

## 📋 Como Executar

1. Certifique-se de ter o Python instalado em sua máquina.
2. Clone este repositório:
   ```bash
   git clone [https://github.com/DIONE1000/modelagem-bancaria.git](https://github.com/DIONE1000/modelagem-bancaria.git)
