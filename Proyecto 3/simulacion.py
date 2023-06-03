lambda_ = 0
colas = []
mu = []
matriz = []

def simule(filename, totalTime):
    readFile(filename)

    print(f"Lambda: {lambda_}")
    print(f"Colas: {colas}")
    print(f"Mu: {mu}")
    print(f"Matriz: {matriz}")

    return 0


def readFile(filename):
    global lambda_, colas, mu, matriz

    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"El archivo {filename} no existe.")
    except IOError:
        print(f"No se puede abrir el archivo {filename}.")

    lambda_ = float(lines[0])
    colas = int(lines[1])

    for i in range(0, colas):
        mu.append(float(lines[i + colas]))

    for i in range(colas+len(mu), len(lines)):
        row = []
        values = lines[i].strip().split()
        for value in values:
            row.append(float(value))
        matriz.append(row)

    return 0

print(simule("archivo.txt", 100))