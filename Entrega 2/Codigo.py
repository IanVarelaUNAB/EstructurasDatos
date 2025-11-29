# =============================================
# ENTREGA 2: Árboles y Jerarquías
# =============================================
import csv

class Personaje:
    def __init__(self, nombre, especie, planeta, nivel_personaje):
        self.nombre = nombre
        self.especie = especie
        self.planeta = planeta
        self.nivel_personaje = nivel_personaje
        self.arsenal = ArsenalHabilidades(self)  # Nombre / Nivel
        self.inventario = []  # objetos

    def nueva_habilidad(self, nombre, nivel=1): 
        if nivel < 1 or nivel > 5:
            print("Nivel debe ser 1-5")
            return None
        return self.arsenal.nueva_habilidad_base(nombre, nivel)

    def poder_total(self):
        poder_hab = self.arsenal.calcular_poder_habilidades()
        # Sumamos el poder de los objetos en el inventario
        poder_obj = sum(n * 100 for _, n in self.inventario)
        return (poder_hab + poder_obj) * self.nivel_personaje

    def __str__(self):
        return f"{self.nombre} (poder {self.poder_total()})"


# ==================== ARBOL BINARIO DE PODER ====================
class NodoBinario:
    def __init__(self, personaje):
        self.personaje = personaje
        self.izq = None
        self.der = None

class ArbolBinarioPoder:
    def __init__(self):
        self.raiz = None

    def insertar(self, personaje):
        if self.raiz is None:
            self.raiz = NodoBinario(personaje)
        else:
            self._insertar_rec(self.raiz, personaje)

    def _insertar_rec(self, nodo, personaje):
        # Comparamos por poder total para ordenar el árbol
        if personaje.poder_total() < nodo.personaje.poder_total():
            if nodo.izq is None:
                nodo.izq = NodoBinario(personaje)
            else:
                self._insertar_rec(nodo.izq, personaje)
        else:
            if nodo.der is None:
                nodo.der = NodoBinario(personaje)
            else:
                self._insertar_rec(nodo.der, personaje)

    def preorden(self):
        print("Preorden (raíz → izq → der):")
        self._preorden(self.raiz)
        print()

    def _preorden(self, nodo):
        if nodo:
            print(f" → {nodo.personaje}")
            self._preorden(nodo.izq)
            self._preorden(nodo.der)

    def inorden(self):
        print("Inorden (ordenado por poder ascendente):")
        self._inorden(self.raiz)
        print()

    def _inorden(self, nodo):
        if nodo:
            self._inorden(nodo.izq)
            print(f" → {nodo.personaje}")
            self._inorden(nodo.der)

    def postorden(self):
        print("Postorden:")
        self._postorden(self.raiz)
        print()

    def _postorden(self, nodo):
        if nodo:
            self._postorden(nodo.izq)
            self._postorden(nodo.der)
            print(f" → {nodo.personaje}")

    def buscar(self, nombre):
        return self._buscar(self.raiz, nombre)

    def _buscar(self, nodo, nombre):
        if nodo is None:
            return None
        if nodo.personaje.nombre == nombre:
            return nodo.personaje
        
        # Como el árbol está ordenado por PODER, no por nombre,
        # la búsqueda por nombre obliga a recorrer todo el árbol.
        resultado = self._buscar(nodo.izq, nombre)
        if resultado:
            return resultado
        return self._buscar(nodo.der, nombre)


# ==================== ARBOL GENERAL DE HABILIDADES ====================
class NodoHabilidad:
    def __init__(self, nombre, nivel):
        self.nombre = nombre
        self.nivel = nivel
        self.hijos = []

    def agregar_mejora(self, nombre_mejora, nivel_mejora):
        nuevo = NodoHabilidad(nombre_mejora, nivel_mejora)
        self.hijos.append(nuevo)
        return nuevo


class ArbolHabilidades:
    def __init__(self, habilidad_base, nivel):
        self.raiz = NodoHabilidad(habilidad_base, nivel)

    def preorden(self):
        self._preorden(self.raiz, 0)

    def _preorden(self, nodo, profundidad):
        print("  " * profundidad + f"→ {nodo.nombre} (nivel {nodo.nivel})")
        for hijo in nodo.hijos:
            self._preorden(hijo, profundidad + 1)


