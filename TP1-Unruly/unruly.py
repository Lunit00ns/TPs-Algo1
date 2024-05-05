"""Lógica del juego Unruly"""

from typing import List, Tuple, Any

Grilla = Any

VACIO = " "
CASILLERO_1= "1"
CASILLERO_0 = "0"

CHARS_VALIDOS = [VACIO, CASILLERO_0, CASILLERO_1]

def crear_grilla(desc: List[str]) -> Grilla:
    """Crea una grilla a partir de la descripción del estado inicial.

    La descripción es una lista de cadenas, cada cadena representa una
    fila y cada caracter una celda. Se puede asumir que la cantidad de las
    filas y columnas son múltiplo de dos. **No** se puede asumir que la
    cantidad de filas y columnas son las mismas.
    Los caracteres pueden ser los siguientes:

    Caracter  Contenido de la celda
    --------  ---------------------
         ' '  Vacío
         '1'  Casillero ocupado por un 1
         '0'  Casillero ocupado por un 0

    Ejemplo:

    >>> crear_grilla([
        '  1 1 ',
        '  1   ',
        ' 1  1 ',
        '  1  0',
    ])
    """
    grilla = []
 
    for f in desc:           
        filas = []                     
        for char in f:
            if char not in CHARS_VALIDOS:
                return False
            filas.append(char)
        grilla.append(filas)

    return grilla

def dimensiones(grilla: Grilla) -> Tuple[int, int]:
    """Devuelve la cantidad de columnas y la cantidad de filas de la grilla
    respectivamente (ancho, alto)"""
    
    alto = len(grilla)     
    ancho = len(grilla[0])   
    
    return(ancho, alto)

def posicion_es_vacia(grilla: Grilla, col: int, fil: int) -> bool:
    """Devuelve un booleano indicando si la posición de la grilla dada por las
    coordenadas `col` y `fil` está vacía"""
    return grilla [fil][col] == VACIO

def posicion_hay_uno(grilla: Grilla, col: int, fil: int) -> bool:
    """Devuelve un booleano indicando si la posición de la grilla dada por las
    coordenadas `col` y `fil` está el valor 1"""
    return grilla[fil][col] == CASILLERO_1

def posicion_hay_cero(grilla: Grilla, col: int, fil: int) -> bool:
    """Devuelve un booleano indicando si la posición de la grilla dada por las
    coordenadas `col` y `fil` está el valor 0"""
    return grilla[fil][col] == CASILLERO_0

def cambiar_a_uno(grilla: Grilla, col: int, fil: int):
    """Modifica la grilla, colocando el valor 1 en la posición de la grilla
    dada por las coordenadas `col` y `fil`"""
    grilla[fil][col] = CASILLERO_1

def cambiar_a_cero(grilla: Grilla, col: int, fil: int):
    """Modifica la grilla, colocando el valor 0 en la posición de la grilla
    dada por las coordenadas `col` y `fil`"""
    grilla[fil][col] = CASILLERO_0

def cambiar_a_vacio(grilla: Grilla, col: int, fil: int):
    """Modifica la grilla, eliminando el valor de la posición de la grilla
    dada por las coordenadas `col` y `fil`"""
    grilla[fil][col] = VACIO

def chars_consecutivos_fila(grilla: Grilla, fil: int) -> bool:
    """Chequea si en determinada fila de la grilla aparecen tres caracteres
    iguales consecutivos. Si es así, devuelve False.""" 
    for char in range(len(grilla[fil])-2):
        if grilla[fil][char] == grilla[fil][char+1] == grilla[fil][char+2]:
            return False
    return True

def fila_es_valida(grilla: Grilla, fil: int) -> bool:
    """Devuelve un booleano indicando si la fila de la grilla denotada por el
    índice `fil` es considerada válida.

    Una fila válida cuando se cumplen todas estas condiciones:
        - La fila no tiene vacíos
        - La fila tiene la misma cantidad de unos y ceros
        - La fila no contiene tres casilleros consecutivos del mismo valor
    """ 
    return(VACIO not in grilla[fil] and
           grilla[fil].count(CASILLERO_0) == grilla[fil].count(CASILLERO_1) and
           chars_consecutivos_fila(grilla,fil))
    
def columna_a_lista(grilla: Grilla, col: int) -> list:
    """Convierte la columna que se pasa como parámetro a una lista para
    trabajar de manera más cómoda."""
    columna = []
    
    for fil in range(len(grilla)):
        for char in grilla[fil][col]:
            columna.append(char)
            
    return columna

def chars_consecutivos_columna(grilla: Grilla, col: int) -> bool:
    """Chequea si en determinada columna de la grilla aparecen tres 
    caracteres iguales consecutivos. Si es así, devuelve False."""
    columna = columna_a_lista(grilla,col)
    
    for char in range(len(columna)-2):
        if columna[char] == columna[char+1] == columna[char+2]:
            return False
    return True
           
def columna_es_valida(grilla: Grilla, col: int) -> bool:
    """Devuelve un booleano indicando si la columna de la grilla denotada por
    el índice `col` es considerada válida.

    Las condiciones para que una columna sea válida son las mismas que las
    condiciones de las filas."""
    
    return(VACIO not in columna_a_lista(grilla,col) and
           columna_a_lista(grilla,col).count(CASILLERO_0) == columna_a_lista(grilla,col).count(CASILLERO_1) and
           chars_consecutivos_columna(grilla,col))

def grilla_terminada(grilla: Grilla) -> bool:
    """Devuelve un booleano indicando si la grilla se encuentra terminada.

    Una grilla se considera terminada si todas sus filas y columnas son
    válidas."""
    
    for dim in range(len(grilla)):
        if not fila_es_valida(grilla, dim) or not columna_es_valida(grilla, dim):
            return False
    return True