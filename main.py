import pygame
import sys
import random

pygame.init()

FPS=60
font = pygame.font.SysFont('Verdana', 16)

screen_width = 840
screen_height = 620

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("prueba juego pong")
clock = pygame.time.Clock()

#objects definition
ball = pygame.Rect(0,0,30,30)
ball.center = (screen_width/2, screen_height/2)

cpu_block = pygame.Rect(0,0,20,100)
cpu_block.centery = screen_height/2

player_block = pygame.Rect(0,0,20,100)
player_block.midright = (screen_width, screen_height/2)


ball_speed_x = 3
ball_speed_y = 3
player_speed = 0
cpu_speed = 3
cpu_score, player_score = 0, 0

#position = velocity * delta + acceleration * delta * delta * 0.5

#posicion = posicion_inicial + velocidad

def reset_ball():
    global ball_speed_x, ball_speed_y
    ball.x = screen_width/2 - 10
    ball.y = random.randint(10,100)
    ball_speed_x*=random.choice([-1,1])
    ball_speed_y*=random.choice([-1,1])

def animate_ball():
    global ball_speed_x, ball_speed_y
    ball.x+= ball_speed_x
    ball.y+= ball_speed_y 
    if ball.bottom >= screen_height or ball.top <=0:
        ball_speed_y*=-1
    if ball.right >= screen_width:
        point_won("cpu")
    if ball.left <= 0:
        point_won("player")
    if ball.colliderect(player_block) or ball.colliderect(cpu_block):
        ball_speed_x*=-1

def point_won(winner):
    global cpu_score, player_score
    if winner == "cpu":
        cpu_score+=1
    if winner == "player":
        player_score+=1
    reset_ball()

def animate_player_block():
    global player_speed
    player_block.y +=player_speed
    if player_block.top <= 0:
        player_block.top = 0
    if player_block.bottom >= screen_height:
        player_block.bottom = screen_height

def animate_cpu_block():
    global cpu_speed
    cpu_speed += random.randint(-3, 3)  # Ajuste la fuerza de la aleatoriedad
    cpu_speed = max(-5, min(5, cpu_speed))  # Limitar la velocidad máxima
    cpu_block.y+= cpu_speed
    if ball.centery <= cpu_block.centery:
        cpu_speed = -3
    if ball.centery >= cpu_block.centery:
        cpu_speed = 3
    if cpu_block.top <= 0:
        cpu_block.top = 0
    if cpu_block.bottom >= screen_height:
        cpu_block.bottom = screen_height

#game loop
while True:
    dt = clock.tick(FPS) / FPS
    #check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_speed = -6
            if event.key == pygame.K_DOWN:
                player_speed = 6
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                player_speed = 0
            if event.key == pygame.K_DOWN:
                player_speed = 0

    #update 
    #ball.x+=ball_speed_x
    #ball.y+=ball_speed_y
    animate_ball()
    animate_player_block()
    animate_cpu_block()
    


    #pygame.draw.rect(screen, "red", ball)
    screen.fill("black")
    cpu_score_surface = font.render(str(cpu_score),True, "yellow")
    player_score_surface = font.render(str(player_score),True, "green")
    screen.blit(cpu_score_surface,(screen_width/4,20))
    screen.blit(player_score_surface,(3*screen_width/4,20))
    pygame.draw.aaline(screen, "white", (screen_width/2,0),(screen_width/2,screen_height))
    pygame.draw.ellipse(screen, "white", ball)
    pygame.draw.rect(screen, "yellow", cpu_block)
    pygame.draw.rect(screen, "green", player_block)
    #update display
    pygame.display.update()
    