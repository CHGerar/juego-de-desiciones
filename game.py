import pygame
import sys
import os

# Inicializar Pygame
pygame.init()

#Configuración de pantalla y colores
ANCHO = 800
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Esacape de la cueva")

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (200, 50, 50)
VERDE = (50, 200, 50)

# Fuentes
fuente_dialogo = pygame.font.Font(None, 28)
fuente_titulo = pygame.font.Font(None, 48)

# Carpeta base
carpeta_base = os.path.dirname(__file__)

# Función para cargar imágenes de manera segura
def cargar_imagen_segura(ruta, ancho, alto):
    try:
        img = pygame.image.load(ruta).convert_alpha()
        return pygame.transform.scale(img, (ancho, alto))
    except Exception as e:
        print(f"Error al cargar {ruta}: {e}")
        superficie = pygame.Surface((ancho, alto))
        superficie.fill(NEGRO)
        return superficie

#Cargar imágenes principales
ruta_inicio = os.path.join(carpeta_base, "imagenes", "inicio.bmp")
ruta_personaje = os.path.join(carpeta_base, "imagenes", "personaje.bmp")
imagen_instrucciones = cargar_imagen_segura(ruta_inicio, ANCHO, ALTO)
personaje_img = cargar_imagen_segura(ruta_personaje, 80, 80)

# Rutas de imágenes para preguntas
imagenes_rutas = [
    os.path.join(carpeta_base, "imagenes", "animal.bmp"),
    os.path.join(carpeta_base, "imagenes", "pasillo.bmp"),
    os.path.join(carpeta_base, "imagenes", "gemas.bmp"),
    os.path.join(carpeta_base, "imagenes", "murcielago.bmp"),
    os.path.join(carpeta_base, "imagenes", "charco.bmp")
]

# Cargar imágenes de preguntas
imagenes_preguntas = [cargar_imagen_segura(ruta, ANCHO, ALTO) for ruta in imagenes_rutas]

# Variables y estados del juego
estado_juego = "instrucciones"
contador_opcion2 = 0
indice_pregunta = 0
MAX_PREGUNTAS = 5

personaje_x = ANCHO // 2
personaje_y = ALTO // 2
velocidad = 5

# Preguntas y respuestas
preguntas = [
    "Acabas de encontrar un animal herido dentro de la cueva. ¿Qué haces?\n1- Vendas su herida.\n2- Lo dejas.",
    "Encuentras un pasaje oscuro y escuchas ruidos extraños.\n1- Decides regresa por otro camino.\n2- Avanzas en silencio.",
    "Ves unas gemas brillantes, pero están cerca de un precipicio.\n1- Te arriesgas a tomarlas.\n2- Decides que es demasiado peligroso.",
    "Un murciélago vuela hacia ti de repente.\n1- Te agachas para evitarlo.\n2- Intentas golpearlo con tu mano.",
    "Te topas con un charco profundo de agua.\n1- Intentas cruzar nadando .\n2- Buscas una piedra para saltar."
]

respuestas_opcion1 = [
    "Cuidas al animal y te sigue agradecido. ¡Continúas tu aventura!",
    "Avanzas y descubres una gema en el suelo.",
    "Logras tomar las gemas sin caer. ¡Qué valiente!",
    "Te agachas y el murcielago pasa de largo.",
    "Cruzas el charco con éxito, ¡el agua estaba fría!"
]

respuestas_opcion2 = [
    "El animal queda atrás, pero avanzas rápido. ¡Continúas tu aventura!",
    "Regresas y evitas un peligro desconocido. ¡Parece que fue la decisión correcta!",
    "Decides no arriesgarte y sigues vivo. A veces, la prudencia es la mejor opción.",
    "Intentas golpearlo y te muerde. ¡Mala elección!",
    "Encuentras una piedra y saltas fácilmente. ¡Bien hecho!"
]

# Funciones de dibujado
def dibujar_dialogo(texto):
    caja_h = 160
    caja = pygame.Surface((ANCHO - 20, caja_h), pygame.SRCALPHA)
    caja.fill((10, 10, 10, 200))
    pantalla.blit(caja, (10, ALTO - caja_h - 10))
    lineas = texto.split('\n')
    y_offset = 0
    for linea in lineas:
        render_texto = fuente_dialogo.render(linea, True, BLANCO)
        pantalla.blit(render_texto, (40, ALTO - caja_h - 10 + y_offset))
        y_offset += 28

