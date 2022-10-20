def parseInput(fileName):
    lineasGenoma = []
    with open(f"instances/{fileName}", 'r') as file:
        for line in file:
            lineasGenoma.append(line.strip())

    m = len(lineasGenoma[0])
    n = len(lineasGenoma)

        
    return lineasGenoma, m, n