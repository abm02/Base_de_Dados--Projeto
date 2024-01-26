import psycopg2

def menuEstat():
    opcao = '0'
    r = 0       #variável a ser devolvida (return) -> 0 se for para o programa terminar ; 1 se for para o programa correr este menu outra vez ; 2 se for para o programa voltar ao menu anterior
    while (opcao not in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'B', 'b', 'E', 'e']):
        print("1 - Identificar a viagens mais vendidas num determinado mês")
        print("2 - Identificar o cliente que mais viagens comprou num determinado mês")
        print("3 - Listar todas as viagens que não tiveram reservas num determinado mês")
        print("4 - Listar as reservas de uma viagem")
        print("5 - Listar as reservas canceladas de uma viagem")
        print("6 - Listar as reservas em lista de espera de uma viagem")
        print("7 - Identificar o percurso com mais clientes num determinado mês")
        print("8 - Identificar o dia do ano em que houve mais vendas")
        print("9 - Identificar o volume de vendas em cada mês de um ano")
        print("B - Regressar ao menu anterior")
        print("E - Terminar o programa")

        opcao = input("Escolha uma opção: ")

        if(opcao not in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'B', 'b', 'E', 'e']):
            print("Insira uma opçõa válida!\n") #informar caso a opção escolhida não seja válida
    
    if (opcao=='1'):  #Se a opção escolhida for "Identificar a viagem mais vendida num determinado mês"
        print("\n\n\nSELECIONE O MÊS QUE PRETENDE ANALISAR:")
        mes, ano = selecionarMesAnoReserva()
        conn = psycopg2.connect("host = localhost dbname=projeto user=postgres password=postgres")
        cur = conn.cursor()
        cur.execute("SELECT idViagem, COUNT(date_trunc('month', dataReserva))  \
                        FROM reserva  \
                        WHERE EXTRACT(MONTH FROM dataReserva) = %s  \
                        and EXTRACT(YEAR FROM dataReserva) = %s   \
                        GROUP BY idViagem", (mes, ano))     #na base de dados, conta o número de reservas de cada viagem no mês escolhido
        
        max = 0
        for linha in cur.fetchall():  
            idViagem, contagem = linha
            if (int(contagem) > max):
                max = contagem               #procura qual o valor máximo da contagem das reservas


        cur.execute("SELECT r.idViagem, v.detalhes  \
                        FROM reserva AS r, viagem AS v  \
                        WHERE EXTRACT(MONTH FROM r.dataReserva) = %s \
                        and EXTRACT(YEAR FROM dataReserva) = %s   \
                        AND r.idViagem = v.idViagem \
                        GROUP BY r.idViagem, v.detalhes \
                        HAVING COUNT(date_trunc('month', r.dataReserva)) = %s", (mes, ano, max,))     #na base de dados, vai buscar todas as viagens em que existiram mais reservas no mês escolhido
        
        print("Viagens mais vendidas no mês escolhido, com", max, "reservas: ")
        for linha in cur.fetchall(): 
            idViagem, detalhes = linha
            print("Viagem número:", idViagem, "-", detalhes)
        
        cur.close()
        conn.close()
        r = 1   #correr este menu outra vez
    
    elif (opcao=='2'):  #Se a opção escolhida for "Identificar o cliente que mais viagens comprou num determinado mês"
        print("\n\n\nSELECIONE O MÊS QUE PRETENDE ANALISAR:")
        mes, ano = selecionarMesAnoReserva() 
        conn = psycopg2.connect("host = localhost dbname=projeto user=postgres password=postgres")
        cur = conn.cursor()
        cur.execute("SELECT idCliente, COUNT(idReserva) \
                        FROM reserva    \
                        WHERE EXTRACT(MONTH FROM dataReserva) = %s   \
                        and EXTRACT(YEAR FROM dataReserva) = %s   \
                        and estado = true   \
                        and listaEspera = false \
                        GROUP BY idCliente", (mes, ano,))     #na base de dados, conta o número de viagens que cada cliente comprou no mês escolhido
        
        max = 0
        for linha in cur.fetchall():  
            idCliente, contagem = linha
            if (int(contagem) > max):
                max = contagem               #procura qual o valor máximo do número de reservas 

        cur.execute("SELECT idCliente, COUNT(idReserva) \
                        FROM reserva    \
                        WHERE EXTRACT(MONTH FROM dataReserva) = %s   \
                        and EXTRACT(YEAR FROM dataReserva) = %s   \
                        and estado = true   \
                        and listaEspera = false \
                        GROUP BY idCliente  \
                        HAVING COUNT(idReserva) = %s", (mes, ano, max, ))   #na base de dados, vai buscar todos os clientesque compraram o maior número de viagens no mês escolhido
        
        print("Clientes que mais viagens compraram no mês escolhido, tendo comprado", max, "viagens: ")
        for linha in cur.fetchall():  
            idCliente, contagem = linha
            print("Cliente número:", idCliente)

        cur.close()
        conn.close()
        r = 1   #correr este menu outra vez

    elif (opcao=='3'): #Se a opção escolhida for "Listar todas as viagens que não tiveram reservas num determinado mês"
        print("\n\n\nSELECIONE O MÊS QUE PRETENDE ANALISAR:")
        mes, ano = selecionarMesAnoViagem() 
        conn = psycopg2.connect("host = localhost dbname=projeto user=postgres password=postgres")
        cur = conn.cursor()
        cur.execute("SELECT v.idViagem, v.detalhes  \
                        FROM viagem AS v, autocarro AS a    \
                        WHERE v.idAutocarro = a.idAutocarro     \
                        and EXTRACT(MONTH FROM v.dataViagem) = %s    \
                        and EXTRACT(YEAR FROM v.dataViagem) = %s  \
                        and v.numLugDisp = a.lotacaoMax", (mes, ano,))  #na base de dados, vai buscar as viagem do mês escolhido que não tiveram reservas

        print("Viagens sem reservas no mês escolhido: ")
        aux = 0
        for linha in cur.fetchall():  
            aux = 1
            idViagem, detalhes = linha
            print("Viagem número:", idViagem, "-", detalhes)

        if (aux == 0):
            print("Não existe nenhuma.")

        cur.close()
        conn.close()
        r = 1   #correr este menu outra vez

    elif (opcao=='4'): #Se a opção escolhida for "Listar as reservas de uma viagem"
        print("\n\n\nSELECIONE A VIAGEM QUE PRETENDE ANALISAR:")
        idViagem = selecionarViagem()
        conn = psycopg2.connect("host = localhost dbname=projeto user=postgres password=postgres")
        cur = conn.cursor()
        cur.execute("SELECT  COUNT(r.idReserva) \
                        FROM viagem AS v, reserva AS r  \
                        WHERE v.idViagem = r.idViagem   \
                        and v.idViagem = %s  \
                        and estado = true   \
                        and listaespera = false", (idViagem,))    #na base de dados, conta o número de reservas da viagem selecionada, que não estão em lista de espera
        
        contagemSemEspera, = cur.fetchone()
        if (contagemSemEspera == 0):
            print("Na viagem escolhida, não existem reservas.")
        else:
            cur.execute("SELECT  COUNT(r.idReserva) \
                        FROM viagem AS v, reserva AS r  \
                        WHERE v.idViagem = r.idViagem   \
                        and v.idViagem = %s  \
                        and estado = true   \
                        and listaespera = true", (idViagem,))    #na base de dados, conta o número de reservas da viagem selecionada, que estão em lista de espera
            
            contagemComEspera, = cur.fetchone()
            if (contagemComEspera == 0):
                print("Na viagem selecionada, existem", contagemSemEspera, "reservas confirmadas.")
            else:
                print("Na viagem selecionada, existem", contagemSemEspera, "reservas confirmadas e", contagemComEspera, "em lista de espera.")
        
        cur.close()
        conn.close()
        r = 1   #correr este menu outra vez

    elif (opcao=='5'): #Se a opção escolhida for "Listar as reservas canceladas de uma viagem"
        print("\n\n\nSELECIONE A VIAGEM QUE PRETENDE ANALISAR:")
        idViagem = selecionarViagem()
        conn = psycopg2.connect("host = localhost dbname=projeto user=postgres password=postgres")
        cur = conn.cursor()
        cur.execute("SELECT  COUNT(r.idReserva) \
                        FROM viagem AS v, reserva AS r  \
                        WHERE v.idViagem = r.idViagem   \
                        and v.idViagem = %s  \
                        and estado = false", (idViagem,))    #na base de dados, conta o número de reservas da viagem selecionada, que foram canceladas
        
        contagem, =cur.fetchone()
        if (contagem == 0):
            print("A viagem selecionada não tem reservas canceladas.")
        else:
            print("A viagem selecionada tem", contagem, "reservas canceladas.")
        
        cur.close()
        conn.close()
        r = 1   #correr este menu outra vez

    elif (opcao=='6'): #Se a opção escolhida for "Listar as reservas em lista de espera de uma viagem"
        print("\n\n\nSELECIONE A VIAGEM QUE PRETENDE ANALISAR:")
        idViagem = selecionarViagem()
        conn = psycopg2.connect("host = localhost dbname=projeto user=postgres password=postgres")
        cur = conn.cursor()
        cur.execute("SELECT  COUNT(r.idReserva) \
                        FROM viagem AS v, reserva AS r  \
                        WHERE v.idViagem = r.idViagem   \
                        and v.idViagem = %s  \
                        and estado = true   \
                        and listaespera = true", (idViagem,))    #na base de dados, conta o número de reservas da viagem selecionada, que estão em lista de espera
            
        contagem, = cur.fetchone()
        if (contagem == 0):
            print("Na viagem selecionada não existem reservas em lista de espera.")
        else:
            print("A viagem selecionada tem", contagem, "reservas em lista de espera.")

        cur.close()
        conn.close()
        r = 1   #correr este menu outra vez

    elif (opcao=='7'): #Se a opção escolhida for "Identificar o percurso com mais clientes num determinado mês"
        print("\n\n\nSELECIONE O MÊS QUE PRETENDE ANALISAR:")
        mes, ano = selecionarMesAnoViagem()
        conn = psycopg2.connect("host = localhost dbname=projeto user=postgres password=postgres")
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT MAX(a.lotacaoMax-v.numLugDisp)  \
                        FROM viagem AS v, autocarro AS a    \
                        WHERE v.idAutocarro = a.idAutocarro     \
                        and EXTRACT(MONTH FROM v.dataViagem) = %s    \
                        and EXTRACT(YEAR FROM v.dataViagem) = %s", (mes, ano,))     #na base de dados, obtem o número máximo de bilhetes vendidos no mês selecionado

        max, = cur.fetchone()

        cur.execute("SELECT v.idViagem, v.detalhes\
                        FROM viagem AS v, autocarro AS a    \
                        WHERE v.idAutocarro = a.idAutocarro     \
                        and EXTRACT(MONTH FROM v.dataViagem) = %s    \
                        and EXTRACT(YEAR FROM v.dataViagem) = %s    \
                        and (a.lotacaoMax-v.numLugDisp) = %s", (mes, ano, max,))     #na base de dados, obtem as informações sobre as viagens com mais bilhetes vendidos
        
        print("Viagens com mais clientes no mês selecionado, com", max, "clientes:")
        for linha in cur.fetchall():
            idViagem, detalhes = linha
            print("Viagem número:", idViagem, "-", detalhes)
        
        cur.close()
        conn.close()
        r = 1   #correr este menu outra vez

    elif (opcao=='8'): #Se a opção escolhida for "Identificar o dia do ano em que houve mais vendas"
        print("\n\n\nSELECIONE O ANO QUE PRETENDE ANALISAR:")
        ano = selecionarAnoReserva()
        conn = psycopg2.connect("host = localhost dbname=projeto user=postgres password=postgres")
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT COUNT(idReserva), EXTRACT(DAY FROM dataReserva) AS dia, EXTRACT(MONTH FROM dataReserva) AS mes \
                        FROM reserva    \
                        WHERE EXTRACT(YEAR FROM dataReserva) = %s \
                        GROUP BY dia, mes   \
                        ORDER BY mes, dia", (ano,))     #na base de dados, conta quantas reservas aconteceram em cada dia do ano selecionado
        
        max = 0
        for linha in cur.fetchall():  
            contagem, dia, mes = linha
            if (int(contagem) > max):
                max = contagem               #procura qual o valor máximo de vendas
                i = 1
                dias = []
                meses = []
                dias.insert(i-1, dia)  #Na célula i-1, coloca o valor do dia que foi lido
                meses.insert(i-1, mes)  #Na célula i-1, coloca o valor do mês que foi lido
            elif (int(contagem) == max):
                i += 1
                dias.insert(i-1, dia)  #Na célula i-1, coloca o valor do dia que foi lido
                meses.insert(i-1, mes)  #Na célula i-1, coloca o valor do mês que foi lido

        print("Dias do ano com mais reservas feitas, com",max, " reservas realizadas: ")
        for aux in range(i):
            print(dias[aux], "/", meses[aux], "/", ano)

        cur.close()
        conn.close()
        r = 1   #correr este menu outra vez

    elif (opcao=='9'): #Se a opção escolhida for "Identificar o volume de vendas em cada mês de um ano"
        print("\n\n\nSELECIONE O ANO QUE PRETENDE ANALISAR:")
        ano = selecionarAnoReserva()
        conn = psycopg2.connect("host = localhost dbname=projeto user=postgres password=postgres")
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT COUNT(idReserva), EXTRACT(MONTH FROM dataReserva) AS mes   \
                        FROM reserva    \
                        WHERE EXTRACT(YEAR FROM dataReserva) = %s \
                        GROUP BY mes    \
                        ORDER BY mes", (ano,))      #na base de dados, é pesquisado quantas reservas foram feitas em cada mês do ano selecionado
        
        print("Volume de vendas em cada mês do ano selecionado:")
        for linha in cur.fetchall():
            contagem, mes = linha
            print("Mês", mes, "-", contagem, "reservas")

        cur.close()
        conn.close()
        r = 1   #correr este menu outra vez

    elif (opcao=='B' or opcao=='b'): #Se a opção escolhida for "Regressar ao menu anterior"
        r = 2   #retornar ao menu anterior
    
    elif (opcao=='E' or opcao=='e'): #Se a opção escolhida for "Terminar o programa"
        r = 0   #terminar o programa

    
    
    return(r)

