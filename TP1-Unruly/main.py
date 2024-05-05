from unruly import *
import niveles
import random

INDICE_COLUMNAS = ['a','b','c','d','e','f','g','h','i','j','k','l',"m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

def imprimir_tablero(grilla: Grilla, nivel: list):
    
    # Indice de columnas
    print("    ", end="")
    for letra_columna in range(len(nivel[0])):
        print(INDICE_COLUMNAS[letra_columna] + " ",end="")
    print("")
    
    # Indice de filas
    indice_filas = 1
    for fila in grilla:
        print(indice_filas, "|", end=" ")
        for char in fila:
            # Cambia los vacíos por guión bajo solo por "estética".
            if char == VACIO:
                char = "_"
            print(char, end=" ")
        print()
        indice_filas +=1
    
def modificar_tablero(grilla: Grilla) -> Grilla:
    """Le permite al usuario modificar una determinada celda con algún valor
    que esté dentro de los CHARS_VALIDOS ('1','0' o ' ').
    Si se ingresa un valor distinto a estos o un formato de entrada inválido,
    se imprime un mensaje de error con el motivo y se le vuelve a dar la
    oportunidad de escribir una entrada válida o salir del programa."""
    
    while True: 
        
        print("""Entrada: [columna,fila,valor]
Para salir: x""")

        celda = input("Entrada: ")
        
        if celda == "x":
            print("Nos vemos!")
            exit()
        
        try: 
            columna, fila, valor = celda.split(",")
            
            if valor in CHARS_VALIDOS:
                columna = INDICE_COLUMNAS.index(columna)
                fila = int(fila) - 1            # Si no pongo el -1 no puedo acceder a la primera fila
                grilla[fila][columna] = valor
                return grilla
            
            else: 
                print("❌ Valor inválido ❌ Solo se permiten los valores '0', '1' y ' '.")
            
        except: 
            print("❌ Formato inválido ❌ Debe ingresar [columna,fila,valor]")
        
def errores_fila(grilla: Grilla, fila_actual: int) -> Grilla:
    """Solo se va a ejecutar si en la función 'main' se detecta que una
    fila que se acaba de completar es inválida. En este caso, se va a
    imprimir un mensaje con el n° de fila que está fallando y el motivo.
    """
    print(f"❌ Error en fila {fila_actual + 1} ❌")
    
    if chars_consecutivos_fila(grilla,fila_actual) == False:
        print("- No pueden haber 3 casilleros consecutivos con el mismo valor.")
            
    if grilla[fila_actual].count(CASILLERO_0) != grilla[fila_actual].count(CASILLERO_1):
        print("- Deben haber la misma cantidad de 0 y 1.")
                
    print("Intenta de vuelta...")
    grilla_mod = modificar_tablero(grilla)
    
    return grilla_mod

def errores_columna(grilla: Grilla, col_actual: int) -> Grilla:
    """Solo se va a ejecutar si en la función 'main' se detecta que una
    columna que se acaba de completar es inválida. En este caso, se va a
    imprimir un mensaje indicando cual columna está fallando y el motivo.
    """
    letra_columna = INDICE_COLUMNAS[col_actual]
    print(f"❌ Error en columna {letra_columna} ❌")
    
    if chars_consecutivos_columna(grilla,col_actual) == False:
        print("- No pueden haber 3 casilleros consecutivos con el mismo valor.")
            
    if columna_a_lista(grilla,col_actual).count(CASILLERO_0) != columna_a_lista(grilla,col_actual).count(CASILLERO_1):
        print("- Deben haber la misma cantidad de 0 y 1.")
                
    print("Intenta de vuelta...")
    grilla_mod = modificar_tablero(grilla)
    
    return grilla_mod

def main():
    nivel = random.choice(niveles.NIVELES)
    grilla = crear_grilla(nivel)
    imprimir_tablero(grilla,nivel)
    
    while grilla_terminada(grilla) == False:
        
        grilla_mod = modificar_tablero(grilla)
        imprimir_tablero(grilla_mod,nivel)
        
        # Verificar validez de cada fila que se completa sin vacíos
        for fila in range(len(grilla_mod)):
            if VACIO not in grilla_mod[fila]:
                # Si la fila es inválida se va a ver por qué y se le permite al usuario modificarla
                if fila_es_valida(grilla_mod, fila) == False:
                    grilla_mod = errores_fila(grilla_mod, fila)
                    imprimir_tablero(grilla_mod,nivel)
            else:
                # Si está todo bien, continua el ciclo
                continue
            
        # Verificar validez de cada columna que se completa sin vacíos
        for col in range(len(grilla_mod[0])):
            if VACIO not in columna_a_lista(grilla_mod,col):
                # Si la columna es inválida se va a ver por qué y se le permite al usuario modificarla
                if columna_es_valida(grilla_mod,col) == False:
                    grilla_mod = errores_columna(grilla_mod,col)
                    imprimir_tablero(grilla_mod,nivel)
            else:
                # Si está todo bien, continua el ciclo
                continue
                    
    print("Juego terminado ✅")
    exit()
        
main()