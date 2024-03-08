import random

#El Juego
Resultados = []
while True:
    print("Bienvenidos mi Casino")
    jugador = random.randint(2, 26)
    dealer =  random.randint(2, 26)
    #La Partida
    while True:
        print("El Jugador Saco: ", jugador, "El Dealer Saco: ", dealer)
        quiere_mas_cartas = input("¿Desea sacar otra carta? S/N ")
        if quiere_mas_cartas == "S":
            jugador = jugador + random.randiant(1, 13)
        else:
            if jugador == dealer:
                print("El Dealer es el Ganador")
                Resultados.append("Dealer")
                break
            elif jugador == 21 or (jugador > dealer and jugador < 21):
                print("El Jugador es el Ganador")
                Resultados.append("Jugador")
                break
            else:
                print("El Dealer es el Ganador")
                Resultados.append("Dealer")
                break
            
     preguntar_si_salir = input("Desea terminar el juego S/N ")
    if preguntar_si_salir == "S" :
        print("Adios, Gracias por perder tu dinero con nosotros!!")
        break
    else:
        print("/n"*20)
print(Resultados)

    