import csv

class Personaje:
    def __init__(self, nombre, especie, planeta, nivel_personaje):
        # Validación de nivel
        if nivel_personaje < 1 or nivel_personaje > 10:
             print("El nivel no puede ser menor a 1 o mayor a 10")
             pass 
             
        self.nombre = nombre
        self.especie = especie
        self.planeta = planeta
        self.nivel_personaje = nivel_personaje  # Nivel (1 a 10)
        self.habilidades = []  # (nombre, nivel)
        self.inventario = []   # (nombre, nivel)

    # Habilidades
    def agregar_habilidad(self, nombre_hab, nivel):
        if nivel < 1 or nivel > 5:
            print("Nivel de habilidad debe ser 1-5")
            return
        
        # Busca si ya existe la habilidad para actualizarla
        for i in range(len(self.habilidades)):
            hab, niv_actual = self.habilidades[i]
            if hab == nombre_hab:
                if niv_actual == nivel: 
                    nuevo_niv = niv_actual + 1
                    if nuevo_niv > 5:
                        print(f"No se puede subir más {nombre_hab}, ya es nivel máximo")
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
        # print(f"Habilidad {nombre_hab} nivel {nivel} agregada")

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
        # print(f"Objeto {nombre_obj} nivel {nivel} agregado")

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
        
        if self.habilidades:
            print("Habilidades:")
            for h, n in self.habilidades:
                print(f"  -> {h}: nivel {n} -> {n*200} poder")
        
        if self.inventario:
            print("Inventario:")
            for o, n in self.inventario:
                print(f"  -> {o}: nivel {n} -> {n*100} poder")
        print()

# ==========================================================
# FUNCIONES DE CARGA
# ==========================================================

def cargar_personajes(ruta="Personajes.csv"):
    personajes = {}
    with open(ruta, encoding="latin-1") as file:
        lector = csv.DictReader(file)
        for fila in lector:
            nombre = fila["nombre"].strip()
            especie = fila["especie"].strip()
            planeta = fila["planeta"].strip()
            nivel = int(fila["nivel"]) 
            personajes[nombre] = Personaje(nombre, especie, planeta, nivel)
    return personajes


def cargar_habilidades(personajes, ruta="Habilidades.csv"):
    with open(ruta, encoding="latin-1") as file:
        lector = csv.DictReader(file)
        for fila in lector:
            personaje = fila["personaje"].strip()
            hab = fila["habilidad"].strip()
            nivel = int(fila["nivel"])
            
            if personaje in personajes:
                personajes[personaje].agregar_habilidad(hab, nivel)


def cargar_inventario(personajes, ruta="Inventario.csv"):
    with open(ruta, encoding="latin-1") as file:
        lector = csv.DictReader(file)
        for fila in lector:
            personaje = fila["personaje"].strip()
            obj = fila["objeto"].strip()
            nivel = int(fila["nivel"])
            if personaje in personajes:
                personajes[personaje].agregar_objeto(obj, nivel)

# ==========================================================
# MAIN
# ==========================================================
if __name__ == "__main__":
    print("\n=== CARGANDO DATOS DESDE CSV ===\n")

    try:
        personajes = cargar_personajes()
        cargar_habilidades(personajes)
        cargar_inventario(personajes)

        print(f"-> Se cargaron {len(personajes)} personajes.")

        print("=== DETALLE DE PERSONAJES ===\n")
        for p in personajes.values():
            p.mostrar()
            
    except FileNotFoundError as e:
        print(f"Error: No se encontró el archivo {e.filename}")
    except KeyError as e:
        print(f"Error en el CSV: No se encontró la columna {e}")
    except ValueError as e:
        print(f"Error de datos: {e}")
