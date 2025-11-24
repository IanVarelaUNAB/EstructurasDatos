import csv


class Personaje:
    def __init__(self, nombre, especie, planeta, nivel_personaje):
         if nivel_personaje < 1 or nivel_personaje > 10:
            raise ValueError("El nivel del personaje debe ser entre 1 y 10") 
             
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

    # Objetos
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

    # CSV
   def cargar_personajes(ruta="Personajes.csv"):
    personajes = {}
    with open(ruta, encoding="utf-8") as file:
        lector = csv.DictReader(file)
        for fila in lector:
            nombre = fila["nombre"]
            especie = fila["especie"]
            planeta = fila["planeta"]
            nivel = int(fila["nivel_personaje"])
            personajes[nombre] = Personaje(nombre, especie, planeta, nivel)
    return personajes


   def cargar_habilidades(personajes, ruta="Habilidades.csv"):
     with open(ruta, encoding="utf-8") as file:
        lector = csv.DictReader(file)
        for fila in lector:
            personaje = fila["personaje"]
            hab = fila["habilidad"]
            nivel = int(fila["nivel"])
            if personaje in personajes:
                personajes[personaje].agregar_habilidad(hab, nivel)


    def cargar_inventario(personajes, ruta="Inventario.csv"):
      with open(ruta, encoding="utf-8") as file:
        lector = csv.DictReader(file)
        for fila in lector:
            personaje = fila["personaje"]
            obj = fila["objeto"]
            nivel = int(fila["nivel"])
            if personaje in personajes:
                personajes[personaje].agregar_objeto(obj, nivel)


   def cargar_universo(ruta="universo_planetas.csv"):
        universo = {}
      with open(ruta, encoding="utf-8") as file:
        lector = csv.DictReader(file)
        for fila in lector:
            origen = fila["origen"]
            destino = fila["destino"]
            distancia = int(fila["distancia"])

            if origen not in universo:
                universo[origen] = []
            if destino not in universo:
                universo[destino] = []

            universo[origen].append((destino, distancia))
            universo[destino].append((origen, distancia))

    return universo

# MAIN
if __name__ == "__main__":
    print("\n=== CARGANDO PERSONAJES DESDE CSV ===\n")

    personajes = cargar_personajes()
    cargar_habilidades(personajes)
    cargar_inventario(personajes)
    universo = cargar_universo()

    print("=== PERSONAJES CARGADOS ===\n")
    for p in personajes.values():
        p.mostrar()

    print("=== UNIVERSO DE PLANETAS ===\n")
    for origen, conexiones in universo.items():
        print(f"{origen}: {conexiones}")





