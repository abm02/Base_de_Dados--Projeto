import psycopg2
from datetime import datetime

def menuViagens(idCliente):

    print("Viagens")
    opcao = "0"
    r = 0   #variável a ser devolvida (return) -> 0 se for para o programa terminar ; 1 se for para o programa correr este menu outra vez ; 2 se for para o programa voltar ao menu anterior
    while(opcao not in ["1","2","3","4","5","B","b","E","e"]):
        print("1-Reservar Viagens;")
        print("2-Cancelar Reserva;")
        print("3-Viagens Reservadas;")
        print("4-Lista Destinos;")
        print("5-Lista Viagens;")
        print("B-Voltar atrás;")
        print("E - Terminar o programa")
        opcao = input("Escolha a opção:")
        if(opcao not in ["1","2","3","4","5","6","B","b","E","e"]):
            print("Insira uma opção válida!\n")
        
    if (opcao=='1'):  #Se a opção escolhida for "Reservar Viagens"
        conn = psycopg2.connect("host=localhost dbname=projeto user=postgres password=postgres")
        cur = conn.cursor()

        cur.execute("SELECT * FROM viagem")

        for linha in cur.fetchall():
            idviagem, detalhes, numlugdisp, numlistaespera = linha
            print(linha)
                    

        opcao_reserva = input("Qual o id da viagem que pretende reservar: ")
        data_e_hora=(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

        if(cur.fetchone()[0] != 0): #verifica se o autocarro está cheio
        #CASO NÃO ESTEJA CHEIO
            # INSERE NA TABELA RESERVA    
            cur.execute("INSERT INTO reserva(idreserva,datareserva,listaespera,estado,idviagem,idcliente) \
                        VALUES  (%s,%s,%s,%s,%s)",(data_e_hora,False,True,opcao_reserva,idCliente))
                        #'listaespera = False' porque não está cheia a viagem
                        #'estado = True' porque reserva está ativa
            
            # UPDATE NA TABELA VIAGEM
            cur.execute("UPDATE viagem \
                        SET numlugdisp = %d \
                        WHERE idviagem = %s",(numlugdisp-1,opcao_reserva))   
                        # 'numlugdisp-1' pois deixa de estar um lugar disponível
        else:
        #CASO ESTEJA CHEIO
            # INSERE NA TABELA RESERVA 
            opcao_ord=0
            while(opcao_ord):
                print("1-Sim\n")
                print("2-Nao\n")
                opcao_ord=input("A viagem neste momento está lotado, pretende ficar em lista de espera?\n")
                if opcao_ord!=1 and opcao_ord!=2:
                    print("Insira uma opçõa válida!\n")

            if opcao_ord==1:
                cur.execute("INSERT INTO reserva(idreserva,datareserva,listaespera,estado,idviagem,idcliente)\
                            VALUES  (%s,%s,%s,%s,%s)",(data_e_hora,True,True,opcao_reserva,idCliente))
                            #'listaespera = True' porque está cheia, logo fica em lista de espera
                            #'estado = True' porque reserva está ativa

            # UPDATE NA TABELA VIAGEM
                cur.execute("UPDATE viagem \
                            SET numlistaespera = %d \
                            WHERE idviagem = %s",(numlistaespera+1,opcao_reserva))   
                            # 'numlistaespera+1' pois deixa de estar um lugar disponível
            
        conn.commit() # indepentemente de estar cheio ou vazio são guardadas as opções
        cur.close()
        conn.close()
        r = 1


    if (opcao=='2'):  #Se a opção escolhida for "Cancelar Reserva"
        conn = psycopg2.connect("host=localhost dbname=projeto user=postgres password=postgres")
        cur = conn.cursor()

        idReserva = selecionarReserva(idCliente)
        if (idReserva == -1):        #Se não existirem reservas possam ser canceladas
            print("Não existem reservas que possam ser canceladas... ")
            r = 1
            return(r)
        
        try:
            cur.execute("UPDATE reserva SET estado=%s\
                        WHERE idreserva=%s",(False,idReserva,))

            cur.execute("SELECT v.numlistaespera, r.idviagem, r.listaEspera, v.numLugDisp     \
                        FROM reserva AS r, viagem AS v  \
                        WHERE r.idviagem = v.idviagem   \
                        AND r.idreserva = %s", (idReserva,))
            
            numlistaespera, idviagem, listaEspera, numLugDisp = cur.fetchone()
            if (listaEspera == 'true'):   #Se o cliente que está a cancelar a viagem estiver em lista de espera
                cur.execute("UPDATE viagem SET numlistaespera=%s\
                                WHERE idviagem=%s",(numlistaespera-1, idviagem,))   #diminui 1 no valor da lista de espera

            else:
                if (numlistaespera == 0):
                    cur.execute("UPDATE viagem SET numLugDisp=%s\
                                    WHERE idviagem=%s",(numLugDisp+1, idviagem,))   #Se não existir lista de espera, aumenta 1 ao número de lugares disponíveis 
                else:
                    cur.execute("UPDATE viagem SET numlistaespera=%s\
                                    WHERE idviagem=%s",(numlistaespera-1, idviagem,))   #Se existir lista de espera, diminui 1 no valor da lista de espera
                    cur.execute("SELECT idCliente, idReserva    \
                                    FROM reserva    \
                                    WHERE idViagem = %s \
                                    AND listaEspera = true  \
                                    AND estado = true   \
                                    ORDER BY dataReserva", (idviagem,)) #vai buscar todos os clientes que estão em lista de espera
                    
                    #Vai buscar o 1º cliente em lista de espera
                    idPrimeiroCliente, idPrimeiraReserva,  = cur.fetchone()
                    #Vai buscar todos os outros clientes em lista de espera
                    idClientesEspera = []
                    idReservasEspera = []
                    i = 0
                    for linha in cur.fetchall():
                        idClienteEsp, idReservaEsp = linha
                        idClientesEspera.insert(i, idClienteEsp)
                        i += 1

                    #Retira o 1º cliente da lista de espera e envia-lhe uma mensagem automática
                    cur.execute("UPDATE reserva \
                                    SET listaEspera=false   \
                                    WHERE idReserva = %s", (idPrimeiraReserva,))
                    
                    dataEnvio = datetime.now().isoformat(' ', 'seconds')     #obtem o timestamp para o momento atual
                    assunto = "Reserva alterada - Já não está em lista de espera"
                    corpoMensagem = "Informamos que na reserva número " + str(idPrimeiraReserva) + " deixou de estar em lista de espera. Assim, o seu lugar nesta viagem está garantido. \
                        Caso deseje cancelar a reserva, pedimos que o faça na nossa aplicação! Muito obrigada e boas viagens!"
                    
                    cur.execute("INSERT INTO mensagem(dataEnvio, assunto, corpoMensagem, idAdmin) \
                                    VALUES (%s, %s, %s, NULL);", (dataEnvio, assunto, corpoMensagem,))       #insere na base de dados a mensagem automática a enviar    
                    cur.execute("SELECT idMensagem  \
                                    FROM mensagem   \
                                    WHERE dataEnvio = %s \
                                    AND assunto = %s   \
                                    AND corpoMensagem = %s", (dataEnvio, assunto, corpoMensagem,))       #na base de dados vai buscar o id da mensagem que acabou de ser escrita
                    idMensagem, = cur.fetchone()
                    cur.execute("INSERT INTO leitura(lida, idCliente, idMensagem)   \
                                VALUES (false, %s, %s);", (idPrimeiroCliente, idMensagem,))

                    #Enviar uma mensagem automática para todos os outros clientes em lista de espera
                    if (numlistaespera > 1):    #Se inicialmente existisse mais do que 1 cliente em lista de espera
                        assunto = "Reserva alterada - Está um lugar mais próximo de sair da lista de espera"
                        corpoMensagem = "Informamos que na viagem número " + str(idviagem) + " existiu um cancelamento. Ainda continua em lista de espera, mas um lugar mais próximo de conseguir o seu lugar! Muito obrigada pela atenção e boas viagens!"
                        cur.execute("INSERT INTO mensagem(dataEnvio, assunto, corpoMensagem, idAdmin) \
                                        VALUES (%s, %s, %s, NULL);", (dataEnvio, assunto, corpoMensagem,))       #insere na base de dados a mensagem automática a enviar    
                        cur.execute("SELECT idMensagem  \
                                        FROM mensagem   \
                                        WHERE dataEnvio = %s \
                                        AND assunto = %s   \
                                        AND corpoMensagem = %s", (dataEnvio, assunto, corpoMensagem,))       #na base de dados vai buscar o id da mensagem que acabou de ser escrita
                        idMensagem, = cur.fetchone()
                        for aux in idClientesEspera:
                            cur.execute("INSERT INTO leitura(lida, idCliente, idMensagem)   \
                                            VALUES (false, %s, %s);", (aux, idMensagem,))     #insere na base de dados, a informação da mensagem na parte da leitura

        except  psycopg2.DatabaseError:
                print("Aconteceu um erro com a base de dados e não foi possível cancelar a reserva.")
                print("Por favor tente outra vez!")
                conn.rollback()
        
        conn.commit()
        cur.close()
        conn.close()
        r = 1


    if (opcao=='3'):  #Se a opção escolhida for "Viagens Reservadas"
        conn = psycopg2.connect("host=localhost dbname=projeto user=postgres password=postgres")
        cur = conn.cursor()

        opcao_ord = "0"
        while(opcao_ord != "1" and opcao_ord !="2" and opcao_ord !="3"and opcao_ord !="4"):
            print("Como pretende ordenar os resultados?")
            print("1-Passado;")
            print("2-Futuro;")
            print("3-Voltar atrás;")
            opcao_ord = input("Escolha a opção:")

            if(opcao_ord != "1" and opcao_ord!="2"and opcao_ord !="3" and opcao_ord !="4"):
                print("Insira uma opçõa válida!\n")

        if opcao_ord == 1: # passado
            cur.execute("SELECT idviagem FROM reserva\
                        WHERE idcliente = %s AND datareserva<%s", (idCliente,datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
            res=cur.fetchall()

            i=0
            while i<len(res):
                cur.execute("SELECT * FROM viagem \
                            WHERE idviagem=%s",res[i])
                print(cur.fetchall())
                i+=1
        elif opcao_ord == 2: # futuro
            cur.execute("SELECT idviagem FROM reserva\
                        WHERE idcliente = %s AND datareserva>%s", (idCliente,datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
            res=cur.fetchall()

            i=0
            while i<len(res):
                cur.execute("SELECT * FROM viagem \
                            WHERE idviagem=%s",res[i])
                print(cur.fetchall())
                i+=1
        elif opcao_ord == 3: # Ordena por nome do local de partida
            print("Exit")
            #return(-1)
            r = 1
            # voltar atrás
        
        cur.close()
        conn.close()
        r = 1

   
    if (opcao=='4'):  #Se a opção escolhida for "Lista Destinos"
        conn = psycopg2.connect("host=localhost dbname=projeto user=postgres password=postgres")
        cur = conn.cursor()
        opcao_ord = "0"
        while(opcao_ord != "1" and opcao_ord !="2" and opcao_ord !="3"and opcao_ord !="4"):
            print("Como pretende ordenar os resultados?")
            print("1-Duração da Viagem;")
            print("2-Distância;")
            print("3-Nome;")
            print("4-Voltar atrás;")
            opcao_ord = input("Escolha a opção:")
            
            if(opcao_ord != "1" and opcao_ord!="2"and opcao_ord !="3" and opcao_ord !="4"):
                print("Insira uma opçõa válida!\n")

        if opcao_ord == 1:# tempo
            cur.execute("SELECT nomeEstacao, distancia, dataviagem,numlugdisp, numlistaespera,duracaoviagem\
                        FROM viagem,estacao \
                        WHERE iddestino = idEstacao\
                        ORDER BY duracaoviagem") # '-1' para ler da ultima palavra da str
        elif opcao_ord == 2: #distancia
            cur.execute("SELECT nomeEstacao, distancia, dataviagem,numlugdisp, numlistaespera, duracaoviagem\
                        FROM viagem,estacao \
                        WHERE iddestino = idEstacao\
                        ORDER BY distancia")
        elif opcao_ord ==3: # ordem alfabética do destino
            cur.execute("SELECT nomeEstacao, distancia, dataviagem,numlugdisp, numlistaespera, duracaoviagem\
                        FROM viagem,estacao \
                        WHERE iddestino = idEstacao\
                        ORDER BY nomeEstacao")
        else:
            cur.close()
            conn.close()
            return(1)


        for linha in cur.fetchall():
            nomeEstacao,distancia, dataviagem, numlugdisp, numlistaespera,duracaoviagem= linha
            print(linha)
        
        cur.close()
        conn.close()
        r = 1


    if (opcao=='5'):  #Se a opção escolhida for "Lista Viagens"
        conn = psycopg2.connect("host=localhost dbname=projeto user=postgres password=postgres")
        cur = conn.cursor()

        opcao_ord = "0"
        while(opcao_ord != "1" and opcao_ord !="2" and opcao_ord !="3"):
            print("Como pretende ordenar os resultados?")
            print("1-Todas;")
            print("2-Reservadas pelo Cliente;")
            print("3-Voltar atrás;")
            opcao_ord = input("Escolha a opção:")

            if(opcao_ord != "1" and opcao_ord!="2"and opcao_ord !="3"):
                print("Insira uma opçõa válida!\n")

        if opcao_ord==1: # todas
            datas=gamaValores()

            cur.execute("SELECT idviagem, detalhes, numlugdisp, numlistaespera FROM viagem\
                WHERE dataviagem>%s and dataviagem<%s",(datas[0],datas[1],))
            #print
            for linha in cur.fetchall():
                idviagem, detalhes, numlugdisp, numlistaespera = linha
                print(linha)
        elif opcao_ord==2: # reservadas pelo cliente
            datas=gamaValores()
            
            cur.execute("SELECT idviagem FROM reserva \
                        WHERE idcliente = %s",(idCliente,))

            res=cur.fetchall() 
            i=0
            while i<len(res):
                cur.execute("SELECT * FROM viagem \
                            WHERE idviagem=%s \
                            and dataviagem>%s and dataviagem<%s ",(res[i],datas[0],datas[1]))
                print(cur.fetchall())
                i+=1
        elif opcao_ord==3:
            cur.close()
            conn.close()
            return(1)
        
        cur.close()
        conn.close()
        r = 1

    return(r)

    
def selecionarReserva(idCliente):
    conn = psycopg2.connect("host = localhost dbname=projeto user=postgres password=postgres")
    cur = conn.cursor()
    dataAgora = datetime.now().isoformat(' ', 'seconds')     #obtem o timestamp para o momento atual
    cur.execute("SELECT  r.idReserva, v.detalhes \
                    FROM reserva AS r, viagem AS v \
                    WHERE r.idViagem = v.idViagem   \
                    AND idCliente = %s \
                    AND v.dataViagem > %s   \
                    AND r.estado = true \
                    ORDER BY idReserva", (idCliente, dataAgora,))
    
    i = 0
    aux = []
    for linha in cur.fetchall():    #vai buscar todas as reservas do cliente em causa
        i += 1
        idReserva, detalhes = linha
        print("Reserva número:", idReserva, "-", detalhes)
        aux.insert(i, str(idReserva))

    if (i == 0):    #Se não existirem reservas que possam ser canceladas
        opcao = -1
    else:
        opcao = 0
        while (opcao not in aux):
            opcao = input("Escolha o número da reserva que pretende: ")
        opcao = int(opcao)

    cur.close()
    conn.close()
    return(opcao)  #Retorna o idViagem
    
def selecionarDiaMesAnoViagem():
    conn = psycopg2.connect("host = localhost dbname=projeto user=postgres password=postgres")
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT extract(month from dataViagem), extract(year from dataViagem),\
                extract(day from dataviagem)\
                FROM viagem    \
                ORDER BY extract(year from dataViagem), extract(month from dataViagem),\
                extract(day from dataviagem)")
    
    meses = []
    anos = []
    dias =[]
    i = 0
    aux = []
    for linha in cur.fetchall():    #vai buscar os números dos meses com viagens
        i += 1
        aux.insert(i, str(i))
        mes, ano,dia = linha
        print(i,"-",dia,"/", mes, "/", ano)
        dias.insert(i-1,dia)
        meses.insert(i-1, mes)  #Na célula i-1, coloca o valor do mês que foi lido
        anos.insert(i-1, ano)  #Na célula i-1, coloca o valor do ano que foi lido
        
    
    opcao = 0
    while (opcao not in aux):
        opcao = input("Escolha uma opção: ")
    
    opcao = int(opcao)
    cur.close()
    conn.close()
    return(dias[opcao-1],meses[opcao-1], anos[opcao-1]) 

def gamaValores():
    print("Selecionar a primeira data da gama:")
    data1=selecionarDiaMesAnoViagem()
    data_in=str(data1[2])+'-'+str(data1[1])\
            +'-'+str(data1[0]) + " 00:00:00"

    print("Selecionar a segunda data da gama:")
    data2=selecionarDiaMesAnoViagem()
    data_fim=str(data2[2])+'-'+str(data2[1])\
        +'-'+str(data2[0]) + " 00:00:00"
    
    return(data_in,data_fim)