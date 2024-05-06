import gamelib

TAMAÑO_CELDA = 25
MARGEN = 10

BOTONES_COLORES = {
    "Personalizado": [10, 40, '#ffffff'],       
    "Violeta": [50, 80, '#9c4f96'],         
    "Rojo": [90, 120, '#ff6355'],
    "Naranja": [130, 160, '#fba949'],
    "Amarillo": [170, 200, '#fae442'],
    "Verde": [210, 240, '#8bd448'],
    "Celeste": [250, 280, '#2aa8f2']
}

def en_rango(i:int, j:int, paint) -> bool:
    '''Recibe dos coordenadas correspondientes a una posición en el tablero.
    Devuelve True si se encuentra dentro de los límites del tablero, False
    en caso contrario.'''
    
    alto_celda = len(paint)
    ancho_celda = len(paint[0])
    
    if i < 0 or i >= alto_celda or j < 0 or j >= ancho_celda:
        return False
    return True

def pixel_a_celda(x:int, y:int, tamaño_celda:int, margen:int) -> tuple:
    '''Convierte coordenadas en píxeles de gamelib a coordenadas de celdas.'''
    
    celda_x = (x - margen) // tamaño_celda
    celda_y = (y - margen) // tamaño_celda
    return celda_x, celda_y

def celda_a_pixel(celda_x:int, celda_y:int, tamaño_celda:int, margen:int) -> tuple:
    '''Convierte coordenadas de celdas a coordenadas en píxeles de gamelib.'''
        
    x = margen + celda_x * tamaño_celda
    y = margen + celda_y * tamaño_celda
    return x, y

def es_hexadecimal(color:str) -> bool:
    '''Verifica si el color dado como parámetro está en formato hexadecimal,
    permitiendo su representación tanto con o sin "#". Devuelve True si el
    color está en formato hexadecimal, y False en caso contrario.'''
    
    if color.startswith("#"):
        hexa = color[1:]
    else:
        hexa = color
    
    if len(hexa) == 6:
        for c in hexa:
            if c not in "0123456789ABCDEFabcdef":
                return False
        return True
    return False

def seleccionar_color(x:int, y:int, color_selec:str, color_perso:str, alto_v:int) -> tuple:
    '''Selecciona el color correspondiente para pintar en base al botón
    de color en el que el usuario hizo clic.'''
    
    for color, boton in BOTONES_COLORES.items():
        x1, x2, hex_color = boton

        if x1 <= x <= x2 and alto_v + 20 <= y <= alto_v + 50:
            if color == "Personalizado":
                nuevo_color = gamelib.input("Ingrese un color en formato hexadecimal: ")
                
                if nuevo_color != None:
                    
                    while not es_hexadecimal(nuevo_color):
                        nuevo_color = gamelib.input("Ingrese otro color en formato hexadecimal: ")
                        
                        if nuevo_color == None:
                            return color_perso, color_perso     # Si se cierra la ventana para seleccionar un color personalizado,
                                                                # se utiliza el útimo color personalizado que esté almacenado
                    if "#" not in nuevo_color:
                        nuevo_color = "#" + nuevo_color 
                    
                    color_selec = nuevo_color
                    color_perso = nuevo_color
                    
                return color_perso, color_perso
                
            color_selec = hex_color
    
    return color_selec, color_perso

def actualizar_color(x:int, y:int, paint:list, color:str) -> list:
    '''Se actualiza el color con el que se van a pintar las celdas del tablero.'''
    
    punto_a, punto_b = pixel_a_celda(x, y, TAMAÑO_CELDA, MARGEN)
    if en_rango(punto_b, punto_a, paint):
        paint[punto_b][punto_a] = color  
    return paint

def pintar_celda(paint:list):
    '''Pinta la celda de la grilla en la que el ususario hace clic.'''
         
    for i in range(len(paint[0])):
        for j in range(len(paint)):
            x, y = celda_a_pixel(i, j, TAMAÑO_CELDA, MARGEN)
            color = paint[j][i]
            gamelib.draw_rectangle(x, y, x + TAMAÑO_CELDA, y + TAMAÑO_CELDA, outline="black", fill=color, width=.5)
            
