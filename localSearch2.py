from math import ceil
from random import randint
from secrets import randbelow
import time
from greedy import getCalidadSolucion

# estructuras para pasar de un entero a un char y de un char a su respectivo entero
intToChar = ["A", "C", "G", "T"]
charToInt = {"A": 0,"C": 1,"G": 2,"T": 3}

def localSearch(sol, lineasGenoma, th, m, bestSoFar, totalTime, timeLimit, localSearchLimit, tunning):

    threshold = int(ceil(m*th))

    # creamos las variables que tendran la mejor solucion y su respectiva calidad
    mejorSol = sol
    mejorCalidad = bestSoFar

    start = time.time()

    # hacemos búsqueda local mientras no se encuentre una mejor solución en un
    # tiempo determinado y no se supere el tiempo límite del problema
    while time.time() - start < localSearchLimit and time.time() - totalTime < timeLimit:

        # largo aleatorio de substring a cambiar
        gap = randint(1, 5)
        i = randbelow(m - gap) # posicion inicial aleatoria
        j = i + gap # posicion final

        # generamos un substring aleatorio
        replace = "".join([intToChar[randbelow(4)] for _ in range(gap)])

        # generamos la nueva solucion y calculamos su calidad
        solAux = mejorSol[:i] + replace + mejorSol[j:]
        calidadAux = getCalidadSolucion(lineasGenoma, solAux, threshold)

        # si la calidad es mejor que la mejor calidad hasta el momento, actualizamos
        if calidadAux > mejorCalidad:

            mejorSol = solAux
            mejorCalidad = calidadAux

            # reiniciamos el timer de búsqueda local
            start = time.time()

            if tunning == 0: print(f"mejor calidad: {mejorCalidad} -------> {time.time() - totalTime} s")

    # retornamos la mejor solucion y su calidad
    return mejorSol, mejorCalidad