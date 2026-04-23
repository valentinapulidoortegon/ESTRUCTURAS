import random

class Simulador:
    def __init__(self):
        self.humedad = 65
        self.temp = 18
        self.dia = 0

    def lectura(self):
        # Variación realista
        self.humedad += random.uniform(-3, 3)
        self.humedad = max(15, min(90, self.humedad))
        
        lluvia = random.uniform(0, 45) if random.random() < 0.5 else 0
        if lluvia > 0:
            self.humedad += lluvia * 0.2
            self.humedad = min(90, self.humedad)
        
        temp = self.temp + random.uniform(-5, 10)
        temp = max(8, min(30, temp))
        
        self.dia += 1
        
        return round(self.humedad, 1), round(lluvia, 1), round(temp, 1)
    
    def simular(self, lista, dias=30, etapa="campo"):
        print(f"\n🌾 Simulando {dias} días en {etapa}")
        print("=" * 75)
        print(" Día  | Estado |  Humedad |  Lluvia | Temp | Etapa     | Alerta")
        print("-" * 75)
        
        alertas = 0
        for _ in range(dias):
            h, ll, t = self.lectura()
            nodo = lista.agregar_lectura(h, ll, t, etapa)
            
            # Determinar icono según estado
            tiene_alerta = nodo.alerta_ambiental()
            if tiene_alerta:
                alertas += 1
                icono = "Alerta"
            else:
                icono = "OK"
            
            # Mostrar TODOS los valores
            alerta_texto = tiene_alerta[0] if tiene_alerta else "OK"
            
            # Formato de fila
            print(f"{self.dia:4d}   | {icono}   | {h:6.1f}%   | {ll:6.1f}mm | {t:6.1f}°C | {etapa:9s} | {alerta_texto}")
        
        print("=" * 75)
        print(f"\n SIMULACIÓN COMPLETADA")
        print(f"   Días simulados: {dias}")
        print(f"   Alertas generadas: {alertas} ({alertas*100//dias}%)")
        print(f"   Total registros en lista: {len(lista)}")