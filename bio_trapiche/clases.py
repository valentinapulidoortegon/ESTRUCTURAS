from datetime import datetime
 
 
class Nodo:
    def __init__(self, humedad_suelo, precipitacion, temperatura_ambiente,
                 timestamp=None, etapa="campo"):
        self.humedad_suelo = humedad_suelo
        self.precipitacion = precipitacion
        self.temperatura_ambiente = temperatura_ambiente
        self.timestamp = timestamp or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.etapa = etapa
        self.siguiente = None
        self.anterior = None
 
    def estres_hidrico(self):
        if self.humedad_suelo < 20:
            return "severo"
        elif self.humedad_suelo < 40:
            return "moderado"
        elif self.humedad_suelo > 80:
            return "exceso"
        return "normal"
 
    def alerta_ambiental(self):
        alertas = []
 
        if self.humedad_suelo < 30:
            alertas.append(f"SEQUIA: Humedad del suelo al {self.humedad_suelo}%")
        elif self.humedad_suelo > 75:
            alertas.append(f"EXCESO AGUA: Suelo con {self.humedad_suelo}% humedad")
 
        if self.precipitacion > 30:
            alertas.append(f"LLUVIA INTENSA: {self.precipitacion}mm en 24h")
        elif self.precipitacion == 0 and self.humedad_suelo < 40:
            alertas.append("SIN LLUVIA: Riesgo de sequia")
 
        if self.temperatura_ambiente < 12:
            alertas.append(f"FRIO EXTREMO: {self.temperatura_ambiente}C - Riesgo para cultivo")
        elif self.temperatura_ambiente > 32:
            alertas.append(f"CALOR EXTREMO: {self.temperatura_ambiente}C - Estres termico")
 
        return alertas
 
    def __str__(self):
        alerta_icono = "[ALERTA]" if self.alerta_ambiental() else "[OK]"
        return (f"[{self.timestamp}] {alerta_icono} "
                f"Humedad:{self.humedad_suelo}% | Lluvia:{self.precipitacion}mm | "
                f"Temp:{self.temperatura_ambiente}C | {self.etapa} | "
                f"Estres:{self.estres_hidrico()}")
 
    def to_dict(self):
        return {
            "humedad_suelo": self.humedad_suelo,
            "precipitacion": self.precipitacion,
            "temperatura_ambiente": self.temperatura_ambiente,
            "timestamp": self.timestamp,
            "etapa": self.etapa
        }
 
    @classmethod
    def from_dict(cls, data):
        return cls(
            humedad_suelo=data["humedad_suelo"],
            precipitacion=data["precipitacion"],
            temperatura_ambiente=data["temperatura_ambiente"],
            timestamp=data.get("timestamp"),
            etapa=data.get("etapa", "campo")
        )
 
 
class ListaCircularDoble:
    def __init__(self):
        self.cabeza = None
        self.tamanio = 0
 
    def vacia(self):
        return self.cabeza is None
 
    def agregar(self, nodo):
        if self.vacia():
            self.cabeza = nodo
            nodo.siguiente = nodo
            nodo.anterior = nodo
        else:
            ultimo = self.cabeza.anterior
            nodo.siguiente = self.cabeza
            nodo.anterior = ultimo
            ultimo.siguiente = nodo
            self.cabeza.anterior = nodo
        self.tamanio += 1
 
    def agregar_lectura(self, humedad_suelo, precipitacion, temperatura_ambiente, etapa="campo"):
        nodo = Nodo(humedad_suelo, precipitacion, temperatura_ambiente, etapa=etapa)
        self.agregar(nodo)
        return nodo
 
    def obtener_todos(self):
        if self.vacia():
            return []
        resultado = []
        actual = self.cabeza
        for _ in range(self.tamanio):
            resultado.append(actual)
            actual = actual.siguiente
        return resultado
 
    def __len__(self):
        return self.tamanio
 
    def __str__(self):
        if self.vacia():
            return "No hay registros ambientales"
        return "\n".join(str(n) for n in self.obtener_todos())
 