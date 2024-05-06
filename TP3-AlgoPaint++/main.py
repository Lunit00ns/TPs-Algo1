import pila
import gamelib
import modificaciones_paint
import manejo_archivos

TAMAÑO_CELDA = 25
MARGEN = 10
ANCHO_MIN = 500

def obtener_dimensiones() -> tuple:
    '''Al iniciar el programa, se ejecuta esta función para obtener las dimensiones
    necesarias para dibujar la ventana y la grilla correctamente.

    Devuelve:
        Una tupla con las dimensiones obtenidas en el siguiente orden:
        (filas: int, columnas: int, ancho_ventana: int, alto_ventana: int)
        Si se cierra la ventana emergente, devuelve None.'''
    
    while True:
        filas = gamelib.input("Cantidad de filas: ")
        columnas = gamelib.input("Cantidad de columnas: ")
        
        if filas is None or columnas is None:
            return None
            
        if filas.isdigit() and columnas.isdigit() and int(filas) > 0 and int(columnas) > 0:
            filas = int(filas)
            columnas = int(columnas)
                
            ancho_v = columnas * TAMAÑO_CELDA
            alto_v = filas * TAMAÑO_CELDA
                
            return filas, columnas, ancho_v, alto_v
            
        gamelib.say("Por favor, ingresá dimensiones válidas (números enteros mayores a 0)")
      
def paint_nuevo(alto:int, ancho:int) -> list:
    '''Inicializa el estado del programa con una imagen vacía de ancho x alto celdas.'''

    paint = []
    for i in range(alto):
        filas = []
        for j in range(ancho):
            filas.append("#ffffff")   
        paint.append(filas)  
    return paint

def paint_mostrar(paint:int, color_selec:str, color_perso:str, ancho_v:int, alto_v:int):
    '''Dibuja la interfaz de la aplicación en la ventana. 
    
    Nota: si el ancho de la ventana que se recibe como parámetro es menor a 350 (es decir, si la
    cantidad de columnas que elige el usuario es menor a 20) se va a redimensionar la ventana con
    la constante ANCHO_MIN para que los botones se muestren correctamente en pantalla.'''
    
    botones_colores = modificaciones_paint.BOTONES_COLORES
    botones_imagenes = manejo_archivos.BOTONES_IMAGENES

    gamelib.draw_begin()
    
    if ancho_v < ANCHO_MIN:
        gamelib.draw_rectangle(0, 0, ANCHO_MIN + 20, alto_v + 100, outline='#ffeacc', fill='#ffeacc')
        gamelib.resize(ANCHO_MIN + 20, alto_v + 100)
    
    gamelib.draw_rectangle(0, 0, ancho_v + 20, alto_v + 100, outline='#ffeacc', fill='#ffeacc')
    gamelib.draw_rectangle(MARGEN, MARGEN, ancho_v + MARGEN, alto_v + MARGEN, outline='#fef7d5', fill="white")
    
    for boton in botones_colores:
        x1, x2, color = botones_colores[boton]
        y1 = alto_v + 20
        y2 = alto_v + 50
        # Remarcar el boton de color seleccionado
        if color == color_selec:
            gamelib.draw_rectangle(x1, y1, x2, y2, fill=None, outline='black', width=3)
            
        if boton == "Personalizado":
            if color_selec != color_perso:
                # Si el color seleccionado es diferente al color personalizado, cambiar el color del botón "Personalizado"
                color = color_perso
            else:
                # Si el color seleccionado es igual al color personalizado, mantener el último color que había sido seleccionado
                color = color_selec
                gamelib.draw_rectangle(x1, y1, x2, y2, fill=None, outline='black', width=3)
                
        gamelib.draw_rectangle(x1, y1, x2, y2, fill=color)
    
    gamelib.draw_image("imgs/flecha_deshacer.gif", 370, alto_v + 13) 
    gamelib.draw_text("Z", 387, alto_v + 75, size=12, fill="black")   
    gamelib.draw_image("imgs/flecha_rehacer.gif", 410, alto_v + 13) 
    gamelib.draw_text("Y", 427, alto_v + 75, size=12, fill="black")    
    gamelib.draw_image("imgs/balde.gif", 450, alto_v + 13)    
    gamelib.draw_text("B", 465, alto_v + 75, size=12, fill="black") 
        
    for boton in botones_imagenes:
        x1, x2 = botones_imagenes[boton][0]
        texto, x = botones_imagenes[boton][1]
        gamelib.draw_rectangle(x1, alto_v + 90, x2, alto_v + 60, fill="#e89a80")
        gamelib.draw_text(texto, x, alto_v + 75, size=12, fill="black")
    
    # Dibujar las líneas de la grilla
    for i in range(len(paint) + 1):
        gamelib.draw_line(MARGEN, MARGEN + i *TAMAÑO_CELDA, ancho_v + MARGEN, MARGEN + i *TAMAÑO_CELDA, fill='black', width=.5)

    for j in range(len(paint[0]) + 1):
        gamelib.draw_line(MARGEN + j * TAMAÑO_CELDA, MARGEN, MARGEN + j * TAMAÑO_CELDA, alto_v + MARGEN, fill='black', width=.5)

    gamelib.draw_end() 
    