def dibujar_final(mensaje, color):
    pantalla.fill(NEGRO)
    titulo = fuente_titulo.render("FIN DEL JUEGO", True, color)
    texto_final = fuente_dialogo.render(mensaje, True, BLANCO)
    texto_reiniciar = fuente_dialogo.render("Presiona R para reiniciar", True, BLANCO)
    pantalla.blit
    pantalla.blit(titulo, (ANCHO//2 - titulo.get_width()//2, ALTO//2 - 80))
    pantalla.blit(texto_final, (ANCHO//2 - texto_final.get_width()//2, ALTO//2 + 20))
    pantalla.blit(texto_reiniciar, (ANCHO//2 - texto_reiniciar.get_width()//2, ALTO - 50))

# Bucle principal
clock = pygame.time.Clock()

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Cambios de estado
        if estado_juego == "instrucciones":
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                estado_juego = "jugando"

        elif estado_juego == "jugando":
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                if indice_pregunta < MAX_PREGUNTAS:
                    estado_juego = "decision"
                else:
                    estado_juego = "final"

        elif estado_juego == "decision":
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1:
                    estado_juego = "jugando"
                    indice_pregunta += 1
                elif evento.key == pygame.K_2:
                    contador_opcion2 += 1
                    estado_juego = "jugando"
                    indice_pregunta += 1

        elif estado_juego == "final":
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_r:
                estado_juego = "instrucciones"
                contador_opcion2 = 0
                indice_pregunta = 0
                personaje_x = ANCHO // 2
                personaje_y = ALTO // 2

    # Movimiento del personaje
    if estado_juego in ("jugando", "decision"):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]: personaje_x -= velocidad
        if teclas[pygame.K_RIGHT]: personaje_x += velocidad
        if teclas[pygame.K_UP]: personaje_y -= velocidad
        if teclas[pygame.K_DOWN]: personaje_y += velocidad

        personaje_x = max(0, min(personaje_x, ANCHO - personaje_img.get_width()))
        personaje_y = max(0, min(personaje_y, ALTO - personaje_img.get_height()))

    # Dibujado
    if estado_juego == "instrucciones":
        pantalla.blit(imagen_instrucciones, (0, 0))
        titulo = fuente_titulo.render("ESCAPE DE LA CUEVA", True, BLANCO)
        instrucciones = fuente_dialogo.render("Presiona ESPACIO para comenzar", True, BLANCO)
        pantalla.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 50))
        pantalla.blit(instrucciones, (ANCHO//2 - instrucciones.get_width()//2, ALTO - 50))

    elif estado_juego == "jugando":
        pantalla.fill(NEGRO)
        pantalla.blit(personaje_img, (personaje_x, personaje_y))

        if indice_pregunta == 0:
            dibujar_dialogo("Bienvenido a la cueva. Usa las flechas para moverte.\nPresiona ESPACIO para avanzar en la historia.")
        elif indice_pregunta < MAX_PREGUNTAS:
            dibujar_dialogo(f"Presiona ESPACIO para la siguiente pregunta. Preguntas restantes: {MAX_PREGUNTAS - indice_pregunta}")
        else:
            dibujar_dialogo("¡Has llegado al final de la cueva!\nPresiona ESPACIO para finalizar.")

    elif estado_juego == "decision":
        # Se dibuja la imagen de fondo correspondiente a la pregunta
        pantalla.blit(imagenes_preguntas[indice_pregunta], (0, 0))
        pantalla.blit(personaje_img, (personaje_x, personaje_y))

        if indice_pregunta < len(preguntas):
            dibujar_dialogo(preguntas[indice_pregunta])

        # --- AÑADIDO: mostrar gema solo en la pregunta de las gemas ---
        if indice_pregunta == 2:  # La tercera pregunta
            ruta_gema = os.path.join(carpeta_base, "imagenes", "gemas.png")
            gema_img = cargar_imagen_segura(ruta_gema, 60, 60)
            pantalla.blit(gema_img, (ANCHO//2 + 150, ALTO//2))  # Ajusta posición si quieres

    elif estado_juego == "final":
        if contador_opcion2 >= 3:
            mensaje = f"Perdiste. Elegiste la opción 2 un total de {contador_opcion2}veces."
            dibujar_final(mensaje, ROJO)
        else:
            mensaje = "¡Felicidades! Lograste salir de la cueva sano y salvo."
            dibujar_final(mensaje, VERDE)

    pygame.display.flip()
    clock.tick(60)
