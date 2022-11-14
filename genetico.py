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


def cross(parents,nPoints=5):
    C = []
    points = []
    crossRange = 300 // nPoints
    for i in range(nPoints):
        points.append(random.randint(i*crossRange, (i+1)*crossRange))

    for p in parents:
        child = ''
        p1Flag = True
        for i in range(len(p['p1']['s'])):
            if i in points:
                p1Flag = not p1Flag
            if p1Flag:
                child += p['p1']['s'][i]
            else:
                child += p['p2']['s'][i]

        C.append({'s': child, 'f': 0})
        
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

def replace(P, C):
    # best 5 solutions from P
    elite = sorted(P, key=itemgetter('f'), reverse=True)[:5]
    
    replacement = sorted(C, key=itemgetter('f'), reverse=True)[:len(P)-5]

    return elite + replacement

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
    pSize = 50
    tournamentSize = 3
    geneticoLimit = 90

    lineasGenoma, m, n = parseInput(fileName)
    threshold = ceil(th * m)

    start = time.time()

    # Población inicial
    P = []

    # Generar población inicial a partir del greedy aleatorizado
    for i in range(pSize):
        # calidad, sol = grasp(m,n,th,lineasGenoma, 1)
        sol,calidad = greedy(m,n,th,lineasGenoma, 0.9)
        aux = {'s': sol, 'f': calidad}
        P.append(aux)

    bestFitness = max(P, key=itemgetter('f'))['f']
    print(f'Initial best fitness: {bestFitness}')

    while time.time() - start < geneticoLimit:
        # Seleccionar padres
        parents = selection(P, tournamentSize)
        # Cruza
        C = cross(parents)
        # Mutación
        mutation(C)
        # Evaluación
        evaluation(C, lineasGenoma, threshold, m)
        # Reemplazo
        P = replace(P, C)

        currentBestFitness = max(P, key=itemgetter('f'))['f']
        if currentBestFitness > bestFitness:
            bestFitness = currentBestFitness
            print(f'New best fitness: {bestFitness} ----> {time.time() - start}s')







if __name__ == "__main__":
    main()