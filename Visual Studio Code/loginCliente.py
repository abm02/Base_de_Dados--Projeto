import psycopg2
import string
import random

def loginCliente():

    conn = psycopg2.connect("host=localhost dbname=projeto user=postgres password=postgres")
    cur = conn.cursor()

    # criação da encriptação
    # https://www.youtube.com/watch?v=vsLBErLWBhA
    # foi aproveitado deste video, no entanto, foi guardada a key para se poder
    # desincriptar o que for guardado na base de dados
    chars = " " + string.punctuation + string.digits + string.ascii_letters
    #chars=list(chars)

    #key=chars.copy()
    #random.shuffle(key)
    key=['J', '^', '.', 'A', '%', '!', 'C', '0', '9', 'L', '3', '2', 'U', 'i', 'I', ';', '/', '}', '(', 'X', '8', 'd', ']', 'z', '&', '-', 'o', 'B', '4', 'Y', 'u', 'b', 'T', '>', 'R', '?', 'l', '$', '\\', 'a', '@', '`', 'V', '5', 'G', '=', 'S', 'N', 'w', 'p', 'y', ')', 'h', '#', 'g', 'O', 'D', '<', 't', 'M', 'q', 'Q', 'r', ',', '*', 'x', 'v', ' ', '7', 'H', "'", '+', 'W', '|', ':', 'Z', 'K', '{', 
'_', 's', 'j', 'e', 'm', 'f', '"', 'c', '6', 'k', 'n', '1', 'E', '~', '[', 'F', 'P']


    while(1):
        print("Para voltar atrás escreva a letra 'E'(exit), no NIF e na password\n")
        nif = input("Inserir NIF:")
        pw = input("Inserir Password:")

        if nif == 'E' and pw == 'E':
            print("EXIT")
            # acrescentar ao menu inicial que se retornar false deve voltar ao menu Inicial

        cur.execute("SELECT nifcliente, passcliente FROM cliente")
        # (+) Verificação das credenciais
        
        for linha in cur.fetchall():
            # carrega uma linha
            nifcliente, passcliente = linha
            #desincripta pass
            decoded_pass=""

            for letter in passcliente:
                index = key.index(letter)
                decoded_pass += chars[index]
    
            #print (decoded_pass)
            # fim da desincriptação 
            if (nifcliente == int(nif)) and (decoded_pass==pw):
                # fechar cursor e terminar conexão
                print("LOG IN VÁLIDO!")
                cur.execute("SELECT idcliente FROM cliente WHERE nifcliente=%s",(nifcliente,))
                res=cur.fetchall()[0]
                cur.close()
                conn.close()
                return(res[0]) 
        print("NIF ou password incorretos! Tente novamente.\n")
