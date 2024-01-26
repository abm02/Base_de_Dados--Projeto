def menuInicial(): 
    opcao = "0"
    while(opcao != "1" and opcao !="2"):
        print("1-Entrar como Administrador;")
        print("2-Entrar como Cliente")
        opcao = input("Escolha a opção:")

        if(opcao != "1" and opcao !="2"):
            print("Insira uma opçõa válida!\n")

    return (opcao);