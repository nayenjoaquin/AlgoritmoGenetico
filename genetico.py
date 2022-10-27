from math import ceil
import sys
import time
from parseInput import parseInput
from greedy import greedy
from greedy import getCalidadSolucion
from grasp import grasp
import random
from operator import itemgetter


intToChar = ['A', 'C', 'G', 'T']

def selection(P, tournamentSize):
    parents = []
    for p in P:

        rivals = [p]

        for i in range(tournamentSize-1):
            randomIndex = random.randint(0, len(P)-1)
            randomCandidate = P[randomIndex]

            if len(randomCandidate['s']) != 300:
                print(f'randomIndex: {randomIndex}')
                print(f'randomCandidate: {randomCandidate}')
                print(f'P[randomIndex]: {P[randomIndex]}')
                printGeneration(P)
                quit()

            rivals.append(P[random.randint(1, len(P)-1)])

        rivals = sorted(rivals, key=itemgetter('f'), reverse=True)

        parents.append({
            'p1': rivals[0],
            'p2': rivals[1]
        })

    
    return parents


def cross(parents):
    C = []
    for p in parents:
        p1 = p['p1']['s']
        p2 = p['p2']['s']
        if len(p1) != 300: print(f'p1: {len(p1)}')
        if len(p2) != 300: print(f'p2: {len(p2)}')
        c = p1[:len(p1)//2] + p2[len(p2)//2:]
        C.append({'s': c, 'f': 0})

    return C

def randomGen(size):
    return ''.join(random.choice(intToChar) for _ in range(size))

def mutation(C):
    gap = random.randint(0, 5)
    for c in C:
        if random.random() < 0.1:
            pos = random.randint(0, len(c['s'])-gap)
            c['s'] = c['s'][:pos] + randomGen(gap) + c['s'][pos+gap:]



def evaluation(P, lineasGenoma, th, m):
    for i in range(len(P)):
        P[i]['f'] = getCalidadSolucion(lineasGenoma, P[i]['s'], th)
    return P

def printGeneration(P):
    for p in P:
        print(p['s'])

def printParentsFitness(parents):
    for p in parents:
        print(p['p1']['f'], p['p2']['f'])

def printFitness(P):
    for p in P:
        print(p['f'])

def main():

    fileName = sys.argv[2]
    th = 0.85
    pSize = 10
    tournamentSize = 3
    geneticoLimit = 90

    lineasGenoma, m, n = parseInput(fileName)
    threshold = ceil(th * m)

    start = time.time()

    # Población inicial
    P = []

    # Generar población inicial a partir del greedy aleatorizado
    for i in range(pSize):
        calidad, sol = grasp(m,n,th,lineasGenoma, 0.5)
        #sol,calidad = greedy(m,n,th,lineasGenoma, 0.9)
        aux = {'s': sol, 'f': calidad}
        P.append(aux)


    # while time.time() - start < geneticoLimit:
    # Seleccionar padres
    parents = selection(P, tournamentSize)
    # Cruza
    C = cross(parents)
    # Mutación
    # mutation(C)
    # Evaluación
    evaluation(C, lineasGenoma, threshold, m)

    # print(f'Initial population best fitness: {max(P, key=itemgetter("f"))["f"]}')
    # print(f'Children population best fitness: {max(C, key=itemgetter("f"))["f"]}')






if __name__ == "__main__":
    main()