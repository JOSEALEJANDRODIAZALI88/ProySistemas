import matplotlib.pyplot as plt

# Simulación de planificación de disco: FCFS, SCAN y C-SCAN

# Supongamos que el cabezal está en la posición inicial 50
inicio_cabezal = 50

# Solicitudes de acceso a pistas
solicitudes = [82, 170, 43, 140, 24, 16, 190]

def fcfs(inicio, solicitudes):
    orden = [inicio] + solicitudes
    movimientos = sum(abs(orden[i+1] - orden[i]) for i in range(len(orden)-1))
    return orden, movimientos

def scan(inicio, solicitudes, direccion='up', pista_max=199):
    solicitudes = sorted(solicitudes)
    orden = [inicio]
    if direccion == 'up':
        arriba = [s for s in solicitudes if s >= inicio]
        abajo = [s for s in solicitudes if s < inicio][::-1]
        orden += arriba + [pista_max] + abajo
    else:
        abajo = [s for s in solicitudes if s <= inicio]
        arriba = [s for s in solicitudes if s > inicio]
        orden += abajo[::-1] + [0] + arriba
    movimientos = sum(abs(orden[i+1] - orden[i]) for i in range(len(orden)-1))
    return orden, movimientos

def c_scan(inicio, solicitudes, pista_max=199):
    solicitudes = sorted(solicitudes)
    orden = [inicio]
    arriba = [s for s in solicitudes if s >= inicio]
    abajo = [s for s in solicitudes if s < inicio]
    orden += arriba + [pista_max, 0] + abajo
    movimientos = sum(abs(orden[i+1] - orden[i]) for i in range(len(orden)-1))
    return orden, movimientos

# Ejecutar algoritmos
orden_fcfs, mov_fcfs = fcfs(inicio_cabezal, solicitudes)
orden_scan, mov_scan = scan(inicio_cabezal, solicitudes)
orden_cscan, mov_cscan = c_scan(inicio_cabezal, solicitudes)

# Graficar movimientos
plt.figure(figsize=(12, 6))
for i, (orden, nombre) in enumerate(zip([orden_fcfs, orden_scan, orden_cscan], ['FCFS', 'SCAN', 'C-SCAN'])):
    plt.plot(range(len(orden)), orden, marker='o', label=f"{nombre} ({sum(abs(orden[i+1]-orden[i]) for i in range(len(orden)-1))} movimientos)")

plt.xlabel("Orden de servicio")
plt.ylabel("Posición del cabezal")
plt.title("Comparación de algoritmos de planificación de disco")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Resultados de movimientos
orden_fcfs, mov_fcfs, orden_scan, mov_scan, orden_cscan, mov_cscan