def selecionarMesAnoReserva():
    conn = psycopg2.connect("host = localhost dbname=projeto user=postgres password=postgres")
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT extract(month from dataReserva), extract(year from dataReserva) \
                FROM reserva    \
                ORDER BY extract(year from dataReserva), extract(month from dataReserva)")      #na base de dados, vai buscar todos os meses e anos em que existem reservas
    
    meses = []
    anos = []
    i = 0
    aux = []
    for linha in cur.fetchall():    #vai buscar os números dos meses com viagens
        i += 1
        aux.insert(i, str(i))
        mes, ano = linha
        print(i, "-", mes, "/", ano)
        meses.insert(i-1, mes)  #Na célula i-1, coloca o valor do mês que foi lido
        anos.insert(i-1, ano)  #Na célula i-1, coloca o valor do ano que foi lido
    
    opcao = 0
    while (opcao not in aux):
        opcao = input("Escolha uma opção: ")
    
    opcao = int(opcao)
    cur.close()
    conn.close()
    return(meses[opcao-1], anos[opcao-1])  #Retorna o número do mês e o ano escolhido

def selecionarAnoReserva():
    conn = psycopg2.connect("host = localhost dbname=projeto user=postgres password=postgres")
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT extract(year from dataReserva) \
                FROM reserva    \
                ORDER BY extract(year from dataReserva)")       #na base de dados, vai buscar todos os anos em que existem reservas
    
    anos = []
    i = 0
    aux = []
    for linha in cur.fetchall():    #vai buscar os números dos meses com viagens
        i += 1
        aux.insert(i, str(i))
        ano, = linha
        print(i, "- Ano:", ano)
        anos.insert(i-1, ano)  #Na célula i-1, coloca o valor do ano que foi lido
    
    opcao = 0
    while (opcao not in aux):
        opcao = input("Escolha uma opção: ")
    
    opcao = int(opcao)
    cur.close()
    conn.close()
    return(anos[opcao-1])  #Retorna o número do ano escolhido

