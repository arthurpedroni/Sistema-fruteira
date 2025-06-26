import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def cadastrar_usuario(usuario,senha,arq):
    try:
        dados = pd.read_csv(arq)  
    except (FileNotFoundError, pd.errors.EmptyDataError):
        dados = pd.DataFrame(columns=['Usuario','Senha'])
        dados.to_csv(arq, index=False)
    
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
    except (FileNotFoundError, pd.errors.EmptyDataError):
        dados = pd.DataFrame(columns=['Usuario','Senha'])
        dados.to_csv(arq, index=False)
        return False, None 

    lista_usu = list(dados['Usuario'])

    tentativas = 3
    while usuario not in lista_usu:
        print(f"Usuário não encontrado. Você tem {tentativas} tentativas")
        usuario = input("Digite seu usuário: ")
        tentativas -= 1
        if tentativas == 0:
            print("Encerrando login.")
            return False, None
    
    indice_usuario = lista_usu.index(usuario)
    senha_correta = str(dados.at[indice_usuario, 'Senha'])

    while senha != senha_correta:
        print("Senha incorreta!")
        senha = input("Digite a sua senha: ")

    print("Login realizado com sucesso!")
    return True, usuario
    
    
def vende_frutas(fruta,qtd,estoque,caixa,conta):

    try:
        dados_estoque = pd.read_csv(estoque)
    except (FileNotFoundError, pd.errors.EmptyDataError):
        dados_estoque = pd.DataFrame(columns=['Fruta','Quantidade','pVenda','pCompra'])
        dados_estoque.to_csv(estoque, index=False)                                   
    lista_fruta = list(dados_estoque['Fruta'])
    lista_pVenda = list(dados_estoque['pVenda'])

    try:
        dados_caixa = pd.read_csv(caixa)
    except (FileNotFoundError, pd.errors.EmptyDataError):
        # Criar estrutura inicial do DataFrame com colunas
        dados_caixa = pd.DataFrame(columns=['Caixa', 'Usuario', 'Data'])
        # Adiciona a linha inicial com R$ 0
        dados_caixa.loc[len(dados_caixa)] = [0, conta, datetime.now().strftime('%d/%m/%Y')]
        dados_caixa.to_csv(caixa, index=False)
    lista_caixa = list(dados_caixa['Caixa'])

    if fruta not in lista_fruta:
        print("A fruta não existe!")
        return False
    indice_fruta = lista_fruta.index(fruta)
    qtd_existente = int(dados_estoque.at[indice_fruta, 'Quantidade'])
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
    dados_caixa.loc[len(dados_caixa)] = [lista_caixa[-1] + (pVenda * qtd), conta, datetime.now().strftime('%d/%m/%Y')]
    dados_caixa.to_csv(caixa, index=False)
    return True
    
def compra(fruta,qtd,estoque,caixa,conta):
    try:
        dados_estoque = pd.read_csv(estoque)
    except (FileNotFoundError, pd.errors.EmptyDataError):
        dados_estoque = pd.DataFrame(columns=['Fruta','Quantidade','pVenda','pCompra'])
        dados_estoque.to_csv(estoque, index=False)                                   
    lista_fruta = list(dados_estoque['Fruta'])
    lista_pCompra = list(dados_estoque['pCompra'])    

    try:
        dados_caixa = pd.read_csv(caixa)
    except (FileNotFoundError, pd.errors.EmptyDataError):
        dados_caixa = pd.DataFrame(columns=['Caixa', 'Usuario', 'Data'])
        dados_caixa.loc[len(dados_caixa)] = [0, conta, datetime.now().strftime('%d/%m/%Y')]
        dados_caixa.to_csv(caixa, index=False)
    lista_caixa = list(dados_caixa['Caixa'])    

    if qtd <= 0:
        print("Quantidade inválida!")
        return False

    # compra de fruta que já está no sistema
    elif fruta in lista_fruta:
        indice_fruta = lista_fruta.index(fruta)
        qtd_existente = int(dados_estoque.at[indice_fruta, 'Quantidade'])
        dados_estoque.at[indice_fruta, 'Quantidade'] = qtd_existente + qtd

        dados_caixa.loc[len(dados_caixa)] = [(lista_caixa[-1] - (float(lista_pCompra[indice_fruta]) * qtd)),conta,datetime.now().strftime('%d/%m/%Y')]
    
    # cadastro de fruta no arquivo
    elif fruta not in lista_fruta:
        pVenda = float(input(f"Valor de venda de {fruta}: "))
        pCompra = float(input(f"Valor de compra de {fruta}: "))
        dados_estoque.loc[len(dados_estoque)] = [fruta, qtd, pVenda, pCompra]
        dados_caixa.loc[len(dados_caixa)] = [(lista_caixa[-1] - (pCompra * qtd)),conta,datetime.now().strftime('%d/%m/%Y')]
        print("Adicionado com sucesso!")
        
    dados_estoque.to_csv(estoque,index = False)
    dados_caixa.to_csv(caixa,index = False)
    return True

def grafico(estoque):
    try:
        dados = pd.read_csv(estoque)
        if dados.empty:
            print("Estoque está vazio.")
            return
        
        frutas = dados['Fruta']
        quantidades = dados['Quantidade'].astype(int)

        plt.figure(figsize=(8, 8))
        plt.pie(quantidades, labels=frutas, autopct='%1.1f%%', startangle=90)
        plt.title("Distribuição de Frutas no Estoque")
        plt.axis('equal')  
        plt.show()

    except Exception as e:
        print("Erro ao gerar gráfico:", e)

sistema_ativo = True
while sistema_ativo:    
    print("Olá! Seja bem vindo ao sistema da fruteira!\nPor favor, faça seu login ou se não tiver uma conta, crie-a!")
    opcao = int(input("1 - Login de usuário\n2 - Cadastrar usuário\n3 - Sair\n"))

    while opcao not in [1,2,3]:                    
        print("Opcão inválida")
        opcao = int(input("1 - Login de usuário \n2 - Cadastrar usuário\n3 - Fechar programa"))

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
            sistema_ativo = False
            break
            
    while sucesso:

        while True:
            print("Selecione a opção desejada")
            try:
                opcao = int(input("1 - Vender frutas\n2 - Comprar frutas\n3 - Gráfico do estoque\n4 - Finalizar sistema\n"))
                break 
            except ValueError:
                print("Valor inválido! Digite um número.")
                
        match opcao:
            case 1:
                fruta = input("Nome da fruta a se vender: ")
                qtd = int(input("Quantidade de frutas a se vender: "))
                vende_frutas(fruta,qtd,'Estoque.csv','Caixa.csv',conta)
            case 2:
                fruta = input("Nome da fruta a se comprar: ")
                qtd = int(input("Quantidade de frutas a se comprar: "))
                
                compra(fruta,qtd,'Estoque.csv','Caixa.csv',conta)
            case 3:
                grafico('Estoque.csv')
            case 4:
                sistema_ativo = False
                break           
            case _:
                break