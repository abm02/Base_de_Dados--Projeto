import psycopg2
import datetime

def envMsgs(idAdmin):
    opcao = '0'
    r = 0   #variável a ser devolvida (return) -> 0 se for para o programa terminar ; 1 se for para o programa correr este menu outra vez ; 2 se for para o programa voltar ao menu anterior
    while (opcao not in ['1', '2', 'B', 'b', 'E', 'e']):
        print("1 - Enviar uma mensagem para todos os clientes")
        print("2 - Enviar uma mensagem para um cliente específico")
        print("B - Regressar ao menu anterior")
        print("E - Terminar o programa")

        opcao = input("Escolha uma opção: ")

        if(opcao not in ['1', '2', 'B', 'b', 'E', 'e']):
            print("Insira uma opçõa válida!\n") #informar caso a opção escolhida não seja válida

    if (opcao=='1'):  #Se a opção escolhida for "Enviar uma mensagem para todos os clientes"
        print("\n\nDEFINA A MENSAGEM QUE QUER ENVIAR:")    
        dataEnvio = datetime.datetime.now().isoformat(' ', 'seconds')     #obtem o timestamp para o momento atual
        assunto = input("Escreva o assunto da mensagem:")
        corpoMensagem = input("Escreva o corpo da mensagem:")

        conn = psycopg2.connect("host = localhost dbname=projeto user=postgres password=postgres")
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO mensagem(dataEnvio, assunto, corpoMensagem, idAdmin) \
                            VALUES (%s, %s, %s, %s);", (dataEnvio, assunto, corpoMensagem, idAdmin,))       #insere na base de dados a mensagem que o utilizador quer enviar
            
            cur.execute("SELECT idMensagem  \
                            FROM mensagem   \
                            WHERE dataEnvio = %s \
                            AND assunto = %s   \
                            AND corpoMensagem = %s  \
                            AND idAdmin = %s", (dataEnvio, assunto, corpoMensagem, idAdmin,))       #na base de dados vai buscar o id da mensagem que acabou de ser escrita
            idMensagem, = cur.fetchone()

            cur.execute("SELECT DISTINCT idCliente  \
                                FROM cliente    \
                                ORDER BY idCliente")    #na base de dados, vai buscar os id de todos os clientes
            for linha in cur.fetchall():
                idCliente = linha
                cur.execute("INSERT INTO leitura(lida, idCliente, idMensagem)   \
                            VALUES (false, %s, %s);", (idCliente, idMensagem,))     #insere na base de dados, a informação da mensagem na parte da leitura
                
        except  psycopg2.DatabaseError:
            print("Aconteceu um erro com a base de dados e não foi possível enviar a mensagem.")
            print("Por favor tente outra vez!")
            conn.rollback()     #Se acontecer algum erro, anula todas as alterações feitas até ao momento
        
        conn.commit()
        cur.close()
        conn.close()
        r = 1   #correr este menu outra vez

    if (opcao=='2'):  #Se a opção escolhida for "Enviar uma mensagem para um cliente específico"
        print("\n\nDEFINA A MENSAGEM QUE QUER ENVIAR:")    
        dataEnvio = datetime.datetime.now().isoformat(' ', 'seconds')     #obtem o timestamp para o momento atual
        assunto = input("Escreva o assunto da mensagem:")
        corpoMensagem = input("Escreva o corpo da mensagem:")

        conn = psycopg2.connect("host = localhost dbname=projeto user=postgres password=postgres")
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO mensagem(dataEnvio, assunto, corpoMensagem, idAdmin) \
                            VALUES (%s, %s, %s, %s);", (dataEnvio, assunto, corpoMensagem, idAdmin,))       #insere na base de dados a mensagem que o utilizador quer enviar
                
            cur.execute("SELECT idMensagem  \
                            FROM mensagem   \
                            WHERE dataEnvio = %s \
                            AND assunto = %s   \
                            AND corpoMensagem = %s  \
                            AND idAdmin = %s", (dataEnvio, assunto, corpoMensagem, idAdmin,))       #na base de dados vai buscar o id da mensagem que acabou de ser escrita
            idMensagem, = cur.fetchone()


            print("\n\nSELECIONE O CLIENTE PARA O QUAL QUER ENVIAR A MENSAGEM:")
            cur.execute("SELECT idCliente, nome  \
                            FROM cliente    \
                            ORDER BY idCliente")        #na base de dados, vai buscar o idCliente e o nome de todos os clientes, para que o administrador escolha para qual é que quer enviar mensagem
            aux = []
            i = 0
            for linha in cur.fetchall():
                    idCliente, nome = linha
                    aux.insert(i, str(idCliente))            
                    i += 1
                    print(idCliente, "-", nome)
            
            idCliente = '-1'
            while (idCliente not in aux):
                idCliente = input("Insira o idCliente do cliente para o qual quer enviar a mensagem:")
            
            cur.execute("INSERT INTO leitura(lida, idCliente, idMensagem)   \
                        VALUES (false, %s, %s);", (idCliente, idMensagem,))     #insere na base de dados, a informação da mensagem na parte da leitura, para o cliente selecionado
                    
        except  psycopg2.DatabaseError:
            print("Aconteceu um erro com a base de dados e não foi possível enviar a mensagem.")
            print("Por favor tente outra vez!")
            conn.rollback()     #Se acontecer algum erro, anula todas as alterações feitas até ao momento
            
        conn.commit()
        cur.close()
        conn.close()
    
    elif (opcao=='B' or opcao=='b'): #Se a opção escolhida for "Regressar ao menu anterior"
        r = 2   #retornar ao menu anterior
    
    elif (opcao=='E' or opcao=='e'): #Se a opção escolhida for "Terminar o programa"
        r = 0   #terminar o programa

    return(r)