# Ejercicio 1: Asignación de espacio en la memoria con Primer, Mejor y Peor Ajuste

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

# ======================
# DATOS DE EJEMPLO
# ======================
procesos = [100, 50, 30, 80, 40]
memoria  = [100, 50, 30, 80, 40]

# ======================
# EJECUTAR SIMULACIÓN
# ======================
resultados = asignacion_memoria_mejorada(procesos, memoria)

# ======================
# IMPRIMIR RESULTADOS
# ======================
for nombre, datos in resultados.items():
    print(f"\n--- {nombre} ---")
    for i, bloque in enumerate(datos["Asignación"]):
        if bloque != -1:
            print(f"Proceso {procesos[i]}MB → Bloque {bloque + 1} ({memoria[bloque]}MB original)")
        else:
            print(f"Proceso {procesos[i]}MB → No asignado")

    print(f"\nFragmentación externa: {datos['Fragmentación externa']} MB")
    print(f"Uso de memoria: {datos['Porcentaje de uso de memoria']}%")
    print(f"Multiprogramación: {datos['Nivel de multiprogramación']} procesos asignados")
    print(f"Trabajos postergados: {datos['Trabajos postergados']}")
