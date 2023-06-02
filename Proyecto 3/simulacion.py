import random

def generate_exponential(rate):
    return -1/rate * math.log(1 - random.random())

def simulate_queues(rate, num_queues, service_rates, transition_matrix, simulation_time):
    event_queue = [(0, 0)]  # (time, queue)
    queues = [[] for _ in range(num_queues)]
    arrivals = 0
    departures = 0
    total_wait_time = 0
    total_queue_length = [0] * num_queues
    queue_lengths = [[] for _ in range(num_queues)]

    while event_queue[0][0] < simulation_time:
        time, queue = event_queue.pop(0)

        if queue == num_queues:
            departures += 1
        else:
            if queue_lengths[queue]:
                wait_time = time - queue_lengths[queue].pop(0)
                total_wait_time += wait_time
                total_queue_length[queue] -= 1
            else:
                wait_time = 0

            if queue == 0:
                arrivals += 1
                next_queue = random.choices(range(num_queues + 1), weights=transition_matrix[queue])[0]
                if next_queue != 0:
                    queue_lengths[next_queue-1].append(time)
                    total_queue_length[next_queue-1] += 1
            else:
                next_queue = queue + 1

            service_time = generate_exponential(service_rates[queue])
            event_queue.append((time + service_time, next_queue))
            event_queue.sort()

    avg_wait_time = total_wait_time / departures
    avg_queue_length = [sum(queue_lengths[i]) / simulation_time for i in range(num_queues)]
    utilization = [total_queue_length[i] / simulation_time for i in range(num_queues)]
    
    return arrivals, departures, avg_queue_length, avg_wait_time, utilization

# Lectura de parámetros desde un archivo
filename = "colas.txt"
with open(filename, 'r') as file:
    rate = float(file.readline())
    num_queues = int(file.readline())
    service_rates = [float(file.readline()) for _ in range(num_queues)]
    transition_matrix = [list(map(float, file.readline().split())) for _ in range(num_queues)]

simulation_time = 100000
arrivals, departures, avg_queue_length, avg_wait_time, utilization = simulate_queues(rate, num_queues, service_rates, transition_matrix, simulation_time)

# Reporte de resultados
for i in range(num_queues):
    print(f"Cola {i+1}:")
    print(f"Número de llegadas: {arrivals}")
    print(f"Número de salidas: {departures}")
    print(f"Longitud promedio de la cola: {avg_queue_length[i]}")
    print(f"Tiempo de espera promedio: {avg_wait_time}")
    print(f"Utilización: {utilization[i]}")
    print()
