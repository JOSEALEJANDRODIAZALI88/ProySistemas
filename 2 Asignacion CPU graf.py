import matplotlib.pyplot as plt

procesos = [
    {'pid': 'P1', 'llegada': 0, 'duracion': 8},
    {'pid': 'P2', 'llegada': 1, 'duracion': 4},
    {'pid': 'P3', 'llegada': 2, 'duracion': 9},
    {'pid': 'P4', 'llegada': 3, 'duracion': 5}
]

def fcfs(procesos):
    tiempo = 0
    resultado = []
    for p in sorted(procesos, key=lambda x: x['llegada']):
        inicio = max(tiempo, p['llegada'])
        fin = inicio + p['duracion']
        resultado.append({
            'PID': p['pid'], 'Inicio': inicio, 'Fin': fin,
            'Llegada': p['llegada'], 'Duración': p['duracion']
        })
        tiempo = fin
    return resultado

def sjf(procesos):
    tiempo = 0
    pendiente = procesos[:]
    resultado = []
    completados = []

    while pendiente:
        disponibles = [p for p in pendiente if p['llegada'] <= tiempo]
        if not disponibles:
            tiempo += 1
            continue
        siguiente = min(disponibles, key=lambda x: x['duracion'])
        inicio = tiempo
        fin = inicio + siguiente['duracion']
        resultado.append({
            'PID': siguiente['pid'], 'Inicio': inicio, 'Fin': fin,
            'Llegada': siguiente['llegada'], 'Duración': siguiente['duracion']
        })
        tiempo = fin
        pendiente.remove(siguiente)
    return resultado

def round_robin(procesos, quantum=3):
    cola = procesos[:]
    tiempo = 0
    en_ejecucion = []
    pendientes = [{'pid': p['pid'], 'llegada': p['llegada'], 'duracion': p['duracion']} for p in cola]
    cola_espera = []

    while pendientes or cola_espera:
        # Agregar procesos nuevos a la cola
        cola_espera += [p for p in pendientes if p['llegada'] <= tiempo]
        pendientes = [p for p in pendientes if p['llegada'] > tiempo]

        if not cola_espera:
            tiempo += 1
            continue

        actual = cola_espera.pop(0)
        ejec = min(quantum, actual['duracion'])
        en_ejecucion.append({
            'PID': actual['pid'],
            'Inicio': tiempo,
            'Fin': tiempo + ejec
        })
        tiempo += ejec
        actual['duracion'] -= ejec
        if actual['duracion'] > 0:
            # vuelve a la cola
            actual['llegada'] = tiempo
            pendientes.append(actual)

    return en_ejecucion

def graficar(planificacion, titulo):
    colores = {'P1': 'skyblue', 'P2': 'lightgreen', 'P3': 'salmon', 'P4': 'orange'}
    fig, ax = plt.subplots()
    for i, item in enumerate(planificacion):
        ax.barh(y=item['PID'], width=item['Fin'] - item['Inicio'],
                left=item['Inicio'], color=colores.get(item['PID'], 'gray'))
        ax.text(x=item['Inicio'] + 0.5, y=i, s=f"{item['Inicio']}-{item['Fin']}", va='center', fontsize=8)

    ax.set_title(titulo)
    ax.set_xlabel("Tiempo")
    ax.set_ylabel("Proceso")
    plt.tight_layout()
    plt.show()

# Ejecutar y graficar cada algoritmo
for metodo, func in [('FCFS', fcfs), ('SJF', sjf), ('Round Robin', round_robin)]:
    plan = func(procesos)
    graficar(plan, f"Planificación {metodo}")
    plt.pause(2)  # Mostrar cada figura por 2 segundos
    plt.close()
