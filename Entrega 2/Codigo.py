# =============================================
# ENTREGA 2: Árboles y Jerarquías
# =============================================

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
        print("Inorden (ordenado por poder):")
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


# ============== Ejemplos ==============
if __name__ == "__main__":
    goku = Personaje("Goku", "Saiyajin", "Vegeta", 9)
    vegeta = Personaje("Vegeta", "Saiyajin", "Vegeta", 8)
    piccolo = Personaje("Piccolo", "Namekiano", "Namek", 6)

    # === Habilidades(todo por el árbol) ===
    kame = goku.nueva_habilidad("Kamehameha", 4)
    kame.agregar_mejora("God Kamehameha", 5)

    genki = goku.nueva_habilidad("Genki Dama", 4)
    genki.agregar_mejora("Universal Spirit Bomb", 5)

    BigBang = vegeta.nueva_habilidad("Big Bang Attack", 4)

    print(" ")
    print(" ")
    print("=== ÁRBOL BINARIO DE PODER ===")
    arbol_poder = ArbolBinarioPoder()
    arbol_poder.insertar(piccolo)
    arbol_poder.insertar(vegeta)
    arbol_poder.insertar(goku)
    arbol_poder.inorden()

    # === Mostrar habilidades de Goku ===
    goku.arsenal.mostrar_todo()

    print(f"\nPoder total final de {goku.nombre}: {goku.poder_total()}")

    # === Mostrar habilidades de Vegeta ===
    vegeta.arsenal.mostrar_todo()
    print(f"\nPoder total final de {vegeta.nombre}: {vegeta.poder_total()}")