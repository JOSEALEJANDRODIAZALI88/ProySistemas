import matplotlib.pyplot as plt
import random

# Tamaño del disco simulado
DISCO_TAMANO = 64

# Crear un disco vacío
def crear_disco():
    return ["Libre"] * DISCO_TAMANO

# Asignación contigua: bloques seguidos
def asignacion_contigua(disco, archivo, tamano):
    for i in range(DISCO_TAMANO - tamano + 1):
        if all(b == "Libre" for b in disco[i:i + tamano]):
            for j in range(tamano):
                disco[i + j] = archivo
            return True
    return False

# Asignación enlazada: bloques aleatorios
def asignacion_enlazada(disco, archivo, tamano):
    libres = [i for i, b in enumerate(disco) if b == "Libre"]
    if len(libres) >= tamano:
        bloques = random.sample(libres, tamano)
        for i in bloques:
            disco[i] = archivo
        return True
    return False

# Asignación indexada: un bloque índice + bloques de datos
def asignacion_indexada(disco, archivo, tamano):
    libres = [i for i, b in enumerate(disco) if b == "Libre"]
    if len(libres) >= tamano + 1:
        index_block = libres[0]
        data_blocks = libres[1:tamano + 1]
        disco[index_block] = f"{archivo}_IDX"
        for i in data_blocks:
            disco[i] = archivo
        return True
    return False

# Mostrar estado del disco en consola
def mostrar_disco_consola(disco, titulo):
    print(f"\n📋 Estado del disco - {titulo}")
    bloques_por_archivo = {}
    for i, bloque in enumerate(disco):
        if bloque != "Libre":
            archivo = bloque.replace("_IDX", "")
            if archivo not in bloques_por_archivo:
                bloques_por_archivo[archivo] = []
            bloques_por_archivo[archivo].append(i)
    for archivo, bloques in bloques_por_archivo.items():
        print(f"Archivo {archivo}: bloques -> {bloques}")
    libres = [i for i, b in enumerate(disco) if b == "Libre"]
    print(f"Bloques libres: {libres}")

# Visualización del disco con colores
def graficar_disco(discos, titulos):
    fig, axes = plt.subplots(len(discos), 1, figsize=(10, 2.5 * len(discos)))
    for ax, disco, titulo in zip(axes, discos, titulos):
        colores = {}
        for i, bloque in enumerate(disco):
            etiqueta = disco[i]
            if etiqueta == "Libre":
                color = 'lightgray'
            elif "_IDX" in etiqueta:
                color = 'black'
            else:
                if etiqueta not in colores:
                    colores[etiqueta] = "#" + ''.join(random.choices("89ABCDEF", k=6))
                color = colores[etiqueta]
            ax.barh(0, 1, left=i, color=color, edgecolor='black')
            if etiqueta != "Libre":
                ax.text(i + 0.5, 0, etiqueta, ha='center', va='center', fontsize=6, color='white')
        ax.set_xlim(0, DISCO_TAMANO)
        ax.set_ylim(-0.5, 0.5)
        ax.set_title(titulo)
        ax.axis('off')
    plt.tight_layout()
    plt.savefig("gestion_disco.png")
    plt.show()
    print("📷 Imagen exportada como 'gestion_disco.png'")

# Archivos de prueba: (nombre, tamaño en bloques)
archivos = [("A", 8), ("B", 10), ("C", 6), ("D", 12)]

# Crear discos para cada estrategia
disco_contiguo = crear_disco()
disco_enlazado = crear_disco()
disco_indexado = crear_disco()

# Asignar archivos
for archivo, tam in archivos:
    asignacion_contigua(disco_contiguo, archivo, tam)
    asignacion_enlazada(disco_enlazado, archivo, tam)
    asignacion_indexada(disco_indexado, archivo, tam)

# Mostrar por consola
mostrar_disco_consola(disco_contiguo, "Asignación Contigua")
mostrar_disco_consola(disco_enlazado, "Asignación Enlazada")
mostrar_disco_consola(disco_indexado, "Asignación Indexada")

# Mostrar gráficamente
graficar_disco(
    [disco_contiguo, disco_enlazado, disco_indexado],
    ["Asignación Contigua", "Asignación Enlazada", "Asignación Indexada"]
)
