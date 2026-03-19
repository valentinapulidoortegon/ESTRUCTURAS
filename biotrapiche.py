import time

class NodoEstacion:
    """Representa una estación en la planta o un punto de control de drones."""
    def __init__(self, nombre, coordenadas):
        self.nombre = nombre
        self.coordenadas = coordenadas
        self.estado_carga = False
        self.siguiente = None
        self.anterior = None # Para listas circulares dobles

class ListaCircularSencilla:
    """Implementación para el Robot AGV (Recolección Infinita)."""
    def __init__(self):
        self.cabeza = None

    def agregar_estacion(self, nombre, coordenadas):
        nuevo_nodo = NodoEstacion(nombre, coordenadas)
        if not self.cabeza:
            self.cabeza = nuevo_nodo
            nuevo_nodo.siguiente = self.cabeza
        else:
            actual = self.cabeza
            while actual.siguiente != self.cabeza:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo
            nuevo_nodo.siguiente = self.cabeza

    def simular_agv(self, ciclos=2):
        """Simula el movimiento del robot por las estaciones."""
        if not self.cabeza:
            return
        
        actual = self.cabeza
        count = 0
        total_nodos = self._contar_nodos()
        
        print(f"--- Iniciando Ciclo de Robot AGV ({ciclos} vueltas) ---")
        while count < (ciclos * total_nodos):
            # Simular detección de carga aleatoria para el ejemplo
            if count % 2 == 0:
                actual.estado_carga = True
            
            print(f"Robot en: {actual.nombre} {actual.coordenadas}")
            if actual.estado_carga:
                print(f"  > [CARGA DETECTADA] Recogiendo panela...")
                actual.estado_carga = False
            
            actual = actual.siguiente
            count += 1
            time.sleep(0.5)
        print("--- Ciclo de AGV Completado ---\n")

    def _contar_nodos(self):
        if not self.cabeza: return 0
        count = 1
        actual = self.cabeza
        while actual.siguiente != self.cabeza:
            count += 1
            actual = actual.siguiente
        return count

class ListaCircularDoble:
    """Implementación para Drones de Inspección (Navegación Flexible)."""
    def __init__(self):
        self.cabeza = None

    def agregar_punto_control(self, nombre, coordenadas):
        nuevo_nodo = NodoEstacion(nombre, coordenadas)
        if not self.cabeza:
            self.cabeza = nuevo_nodo
            nuevo_nodo.siguiente = self.cabeza
            nuevo_nodo.anterior = self.cabeza
        else:
            ultimo = self.cabeza.anterior
            ultimo.siguiente = nuevo_nodo
            nuevo_nodo.anterior = ultimo
            nuevo_nodo.siguiente = self.cabeza
            self.cabeza.anterior = nuevo_nodo

    def simular_dron(self):
        """Simula inspección con retroceso ante anomalías."""
        if not self.cabeza: return
        
        actual = self.cabeza
        print("--- Iniciando Inspección de Dron (Ruta Circular Doble) ---")
        
        # Paso 1: Avanzar
        print(f"Dron avanzando a: {actual.nombre}")
        actual = actual.siguiente
        print(f"Dron avanzando a: {actual.nombre}")
        
        # Paso 2: Simular anomalía y retroceder
        print(f"  ! [ANOMALÍA DETECTADA] en {actual.nombre}. Re-inspeccionando punto anterior...")
        actual = actual.anterior
        print(f"Dron retrocedió a: {actual.nombre} para captura de imagen detallada.")
        
        # Paso 3: Continuar flujo normal
        actual = actual.siguiente.siguiente
        print(f"Dron retomando ruta hacia: {actual.nombre}")
        print("--- Inspección de Dron Finalizada ---\n")

# Pruebas del Sistema
if __name__ == "__main__":
    # 1. Configurar AGV (Circular Sencilla)
    trapiche_agv = ListaCircularSencilla()
    trapiche_agv.agregar_estacion("Molienda", (0, 0))
    trapiche_agv.agregar_estacion("Evaporación", (10, 5))
    trapiche_agv.agregar_estacion("Moldeo", (20, 0))
    trapiche_agv.simular_agv(ciclos=1)

    # 2. Configurar Dron (Circular Doble)
    dron_sumapaz = ListaCircularDoble()
    dron_sumapaz.agregar_punto_control("Sector Norte - Cañaduzal", (100, 200))
    dron_sumapaz.agregar_punto_control("Sector Este - Mantenimiento", (150, 250))
    dron_sumapaz.agregar_punto_control("Sector Sur - Cosecha", (100, 300))
    dron_sumapaz.simular_dron()
