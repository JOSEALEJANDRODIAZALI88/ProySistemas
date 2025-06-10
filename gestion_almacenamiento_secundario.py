# -*- coding: utf-8 -*-
"""
Simulación de algoritmos de asignación de espacio en almacenamiento secundario
Métodos: Contigua, Enlazada, Indexada
"""
import random
import matplotlib.pyplot as plt
import pandas as pd

# Parámetros de simulación
N_BLOQUES = 64
ARCHIVOS_INICIALES = [("A", 8), ("B", 10), ("C", 6), ("D", 12)]
T_SEEK = 1.0        # Tiempo de seek (ms)
T_TRANS = 0.1       # Tiempo de transferencia por bloque (ms)
T_PTR = 0.05        # Tiempo adicional por puntero (ms)
T_SEEK_IDX = 1.2    # Seek para índice (ms)
T_TRANS_IDX = 0.2   # Transferencia de índice (ms)
N_ACCESOS_ALE = 10  # Accesos aleatorios a simular

# --- Funciones básicas ---

def crear_disco():
    return [None] * N_BLOQUES

def borrar_archivo(disco, etiqueta):
    for i, b in enumerate(disco):
        if b == etiqueta or b == f"{etiqueta}_IDX":
            disco[i] = None

# Asignación contigua
def asignacion_contigua(disco, etiqueta, k):
    for i in range(N_BLOQUES - k + 1):
        if all(b is None for b in disco[i:i + k]):
            for j in range(k):
                disco[i + j] = etiqueta
            return True
    return False

# Asignación enlazada
def asignacion_enlazada(disco, etiqueta, k):
    libres = [i for i, b in enumerate(disco) if b is None]
    if len(libres) < k:
        return False
    seleccion = random.sample(libres, k)
    for i in seleccion:
        disco[i] = etiqueta
    return True

# Asignación indexada
def asignacion_indexada(disco, etiqueta, k):
    libres = [i for i, b in enumerate(disco) if b is None]
    if len(libres) < k + 1:
        return False
    idx = libres[0]
    disco[idx] = f"{etiqueta}_IDX"
    for i in libres[1:k+1]:
        disco[i] = etiqueta
    return True

# --- Métricas ---

def ocupacion(disco):
    usados = sum(1 for b in disco if b is not None)
    return usados / N_BLOQUES * 100

def fragmentacion_externa(disco):
    huecos = []
    tamaño = 0
    for b in disco + ["X"]:
        if b is None:
            tamaño += 1
        elif tamaño > 0:
            huecos.append(tamaño)
            tamaño = 0
    if not huecos:
        return 0, 0
    return len(huecos), sum(huecos)/len(huecos)

def tiempo_secuencial(disco, etiqueta, metodo):
    # Número de bloques del archivo
    k = sum(1 for b in disco if b == etiqueta)
    if metodo == 'contigua':
        return k * (T_SEEK + T_TRANS)
    if metodo == 'enlazada':
        return k * (T_SEEK + T_TRANS) + (k - 1) * T_PTR
    if metodo == 'indexada':
        return T_SEEK_IDX + T_TRANS_IDX + k * T_TRANS
    return None

def tiempo_aleatorio(disco, etiqueta, metodo):
    posiciones = [i for i, b in enumerate(disco) if b == etiqueta]
    if not posiciones:
        return None
    tiempos = []
    for _ in range(N_ACCESOS_ALE):
        pos = random.choice(posiciones)
        if metodo == 'contigua':
            tiempos.append(T_SEEK + T_TRANS)
        elif metodo == 'enlazada':
            # suponemos recorrido medio a la mitad de la cadena
            pasos = posiciones.index(pos)
            tiempos.append(T_SEEK + T_TRANS + pasos * T_PTR)
        else:  # indexada
            tiempos.append(T_SEEK_IDX + T_TRANS_IDX + T_TRANS)
    return sum(tiempos) / len(tiempos)

# --- Simulación ---

def simular():
    resultados = []
    # Crear discos vacíos
    discos = {
        'contigua': crear_disco(),
        'enlazada': crear_disco(),
        'indexada': crear_disco()
    }
    # 1. Inserción inicial A, B, C, D
    for etiqueta, k in ARCHIVOS_INICIALES:
        for m, d in discos.items():
            func = {
                'contigua': asignacion_contigua,
                'enlazada': asignacion_enlazada,
                'indexada': asignacion_indexada
            }[m]
            func(d, etiqueta, k)
    # 2. Borrado de C
    for d in discos.values():
        borrar_archivo(d, 'C')
    # 3. Inserción de E (tamaño 5)
    for d in discos.values():
        asignacion_contigua(d, 'E', 5) if d is discos['contigua'] else \
        asignacion_enlazada(d, 'E', 5) if d is discos['enlazada'] else \
        asignacion_indexada(d, 'E', 5)
    # 4. Cálculo métricas
    for metodo, d in discos.items():
        uso = ocupacion(d)
        n_huecos, media_hue = fragmentacion_externa(d)
        t_seq = tiempo_secuencial(d, 'B', metodo)
        t_ale = tiempo_aleatorio(d, 'B', metodo)
        resultados.append({
            'Método': metodo,
            'Uso (%)': uso,
            'N huescos': n_huecos,
            'Media huecos': media_hue,
            'T secuencial B (ms)': t_seq,
            'T aleatorio B (ms)': t_ale
        })
    return pd.DataFrame(resultados)

if __name__ == '__main__':
    df = simular()
    print(df)
    # Gráficos de uso y tiempos
    df.set_index('Método')[['Uso (%)', 'T secuencial B (ms)', 'T aleatorio B (ms)']].plot.bar(figsize=(8,5))
    plt.ylabel('Valor')
    plt.title('Comparativa métricas por método')
    plt.tight_layout()
    plt.show()
