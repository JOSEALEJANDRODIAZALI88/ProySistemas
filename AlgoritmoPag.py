import random
from collections import deque
import matplotlib.pyplot as plt

def imprimir_metricas(nombre, fallos, total, resultados, costos):
    aciertos = total - fallos
    frecuencia = fallos / total
    rendimiento = 1 - frecuencia
    costo = fallos * 3 + aciertos * 1

    print(f"\n== {nombre} ==")
    print(f"Tiempo (Cantidad de Referencias): {total}")
    print(f"Número de Fallos: {fallos}")
    print(f"Frecuencia: {fallos}/{total} = {frecuencia:.2f}")
    print(f"Rendimiento: 1 - {frecuencia:.2f} = {rendimiento:.2f}")
    print(f"Rendimiento (%): {rendimiento * 100:.2f}%")
    print(f"Costo total: {fallos}*3 + {aciertos}*1 = {costo}")

    resultados[nombre] = rendimiento * 100
    costos[nombre] = costo

def fifo(reference_string, num_frames, resultados, costos):
    memory = deque()
    page_faults = 0
    for page in reference_string:
        if page not in memory:
            page_faults += 1
            if len(memory) >= num_frames:
                memory.popleft()
            memory.append(page)
    imprimir_metricas("FIFO", page_faults, len(reference_string), resultados, costos)

def lru(reference_string, num_frames, resultados, costos):
    memory = []
    page_faults = 0
    for page in reference_string:
        if page in memory:
            memory.remove(page)
        else:
            page_faults += 1
            if len(memory) >= num_frames:
                memory.pop(0)
        memory.append(page)
    imprimir_metricas("LRU", page_faults, len(reference_string), resultados, costos)

def optimal(reference_string, num_frames, resultados, costos):
    memory = []
    page_faults = 0
    for i in range(len(reference_string)):
        page = reference_string[i]
        if page not in memory:
            page_faults += 1
            if len(memory) < num_frames:
                memory.append(page)
            else:
                future = reference_string[i+1:]
                indices = [(p, future.index(p) if p in future else float('inf')) for p in memory]
                victim = max(indices, key=lambda x: x[1])[0]
                memory.remove(victim)
                memory.append(page)
    imprimir_metricas("ÓPTIMO", page_faults, len(reference_string), resultados, costos)

def nru(reference_string, num_frames, resultados, costos):
    random.seed(0)
    memory = {}
    page_faults = 0
    for page in reference_string:
        if page not in memory:
            page_faults += 1
            if len(memory) >= num_frames:
                classes = {0: [], 1: [], 2: [], 3: []}
                for p in memory:
                    r = memory[p]['R']
                    m = memory[p]['M']
                    clase = 2*r + m
                    classes[clase].append(p)
                for c in range(4):
                    if classes[c]:
                        victim = random.choice(classes[c])
                        del memory[victim]
                        break
            memory[page] = {'R': random.randint(0,1), 'M': random.randint(0,1)}
        else:
            memory[page]['R'] = 1
    imprimir_metricas("NRU", page_faults, len(reference_string), resultados, costos)

def graficar(resultados, costos):
    algoritmos = list(resultados.keys())
    rendimientos = list(resultados.values())
    costo_valores = list(costos.values())

    # Gráfico de Rendimiento
    plt.figure(figsize=(10,5))
    plt.subplot(1, 2, 1)
    plt.bar(algoritmos, rendimientos, color='skyblue')
    plt.title('Rendimiento (%) por Algoritmo')
    plt.ylabel('Rendimiento (%)')
    plt.ylim(0, 100)

    # Gráfico de Costo
    plt.subplot(1, 2, 2)
    plt.bar(algoritmos, costo_valores, color='salmon')
    plt.title('Costo Total por Algoritmo')
    plt.ylabel('Costo')
    plt.ylim(0, max(costo_valores) + 5)

    plt.tight_layout()
    plt.show()

# MAIN
if __name__ == "__main__":
    reference_string = [2, 3, 2, 1, 5, 2, 4, 5, 3, 2, 5, 2]
    num_frames = 3

    resultados = {}
    costos = {}

    fifo(reference_string, num_frames, resultados, costos)
    lru(reference_string, num_frames, resultados, costos)
    optimal(reference_string, num_frames, resultados, costos)
    nru(reference_string, num_frames, resultados, costos)

    graficar(resultados, costos)
