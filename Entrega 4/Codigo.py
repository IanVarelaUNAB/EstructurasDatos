import heapq
from collections import deque

# =============================================
# CLASES BASE (PERSONAJE Y HABILIDADES)
# =============================================

class Personaje:
    def __init__(self, nombre, especie, planeta, nivel_personaje):
        self.nombre = nombre
        self.especie = especie
        self.planeta = planeta
        self.nivel_personaje = nivel_personaje
        self.arsenal = ArsenalHabilidades(self)
        self.inventario = [] 

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

    def inorden(self):
        print("Inorden (ordenado por poder):")
        self._inorden(self.raiz)
        print()

    def _inorden(self, nodo):
        if nodo:
            self._inorden(nodo.izq)
            print(f" -> {nodo.personaje}")
            self._inorden(nodo.der)


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
        print(f"{'='*60}")


# ==========================================================
# PLANIFICADOR DE ENTRENAMIENTO (ORDENAMIENTO TOPOLÓGICO)
# ==========================================================
class PlanificadorEntrenamiento:
    def __init__(self):
        # Grafo de dependencias: { "Habilidad A": ["Habilidad B"] } (A desbloquea B)
        self.grafo = {}
        # Contador de requisitos: { "Habilidad B": 1 } (B necesita 1 requisito)
        self.grados_entrada = {}

    def agregar_requisito(self, requisito, habilidad):
        # Si no existen en el diccionario, los iniciamos
        if requisito not in self.grafo:
            self.grafo[requisito] = []
            self.grados_entrada[requisito] = 0
        if habilidad not in self.grafo:
            self.grafo[habilidad] = []
            self.grados_entrada[habilidad] = 0
        
        # Creamos la relación
        self.grafo[requisito].append(habilidad)
        self.grados_entrada[habilidad] += 1

    def obtener_plan_entrenamiento(self):
        # Algoritmo de Kahn (Simplificado)
        cola = deque()
        # Buscamos las que NO tienen requisitos (grado 0)
        for hab, grado in self.grados_entrada.items():
            if grado == 0:
                cola.append(hab)
        
        orden_final = []
        
        while cola:
            actual = cola.popleft()
            orden_final.append(actual)

            if actual in self.grafo:
                for siguiente in self.grafo[actual]:
                    self.grados_entrada[siguiente] -= 1
                    if self.grados_entrada[siguiente] == 0:
                        cola.append(siguiente)
        
        return orden_final


# ==========================================================
# GRAFO UNIVERSO (MODIFICADO CON DIJKSTRA)
# ==========================================================
class GrafoUniverso:
    def __init__(self):
        # Clave = Planeta
        # Valor = Lista de tuplas (vecino, distancia)
        self.rutas = {}

    def agregar_ruta(self, origen, destino, distancia=1):
        if origen not in self.rutas: self.rutas[origen] = []
        if destino not in self.rutas: self.rutas[destino] = []

        # Guardamos TUPLAS: (nombre_vecino, distancia)
        self.rutas[origen].append((destino, distancia))
        self.rutas[destino].append((origen, distancia))

    # --- BFS (Modificado para ignorar distancias) ---
    def buscar_ruta_mas_corta_bfs(self, inicio, fin):
        print(f"\nBusca ruta BFS (saltos) de {inicio} a {fin}...")
        if inicio not in self.rutas or fin not in self.rutas: return None

        cola = deque([[inicio]])
        visitados = {inicio}

        while cola:
            camino = cola.popleft()
            actual = camino[-1]

            if actual == fin: return camino

            # Solo usamos 'vecino' porque BFS no mira distancias
            for vecino, _ in self.rutas.get(actual, []):
                if vecino not in visitados:
                    visitados.add(vecino)
                    nuevo = list(camino)
                    nuevo.append(vecino)
                    cola.append(nuevo)
        return None

    # --- DFS (ignora distancias) ---
    def explorar_dfs(self, actual, visitados=None):
        if visitados is None:
            visitados = set()
            print(f"\nExplorando universo desde {actual} (DFS):")
        
        visitados.add(actual)
        print(f" -> Visitando: {actual}")

        for vecino, _ in self.rutas.get(actual, []):
            if vecino not in visitados:
                self.explorar_dfs(vecino, visitados)

    # --- DIJKSTRA (Usa distancias reales) ---
    def camino_optimo_dijkstra(self, inicio, fin):
        print(f"\nCalculando ruta óptima (Dijkstra) de {inicio} a {fin}...")
        
        # Cola prioridad guarda: (distancia_acumulada, planeta_actual)
        cola_prio = [(0, inicio)]
        distancias = {inicio: 0}
        padres = {inicio: None} # Para reconstruir el camino
        visitados = set()

        while cola_prio:
            dist_actual, actual = heapq.heappop(cola_prio)

            if actual in visitados: continue
            visitados.add(actual)

            if actual == fin: break # Llegamos

            for vecino, peso in self.rutas.get(actual, []):
                nueva_dist = dist_actual + peso
                
                # Si encontramos un camino más rápido a este vecino
                if nueva_dist < distancias.get(vecino, float('inf')):
                    distancias[vecino] = nueva_dist
                    padres[vecino] = actual
                    heapq.heappush(cola_prio, (nueva_dist, vecino))

        # Reconstruir camino hacia atrás
        if fin not in distancias: return None, 0

        camino = []
        paso = fin
        while paso:
            camino.insert(0, paso)
            paso = padres[paso]
            
        return camino, distancias[fin]


