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
    
def login(usuario,senha,arq):
    try:
        dados = pd.read_csv(arq)  
    except FileNotFoundError:
        print("Arquivo não encontrado!")
        return False

    lista_usu = list(dados['Usuario'])
    if usuario in lista_usu:
        indice_usuario = lista_usu.index(usuario)
        senha_correta = str(dados.at[indice_usuario, 'Senha'])
        while senha_correta != senha:
            print("Senha incorreta!")
            senha = input("Digite a sua senha: ")
        return True, indice_usuario
    else:
        print("Usuário não cadastrado!")
        return False, None
    
def vende_frutas(fruta,qtd,arq):
    try:
        dados = pd.read_csv(arq)
        lista_fruta = list(dados['Fruta'])
        lista_qtd = list(dados['Quantidade'])
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
    dados.at[indice_fruta, 'Quantidade'] = qtd_existente - qtd
    dados.to_csv(arq,index = False)
    return True

def add_frutas(fruta,qtd,arq):
    dados = pd.read_csv(arq)
    lista_fruta = list(dados['Fruta'])
    lista_qtd = list(dados['Quantidade'])
    if fruta in lista_fruta and qtd > 0:
        indice_fruta = lista_fruta.index(fruta)
        qtd_existente = lista_qtd[indice_fruta]
        dados.at[indice_fruta, 'Quantidade'] = qtd_existente + qtd
        dados.to_csv(arq,index = False)
        return True
    elif fruta not in lista_fruta and qtd > 0:
        dados.loc[len(dados)] = [fruta,qtd]
        dados.to_csv(arq,index = False)
        return True
    else:
        return False
    
print("Olá! Seja bem vindo ao sistema da fruteira!\nPor favor, faça seu login ou se não tiver uma conta, crie-a!")
opcao = int(input("1 - Cadastrar usuário\n2 - Login de usuário"))                     
match opcao:
    case 1:
        n = input("Insira seu nome de usuário: ")
        s = input("Insira sua senha: ")
        valida = login(n,s,'Usuarios.csv')
    case 2:
        n = input("Qual seu nome: ")
        s = input("Qual sua senha: ")
        valida = cadastrar_usuario(n,s,'Usuarios.csv')
        print("Conta registrada. Por favor, faça o login novamente.")
    case _:
        print("Opcão inválida")

opcao = int(input("1 - Vender frutas\n"))
match opcao:
    case 1:
        x = input()
        y = int(input())
        vende_frutas(x,y,'Estoque1.csv')
        
