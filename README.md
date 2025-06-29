# Sistema de Gestão de Fruteira

Este projeto é um sistema simples de gerenciamento de estoque, caixa e usuários para uma fruteira, feito com **Python** e utilizando **pandas**, **matplotlib** e **datetime** para manipulação de dados e visualização gráfica.

## Funcionalidades

- Cadastro de novos usuários com confirmação de senha.
- Login com verificação de tentativas.
- Registro e atualização do estoque de frutas.
- Vendas de frutas com atualização automática do estoque e caixa.
- Compras de frutas, incluindo frutas já registradas ou novas.
- Geração de gráfico de pizza com a distribuição atual do estoque.

## Estrutura dos Arquivos

- **Usuarios.csv**: Armazena os nomes de usuários e suas senhas.
- **Estoque.csv**: Armazena os dados das frutas: nome, quantidade, preço de venda e de compra.
- **Caixa.csv**: Armazena os valores do caixa com histórico de operações, nome do usuário e data.

## Requisitos

- Python 3.7+
- Bibliotecas:
  - `pandas`
  - `matplotlib`

Você pode instalar as dependências com:

```bash
pip install pandas matplotlib