# ==================== ARSENAL DE HABILIDADES ====================
class ArsenalHabilidades:
    def __init__(self, personaje):
        self.personaje = personaje
        self.arboles = []

    def nueva_habilidad_base(self, nombre, nivel):
        arbol = ArbolHabilidades(nombre, nivel)
        self.arboles.append(arbol)
        return arbol.raiz

    def calcular_poder_habilidades(self):
        total = 0
        for arbol in self.arboles:
            total += self._calcular_poder_nodo(arbol.raiz)
        return total

    def _calcular_poder_nodo(self, nodo):
        if not nodo:
            return 0
        poder = nodo.nivel * 200
        for hijo in nodo.hijos:
            poder += self._calcular_poder_nodo(hijo)
        return poder

    def mostrar_todo(self):
        print(f"\n{'='*60}")
        print(f"   HABILIDADES EVOLUTIVAS DE {self.personaje.nombre.upper()}")
        print(f"{'='*60}")
        if not self.arboles:
            print("   → No tiene habilidades evolutivas")
        else:
            for i, arbol in enumerate(self.arboles, 1):
                print(f"\n{i}) {arbol.raiz.nombre}")
                arbol.preorden()
        
        poder_hab = self.calcular_poder_habilidades()
        print(f"\n→ Poder total por habilidades: {poder_hab}")
        print(f"→ Total de líneas evolutivas: {len(self.arboles)}")
        print(f"{'='*60}")

# ==================== CARGA DE CSVs====================

def cargar_personajes_csv(ruta):
    personajes = {}
    # encoding="latin-1" asi toma la "ñ"
    with open(ruta, newline="", encoding="latin-1") as f:
        reader = csv.DictReader(f)
        for fila in reader:
            nombre = fila["nombre"].strip()
            especie = fila["especie"].strip()
            planeta = fila["planeta"].strip()
            nivel = int(fila["nivel"])
            personajes[nombre] = Personaje(nombre, especie, planeta, nivel)
    return personajes


def cargar_habilidades_csv(personajes, ruta):
    with open(ruta, newline="", encoding="latin-1") as f:
        reader = csv.DictReader(f)

        for fila in reader:
            personaje = fila["personaje"].strip()
            habilidad = fila["habilidad"].strip()
            nivel = int(fila["nivel"])
            
            mejora = fila.get("mejora", "") 
            nivel_mej = fila.get("nivel_mejora", "0")

            if personaje not in personajes:
                continue

            nodo_base = personajes[personaje].nueva_habilidad(habilidad, nivel)
            
            if nodo_base and mejora.strip() and nivel_mej:
                try:
                    lvl_m = int(nivel_mej)
                    if lvl_m > 0:
                        nodo_base.agregar_mejora(mejora, lvl_m)
                except ValueError:
                    pass


def cargar_inventario_csv(personajes, ruta):
    with open(ruta, newline="", encoding="latin-1") as f:
        reader = csv.DictReader(f)
        for fila in reader:
            pj = fila["personaje"].strip()
            obj = fila["objeto"].strip()
            nivel = int(fila["nivel"])

            if pj in personajes:
                personajes[pj].inventario.append((obj, nivel))


# ==================== MAIN ====================
if __name__ == "__main__":
    # Carga de CSV
    print("Cargando archivos CSV...")
    try:
        personajes = cargar_personajes_csv("Personajes.csv")
        cargar_habilidades_csv(personajes, "Habilidades.csv")
        cargar_inventario_csv(personajes, "Inventario.csv")
        print(f"Se cargaron {len(personajes)} personajes.\n")

        # Arbol binario de poder
        arbol = ArbolBinarioPoder()
        for pj in personajes.values():
            arbol.insertar(pj)

        # Muestra arbol binario
        print("=== ÁRBOL BINARIO DE PODER (INORDEN) ===")
        arbol.inorden()

        # Arbol general de habilidades por personaje
        print("\n=== DETALLE DE HABILIDADES E INVENTARIO ===")
        for pj in personajes.values():
            pj.arsenal.mostrar_todo()
            print(f"   [Datos Base] Especie: {pj.especie} | Nivel: {pj.nivel_personaje}")
            if pj.inventario:
                print(f"   [Inventario]: {pj.inventario}")
            print(f"→ Poder Total Global de {pj.nombre}: {pj.poder_total()}")
            print("\n" + "="*60)
            
    except FileNotFoundError as e:
        print(f"\n[ERROR] No se encontró el archivo: {e.filename}")
        print("Asegúrate de que los 3 archivos .csv estén en la misma carpeta que este código.")
    except Exception as e:
        print(f"\n[ERROR] Ocurrió un error inesperado: {e}")
