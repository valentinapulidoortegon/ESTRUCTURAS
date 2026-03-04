class NodoTrabajo:
    """Representa un trabajo disponible en la tienda."""
    def __init__(self, puesto):
        self.puesto = puesto    
        self.siguiente = None    

class ListaTrabajos:
    """Lista simplemente enlazada para almacenar los puestos vacantes."""
    def __init__(self):
        self.cabeza = None

    def agregar(self, puesto):
        """Agrega un nuevo puesto al final de la lista."""
        nuevo = NodoTrabajo(puesto)
        if self.cabeza is None:
            self.cabeza = nuevo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo

    def eliminar(self, puesto):
        """Elimina el primer puesto que coincida con el nombre dado."""
        actual = self.cabeza
        previo = None
        while actual:
            if actual.puesto == puesto:
                if previo is None: 
                    self.cabeza = actual.siguiente
                else:
                    previo.siguiente = actual.siguiente
                return True
            previo = actual
            actual = actual.siguiente
        return False

    def mostrar(self):
        """Muestra todos los puestos disponibles."""
        print("Puestos vacantes:")
        actual = self.cabeza
        while actual:
            print("  -", actual.puesto)
            actual = actual.siguiente
        print("------------------------")


    def contar_recursivo(self):
        """Método público: inicia el conteo desde la cabeza."""
        return self._contar_recursivo(self.cabeza)

    def _contar_recursivo(self, nodo):
        """Método privado recursivo: cuenta los nodos a partir de 'nodo'."""
        if nodo is None:
            return 0
        return 1 + self._contar_recursivo(nodo.siguiente)

class NodoHistorial:
    """Nodo doblemente enlazado para el historial de solicitudes."""
    def __init__(self, evento):
        self.evento = evento 
        self.siguiente = None
        self.anterior = None

class ListaHistorial:
    """Lista doblemente enlazada para registrar las acciones de un estudiante."""
    def __init__(self):
        self.primero = None
        self.ultimo = None

    def agregar_evento(self, evento):
        """Agrega un evento al final del historial."""
        nuevo = NodoHistorial(evento)
        if self.primero is None:
            self.primero = nuevo
            self.ultimo = nuevo
        else:
            self.ultimo.siguiente = nuevo
            nuevo.anterior = self.ultimo
            self.ultimo = nuevo

    def mostrar_adelante(self):
        """Muestra el historial desde el más antiguo al más reciente."""
        print("Historial (de antiguo a reciente):")
        actual = self.primero
        while actual:
            print("  ", actual.evento)
            actual = actual.siguiente
        print("----------------------------------------")

    def mostrar_atras(self):
        """Muestra el historial desde el más reciente al más antiguo."""
        print("Historial (de reciente a antiguo):")
        actual = self.ultimo
        while actual:
            print("  ", actual.evento)
            actual = actual.anterior
        print("----------------------------------------")


if __name__ == "__main__":
    tienda = ListaTrabajos()
    tienda.agregar("Cajero")
    tienda.agregar("Auxiliar de bodega")
    tienda.agregar("Vendedor")
    tienda.mostrar()

    print(f"Total de puestos (recursivo): {tienda.contar_recursivo()}")

    tienda.eliminar("Auxiliar de bodega")
    print("\nDespués de eliminar 'Auxiliar de bodega':")
    tienda.mostrar()

    estudiante = ListaHistorial()
    estudiante.agregar_evento("Juan Pérez se registró")
    estudiante.agregar_evento("Solicitó puesto: Cajero")
    estudiante.agregar_evento("Solicitó puesto: Vendedor")
    estudiante.agregar_evento("Entrevista programada")

    print()
    estudiante.mostrar_adelante()
    estudiante.mostrar_atras() 
