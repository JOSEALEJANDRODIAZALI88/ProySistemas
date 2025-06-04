class MemoryManager:
    def __init__(self, memory_blocks):
        # Guardamos la copia original de los bloques
        self.original_blocks = memory_blocks[:]

    def reset(self):
        # Restauramos los bloques para cada simulación
        self.blocks = self.original_blocks[:]

    def print_blocks(self):
        print("Estado actual de los bloques:", self.blocks)

    def primeraSalida(self, requests):
        print("\n== Primera-Salida ==")
        self.reset()
        for request in requests:
            allocated = False
            for i in range(len(self.blocks)):
                if self.blocks[i] >= request:
                    print(f"Solicitud {request} asignada al bloque {self.blocks[i]}")
                    self.blocks[i] -= request
                    allocated = True
                    break
            if not allocated:
                print(f"Solicitud {request} no pudo ser asignada")
            self.print_blocks()

    def mejorSalida(self, requests):
        print("\n== Mejor-Salida ==")
        self.reset()
        for request in requests:
            best_index = -1
            best_size = float('inf')
            for i, size in enumerate(self.blocks):
                if request <= size < best_size:
                    best_size = size
                    best_index = i
            if best_index != -1:
                print(f"Solicitud {request} asignada al bloque {self.blocks[best_index]}")
                self.blocks[best_index] -= request
            else:
                print(f"Solicitud {request} no pudo ser asignada")
            self.print_blocks()

    def peorSalida(self, requests):
        print("\n== Peor-Salida ==")
        self.reset()
        for request in requests:
            worst_index = -1
            worst_size = -1
            for i, size in enumerate(self.blocks):
                if size >= request and size > worst_size:
                    worst_size = size
                    worst_index = i
            if worst_index != -1:
                print(f"Solicitud {request} asignada al bloque {self.blocks[worst_index]}")
                self.blocks[worst_index] -= request
            else:
                print(f"Solicitud {request} no pudo ser asignada")
            self.print_blocks()


memory_blocks = [100, 500, 200, 300, 600]  # Huecos de memoria disponibles
solicitudes = [212, 417, 112, 426]         # Solicitudes de memoria

mm = MemoryManager(memory_blocks)
mm.primeraSalida(solicitudes)
mm.mejorSalida(solicitudes)
mm.peorSalida(solicitudes)


