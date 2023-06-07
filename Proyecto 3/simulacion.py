from clases import *
import random
import math

lambda_ = 0
queues = []
mu = []
matrix = []
eventQueue = []
clients = []
countClient = 0
nQueues = 0

def simule(filename, totalTime):
    readFile(filename)

    create(totalTime)

    #print(f"Lambda: {lambda_}")
    #print(f"queues: {queues}")
    #print(f"Mu: {mu}")
    #print(f"matrix: {matrix}")
    return 0


def readFile(filename):
    global lambda_, queues, mu, matrix, nQueues

    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"El archivo {filename} no existe.")
    except IOError:
        print(f"No se puede abrir el archivo {filename}.")

    lambda_ = float(lines[0])
    nQueues = int(lines[1])

    # Crear colas
    for i in range(0, nQueues):
        queues.append(Queue(i))

    # Leer mu de colas y agregar a la lista
    for i in range(0, nQueues):
        mu.append(float(lines[i + nQueues]))

    # Leer cadena de markov y agregar a la matriz
    for i in range(nQueues+len(mu), len(lines)):
        row = []
        values = lines[i].strip().split()
        for value in values:
            row.append(float(value))
        matrix.append(row)

    return 0

def getTime(number):
    if len(eventQueue) == 0:
        return (-1 * math.log(random.random())) / number
    else:
        return eventQueue[len(eventQueue) - 1].tiempo + ((-1 * math.log(random.random())) / number)
    
def getDecision():
    rand = random.random()  # Generar número aleatorio entre 0 y 1
    total = 0.0
    queue = -1

    # Recorrer las columnas de la matriz
    for i in range(len(matrix[0])):
        total += matrix[0][i]  # Sumar la probabilidad de la columna actual

        # Verificar si el número aleatorio está dentro de la suma acumulada de probabilidades
        if rand <= total:
            queue = i
            break

    return queue

# Función para insertar un evento en el arreglo de eventos
def insert_event(event):
    global eventQueue

    # Verificar si el arreglo de eventos está vacío
    if not eventQueue:
        eventQueue.append(event)
    else:
        # Recorrer el arreglo de eventos y encontrar la posición adecuada según el atributo de tiempo
        for i in range(len(eventQueue)):
            if event.time < eventQueue[i].time:
                eventQueue.insert(i, event)
                break
        else:
            # Si no se encontró una posición adecuada, insertar el evento al final del arreglo
            eventQueue.append(event)


def create(totalTime):
    global countClient, eventQueue

    time = getTime(lambda_)
    client = Client(countClient)
    clients.append(client)
    insert_event(Event(client.id_client, "Llegada al sistema", time))
    countClient += 1
    if time >= totalTime:
        return 0
    
    decision(totalTime, client)

    #crear siguiente cliente
    create(totalTime)


def decision(totalTime, client):
    #decision cadena de markov
    n = getDecision()

    #cuando si entra a una cola
    if n != -1:
        #si el servidor esta ocupado
        if queues[n].server == True:
            time = getTime(lambda_)
            insert_event(Event(client.id_client, "Entrada a cola {n}", time))
        #si el servidor esta libre
        else:
            queues[n].server = True
            time = getTime(lambda_)
            insert_event(Event(client.id_client, "Entra a servidor {n}", time))

            #tiempo de servicio
            time = getTime(mu[n])
            insert_event(Event(client.id_client, "Salida de cola {n}", time))

            #vuelve a escoger desicion
            decision(totalTime, client)

    #cuando no entra a cola
    else:
        time = getTime(lambda_)
        insert_event(Event(client.id_client, "Salida del sistema", time))

    return 0



#print(simule("archivo.txt", 100))