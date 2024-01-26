import psycopg2
def atrEstatuto():
    print("Atribuir Estatutos")

    conn = psycopg2.connect("host=localhost dbname=projeto user=postgres password=postgres")
    cur = conn.cursor()

    id_cliente = input("Insira o ID do cliente a quem pretende atribuir estatuto gold:")

    cur.execute("UPDATE cliente \
                SET clientegold = true \
                WHERE idcliente=%s",(id_cliente,))
    
    opcao_ord = 0
    while (opcao_ord not in ['1',"B",'b','e','E']):
        print("1 - Atribuir estatuto a outro cliente")
        print("B - Regressar ao menu anterior")
        print("E - Terminar o programa")

        opcao_ord = input("Escolha uma opção: ")

        if  (opcao_ord not in ['1',"B",'b','e','E']):
            print("Insira uma opção válida!\n")
    if opcao_ord == 1:
        r=1
    elif opcao_ord == 'b' or opcao_ord == 'B':
        r=2
    elif opcao_ord == 'e' or opcao_ord == 'E':
        r=0
    
    
    conn.commit()    
    cur.close()
    conn.close()
    
    return(r)
    