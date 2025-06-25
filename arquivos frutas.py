import pandas as pd 

def cadastrar_usuario(usuario,senha,arq):
    try:
        dados = pd.read_csv(arq)  
    except FileNotFoundError:
        print("Arquivo não encontrado!")
        return False
    
    lista_usu = list(dados['Usuario'])
    if usuario in lista_usu:
        return False
    else:
        confirm_sen = input("Confirmar senha: ")
        while confirm_sen != senha:
            print("Senha diferente!")
            confirm_sen = input("Confirmar senha: ")
        dados.loc[len(dados)] = [usuario,senha]
        dados.to_csv(arq,index = False)
        return True
    
def login(usuario, senha, arq):
    try:
        dados = pd.read_csv(arq)
    except FileNotFoundError:
        print("Arquivo não encontrado!")
        return False, None 

    lista_usu = list(dados['Usuario'])

    while usuario not in lista_usu:
        usuario = input("Usuário não existente. Tente novamente: ")
    
    indice_usuario = lista_usu.index(usuario)
    senha_correta = str(dados.at[indice_usuario, 'Senha'])

    while senha != senha_correta:
        print("Senha incorreta!")
        senha = input("Digite a sua senha: ")

    print("Login realizado com sucesso!")
    return True, usuario
    
    
def vende_frutas(fruta,qtd,estoque,caixa):
    try:
        dados_estoque = pd.read_csv(estoque)
        lista_fruta = list(dados_estoque['Fruta'])
        lista_qtd = list(dados_estoque['Quantidade'])
    except FileNotFoundError:
        print("Arquivo não encontrado!")
        return False
    
    try:
        dados_caixa = pd.read_csv(caixa)
        lista_caixa = list(dados_estoque['Caixa'])
        lista_usuario = list(dados_estoque['Usuario'])
        lista_data = list(dados_estoque['Data'])
    except FileNotFoundError:
        print("Arquivo não encontrado!")
        return False
    
    if fruta not in lista_fruta:
        print("A fruta não existe!")
        return False
    indice_fruta = lista_fruta.index(fruta)
    qtd_existente = lista_qtd[indice_fruta]
    if qtd <= 0:
        print("Quantidade inválida!")
        return False
    if qtd_existente - qtd < 0:
        print("Não possui essa quantidade em estoque!")
        return False
    print("Venda efetuada com sucesso!")
    dados_estoque.at[indice_fruta, 'Quantidade'] = qtd_existente - qtd
    dados_estoque.to_csv(estoque,index = False)
    return True

def add_frutas(fruta,qtd,pVenda,pCompra,arq):
    try:
        dados = pd.read_csv(arq)
        lista_fruta = list(dados['Fruta'])
        lista_qtd = list(dados['Quantidade'])
    except FileNotFoundError:
        print("Arquivo não encontrado!")
        return False
    
    if fruta in lista_fruta and qtd > 0:
        indice_fruta = lista_fruta.index(fruta)
        qtd_existente = lista_qtd[indice_fruta]
        dados.at[indice_fruta, 'Quantidade'] = qtd_existente + qtd
        dados.to_csv(arq,index = False)
        return True
    elif fruta not in lista_fruta and qtd > 0:
        dados.loc[len(dados)] = [fruta, qtd, pVenda, pCompra]
        dados.to_csv(arq,index = False)
        print("Adicionado com sucesso!")
        return True
    else:
        return False
    
# print("Olá! Seja bem vindo ao sistema da fruteira!\nPor favor, faça seu login ou se não tiver uma conta, crie-a!")
# opcao = int(input("1 - Cadastrar usuário\n2 - Login de usuário\n")) 
# while opcao != 1 and opcao != 2:                    
#     print("Opcão inválida")
#     opcao = int(input("1 - Cadastrar usuário\n2 - Login de usuário\n"))

# if opcao == 2:
#     n = input("Insira seu nome de usuário: ")
#     s = input("Insira sua senha: ")
#     sucesso, conta = login(n,s,'Usuarios.csv')

# elif opcao == 1:
#     n = input("Qual seu nome: ")
#     s = input("Qual sua senha: ")
#     valida = cadastrar_usuario(n,s,'Usuarios.csv')
#     print("Conta registrada. Por favor, faça o login novamente.")
#     sucesso, conta = login(n,s,'Usuarios.csv')

while True:
    print("Selecione a opção desejada")
    try:
        opcao = int(input("1 - Vender frutas\n"))
        break 
    except ValueError:
        print("Valor inválido! Digite um número.")
match opcao:
    case 1:
        x = input()
        y = int(input())
        vende_frutas(x,y,'Estoque.csv','Caixa.csv')
    case 2:
        f = input()
        q = int(input())
        pv = float(input())
        pc = float(input())
        add_frutas(f,q,pv,pc,'Estoque.csv')
    case _:
        print("Opção inválida.")
