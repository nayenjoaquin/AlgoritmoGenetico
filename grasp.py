import time
from greedy import greedy
from localSearch2 import localSearch as localSearch2




def grasp(m,n,th,lineasGenoma,timeLimit):
    start = time.time()
    bestSoFar = 0
    bestSol = ""

    while time.time() - start < timeLimit:
        sol,calidad = greedy(m,n,th,lineasGenoma, 0.9)
        bestSol = sol
        bestSoFar = calidad

        sol, calidad = localSearch2(sol, lineasGenoma, th, m, bestSoFar, start, timeLimit, 0.25,1)
        if calidad > bestSoFar:
            bestSoFar = calidad
            bestSol = sol

    return bestSoFar, bestSol