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