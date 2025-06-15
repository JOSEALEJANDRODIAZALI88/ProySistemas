import matplotlib.pyplot as plt

# Función principal de asignación
def asignacion_memoria_mejorada(procesos, memoria):
    resultados = {}

    def aplicar_algoritmo(nombre, seleccion_bloque):
        espacio_restante = memoria[:]
        asignacion = [-1] * len(procesos)  # Guarda el índice del bloque asignado a cada proceso

        for i, proceso in enumerate(procesos):
            indices_validos = [j for j, bloque in enumerate(espacio_restante) if bloque >= proceso]
            if indices_validos:
                idx = seleccion_bloque(indices_validos, proceso, espacio_restante)
                espacio_restante[idx] -= proceso
                asignacion[i] = idx  # Guardar a qué bloque fue asignado

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

    # Ejecutar los tres algoritmos
    aplicar_algoritmo("Primer Ajuste", lambda indices, p, esp: indices[0])
    aplicar_algoritmo("Mejor Ajuste", lambda indices, p, esp: min(indices, key=lambda i: esp[i] - p))
    aplicar_algoritmo("Peor Ajuste", lambda indices, p, esp: max(indices, key=lambda i: esp[i] - p))

    return resultados


# Función para graficar cada resultado en ventana separada
def graficar_resultados(resultados, procesos, memoria):
    for nombre, datos in resultados.items():
        asignaciones = datos["Asignación"]
        colores = ['green' if a != -1 else 'red' for a in asignaciones]
        etiquetas = [f'P{i+1} ({procesos[i]}MB)' for i in range(len(procesos))]

        plt.figure()
        plt.bar(etiquetas, procesos, color=colores)
        plt.title(f'Asignación de Memoria - {nombre}')
        plt.xlabel('Procesos')
        plt.ylabel('Tamaño (MB)')
        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()

        # Añadir resumen como texto en la parte inferior
        resumen = (
            f"Fragmentación externa: {datos['Fragmentación externa']} MB\n"
            f"Uso de memoria: {datos['Porcentaje de uso de memoria']}%\n"
            f"Multiprogramación: {datos['Nivel de multiprogramación']} procesos\n"
            f"Trabajos postergados: {datos['Trabajos postergados']}"
        )
        plt.figtext(0.99, 0.01, resumen, horizontalalignment='right', fontsize=8, bbox={"facecolor": "white", "alpha": 0.5})

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
graficar_resultados(resultados, procesos, memoria)
