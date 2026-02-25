def invertirCadena(textoParaInvertir):
    # Caso base: si la cadena está vacía o tiene un solo carácter
    if len(textoParaInvertir) <= 1:
        return textoParaInvertir
    
    # Caso recursivo: último carácter + resto de la cadena procesada
    return textoParaInvertir[-1] + invertirCadena(textoParaInvertir[:-1])

resultadoFinal = invertirCadena("Recursion")
print(resultadoFinal) # Salida: noisruceR