# ==========================================================
# MAIN INTEGRADO (TESTEOS COMPLETOS)
# ==========================================================
if __name__ == "__main__":
    
    # ---------------------------------------------------------
    # PARTE 1: PERSONAJES Y ÁRBOLES
    # ---------------------------------------------------------
    print("\n" + "="*50)
    print("=== 1. GESTIÓN DE PERSONAJES (ENTREGAS 1 y 2) ===")
    print("="*50)

    # Creación de personajes
    goku = Personaje("Goku", "Saiyajin", "Tierra", 10)
    vegeta = Personaje("Vegeta", "Saiyajin", "Vegeta", 9)
    piccolo = Personaje("Piccolo", "Namekiano", "Namek", 8)

    # Agregando habilidades evolutivas (Árboles Generales)
    # GOKU
    kame = goku.nueva_habilidad("Kamehameha", 1)
    if kame: # Verificamos que se creó
        kame.agregar_mejora("Kamehameha x10", 3)
        mejora_god = kame.agregar_mejora("God Kamehameha", 5)
    
    genki = goku.nueva_habilidad("Genki Dama", 2)
    
    # VEGETA
    galick = vegeta.nueva_habilidad("Galick Ho", 2)
    if galick:
        galick.agregar_mejora("Final Flash", 4)

    # Árbol Binario de Poder (Ordenamiento)
    print("\n--- Insertando en Árbol Binario de Poder ---")
    arbol_poder = ArbolBinarioPoder()
    arbol_poder.insertar(piccolo)
    arbol_poder.insertar(vegeta)
    arbol_poder.insertar(goku) # Goku es el más fuerte, debería ir a la derecha
    
    # Mostramos
    arbol_poder.inorden() # Debería salir Piccolo -> Vegeta -> Goku
    goku.arsenal.mostrar_todo()


    # ---------------------------------------------------------
    # PLANIFICADOR DE ENTRENAMIENTO (ENTREGA 4)
    # ---------------------------------------------------------
    print("\n" + "="*50)
    print("=== PLANIFICADOR DE ENTRENAMIENTO (Topológico) ===")
    print("="*50)

    # EJEMPLO A: Entrenamiento Básico
    print("\n[CONTEXTO A] Entrenamiento Físico Saiyajin:")
    entrenador_fisico = PlanificadorEntrenamiento()
    
    entrenador_fisico.agregar_requisito("Resistencia", "Velocidad")     # 1. Resistencia desbloquea Velocidad
    entrenador_fisico.agregar_requisito("Velocidad", "Vuelo")           # 2. Velocidad desbloquea Vuelo
    entrenador_fisico.agregar_requisito("Vuelo", "Combate Aéreo")       # 3. Vuelo desbloquea Combate Aéreo
    entrenador_fisico.agregar_requisito("Resistencia", "Fuerza Bruta")  # 4. Resistencia TAMBIÉN desbloquea Fuerza
    
    plan_fisico = entrenador_fisico.obtener_plan_entrenamiento()
    print(f" -> Orden lógico: {plan_fisico}")
    # Resultado esperado: Resistencia va primero. Luego Velocidad y Fuerza. Al final Combate Aéreo.

    
    # EJEMPLO B: Requisitos Múltiples
    # "Para hacer la Fusión, necesitas Control de Ki Y Baile sincronizado."
    print("\n[CONTEXTO B] Técnica de la Fusión:")
    entrenador_tecnico = PlanificadorEntrenamiento()
    
    entrenador_tecnico.agregar_requisito("Meditar", "Control de Ki")
    entrenador_tecnico.agregar_requisito("Clase de Baile", "Ritmo")
    
    # La Fusión requiere DOS cosas previas:
    entrenador_tecnico.agregar_requisito("Control de Ki", "Fusión")
    entrenador_tecnico.agregar_requisito("Ritmo", "Fusión")
    
    plan_tecnico = entrenador_tecnico.obtener_plan_entrenamiento()
    print(f" -> Orden lógico: {plan_tecnico}")
    # Resultado esperado: Meditar y Clase de Baile primero. Fusión SOLO al final.


    # ---------------------------------------------------------
    # NAVEGACIÓN Y RUTAS 
    # ---------------------------------------------------------
    print("\n" + "="*50)
    print("=== 3. NAVEGACIÓN UNIVERSAL (Grafos, BFS y Dijkstra) ===")
    print("="*50)
    
    universo = GrafoUniverso()

    # Mapa del Universo (Distancias en Años Luz)
    # Tierra está conectada a Marte (muy cerca) y a la Luna (pegada)
    universo.agregar_ruta("Tierra", "Luna", 1) 
    universo.agregar_ruta("Tierra", "Marte", 50)
    
    # Rutas lejanas
    universo.agregar_ruta("Marte", "Cinturón Asteroides", 100)
    universo.agregar_ruta("Cinturón Asteroides", "Júpiter", 200)
    universo.agregar_ruta("Júpiter", "Saturno", 200)

    # Un "Atajo" de agujero de gusano (Saltos cortos, distancia larga)
    # Supongamos un portal antiguo: Conecta Tierra directo con Saturno pero es peligroso/lento (1000 de coste)
    universo.agregar_ruta("Tierra", "Portal Antiguo", 10)
    universo.agregar_ruta("Portal Antiguo", "Saturno", 1000) 

    print("\n--- Caso: Viajar de TIERRA a SATURNO ---")

    # 1. BFS (Busca MENOS SALTOS)
    # BFS va a ver: Tierra -> Portal -> Saturno (Solo 2 saltos). Para BFS es "Mejor"
    camino_bfs = universo.buscar_ruta_mas_corta_bfs("Tierra", "Saturno")
    print(f"[BFS] Ruta: {camino_bfs}")

    # 2. Dijkstra (Busca MENOR DISTANCIA/COSTO)
    # Dijkstra va a ver que el Portal cuesta 1000. 
    # Va a preferir ir Tierra->Marte->Cinturón->Júpiter->Saturno (50+100+200+200 = 550)
    camino_dij, distancia = universo.camino_optimo_dijkstra("Tierra", "Saturno")
    print(f"[Dijkstra] Ruta: {camino_dij}")
    print(f" -> Costo total: {distancia} años luz")

    if len(camino_bfs) < len(camino_dij):
        print("\nCONCLUSIÓN: BFS encontró un camino con menos paradas, pero Dijkstra encontró el camino más rápido.")