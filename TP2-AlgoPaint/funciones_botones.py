import gamelib
import png

BOTONES_COLORES = {
    "Personalizado": [10, 40, '#ffffff'],     # Solo están las coordenadas para "x1" y "x2" ya que "y1" e "y2"  
    "Violeta": [50, 80, '#9c4f96'],         # son las mismas para todos los botones del diccionario
    "Rojo": [90, 120, '#ff6355'],
    "Naranja": [130, 160, '#fba949'],
    "Amarillo": [170, 200, '#fae442'],
    "Verde": [210, 240, '#8bd448'],
    "Celeste": [250, 280, '#2aa8f2']
}

BOTONES_IMAGENES = {
    "Guardar_PPM": [(10, 120),("Guardar PPM", 65)],
    "Cargar_PPM": [(130, 240),("Cargar PPM", 185)],
    "Guardar_PNG": [(250, 360),("Guardar PNG", 305)]
}

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

def decimal_a_hexadecimal(decimal:list, max_valor:int) -> list:
    '''Convierte una lista de listas de enteros que representan colores en
    formato decimal a su representación hexadecimal.
    
    Retorna:
        Una lista de listas donde cada sublista representa una fila de la
        grilla, y cada elemento de estas sublistas una celda.
    
    Ejemplo:
        >>> decimal_a_hexadecimal([[(255,0,0), (170,85,0), (85,170,0), (0,255,0)],
                                   [(170,0,85), (141,85,85), (113,170,85), (85,255,85)]], 255)
                
        [['#ff0000', '#550000', '#55aa00', '#00ff00'],
         ['#aa0055', '#8d5555', '#71aa55', '#55ff55']]
    '''
    grilla_hexa = []

    for fila in decimal:
        fila_hexa = []
        for color in fila:
            r, g, b = color
            color_hexa = "#"
            if 0 <= r <= max_valor:
                color_hexa += f'{r:02x}'
            if 0 <= g <= max_valor:
                color_hexa += f'{g:02x}'
            if 0 <= b <= max_valor:
                color_hexa += f'{b:02x}'
            fila_hexa.append(color_hexa)
        grilla_hexa.append(fila_hexa)

    return grilla_hexa

def hexadecimal_a_decimal(hexa:list) -> list:
    '''Convierte una lista de listas de strings que representan colores en
    formato hexadecimal a su representación decimal (r,g,b). Si se encuentra
    un str vacío, se elige el color blanco (255,255,255) para representarlo.
    
    Retorna:
        Una lista de listas donde cada sublista representa una fila de la
        grilla, y cada elemento de estas sublistas una celda.
    
    Ejemplo:
        >>> hexadecimal_a_decimal([['#ff0000', '#550000', '#55aa00', '#00ff00'],
                                   ['', '#8d5555', '', '#55ff55']])
                
        [[(255,0,0), (85,0,0), (85,170,0), (0,255,0)],
         [(255,255,255), (141,85,85), (255,255,255), (85,255,85)]]
    '''
    grilla_dec = []
    
    for fila in hexa:
        fila_dec = []
        for color in fila:
            if color == "":
                fila_dec.append((255,255,255))
            else:
                r = (int(color[1:3], 16))
                g = (int(color[3:5], 16))
                b = (int(color[5:7], 16))
                rgb = (r, g, b)
                fila_dec.append(rgb)
        grilla_dec.append(fila_dec)
        
    return grilla_dec

def verificar_formato(ruta:str, formato:str) -> bool:
    '''Si la ruta contiene una extensión, se verifica que este sea el solicitado.

    Retorna:
        True si la ruta tiene la extensión del formato válido o si el usuario
        no ingresó una extensión. False si la ruta tiene una extensión diferente
        al formato que se solicita.'''
    
    if "." in ruta:
        ruta, extension = ruta.split(".")
        if extension == formato:
            return True
        return False
    return True

