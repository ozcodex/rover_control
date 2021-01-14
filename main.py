import requests
import pygame
import threading
import sys

def call_action(action='stop'):
        try:
            response = requests.get('http://192.168.20.38/action='+action, timeout=1)
            print("Succeded")
            print(response.elapsed.total_seconds() * 1000)
        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout):
            print("Timed out!")
        except:
            print("Error!", sys.exc_info()[0])

def ping_connection():
    print("")

def close():
    call_action('stop')
    quit()

######### MAIN ########

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
            action="stop"
            rect.x = 344
            rect.y = 224
            if event.key == pygame.K_UP:
                rect.y -= 32
                threading.Thread(name='action_daemon', target=call_action, daemon=True, args=('forward',)).start()
            elif event.key == pygame.K_DOWN:
                rect.y += 32               
                threading.Thread(name='action_daemon', target=call_action, daemon=True, args=('backward',)).start()
            elif event.key == pygame.K_LEFT:
                rect.x -= 32
                threading.Thread(name='action_daemon', target=call_action, daemon=True, args=('left',)).start()
            elif event.key == pygame.K_RIGHT:
                rect.x += 32
                threading.Thread(name='action_daemon', target=call_action, daemon=True, args=('right',)).start()
            elif event.key == pygame.K_ESCAPE:
                close()
        elif event.type == pygame.KEYUP:
            rect.x = 344
            rect.y = 224
            threading.Thread(name='action_daemon', target=call_action, daemon=True, args=('stop',)).start()

    screen.fill(BLACK)
    screen.blit(image, rect)
    pygame.display.update()
