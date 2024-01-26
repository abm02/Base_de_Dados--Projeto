def menu1():
    opcao = "0"
    while(opcao != "1" and opcao !="2" and opcao !="3"):
        print("1-Viagens;")
        print("2-Mensagens;")
        print("3-Voltar atrás")
        opcao = input("Escolha a opção:")

        if(opcao != "1" and opcao !="2"and opcao !="3"):
            print("Insira uma opçõa válida!\n")

    return (opcao)