import requests
import pygame
import pygame_gui
import threading
import sys

#Settings & Globals
timeout = 1 #(seconds)
ip_address = "192.168.20.38"

FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#### FUNCTIONS ####

def call_action(action='stop'):
        try:
            response = requests.get('http://'+ip_address+'/action='+action,
                    timeout=timeout)
            print("Succeded")
            print(response.elapsed.total_seconds() * 1000 + " ms") 
        except (requests.exceptions.ReadTimeout,
                requests.exceptions.ConnectTimeout):
            print("Timed out!")
        except:
            print("Error!", sys.exc_info()[0])

def ping_connection():
    print("")

def close():
    call_action('stop')
    quit()

def connect(new_ip):
    global ip_address
    ip_address = new_ip

######### MAIN ########

pygame.init()
pygame.display.set_caption('Rover Control')

screen = pygame.display.set_mode((720, 480))
clock = pygame.time.Clock()

######## GUI ##############
manager = pygame_gui.UIManager((800, 600))

rect = pygame.Rect((344, 224), (32, 32))
image = pygame.Surface((32, 32))
image.fill(WHITE)

hello_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((220, 25), (100, 30)),
        text='Connect', manager=manager)

address_box = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(
        relative_rect=pygame.Rect((50, 25), (150, 30)), manager= manager)

####### RUNNING CYCLE #######

while True:
    clock.tick(FPS)
    time_delta = clock.tick(60)/1000.0
    
    #Event mannaging
    for event in pygame.event.get():
        #Blocking Events
        if event.type == pygame.QUIT:
            close()
        elif event.type == pygame.KEYDOWN:
            action="stop"
            rect.x = 344
            rect.y = 224
            if event.key == pygame.K_UP:
                rect.y -= 32
                threading.Thread(name='action_daemon', target=call_action, 
                        daemon=True, args=('forward',)).start()
            elif event.key == pygame.K_DOWN:
                rect.y += 32               
                threading.Thread(name='action_daemon', target=call_action, 
                        daemon=True, args=('backward',)).start()
            elif event.key == pygame.K_LEFT:
                rect.x -= 32
                threading.Thread(name='action_daemon', target=call_action, 
                        daemon=True, args=('left',)).start()
            elif event.key == pygame.K_RIGHT:
                rect.x += 32
                threading.Thread(name='action_daemon', target=call_action, 
                        daemon=True, args=('right',)).start()
            elif event.key == pygame.K_ESCAPE:
                close()
        elif event.type == pygame.KEYUP:
            rect.x = 344
            rect.y = 224
            if event.key in [pygame.K_UP,pygame.K_DOWN,pygame.K_LEFT,pygame.K_RIGHT]:
                threading.Thread(name='action_daemon', target=call_action, 
                    daemon=True, args=('stop',)).start()
        #Independent Events
        if event.type == pygame.USEREVENT:
             if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                 if event.ui_element == hello_button:
                    connect(address_box.get_text()) 
        manager.process_events(event)

    manager.update(time_delta)
    screen.fill(BLACK)
    screen.blit(image, rect)
    manager.draw_ui(screen)

    pygame.display.update()
