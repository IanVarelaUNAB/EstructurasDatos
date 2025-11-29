import heapq  # Librería para la "Cola de Prioridad"
from collections import deque # Librería para BFS

# ==========================================================
# PARTE A: GESTOR DE MISIONES (COLA DE PRIORIDAD)
# ==========================================================
# Usamos un "Heap" o "Montículo Binario" inventado por J.W.J. Williams en 1964.
# Mantiene automáticamente el elemento más "importante" al principio.
# ==========================================================

class GestorMisiones:
    def __init__(self):
        self.cola_misiones = []

    def agregar_mision(self, nombre, nivel_amenaza):
        # Python usa "Min-Heap" asi que lo guardamos en un numero negativo
        # Así Ej: el -10 saldria primero.
        prioridad = -nivel_amenaza
        
        # Guardamos una tupla: (prioridad, nombre)
        heapq.heappush(self.cola_misiones, (prioridad, nombre))
        print(f"-> Misión agregada: {nombre} (Amenaza: {nivel_amenaza})")

    def sacar_mision(self):
        if len(self.cola_misiones) == 0:
            print("No hay misiones pendientes.")
            return None
        
        # heappop saca automáticamente la de mayor prioridad (número más negativo)
        prioridad, nombre = heapq.heappop(self.cola_misiones)
        
        # Convertimos la prioridad de nuevo a positivo para mostrarla
        nivel_real = -prioridad 
        print(f"!!! MISION ASIGNADA: {nombre} (Amenaza: {nivel_real}) !!!")
        return nombre

    def mostrar_pendientes(self):
        print("\n--- Misiones en espera (El orden interno puede variar) ---")
        # Hacemos una copia ordenada solo para mostrar, sin tocar la cola real
        lista_ordenada = sorted(self.cola_misiones)
        for prio, nom in lista_ordenada:
            print(f"  * {nom} - Nivel {-prio}")
        print("--------------------------------------------------------\n")


# ==========================================================
# PARTE B: GRAFO DEL UNIVERSO (BFS y DFS)
# ==========================================================
# Inventado por Leonhard Euler en 1736 probandolo por primera vez con Los Puentes de Königsberg
# En nuestro caso:
# - Nodos = Planetas
# - Aristas = Rutas
# - BFS (Anchura): Busca por capas (encuentra camino con menos saltos).
# - DFS (Profundidad): Explora un camino hasta el fondo antes de volver.
# ==========================================================

class GrafoUniverso:
    def __init__(self):
        # Clave = Planeta, Valor = Lista de vecinos
        self.rutas = {}

    def agregar_ruta(self, origen, destino):
        # Si el planeta no existe en el diccionario, creamos su lista
        if origen not in self.rutas:
            self.rutas[origen] = []
        if destino not in self.rutas:
            self.rutas[destino] = []

        # Agregamos la conexión (Ida y Vuelta)
        self.rutas[origen].append(destino)
        self.rutas[destino].append(origen)
        # print(f"Ruta creada: {origen} <--> {destino}")

    # --- ALGORITMO BFS (Búsqueda en Anchura) ---
    # Sirve para encontrar la ruta con menos escalas
    def buscar_ruta_mas_corta_bfs(self, inicio, fin):
        print(f"\nBusca ruta BFS de {inicio} a {fin}...")
        cola = deque() 
        cola.append([inicio]) # Empezamos con el planeta origen
        
        visitados = {inicio} # Para no repetir planetas

        while len(cola) > 0:
            camino = cola.popleft() # Sacamos el primer camino de la fila
            ultimo_planeta = camino[-1] # Vemos cuál es el último planeta visitado

            if ultimo_planeta == fin:
                return camino

            # Revisamos los vecinos
            vecinos = self.rutas.get(ultimo_planeta, [])
            for vecino in vecinos:
                if vecino not in visitados:
                    visitados.add(vecino)
                    nuevo_camino = list(camino) # Copiamos el camino actual
                    nuevo_camino.append(vecino) # Le agregamos el vecino
                    cola.append(nuevo_camino)
        
        return None # No se encontró camino

    # --- ALGORITMO DFS (Búsqueda en Profundidad) ---
    # Sirve para explorar o ver si dos cosas están conectadas (aunque sea lejos)
    def explorar_dfs(self, actual, visitados=None):
        if visitados is None:
            visitados = set()
            print(f"\nExplorando universo desde {actual} (DFS):")

        visitados.add(actual)
        print(f" -> Visitando: {actual}")

        vecinos = self.rutas.get(actual, [])
        for vecino in vecinos:
            if vecino not in visitados:
                self.explorar_dfs(vecino, visitados)


# ==========================================================
# MAIN TESTEOS
# ==========================================================
if __name__ == "__main__":
    
    # 1. PRUEBA DE MISIONES
    print("=== GESTIÓN DE MISIONES (PRIORIDADES) ===")
    gestor = GestorMisiones()
    
    # Misiones desordenadas
    gestor.agregar_mision("Entregar paquete", 2)
    gestor.agregar_mision("Salvar la galaxia", 10) # Debería salir primero
    gestor.agregar_mision("Escoltar nave comercial", 5)
    
    gestor.mostrar_pendientes()

    # Sacamos misiones (deben salir por orden de importancia)
    gestor.sacar_mision() # Esperamos la de nivel 10
    gestor.sacar_mision() # Esperamos la de nivel 5
    gestor.sacar_mision() # Esperamos la de nivel 2

    print("\n" + "="*50 + "\n")

    # 2. PRUEBA DEL UNIVERSO (GRAFOS)
    print("=== NAVEGACIÓN (GRAFOS) ===")
    universo = GrafoUniverso()

    # Rutas (Se puede usar csv como en el ejercicio 1)
    universo.agregar_ruta("Tierra", "Luna")
    universo.agregar_ruta("Tierra", "Marte")
    universo.agregar_ruta("Marte", "Jupiter")
    universo.agregar_ruta("Jupiter", "Saturno")
    universo.agregar_ruta("Jupiter", "Planeta X")
    universo.agregar_ruta("Planeta X", "Namek")
    universo.agregar_ruta("Planeta X", "Planeta vegita")
    universo.agregar_ruta("Luna", "Estación Espacial")
    
    # DFS (Exploración)
    universo.explorar_dfs("Tierra")

    # BFS (Buscar camino)
    camino = universo.buscar_ruta_mas_corta_bfs("Tierra", "Saturno")

    print(f"\nCamino encontrado (BFS): {camino}")