def inicializar_imagen_ppm(ruta_entrada:str) -> tuple:
    '''Dado un archivo PPM con información de una imagen, carga todos los datos
    necesarios en la memoria para su posterior uso.
    
    Nota: La estructura de datos elegida para procesar los archivos PPM es en
    forma de matriz, es decir, se toma cada línea del archivo PPM como si
    representara una fila de la grilla.'''
    
    try:
        with open(ruta_entrada, 'r') as archivo:
            lineas = archivo.readlines()
            ancho, alto = lineas[1].split()
            int_max = int(lineas[2])
                
            grilla_dec = []
                
            for linea in lineas[3:]:
                linea = linea.rstrip('\n')
                numeros = linea.split()
                linea_dec = []
                for i in range(0,len(numeros),3):
                    r, g, b = map(int, numeros[i:i+3])
                    linea_dec.append((r, g, b))
                grilla_dec.append(linea_dec)
                    
            grilla_hexa = decimal_a_hexadecimal(grilla_dec, int_max)
            
    except FileNotFoundError:
        gamelib.say(f"El archivo '{ruta_entrada}' no existe")
        return None, 0, 0
    
    except IndexError:
        gamelib.say(f"El archivo '{ruta_entrada}' está corrupto o intentas acceder a una posición que no existe")
        return None, 0, 0
            
    return grilla_hexa, ancho, alto   

def cargar_imagen_ppm(tamaño_c:int) -> tuple: 
    '''Carga los datos de una imagen desde un archivo PPM ingresado por el usuario
    y devuelve su representación en forma de grilla de colores, junto con su ancho
    y alto correspondientes.'''
    
    ruta = gamelib.input("Ingrese la ruta de su archivo PPM: ")
    
    if ruta == None:
        return None, 0, 0
    
    while not verificar_formato(ruta, "ppm"):
        gamelib.say("Se ingresó un formato inválido. Acordate de usar la extensión '.ppm' e intenta de vuelta.")
        ruta = gamelib.input("Ingrese la ruta de su archivo PPM: ")
        
        if ruta == None:
            return None, 0, 0
        
    if not ruta.endswith("." + "ppm"):
        ruta += "." + "ppm"
       
    campos = inicializar_imagen_ppm(ruta)
    paint = campos[0]
    columnas = int(campos[1])
    filas = int(campos[2])
    ancho_v = columnas * tamaño_c
    alto_v = filas * tamaño_c

    return paint, ancho_v, alto_v

def guardar_imagen_ppm(paint):
    '''Guarda la imagen en un archivo especificado por el usuario con formato
    PPM. Si el archivo no existe, se crea uno en el disco. Si ya existe, se
    sobrescribe con la información proporcionada en el parámetro "paint".'''
    
    ruta_salida = gamelib.input("Nombre del archivo: ")
    
    if ruta_salida == None:
        return
    
    while not verificar_formato(ruta_salida, "ppm"):
        gamelib.say("Se ingresó un formato inválido. Por favor, usá la extensión '.ppm' e intenta de vuelta")
        ruta_salida = gamelib.input("Nombre del archivo: ")

        if ruta_salida == None:
            return
        
    if not ruta_salida.endswith("." + "ppm"):
        ruta_salida += "." + "ppm"
    
    ancho = len(paint[0])
    alto = len(paint)
    paint_dec = hexadecimal_a_decimal(paint)
    
    with open(ruta_salida, "w") as salida:
        salida.write(f"P3\n{ancho} {alto}\n255\n")
        
        for fila in paint_dec:
            fila_ppm = ""
            for celda in fila:
                r, g, b = celda
                fila_ppm += f"{r} {g} {b} " 
            salida.write(f"{fila_ppm}\n")
    
    gamelib.say("Imagen guardada exitosamente!")
    
def guardar_imagen_png(paint):
    '''Guarda la imagen en un archivo especificado por el usuario con formato
    PNG con color indexado. Si el archivo no existe, se crea uno en el disco.
    Si ya existe, se sobrescribe con la información proporcionada en el
    parámetro "paint".'''
    
    ruta_salida = gamelib.input("Nombre del archivo: ")
    
    if ruta_salida == None:
        return
    
    while not verificar_formato(ruta_salida, "png"):
        gamelib.say("Se ingresó un formato inválido. Por favor, usá la extensión '.png' e intenta de vuelta")
        ruta_salida = gamelib.input("Nombre del archivo: ")

        if ruta_salida == None:
            return
        
    if not ruta_salida.endswith("." + "png"):
        ruta_salida += "." + "png"
    
    paleta = []
    imagen = []
    grilla_dec = hexadecimal_a_decimal(paint)
    
    for linea in grilla_dec:
        fila = []
        for color in linea:
            if color not in paleta:
                paleta.append(color)
            indice_color = paleta.index(color)
            fila.append(indice_color)
        imagen.append(fila)  
        
    png.escribir(ruta_salida, paleta, imagen)
    gamelib.say("Imagen guardada exitosamente!")