def balde_pintura(x:int, y:int, paint:list, color_selec:str):
    '''Observa el color actual de la celda sobre la que está posicionada el mouse al
    momento de llamar a la función y el botón de color seleccionado. Luego llama a
    la función pintar_celdas_vecinas() para pintar el área deseada.'''
    
    a, b = pixel_a_celda(x, y, TAMAÑO_CELDA, MARGEN)
    if en_rango(a, b, paint):
        color_actual = paint[b][a]
        pintar_celdas_vecinas(a, b, color_actual, color_selec, paint)
        
def pintar_celdas_vecinas(i:int, j:int, color_actual:str, color_selec:str, paint:list):
    '''Se usan los movimientos hacia arriba, abajo, izquierda y derecha para acceder a
    las celdas vecinas de la celda actual en la grilla. Si estas celdas son del mismo
    color que la celda actual, pinta a todas del color seleccionado.
    
    Nota: La celda actual es sobre la que está posicionado el mouse al momento de usar
    el balde de pintura.'''
    if not en_rango(j, i, paint):
        return

    if paint[j][i] != color_actual:     # el color de la nueva celda no coincide con el color actual
        return

    if paint[j][i] == color_selec:      # la nueva celda ya fue pintada del color seleccionado
        return

    paint[j][i] = color_selec

    desplazamientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]  

    for movimiento_x, movimiento_y in desplazamientos:
        nueva_celda_x = i + movimiento_x
        nueva_celda_y = j + movimiento_y
        pintar_celdas_vecinas(nueva_celda_x, nueva_celda_y, color_actual, color_selec, paint)
            
def actualizar_movimientos(estados_grilla, x:int, y:int, paint:list, func, color_selec:str):
    '''Actualiza la grilla después de realizar una acción de pintado y la pila de "estados_grilla",
    donde se guardan todos los movimientos que involucran una modificación de esta.
    
    El parámetro func es la función a utilizar para realizar la acción de pintado, la cual puede ser:
        - "actualizar_color" si el usuario quiere pintar una celda con el clic, ya sea uno solo o
        manteniendo presionado el botón.
        - "balde_pintura" si usa el balde para pintar un área determinada.'''
    
    celda_x, celda_y = pixel_a_celda(x, y, TAMAÑO_CELDA, MARGEN)
    if en_rango(celda_y, celda_x, paint):
        copia_paint = []
        for fila in paint:
            copia_fila = list(fila)
            copia_paint.append(copia_fila)
        estados_grilla.apilar(copia_paint)
        paint = func(x, y, paint, color_selec)
        
def deshacer(estados_grilla, movimientos_descartados, inicio:list) -> list:
    '''Deshace el último movimiento realizado en la grilla y lo apila en "movimientos
    descartados". Retorna el estado de la grilla después de deshacer el último movimiento.
    Si no hay más movimientos por deshacer, retorna una grilla vacía.'''
    
    paint = estados_grilla.desapilar()
    if estados_grilla.esta_vacia():
        estados_grilla.apilar(inicio)
        return inicio
    else:
        movimientos_descartados.apilar(paint)
    return paint
    
def rehacer(estados_grilla, movimientos_descartados, inicio:list) -> list:
    '''Rehace el último movimiento que fue guardado en la pila de "movimientos descartados".
    Retorna el estado de la grilla después de rehacer el último movimiento. Si no hay más
    movimientos por rehacer, devuelve la grilla con la última modificación realizada antes
    de comenzar a deshacer movimientos.'''
    
    paint = movimientos_descartados.desapilar()
    if movimientos_descartados.esta_vacia():
        movimientos_descartados.apilar(inicio)
        return estados_grilla.ver_tope()               # No hay más movimientos para rehacer
    else:
        estados_grilla.apilar(paint)
    return paint