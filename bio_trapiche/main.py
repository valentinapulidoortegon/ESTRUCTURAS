import os
from clases import ListaCircularDoble  # ← IMPORTANTE: "clases" con S
from funciones import guardar_json, cargar_json, racha_sequia, promedio_temp, contar_estres, predecir_helada, reporte
from simulador import Simulador

lista = ListaCircularDoble()
sim = Simulador()

def limpiar():
    os.system('cls' if os.name == 'nt' else 'clear')

def menu():
    while True:
        print("\n" + "=" * 55)
        print("     🌾 BIO-TRAPICHE - Monitoreo Ambiental 🌾")
        print("=" * 55)
        print("1.  Ver todos los registros")
        print("2.  Simular datos (30 días)")
        
        print("3.  Racha más larga de sequía (recursivo)")
        print("4.  Promedio temperatura últimos N días (recursivo)")
        print("5.  Contar días con estrés hídrico (recursivo)")
        print("6.  Predecir riesgo de helada (recursivo)")
        print("7.  Generar reporte completo")
        print("8.  Guardar / Cargar datos")
        print("0.  Salir")
        print("-" * 55)
        print(f" Registros: {len(lista)}")
        print("=" * 55)
        
        op = input("Opción: ").strip()
        
        if op == "1":
            print("\n" + str(lista))
        
        elif op == "2":
            try:
                dias = int(input("Días a simular (30): ") or 30)
                etapa = input("Etapa (campo/cosecha/almacen): ") or "campo"
                sim.simular(lista, dias, etapa)
            except ValueError:
                print("❌ Número inválido")
        
        elif op == "3":
            if lista.vacia():
                print("⚠️ Sin datos")
            else:
                r = racha_sequia(lista)
                print(f"\n🔥 Racha más larga de sequía: {r} días")
                if r >= 10:
                    print("   ⚠️ ALERTA: Sequía prolongada!")
        
        elif op == "4":
            if lista.vacia():
                print("⚠️ Sin datos")
            else:
                try:
                    n = int(input("Últimos N días: "))
                    n = min(n, len(lista))
                    prom = promedio_temp(lista, n)
                    print(f"\n🌡️ Promedio temperatura últimos {n} días: {prom:.1f}°C")
                except ValueError:
                    print("❌ Número inválido")
        
        elif op == "5":
            if lista.vacia():
                print("⚠️ Sin datos")
            else:
                estres = contar_estres(lista)
                pct = (estres / len(lista)) * 100
                print(f"\n⚠️ Días con estrés hídrico: {estres} de {len(lista)} ({pct:.1f}%)")
                if pct > 30:
                    print("   🚨 ALERTA: Alto estrés hídrico!")
        
        elif op == "6":
            if lista.vacia():
                print("⚠️ Sin datos")
            else:
                nodo, dias = predecir_helada(lista)
                if nodo:
                    print(f"\n❄️ Riesgo de helada en {dias} días")
                    print(f"   Temperatura esperada: {nodo.temperatura_ambiente}°C")
                else:
                    print("\n✅ Sin riesgo de helada en los próximos 30 días")
        
        elif op == "7":
            reporte(lista)
        
        elif op == "8":
            print("\n1. Guardar\n2. Cargar")
            sub = input("Opción: ")
            if sub == "1":
                guardar_json(lista)
            elif sub == "2":
                cargar_json(lista)
        
        elif op == "0":
            print("\n👋 ¡Hasta luego!")
            break
        
        else:
            print("❌ Opción inválida")
        
        input("\nPresione Enter...")
        limpiar()

if __name__ == "__main__":
    menu()
