import psycopg2
import menuInicial
import menuAdmin
import menu2
import menuGestViagens
import menuEstat
import atrEstatuto
import envMsgs
import menuCliente
import registoCliente
import loginCliente
import menu1
import menuViagens
import menuMsgs
from datetime import datetime # para tempo


# Estabelecimento da ligação à base de dados
conn = psycopg2.connect("host=localhost dbname=projeto user=postgres password=postgres")
cur = conn.cursor()
#

AdminOuCliente = int(menuInicial.menuInicial())  #AdminOuCliente terá o valor 1 se se tiver entrado como administrador e 2 se tiver entrado como Cliente

if (AdminOuCliente == 1):       #Se for administrador
    opcaoMenuAdmin=menuAdmin.menuAdmin()

    auxMenu2 = -1   #Colocar o valor -1 quando for para regressar ao Menu2
    while (auxMenu2 == -1):
        auxMenu2 = 0
        opcaoMenu2 = int(menu2.menu2())
        if (opcaoMenu2 == 1):   #Se a opção escolhida no Menu2 for Gestão de Viagens
            opcaoGestViagens = int(menuGestViagens.menuGestViagens())
            if (opcaoGestViagens == 0):  #Se a opção escolhida no menuGestViagens for Lista de Viagens
                #termina programa
                exit()
            
            elif (opcaoGestViagens == 1): #Se a opção escolhida no menuGestViagens for Adicionar Viagens
                #volta a correr programa
                auxMenu2=-1
            
            elif (opcaoGestViagens == 2): #Se a opção escolhida no menuGestViagens for Adicionar Viagens
                auxMenu2=-1
                opcaoMenu2 = 1
            
        elif (opcaoMenu2 == 2):   #SE A OPÇÃO ESCOLHIDA NO Menu2 FOR Estatísticas------------------------------------------------
            auxMenuEstat = -1 #Colocar o valor -1 quando for para regressar ao menuEstat
            while (auxMenuEstat == -1):
                opcaoMenuEstat = menuEstat.menuEstat()
                if (opcaoMenuEstat == 0):  #terminar
                    exit()
                elif (opcaoMenuEstat == 1):  #repetir o menuEstat
                    auxMenuEstat = -1
                elif (opcaoMenuEstat == 2):  #voltar ao Menu2
                    auxMenuEstat = 0
                    auxMenu2 = -1

        elif (opcaoMenu2 == 3):   #Se a opção escolhida no Menu2 for Atribuir Estatutos
            auxMenuEstatuto = -1
            while(auxMenuEstatuto==-1):
                opcaoEstatuto=atrEstatuto.atrEstatuto()
                if (opcaoEstatuto == 0):
                    exit()
                elif (opcaoEstatuto == 1):
                    auxMenuEstatuto=-1
                elif (opcaoEstatuto == 2):
                    auxMenuEstatuto=0
                    auxMenu2 = -1
        elif (opcaoMenu2 == 4):   #SE A OPÇÃO ESCOLHIDA NO Menu2 FOR Enviar Mensagem ------------------------------------------------
            auxEnvMsgs = -1 #Colocar o valor -1 quando for para regressar ao envMsgs
            while (auxEnvMsgs == -1):
                opcaoEnvMsgs = envMsgs.envMsgs()  
                if (opcaoEnvMsgs == 0):  #terminar
                    exit()
                elif (opcaoEnvMsgs == 1):  #repetir o envMsgs
                    auxEnvMsgs = -1
                elif (opcaoEnvMsgs == 2):  #voltar ao Menu2
                    auxEnvMsgs = 0
                    auxMenu2 = -1

        elif (opcaoMenu2 == 5):   #Se a opção escolhida no Menu2 for Voltar atrás
            menuAdmin.menuAdmin()

elif (AdminOuCliente == 2):       #Se for cliente
    auxMenuCliente = -1 #Colocar o valor -1 quando for para regressar ao MenuCliente
    while (auxMenuCliente == -1):
        auxMenuCliente = 0
        opcaoMenuCliente = int(menuCliente.menuCliente())
        if (opcaoMenuCliente == 1):     #Se a opção escolhida no MenuCliente for Registar
            registoCliente.registoCliente()
            idCliente=loginCliente.loginCliente()
        elif (opcaoMenuCliente == 2):     #Se a opção escolhida no MenuCliente for Login
            idCliente=loginCliente.loginCliente()
            
        elif (opcaoMenuCliente == 3):     #Se a opção escolhida no MenuCliente for Voltar atrás
            auxMenuCliente = 0
            AdminOuCliente=0

        auxMenu1 = -1   #Colocar o valor -1 quando for para regressar ao Menu1
        while (auxMenu1 == -1):
            auxMenu1 = 0
            opcaoMenu1 = int(menu1.menu1())
            if (opcaoMenu1 == 1):   #Se a opção escolhida no Menu1 for Viagens
                opcaoMenuViagens = menuViagens.menuViagens(idCliente)
                if (opcaoMenuViagens == 0):     #Se a opção escolhida no menuViagens for Reservar Viagens
                    exit()
                elif (opcaoMenuViagens == 1):     #Se a opção escolhida no menuViagens for Viagens Reservadas
                    auxMenu1=-1        
                elif (opcaoMenuViagens == 2):     #Se a opção escolhida no menuViagens for Lista Destinos
                    auxMenu1=-1
                    opcaoMenu1=0
                

            elif (opcaoMenu1 == 2): #SE A OPÇÃO ESCOLHIDA NO Menu1 FOR Mensagens ------------------------------------------------
                auxMenuMsgs = -1 #Colocar o valor -1 quando for para regressar ao menuMsgs
                while (auxMenuMsgs == -1):
                    opcaoMenuMsgs = menuMsgs.menuMsgs(idCliente) 
                    if (opcaoMenuMsgs == 0):  #terminar
                        exit()
                    elif (opcaoMenuMsgs == 1):  #repetir o MenuMsgs
                        auxMenuMsgs = -1
                    elif (opcaoMenuMsgs == 2):  #voltar ao Menu1
                        auxMenuMsgs = 0
                        auxMenu1 = -1

            elif (opcaoMenu1 == 3): #Se a opção escolhida no Menu1 for Voltar atrás
                auxMenuCliente = -1