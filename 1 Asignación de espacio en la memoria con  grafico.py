import matplotlib.pyplot as plt

def asignacion_memoria_mejorada(procesos, memoria):
    resultados = {}

    def aplicar_algoritmo(nombre, seleccion_bloque):
        espacio_restante = memoria[:]
        asignacion = [-1] * len(procesos)

        for i, proceso in enumerate(procesos):
            indices_validos = [j for j, bloque in enumerate(espacio_restante) if bloque >= proceso]
            if indices_validos:
                idx = seleccion_bloque(indices_validos, proceso, espacio_restante)
                espacio_restante[idx] -= proceso
                asignacion[i] = idx

        procesos_asignados = sum(1 for a in asignacion if a != -1)
        memoria_utilizada = sum(memoria) - sum(espacio_restante)
        fragmentacion_externa = sum(espacio_restante)
        porcentaje_uso_memoria = (memoria_utilizada / sum(memoria)) * 100
        trabajos_postergados = len(procesos) - procesos_asignados

        resultados[nombre] = {
            "Asignación": asignacion,
            "Fragmentación externa": fragmentacion_externa,
            "Porcentaje de uso de memoria": round(porcentaje_uso_memoria, 2),
            "Nivel de multiprogramación": procesos_asignados,
            "Trabajos postergados": trabajos_postergados
        }

    aplicar_algoritmo("Primer Ajuste", lambda indices, p, esp: indices[0])
    aplicar_algoritmo("Mejor Ajuste", lambda indices, p, esp: min(indices, key=lambda i: esp[i] - p))
    aplicar_algoritmo("Peor Ajuste", lambda indices, p, esp: max(indices, key=lambda i: esp[i] - p))

    return resultados


def graficar_resultados_con_espacio_memoria(resultados, procesos, memoria):
    for nombre, datos in resultados.items():
        asignaciones = datos["Asignación"]
        bloques = [f'B{i+1} ({memoria[i]}MB)' for i in range(len(memoria))]
        ocupacion_bloques = [0] * len(memoria)

        for i, bloque_id in enumerate(asignaciones):
            if bloque_id != -1:
                ocupacion_bloques[bloque_id] += procesos[i]

        plt.figure()
        bar_width = 0.4
        indices = range(len(memoria))
        plt.bar(indices, memoria, width=bar_width, label='Memoria Total', color='lightgray')
        plt.bar(indices, ocupacion_bloques, width=bar_width, label='Memoria Usada', color='green')

        plt.title(f'Uso de Memoria por Bloque - {nombre}')
        plt.xlabel('Bloques de Memoria')
        plt.ylabel('Tamaño (MB)')
        plt.xticks(indices, bloques, rotation=45)
        plt.legend()
        plt.grid(axis='y', linestyle='--', alpha=0.6)
        plt.tight_layout()

        resumen = (
            f"Fragmentación externa: {datos['Fragmentación externa']} MB\n"
            f"Uso de memoria: {datos['Porcentaje de uso de memoria']}%\n"
            f"Multiprogramación: {datos['Nivel de multiprogramación']} procesos\n"
            f"Trabajos postergados: {datos['Trabajos postergados']}"
        )
        plt.figtext(0.99, 0.01, resumen, horizontalalignment='right', fontsize=8,
                    bbox={"facecolor": "white", "alpha": 0.5})

    plt.show()


# ======================
# DATOS DE ENTRADA
# ======================
procesos = [100, 50, 30, 80, 40]
memoria  = [120, 50, 200, 70, 60]

# ======================
# EJECUCIÓN
# ======================
resultados = asignacion_memoria_mejorada(procesos, memoria)
graficar_resultados_con_espacio_memoria(resultados, procesos, memoria)

