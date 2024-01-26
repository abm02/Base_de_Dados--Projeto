def menu2():
    opcao = "0"
    while(opcao != "1" and opcao !="2" and opcao !="3"and opcao !="4"and opcao !="5"):
        print("1-Gestão de Viagens;")
        print("2-Estatísticas;")
        print("3-Atribuir Estatutos")
        print("4-Enviar Mensagem;")
        print("5-Voltar atrás")
        opcao = input("Escolha a opção:")

        if(opcao != "1" and opcao !="2"and opcao !="3" and opcao !="4"and opcao !="5"):
            print("Insira uma opçõa válida!\n")

    return (opcao)