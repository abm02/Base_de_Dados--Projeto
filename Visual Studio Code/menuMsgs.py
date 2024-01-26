import psycopg2

def menuMsgs(idCliente):
    opcao = '0'
    r = 0   #variável a ser devolvida (return) -> 0 se for para o programa terminar ; 1 se for para o programa correr este menu outra vez ; 2 se for para o programa voltar ao menu anterior
    while (opcao not in ['1', '2', '3', 'B', 'b', 'E', 'e']):
        print("1 - Ver mensagens já lidas")
        print("2 - Ver mensagens ainda não lidas")
        print("3 - Ver mensagens todas as mensagens")
        print("B - Regressar ao menu anterior")
        print("E - Terminar o programa")

        opcao = input("Escolha uma opção: ")

    if (opcao=='1'):  #Se a opção escolhida for "Ver mensagens já lidas"
        verMensagensLidas(idCliente)
        r = 1       #correr este menu outra vez

    if (opcao=='2'):  #Se a opção escolhida for "Ver mensagens ainda não lidas"
        verMensagensNaoLidas(idCliente)
        r = 1       #correr este menu outra vez

    if (opcao=='3'):  #Se a opção escolhida for "Ver mensagens todas as mensagens"
        verMensagensNaoLidas(idCliente)
        verMensagensLidas(idCliente)
        r = 1       #correr este menu outra vez

    elif (opcao=='B' or opcao=='b'): #Se a opção escolhida for "Regressar ao menu anterior"
        r = 2   #retornar ao menu anterior
    
    elif (opcao=='E' or opcao=='e'): #Se a opção escolhida for "Terminar o programa"
        r = 0   #terminar o programa

    return(r)

def verMensagensLidas(idCliente):
    print("\n\nMENSAGENS JÁ LIDAS:")    
    conn = psycopg2.connect("host = localhost dbname=projeto user=postgres password=postgres")
    cur = conn.cursor()
    cur.execute("SELECT * FROM MensagensLidas(%s);", (idCliente,))       #chama e realiza o procedimento "verMensagensLidas"
    
    aux = 0
    for linha in cur.fetchall():
        aux = 1
        dataEnvio, assunto, CorpoMensagem = linha
        print("Data de envio:", dataEnvio)
        print("Assunto:", assunto)
        print("Mensagem:", CorpoMensagem)
        print("")                               #imprime no ecrã os dados de todas as mensagens do cliente já lidas

    if (aux == 0):
        print("Não existem mensagens lidas.")
        
    cur.close()
    conn.close()
    
def verMensagensNaoLidas(idCliente):
    print("\n\nMENSAGENS AINDA NÃO LIDAS:") 
    conn = psycopg2.connect("host = localhost dbname=projeto user=postgres password=postgres")
    cur = conn.cursor()
    cur.execute("SELECT * FROM MensagensNaoLidas(%s);", (idCliente,))       #chama e realiza o procedimento "verMensagensLidas"
    
    aux = 0
    for linha in cur.fetchall():
        aux = 1
        dataEnvio, assunto, CorpoMensagem = linha
        print("Data de envio:", dataEnvio)
        print("Assunto:", assunto)
        print("Mensagem:", CorpoMensagem)
        print("")                               #imprime no ecrã os dados de todas as mensagens do cliente já lidas

    if (aux == 0):
        print("Não existem mensagens não lidas.")
    
    conn.commit()   #garante que a atualização é feita  
    cur.close()
    conn.close()