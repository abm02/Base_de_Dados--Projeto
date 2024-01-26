# Interface Ramo do administrador
import psycopg2
import string
import random
def menuAdmin():
    
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



   # (!) arranjar maneira de voltar para trás
    while(1):
        print("Para voltar atrás escreva a letra 'E'(exit), no email e na password\n")
        email = input("Inserir Email: ")
        pw = input("Inserir Password: ")
        cur.execute("SELECT emailadmin,passadmin FROM administrador ")

        if email == 'E' and pw == 'E':
            return(False)


        for linha in cur.fetchall():
            emailadmin, passadmin = linha

            #desincripta pass
            decoded_pass=""

            for letter in passadmin:
                index = key.index(letter)
                decoded_pass += chars[index]
    
            #print (decoded_pass)
            # fim da desincriptação 


            if emailadmin == email and pw == decoded_pass:
                print("LOGIN VÁLIDO!")
                #fecha o cursor e termina conexão
                cur.close()
                conn.close()
                return(True) 
        print("E-mail ou password incorretos! Tente novamente.\n")
