import json
import sys

sys.setrecursionlimit(5000)


# ========== PERSISTENCIA ==========
def guardar_json(lista, archivo="datos.json"):
    datos = [n.to_dict() for n in lista.obtener_todos()]
    with open(archivo, 'w', encoding='utf-8') as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)
    print(f"✅ Guardado en {archivo}")


def cargar_json(lista, archivo="datos.json"):
    from clases import Nodo
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            datos = json.load(f)
        for d in datos:
            lista.agregar(Nodo.from_dict(d))
        print(f"✅ Cargados {len(datos)} registros")
    except FileNotFoundError:
        print(f"❌ No se encontró {archivo}")


# ========== RECURSIVA 1: Días consecutivos de sequía ==========
def racha_sequia(lista, nodo=None, actual=0, mejor=0):
    if lista.vacia():
        return 0
    
    if nodo is None:
        nodo = lista.cabeza
    
    es_sequia = (nodo.humedad_suelo < 30 and nodo.precipitacion < 5)
    
    if es_sequia:
        nueva_actual = actual + 1
        nueva_mejor = max(mejor, nueva_actual)
    else:
        nueva_actual = 0
        nueva_mejor = mejor
    
    if nodo.siguiente == lista.cabeza:
        return nueva_mejor
    
    return racha_sequia(lista, nodo.siguiente, nueva_actual, nueva_mejor)


# ========== RECURSIVA 2: Promedio de temperatura últimos N días ==========
def promedio_temp(lista, n, nodo=None, cont=0, suma=0):
    if lista.vacia() or n <= 0:
        return 0
    
    if nodo is None:
        nodo = lista.cabeza.anterior  # el más reciente
    
    suma += nodo.temperatura_ambiente
    
    if cont + 1 >= n or nodo.anterior == lista.cabeza.anterior:
        return suma / (cont + 1)
    
    return promedio_temp(lista, n, nodo.anterior, cont + 1, suma)


# ========== RECURSIVA 3: Contar días con estrés hídrico ==========
def contar_estres(lista, nodo=None, acum=0):
    if lista.vacia():
        return 0
    
    if nodo is None:
        nodo = lista.cabeza
    
    if nodo.estres_hidrico() in ["severo", "moderado"]:
        acum += 1
    
    if nodo.siguiente == lista.cabeza:
        return acum
    
    return contar_estres(lista, nodo.siguiente, acum)


# ========== RECURSIVA 4: Buscar si habrá helada ==========
def predecir_helada(lista, nodo=None, dias=0):
    if lista.vacia():
        return None, -1
    
    if nodo is None:
        nodo = lista.cabeza
    
    if nodo.temperatura_ambiente < 10:
        return nodo, dias
    
    if dias >= 30 or nodo.siguiente == lista.cabeza:
        return None, -1
    
    return predecir_helada(lista, nodo.siguiente, dias + 1)


# ========== REPORTE SIMPLE ==========
def reporte(lista):
    if lista.vacia():
        print("Sin datos")
        return
    
    nodos = lista.obtener_todos()
    
    humedades = [n.humedad_suelo for n in nodos]
    temps = [n.temperatura_ambiente for n in nodos]
    lluvias = [n.precipitacion for n in nodos]
    
    print("\n" + "=" * 50)
    print("📋 REPORTE AMBIENTAL")
    print("=" * 50)
    print(f"Registros: {len(nodos)}")
    print(f"Humedad: promedio {sum(humedades)/len(humedades):.1f}% | min {min(humedades)}% | max {max(humedades)}%")
    print(f"Temperatura: promedio {sum(temps)/len(temps):.1f}°C | min {min(temps)}°C | max {max(temps)}°C")
    print(f"Lluvia total: {sum(lluvias):.1f}mm")
    print(f"Días con sequía: {sum(1 for n in nodos if n.humedad_suelo < 30 and n.precipitacion < 5)}")
    print(f"Racha más larga sequía: {racha_sequia(lista)} días")
    print(f"Días con estrés hídrico: {contar_estres(lista)}")
    
    helada_nodo, dias = predecir_helada(lista)
    if helada_nodo:
        print(f"⚠️ Riesgo de helada en {dias} días (temp: {helada_nodo.temperatura_ambiente}°C)")
    else:
        print("✅ Sin riesgo de helada en 30 días")
    print("=" * 50)