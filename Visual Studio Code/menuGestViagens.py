import psycopg2
from datetime import datetime

def menuGestViagens():
    opcao = "0"
    while(opcao != "1" and opcao !="2" and opcao !="3" and opcao !="4" and opcao !="5" and opcao !="6"):
        print("1-Lista de Viagens;")
        print("2-Adicionar Viagens;")
        print("3-Remover Viagens;")
        print("4-Corrigir preços de Viagens;")
        print("5-Inserir Novos Autocarros;")
        print("6-Voltar atrás")
        opcao = input("Escolha a opção:")

        if(opcao != "1" and opcao !="2"and opcao !="3" and opcao !="4" and opcao !="5" and opcao !="6"):
            print("Insira uma opçõa válida!\n")

    return (opcao)

def listaViagens():

    conn = psycopg2.connect("host=localhost dbname=projeto user=postgres password=postgres")
    cur = conn.cursor()

    opcao_ord = "0"
    while(opcao_ord != "1" and opcao_ord !="2" and opcao_ord !="3"and opcao_ord !="4"):
        print("Como pretende ordenar os resultados?")
        print("1-Viagens que já decorreram;")
        print("2-Viagens por decorrer;")
        print("3-Todas;")
        print("4-Voltar atrás;")
        opcao_ord = input("Escolha a opção:")
        if(opcao_ord != "1" and opcao_ord!="2"and opcao_ord !="3" and opcao_ord !="4"):
            print("Insira uma opçõa válida!\n")
        if opcao_ord == 1: # decorridas
            cur.execute("SELECT idviagem, detalhes, numlugdisp, numlistaespera \
                        FROM viagem \
                        ORDER BY datareserva<%s",(datetime.now().strftime("%d/%m/%Y %H:%M:%S")))         
        elif opcao_ord==2: # por decorrer
            cur.execute("SELECT idviagem, detalhes, numlugdisp, numlistaespera\
                        FROM viagem \
                        ORDER BY datareserva>%s",(datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
        elif opcao_ord==3: #todas
            cur.execute("SELECT * FROM viagem")
                #inserir print
        for linha in cur.fetchall():
            idviagem, detalhes, numlugdisp, numlistaespera = linha
            print(linha)
        conn.commit()

def adcViagem():

    conn = psycopg2.connect("host=localhost dbname=projeto user=postgres password=postgres")
    cur = conn.cursor()

    #Print dos IDS da estação
    cur.execute("SELECT idestacao,nomeestacao FROM estacao")
    for linha in cur.fetchall():
        idestacao,nomeestacao=linha 
        print(linha)

    idor=input("Insira o ID do local de origem: ")
    iddest=input("Insira o ID do local de destino: ")
    
    #através dos ids vai buscar os nomes e os destinos
    cur.execute("SELECT nomeestacao FROM estacao\
                WHERE idestacao=%s",idor)
    est_or= cur.fetchone()[0]

    cur.execute("SELECT nomeestacao FROM estacao\
                WHERE idestacao=%s",iddest)
    est_dest= cur.fetchone()[0]

    det = est_or + " to " + est_dest
    #

    data_e_hora=input("Insira a data de partida no formato [YY-MM-DD] [HH:MM:SS]: ")
    
    idbus=input("Insira o id do autocarro atribuído à viagem: ")
    
    #através do id do autocarro vai buscar o número de lugares
    cur.execute("SELECT lotacaomax FROM autocarro \
                WHERE idautocarro=%s",idbus)
    lug=cur.fetchone()[0]
     
    numespera=0 # uma vez que todos os lugares estão vagos não há ninguém em lista de espera
    
    dist=input("Insira a distância entre os locais: ") # varia consoante a rota

    preco = input("Qual o preco do bilhete? ")

    # insere na tabela viagem
    cur.execute("INSERT INTO viagem(idviagem,detalhes,distancia,dataviagem, numlugdisp,numlistaespera,idorigem,iddestino,idautocarro)\
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",(det,dist,data_e_hora,lug,numespera,idor,iddest,idbus))
                
    # insere na tabela preco
    cur.execute("INSERT INTO preco(preco,datamudanca,idviagem)\
                VALUES (%s,%s,%s)",(preco,datetime.now().strftime("%d/%m/%Y %H:%M:%S"),id))

    # PRINT
    cur.execute("SELECT idviagem,detalhes,distancia,dataviagem,numlugdisp,numlistaespera,idautocarro\
                 FROM viagem")
    for linha in cur.fetchall():
        idviagem,detalhes,distancia,dataviagem,numlugdisp,numlistaespera,idautocarro=linha 
        print(linha)

    conn.commit()


def remViagem():
    
    conn = psycopg2.connect("host=localhost dbname=projeto user=postgres password=postgres")
    cur = conn.cursor()

    val = True # variável de verificação se se pode eliminar ou não

    eliminaID=input("Qual o id da viagem a eliminar?")

    cur.execute("SELECT idviagem FROM reserva")

    # verificar se a viagem já tem reservas ou não
    res=cur.fetchall() 
    i=0
    while i<len(res):
        if res[i][0] == int(eliminaID):
            print("Não é possível eliminar este viagem pois já contém reservas!")
            val=False
        i+=1
       
    # elimina
    if val == True:
        cur.execute("DELETE FROM preco \
                    WHERE idviagem = %s",eliminaID)
        cur.execute("DELETE FROM reserva \
                    WHERE idviagem = %s",eliminaID)
        cur.execute("DELETE FROM viagem \
                    WHERE idviagem = %s",eliminaID)
        # temos de eliminar por esta ordem por causa dos constraints das primary keys
        
        # PRINT
        cur.execute("SELECT * FROM viagem")
        for linha in cur.fetchall():
            idviagem,detalhes,distancia,dataviagem, numlugdisp,numlistaespera,idorigem,iddestino,idautocarro = linha
            print(linha)
        
        conn.commit()

def atualPreco():
    
    conn = psycopg2.connect("host=localhost dbname=projeto user=postgres password=postgres")
    cur = conn.cursor()

    id=input("Qual o id da viagem em que pretende alterar o preço?")
    novo_preco=input("Qual o novo preço a colocar?")
    nova_data=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    cur.execute("INSERT INTO preco(preco,datamudanca,idviagem) \
                VALUES (%s,%s,%s)",(novo_preco,nova_data,id))
    conn.commit()
    cur.close()
    conn.close()

def insAutocarro():
    
    conn = psycopg2.connect("host=localhost dbname=projeto user=postgres password=postgres")
    cur = conn.cursor()

    nova_matricula=input("Qual a matrícula do novo autocarro?")
    lotacao_max = input("Insira a lotação máxima do autocarro:")
    cur.execute("INSERT INTO autocarro(idautocarro,matricula,lotacaomax)\
                VALUES (%s,%s) ",(nova_matricula, lotacao_max))
    
    conn.commit()
    cur.close()
    conn.close()
    
def updateViagens():
    conn = psycopg2.connect("host=localhost dbname=projeto user=postgres password=postgres")
    cur = conn.cursor()

    id=input("Qual o id da Viagem que pretende atualizar?")
    val = True # variável de verificação se se pode eliminar ou não

    cur.execute("SELECT idviagem FROM reserva")
    
    # verificar se a viagem já tem reservas ou não
    res=cur.fetchall() 
    i=0
    while i<len(res):
        if res[i][0] == int(id):
            print("Não é possível eliminar este viagem pois já contém reservas!")
            val=False
        i+=1
       
    # elimina
    if val == True: 
        # não se pode alterar: detalhes, distancia
        opcao_ord = "0"
        while(opcao_ord != "1" and opcao_ord !="2" and opcao_ord !="3"and opcao_ord !="4"):
            print("Que dado pretende alterar?")
            print("1-Duração da Viagem;")
            print("2-Data e Hora da Viagem;")
            print("3-Autocarro;")
            print("4-Voltar atrás;")
            opcao_ord = input("Escolha a opção:")
            
            if(opcao_ord != "1" and opcao_ord!="2"and opcao_ord !="3" and opcao_ord !="4"):
                print("Insira uma opçõa válida!\n")
        if opcao_ord==1:
            nova_duracao=input("Insira a nova duração da viagem [HH:MM:ss]: ")
            cur.execute("UPDATE viagem SET duracaoviagem=%s \
                        WHERE idviagem=%s ",(nova_duracao,id))
        elif opcao_ord==2:
            data_e_hora=input("Insira a data de partida no formato [YY-MM-DD] [HH:MM:SS]: ")
            cur.execute("UPDATE viagem SET dataviagem=%s \
                        WHERE idviagem=%s",(data_e_hora,id))
        elif opcao_ord==3:
            novo_bus=input("Insira o novo autocarro atribuido a esta viagem: ")
            
            cur.execute("UPDATE viagem SET idautocarro = %s\
                        WHERE idviagem=%s",(novo_bus,id)) # atualiza autocarro
            
            cur.execute("SELECT lotacaomax FROM autocarro \
                    WHERE idautocarro=%s",novo_bus)
            lug=cur.fetchone()[0] # vai buscar lotacao max do autocarro para retirar o numlugdisp

            cur.execute("UPDATE viagem SET numlugdisp=%s \
                        WHERE idviagem=%s",(lug, id)) # coloca novo numlugdisp
            
            # como só pode ser alterado sem reservas o 'numlistaespera' continua igual
    conn.commit() 







    conn.commit()
    conn.close()
    cur.close()