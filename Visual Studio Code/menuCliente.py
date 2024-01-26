def menuCliente():
    
    opcaoC = "0"

    while(opcaoC != "1" and opcaoC !="2" and opcaoC !="3"):
        print("1-Registar;")
        print("2-Log in;")
        print("3-Voltar atrás;")
        opcaoC = input("Escolha a opção:")
        if(opcaoC != "1" and opcaoC !="2" and opcaoC !="3"):
            print("Insira uma opçõa válida!\n")

    return (opcaoC)