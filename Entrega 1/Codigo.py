class Personaje:
    def __init__(self, nombre, especie, planeta, nivel_personaje):
        self.nombre = nombre
        self.especie = especie
        self.planeta = planeta
        self.nivel_personaje = nivel_personaje  # Nivel (1 a 10)
        self.habilidades = []  # (nombre/nivel)
        self.inventario = []   # (nombre/nivel)

    # Habilidades
    def agregar_habilidad(self, nombre_hab, nivel):
        if nivel < 1 or nivel > 5:
            print("Nivel de habilidad debe ser 1-5")
            return
        
        # Busca si ya existe la habilidad
        for i in range(len(self.habilidades)):
            hab, niv_actual = self.habilidades[i]
            if hab == nombre_hab:
                if niv_actual == nivel: # Mismo nivel se sube a no ser que ya sea 5
                    nuevo_niv = niv_actual + 1
                    if nuevo_niv > 5:
                        print(f"No se puede subir más {nombre_hab}, nada cambió")
                        return
                    self.habilidades[i] = (hab, nuevo_niv)
                    print(f"{nombre_hab} subió a nivel {nuevo_niv}")
                    return
                else:
                    # Si es diferente nivel se queda con el mayor
                    if nivel > niv_actual:
                        self.habilidades[i] = (hab, nivel)
                        print(f"{nombre_hab} actualizado a nivel {nivel} (era {niv_actual})")
                    else:
                        print(f"{nombre_hab} ya existe en nivel {niv_actual}, nada cambia")
                    return
        
        # Si no existe agrega uno nuevo
        self.habilidades.append((nombre_hab, nivel))
        print(f"Habilidad {nombre_hab} nivel {nivel} agregada")

    def quitar_habilidad(self, nombre_hab):
        for hab in self.habilidades:
            if hab[0] == nombre_hab:
                self.habilidades.remove(hab)
                print(f"Habilidad {nombre_hab} eliminada")
                return
        print(f"No se encontró {nombre_hab}")

    # Objetso
    def agregar_objeto(self, nombre_obj, nivel):
        if nivel < 1 or nivel > 5:
            print("Nivel de objeto debe ser 1-5")
            return
        self.inventario.append((nombre_obj, nivel))
        print(f"Objeto {nombre_obj} nivel {nivel} agregado")

    def quitar_objeto(self, nombre_obj):
        for obj in self.inventario:
            if obj[0] == nombre_obj:
                self.inventario.remove(obj)
                print(f"Objeto {nombre_obj} eliminado")
                return
        print(f"No se encontró {nombre_obj}")

    # Poder

    def poder_objetos(self):
        total = 0
        for _, nivel in self.inventario:
            total += nivel * 100
        return total

    def poder_habilidades(self):
        total = 0
        for _, nivel in self.habilidades:
            total += nivel * 200
        return total

    def poder_total(self):
        base = self.poder_objetos() + self.poder_habilidades()
        return base * self.nivel_personaje

    # Mostrar todo
    def mostrar(self):
        print(f"--- {self.nombre} ---")
        print(f"Especie: {self.especie} | Planeta: {self.planeta}")
        print(f"Nivel del personaje: {self.nivel_personaje}")
        print(f"Poder total: {self.poder_total()}")
        print("Habilidades:")
        for h, n in self.habilidades:
            print(f"  -> {h}: nivel {n} -> {n*200} poder")
        print("Inventario:")
        for o, n in self.inventario:
            print(f"  -> {o}: nivel {n} -> {n*100} poder")
        print()

# Ejemplo de uso:

goku = Personaje("Goku", "Saiyajin", "Vegita", 7)

# Agregar habilidades
goku.agregar_habilidad("Kamehameha", 3)   # Se agrega
goku.agregar_habilidad("Kamehameha", 3)   # Sube a 4
goku.agregar_habilidad("Kamehameha", 2)   # Existe en 4, nada cambia
goku.agregar_habilidad("Kamehameha", 5)   # Existe en 4 Sube a 5
goku.agregar_habilidad("Genki Dama", 1)   # Se agrega
# Agregar Objetos
goku.agregar_objeto("Semilla del hermitaño", 1)

goku.mostrar()