def selecionarMesAnoViagem():
    conn = psycopg2.connect("host = localhost dbname=projeto user=postgres password=postgres")
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT extract(month from dataViagem), extract(year from dataViagem) \
                FROM viagem    \
                ORDER BY extract(year from dataViagem), extract(month from dataViagem)")    #na base de dados, vai buscar todos os meses e anos em que existem viagens
    
    meses = []
    anos = []
    i = 0
    aux = []
    for linha in cur.fetchall():    #vai buscar os números dos meses com viagens
        i += 1
        aux.insert(i, str(i))
        mes, ano = linha
        print(i, "-", mes, "/", ano)
        meses.insert(i-1, mes)  #Na célula i-1, coloca o valor do mês que foi lido
        anos.insert(i-1, ano)  #Na célula i-1, coloca o valor do ano que foi lido
    
    opcao = 0
    while (opcao not in aux):
        opcao = input("Escolha uma opção: ")
    
    opcao = int(opcao)
    cur.close()
    conn.close()
    return(meses[opcao-1], anos[opcao-1])  #Retorna o número do mês e o ano escolhido

def selecionarViagem():
    conn = psycopg2.connect("host = localhost dbname=projeto user=postgres password=postgres")
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT  idViagem, detalhes, dataViagem \
                    FROM viagem \
                    ORDER BY idViagem")     #na base de dados, vai buscar todas as vuagens que existem
    
    i = 0
    aux = []
    for linha in cur.fetchall():    #vai buscar os números dos meses com viagens
        i += 1
        idViagem, detalhes, dataViagem = linha
        print("Viagem número:", idViagem, "-", detalhes, "-", dataViagem)
        aux.insert(i, str(idViagem))

    opcao = 0
    while (opcao not in aux):
        opcao = input("Escolha o número da viagem que pretende: ")

    opcao = int(opcao)
    cur.close()
    conn.close()
    return(opcao)  #Retorna o idViagem