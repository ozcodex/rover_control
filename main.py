import requests
import pygame

def call_action(action='stop'):
        try:
            response = requests.get('http://192.168.20.38/action='+action, timeout=1)
            print("Success!")
        except:
            print("Error!")


def close():
    call_action('stop')
    quit()

pygame.init()
pygame.display.set_caption('Rover Control')

screen = pygame.display.set_mode((720, 480))
clock = pygame.time.Clock()
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

rect = pygame.Rect((344, 224), (32, 32))
image = pygame.Surface((32, 32))
image.fill(WHITE)

while True:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            close()
        elif event.type == pygame.KEYDOWN:
            rect.x = 344
            rect.y = 224
            if event.key == pygame.K_UP:
                rect.y -= 16
                call_action('forward')
            elif event.key == pygame.K_DOWN:
                rect.y += 16
                call_action('backward')
            elif event.key == pygame.K_LEFT:
                rect.x -= 16
                call_action('left')
            elif event.key == pygame.K_RIGHT:
                rect.x += 16
                call_action('right')
            elif event.key == pygame.K_ESCAPE:
                close()
        elif event.type == pygame.KEYUP:
            call_action('stop')
            rect.x = 344
            rect.y = 224

    screen.fill(BLACK)
    screen.blit(image, rect)
    pygame.display.update()
