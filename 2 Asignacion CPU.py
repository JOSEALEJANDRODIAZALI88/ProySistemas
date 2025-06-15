# Simulación de planificación de CPU: FCFS, SJF, Round Robin

from collections import deque
import pandas as pd

# Definición de procesos: (ID, tiempo de llegada, duración)
procesos = [
    ("P1", 0, 8),
    ("P2", 1, 4),
    ("P3", 2, 9),
    ("P4", 3, 5)
]

def fcfs(procesos):
    procesos_ordenados = sorted(procesos, key=lambda x: x[1])  # orden por llegada
    tiempo = 0
    resultados = []

    for pid, llegada, duracion in procesos_ordenados:
        if tiempo < llegada:
            tiempo = llegada
        inicio = tiempo
        fin = inicio + duracion
        resultados.append((pid, llegada, duracion, inicio, fin, fin - llegada, inicio - llegada))
        tiempo = fin

    return resultados

def sjf(procesos):
    procesos = sorted(procesos, key=lambda x: x[1])  # ordenar por llegada
    lista_espera = []
    tiempo = 0
    completados = []
    i = 0

    while len(completados) < len(procesos):
        while i < len(procesos) and procesos[i][1] <= tiempo:
            lista_espera.append(procesos[i])
            i += 1
        if lista_espera:
            lista_espera.sort(key=lambda x: x[2])  # ordenar por duración
            pid, llegada, duracion = lista_espera.pop(0)
            inicio = tiempo
            fin = inicio + duracion
            completados.append((pid, llegada, duracion, inicio, fin, fin - llegada, inicio - llegada))
            tiempo = fin
        else:
            tiempo += 1

    return completados

def round_robin(procesos, quantum=3):
    procesos = sorted(procesos, key=lambda x: x[1])
    cola = deque()
    tiempo = 0
    i = 0
    resultado = []
    tiempos_restantes = {p[0]: p[2] for p in procesos}
    inicio_proceso = {}
    completados = set()

    while len(completados) < len(procesos):
        while i < len(procesos) and procesos[i][1] <= tiempo:
            cola.append(procesos[i][0])
            i += 1

        if not cola:
            tiempo += 1
            continue

        actual = cola.popleft()
        if actual not in inicio_proceso:
            inicio_proceso[actual] = tiempo

        ejec = min(quantum, tiempos_restantes[actual])
        tiempo += ejec
        tiempos_restantes[actual] -= ejec

        while i < len(procesos) and procesos[i][1] <= tiempo:
            cola.append(procesos[i][0])
            i += 1

        if tiempos_restantes[actual] > 0:
            cola.append(actual)
        else:
            p = next(p for p in procesos if p[0] == actual)
            fin = tiempo
            resultado.append((actual, p[1], p[2], inicio_proceso[actual], fin, fin - p[1], inicio_proceso[actual] - p[1]))
            completados.add(actual)

    return resultado

# Ejecutar simulaciones
df_fcfs = pd.DataFrame(fcfs(procesos), columns=["PID", "Llegada", "Duración", "Inicio", "Fin", "Turnaround", "Espera"])
df_sjf = pd.DataFrame(sjf(procesos), columns=["PID", "Llegada", "Duración", "Inicio", "Fin", "Turnaround", "Espera"])
df_rr = pd.DataFrame(round_robin(procesos), columns=["PID", "Llegada", "Duración", "Inicio", "Fin", "Turnaround", "Espera"])

# Mostrar resultados
print("\n--- FCFS ---\n", df_fcfs)
print("\n--- SJF ---\n", df_sjf)
print("\n--- Round Robin ---\n", df_rr)
