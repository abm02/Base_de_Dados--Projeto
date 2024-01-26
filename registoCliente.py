import psycopg2
import string
import random
def registoCliente():
    
    print("Registo Cliente\n")

    conn = psycopg2.connect("host=localhost dbname=projeto user=postgres password=postgres")
    cur = conn.cursor()
    
    novo_nif=input("Insira o seu NIF: ")
    novo_nome = input("Insira o seu primeiro e último nome: ")
    novo_num = input("Insira o seu número de telemóvel: ")
    novo_email = input("Insira o seu e-mail: ")
    novo_status= False # só pode ser atribuido pelo admin por isso quando se regista vai estar a false
    nova_pass=input("Insira uma password:")
    
    # encriptação da password
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
    
    encripted_pass=""

    for letter in nova_pass:
        index = chars.index(letter)
        encripted_pass += key[index]
    
    #print (encripted_pass)
    # fim da encriptação
    cur.execute("INSERT INTO cliente(idcliente,nifcliente, nome, numtelemovel,email,clientegold,passcliente) \
        VALUES (%s,%s,%s,%s,%s,%s)",(novo_nif,novo_nome, novo_num, novo_email, novo_status,encripted_pass))
    
    conn.commit() # para colocar a alteração na base de dados
    cur.close()
    conn.close()