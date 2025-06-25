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
        lista_pVenda = list(dados_estoque['pVenda'])
        lista_pCompra = list(dados_estoque['pCompra'])
    except FileNotFoundError:
        print("Arquivo não encontrado!")
        return False
    
    try:
        dados_caixa = pd.read_csv(caixa)
        lista_caixa = list(dados_caixa['Caixa'])
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
    pVenda = lista_pVenda[indice_fruta]
    print("Venda efetuada com sucesso!")
    dados_estoque.at[indice_fruta, 'Quantidade'] = qtd_existente - qtd
    dados_estoque.to_csv(estoque,index = False)
    dados_caixa.loc[len(dados_caixa)] = [lista_caixa[-1] + (pVenda * qtd), conta, '25/06/2025']
    dados_caixa.to_csv(caixa, index=False)
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
while True:    
    print("Olá! Seja bem vindo ao sistema da fruteira!\nPor favor, faça seu login ou se não tiver uma conta, crie-a!")
    opcao = int(input("1 - Login de usuário\n2 - Cadastrar usuário\n3 - Sair\n")) 
    while opcao not in [1,2,3]:                    
        print("Opcão inválida")
        opcao = int(input("1 - Login de usuário \n2 - Cadastrar usuário\n"))
    match opcao:
        case 1:
            n = input("Insira seu nome de usuário: ")
            s = input("Insira sua senha: ")
            sucesso, conta = login(n,s,'Usuarios.csv')

        case 2:
            n = input("Qual seu nome: ")
            s = input("Qual sua senha: ")
            valida = cadastrar_usuario(n,s,'Usuarios.csv')
            print("Conta registrada. Fazendo login...")
            sucesso, conta = login(n,s,'Usuarios.csv')
        case 3:
            break
            
    while True:
        while True:
            print("Selecione a opção desejada")
            try:
                opcao = int(input("1 - Vender frutas\n"))
                break 
            except ValueError:
                print("Valor inválido! Digite um número.")
                
        match opcao:
            case 1:
                fruta = input("Nome da fruta: ")
                qtd = int(input("Quantidade de frutas: "))
                vende_frutas(fruta,qtd,'Estoque.csv','Caixa.csv')
            case 2:
                f = input()
                q = int(input())
                pv = float(input())
                pc = float(input())
                add_frutas(f,q,pv,pc,'Estoque.csv')
            case _:
                break
        break
