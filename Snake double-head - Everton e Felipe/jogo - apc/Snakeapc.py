import pygame, random
from pygame.locals import *

# Posição aleatoria dentro do grid
def on_grid_random():
    x = random.randint(0,590)
    y = random.randint(0,590)
    return (x//10*10,y//10*10) # como a divisão é inteira, ela vai 
                               # dá sempre multiplos de 10, ou seja, a posição
                               # vai ser aleatoria mas estará sempre no grid
                               # como será multiplos de 10, vai ficar tudo alinhado

def colisão(c1,c2):
    return (c1[0] == c2[0]) and (c1[1] == c2[1]) 

# Posições #
UP = 0 
RIGHT = 1 
DOWN = 2
LEFT = 3


pygame.init()


# Janela do game #
screen = pygame.display.set_mode((600, 600)) # Objeto de tela
pygame.display.set_caption('Snake Double-head')


# Cobra #
snake = [(200, 200), (210, 200), (220, 200)] # A cobra é uma lista de segmentos, 
skin_da_snake = pygame.Surface((10,10))      # entao cada segmento vai ser uma tupla, 
skin_da_snake.fill((0, 255, 0))              # ou seja, uma lista de tuplas
                                             # Surface cria uma surperficie, so que passamos a altura e a largura na tupla
                                             # Fill preenche a superficie com uma cor em rbg

# Maçã #
posiçao_da_maça = on_grid_random() # Se colocar mais que 590 a maça vai sair da tela
apple = pygame.Surface((10,10))                                  # pois a cobra tem o tamanho de 10/10
apple.fill((255, 0, 0))


direção = LEFT
clock = pygame.time.Clock() # Limita o fps, pra um tempo determinado, se tirar isso a cobra vai ficar muito rapida


font = pygame.font.Font('freesansbold.ttf', 18)
score = 0

# Loop principal #
game_over = False
while not game_over:

    clock.tick(30)
    

    for event in pygame.event.get(): # Esse é o evento de fechar o jogo
        if event.type == QUIT:  # quando o evento for do tipo quit, vai fechar o jogo
            pygame.quit()

        # Controlar cobra
        if event.type == KEYDOWN: #  Este evento é disparado sempre que uma tecla é pressionada
            if event.key == K_UP:
                direção = UP
            if event.key == K_DOWN:
                direção = DOWN
            if event.key == K_RIGHT:
                direção = RIGHT
            if event.key == K_LEFT:
                direção = LEFT
    
    # Colisão da cobra na maça
    if colisão(snake[0], posiçao_da_maça):
        posiçao_da_maça = on_grid_random()                      # se a cobra colide com a maça, ela come a maça, entao eu randomizo um novo local pra maça nascer
        snake.append((0,0))
        musica= pygame.mixer.music.load('Barulho de Cobra.mp3')
        pygame.mixer.music.play()                               # o paramentro -1 faz com que quando a musica acabe ela recomece
        score+=1


    # Verificando se  a cobra colide com a parede
    if snake[0][0] == 600 or snake[0][1] == 600 or snake[0][0] < 0 or snake[0][1] < 0:
        game_over = True
        break
    
    if game_over:

        break

    # Toda posição do corpo da cobra vai ocupar a posiçao que o corpo da frente tava ocupando antes
    for i in range(len(snake)-1, 0, -1):         # Comprimento da cobra, vai ate 0, e o -1 serve pra ir ao contrario, inves de incrementar ele decrementa
        snake[i]=(snake[i-1][0], snake[i-1][1]) # subtrai 1 de i porque preciso da posiçao anterior pra definir a posterior 



    # Movimento #
    if direção == UP:
        snake[0] = (snake[0][0], snake[0][1] - 10) # Quando a cobra vai pra cima o Y diminui 10
                         # x          # y
    if direção ==  DOWN:
        snake[0] = (snake[0][0], snake[0][1] + 10) # Quando a cobra vai pra baixo o Y aumenta 10
    if direção == RIGHT:
        snake[0] = (snake[0][0] + 10, snake[0][1]) # Quando a cobra vai pra esquerda o X aumenta 10
    if direção == LEFT:
        snake[0] = (snake[0][0] - 10, snake[0][1]) # Quando a cobra vai pra direita o X diminui 10


    screen.fill((0,0,0)) # limpa a tela
    screen.blit(apple, posiçao_da_maça)

    for x in range(0, 600, 10): # Desenha linhas verticais no eixo x
        pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, 600))
    for y in range(0, 600, 10): # Desenha linhas verticais no eixo y
        pygame.draw.line(screen, (40, 40, 40), (0, y), (600, y))


    score_font = font.render(f'Score: {score}', True, (0, 255, 0))
    score_rect = score_font.get_rect()
    score_rect.topleft = (600 - 120, 10)
    screen.blit(score_font, score_rect)

    for pos in snake:
        screen.blit(skin_da_snake, pos) # plota desenho e posição da cobra

    pygame.display.update()

while True:
    game_over_font = pygame.font.Font('freesansbold.ttf', 75)
    game_over_screen = game_over_font.render('Game Over', True, (255, 0, 0))
    game_over_rect = game_over_screen.get_rect()
    game_over_rect.midtop = (600 / 2, 10)
    screen.blit(game_over_screen, game_over_rect)
    pygame.display.update()
    pygame.time.wait(500)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()