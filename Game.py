import pygame
import random
import sys
from pygame.locals import *

# Inicializar Pygame
pygame.init()

# Definir colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Definir dimensiones de pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Juego de Prueba')

# Definir fuentes
font = pygame.font.Font(None, 36)

# Cargar imagen para los elementos
img_castor = pygame.image.load("CODIGO\Python\Juego\img_castor.png")
img_castor = pygame.transform.scale(img_castor, (50, 50))

# Definir temporizador
clock = pygame.time.Clock()

# Pantalla de introducción
def show_intro():
    intro = True
    timer = 3  # Temporizador de 3 segundos
    btnOmitir = pygame.Rect(600, 500, 150, 50)
    
    while intro:
        screen.fill(WHITE)
        titulo = font.render("Bienvenido al juego!", True, BLACK)
        reglas = font.render("Reglas: Selecciona los castores para ganar puntos!! ", True, BLACK)
        txtTimer = font.render(f"El juego comenzará en: {timer}", True, BLACK)
        txtOmitir = font.render("Omitir", True, WHITE)
        
        screen.blit(titulo, (250, 100))
        screen.blit(reglas, (100, 200))
        screen.blit(txtTimer, (250, 300))
        
        pygame.draw.rect(screen, RED, btnOmitir)
        screen.blit(txtOmitir, (620, 510))
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if btnOmitir.collidepoint(event.pos):
                    intro = False
                    return  # Omitir temporizador si se presiona el botón
        
        pygame.display.update()
        pygame.time.delay(500)
        timer -= 1
        
        if timer < 0:
            intro = False

# Pantalla final con la puntuación y opción de reiniciar
def show_score(score):
    show = True
    btnPlayAgain = pygame.Rect(300, 400, 200, 50)
    
    while show:
        screen.fill(WHITE)
        txtScoreFinal = font.render(f"Tu puntuación: {score}", True, BLACK)
        txtPlayAgain = font.render("Jugar de nuevo", True, WHITE)
        
        screen.blit(txtScoreFinal, (250, 250))
        pygame.draw.rect(screen, GREEN, btnPlayAgain)
        screen.blit(txtPlayAgain, (320, 410))
          
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()  #Función para cerrar Python sin necesidad de un flag
            elif event.type == MOUSEBUTTONDOWN:
                if btnPlayAgain.collidepoint(event.pos):
                    return  # Reiniciar el juego si se presiona el botón

        pygame.display.update()

# Pantalla del juego principal
def game_loop():
    score = 0
    game_time = 15  # Temporizador para la duración del juego
    game_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(game_timer, 1000)
    
    elements = []
    last_element_spawn_time = 0
    
    running = True
    game_active = False
    vidaCastores = 720  # Duración de los castores (segundos x 1000)
    
    while running:
        screen.fill(WHITE)
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                # Comprobar si se hizo clic en algún elemento
                for element in elements[:]:
                    if element['rect'].collidepoint(mouse_pos):
                        score += 1
                        elements.remove(element)
            elif event.type == game_timer:
                game_time -= 1
                if game_time <= 0:
                    running = False  # Termina el juego cuando el temporizador llega a 0

        # Generar nuevos elementos en intervalos entre 1 y 3 segundos
        current_time = pygame.time.get_ticks()
        if current_time - last_element_spawn_time > random.randint(1000, 3000):
            x = random.randint(0, SCREEN_WIDTH - 50)
            y = random.randint(0, SCREEN_HEIGHT - 50)
            rect = img_castor.get_rect(topleft=(x, y))
            elements.append({'rect': rect, 'spawn_time': current_time})
            last_element_spawn_time = current_time

        # Dibujar y actualizar elementos
        for element in elements[:]:
            if current_time - element['spawn_time'] > vidaCastores:
                elements.remove(element)
            else:
                screen.blit(img_castor, element['rect'].topleft)

        # Mostrar puntaje
        score_text = font.render(f"Puntuación: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        
        # Mostrar temporizador
        timer_text = font.render(f"Tiempo: {game_time}s", True, BLACK)
        screen.blit(timer_text, (650, 10))
        
        pygame.display.update()
        clock.tick(60)
    
    show_score(score)  # Mostrar pantalla de puntuación al finalizar el juego

# Programa principal
def main():
    show_intro()  # Pantalla de introducción con temporizador y botón de omitir
    while True:
        game_loop()  # Pantalla del juego
        # Al finalizar el juego, regresa al loop para permitir jugar nuevamente

if __name__ == '__main__':
    main()