def manejar_clic_boton(ev, color_selec: str, color_perso: str, paint, ancho_v:int, alto_v: int) -> tuple:
    '''Maneja el evento de clic de un botón.

    Procesa el evento "ev" correspondiente a un clic de botón y realiza diferentes acciones
    dependiendo del botón en el que se hizo clic. Esto incluye el manejo de los botones de
    selección de color y los botones para guardar/cargar imágenes.'''
    
    if ev.type == gamelib.EventType.ButtonPress and ev.mouse_button == 1:
        x, y = ev.x, ev.y 

        # Se hizo clic en alguno de los botones de colores
        color_selec, color_perso = modificaciones_paint.seleccionar_color(x, y, color_selec, color_perso, alto_v)
        paint = modificaciones_paint.actualizar_color(x, y, paint, color_selec)
        pintando = True

        # Se hizo clic en el botón Cargar PPM
        if 130 <= x <= 240 and alto_v + 60 <= y <= alto_v + 90:
            paint_ppm, ancho_ppm, alto_ppm = manejo_archivos.cargar_imagen_ppm(TAMAÑO_CELDA)
            if paint_ppm is not None:
                paint = paint_ppm
                alto_v = alto_ppm
                ancho_v = ancho_ppm
                gamelib.resize(ancho_v + MARGEN * 2, alto_v + 100)
                pintando = False
            else:
                paint_mostrar(paint, color_selec, color_perso, ancho_v, alto_v)
                        
        # Se hizo clic en el botón Guardar PPM    
        if 10 <= x <= 120 and alto_v + 60 <= y <= alto_v + 90:
            manejo_archivos.guardar_imagen_ppm(paint)
            pintando = False

        # Se hizo clic en el botón Guardar PNG
        if 250 <= x <= 360 and alto_v + 60 <= y <= alto_v + 90:
            manejo_archivos.guardar_imagen_png(paint)
            pintando = False

    return color_selec, color_perso, paint, pintando, ancho_v, alto_v

def main():
    gamelib.title("AlgoPaint by Luna")
    dimensiones = obtener_dimensiones() 
    
    if dimensiones is None:
        return  

    filas, columnas, ancho_v, alto_v = dimensiones
    gamelib.resize(ancho_v + MARGEN * 2, alto_v + 100)
    
    pintando = False
    color_selec = "#2aa8f2"          # Almacena el color del botón seleccionado (cualquiera de los 6 colores fijos)
    color_perso = "#ffffff"          # Almacena el color perso ingresado por el usuario al hacer clic en el botón "Personalizado"                   
    
    paint = paint_nuevo(filas, columnas)
    inicio = paint_nuevo(filas, columnas)
    
    estados_grilla = pila.Pila()
    movimientos_descartados = pila.Pila()
    
    estados_grilla.apilar(paint)
    movimientos_descartados.apilar(paint)
    
    while gamelib.loop(fps=15):
        paint_mostrar(paint, color_selec, color_perso, ancho_v, alto_v)
        modificaciones_paint.pintar_celda(paint)

        for ev in gamelib.get_events():
            if ev.type == gamelib.EventType.ButtonPress and ev.mouse_button == 1:
                x, y = ev.x, ev.y
                campos = manejar_clic_boton(ev, color_selec, color_perso, paint, ancho_v, alto_v)
                color_selec, color_perso, paint, pintando, ancho_v, alto_v = campos
                              
            if ev.type == gamelib.EventType.ButtonRelease and ev.mouse_button == 1:    
                pintando = False     
                
            if pintando:
                x, y = ev.x, ev.y
                modificaciones_paint.actualizar_movimientos(estados_grilla, x, y, paint, modificaciones_paint.actualizar_color, color_selec)
               
            if ev.type == gamelib.EventType.KeyPress and ev.key == 'z':
                paint = modificaciones_paint.deshacer(estados_grilla, movimientos_descartados, inicio)
            
            if ev.type == gamelib.EventType.KeyPress and ev.key == 'y':
                paint = modificaciones_paint.rehacer(estados_grilla, movimientos_descartados, inicio)
                
            if ev.type == gamelib.EventType.KeyPress and ev.key == 'b':
                x, y = ev.x, ev.y  
                modificaciones_paint.actualizar_movimientos(estados_grilla, x, y, paint, modificaciones_paint.balde_pintura, color_selec)
                 
            elif ev.type == gamelib.EventType.KeyPress and ev.key == 'Escape':
                return
                
gamelib.init(main)