import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import random

# Clase que representa un bloque de memoria
class Bloque:
    def __init__(self, inicio, tamano, libre=True, proceso=None):
        self.inicio = inicio
        self.tamano = tamano
        self.libre = libre
        self.proceso = proceso

# Función para asignar procesos a la memoria
def asignar_procesos(memoria, procesos, algoritmo):
    memoria = [Bloque(0, 1000)]
    for nombre, tam in procesos:
        candidatos = []
        for i, bloque in enumerate(memoria):
            if bloque.libre and bloque.tamano >= tam:
                candidatos.append((i, bloque))

        if not candidatos:
            continue

        if algoritmo == "first_fit":
            i, bloque = candidatos[0]
        elif algoritmo == "best_fit":
            i, bloque = min(candidatos, key=lambda x: x[1].tamano)
        elif algoritmo == "worst_fit":
            i, bloque = max(candidatos, key=lambda x: x[1].tamano)

        nuevo = Bloque(bloque.inicio, tam, libre=False, proceso=nombre)
        if bloque.tamano > tam:
            bloque.inicio += tam
            bloque.tamano -= tam
            memoria.insert(i, nuevo)
        else:
            memoria[i] = nuevo

    return memoria

# Mostrar estado en consola
def mostrar_estado_consola(memoria, nombre_algoritmo):
    print(f"\n📋 Estado de la memoria - {nombre_algoritmo}")
    for bloque in memoria:
        estado = "Libre" if bloque.libre else f"Ocupado por {bloque.proceso}"
        print(f"[{bloque.inicio}-{bloque.inicio + bloque.tamano - 1}] {estado} ({bloque.tamano} KB)")

# Obtener color único por proceso
def obtener_color_aleatorio(nombre, colores_usados):
    colores = list(mcolors.TABLEAU_COLORS.values())
    random.seed(nombre)
    color = random.choice(colores)
    while color in colores_usados:
        color = random.choice(colores)
    colores_usados.add(color)
    return color

# Graficar y guardar como imagen
def graficar_memorias_coloreadas(memorias, titulos, archivo_salida):
    fig, axes = plt.subplots(len(memorias), 1, figsize=(10, 2.5 * len(memorias)))
    for ax, memoria, titulo in zip(axes, memorias, titulos):
        inicio = 0
        colores_usados = set()
        for bloque in memoria:
            if bloque.libre:
                color = 'lightgray'
                etiqueta = 'Libre'
            else:
                color = obtener_color_aleatorio(bloque.proceso, colores_usados)
                etiqueta = bloque.proceso
            ax.barh(0, bloque.tamano, left=inicio, color=color, edgecolor='black')
            ax.text(inicio + bloque.tamano / 2, 0, etiqueta, ha='center', va='center', fontsize=8, color='black')
            inicio += bloque.tamano
        ax.set_xlim(0, 1000)
        ax.set_ylim(-0.5, 0.5)
        ax.set_title(titulo)
        ax.axis('off')
    plt.tight_layout()
    plt.savefig(archivo_salida)
    plt.show()
    print(f"📷 Gráfico exportado como: {archivo_salida}")

# Procesos de prueba
procesos = [("A", 200), ("B", 300), ("C", 100), ("D", 150), ("E", 250)]

# Simulación
mem_first = asignar_procesos([], procesos, "first_fit")
mem_best = asignar_procesos([], procesos, "best_fit")
mem_worst = asignar_procesos([], procesos, "worst_fit")

# Mostrar en consola
mostrar_estado_consola(mem_first, "First Fit")
mostrar_estado_consola(mem_best, "Best Fit")
mostrar_estado_consola(mem_worst, "Worst Fit")

# Graficar y exportar
graficar_memorias_coloreadas(
    [mem_first, mem_best, mem_worst],
    ["First Fit (Colores por proceso)", "Best Fit (Colores por proceso)", "Worst Fit (Colores por proceso)"],
    "asignacion_memoria.png"
)
