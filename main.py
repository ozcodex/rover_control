import requests
import pygame
import pygame_gui
import threading
import sys

#Settings & Globals
timeout = 1 #(seconds)
ip_address = "192.168.20.38"
html_log = "System Started!<br>"
status = False

FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#### FUNCTIONS ####

def call_action(action='stop'):
        global html_log,status
        try:
            response = requests.get('http://'+ip_address+'/action='+action,
                    timeout=timeout)
            print("Succeded")
            res_time = response.elapsed.total_seconds() * 1000
            print(str(res_time) + " ms") 
        except (requests.exceptions.ReadTimeout,
                requests.exceptions.ConnectTimeout):
            status = False
            html_log += "Connection lost!<br>"
        except:
            status = False
            html_log += "Connection lost!<br>"
            print(sys.exc_info())

def ping_connection(log=False):
    global html_log,status
    try:
        response = requests.get('http://'+ip_address+'/action=ping',
                    timeout=timeout)
        res_time = response.elapsed.total_seconds() * 1000
        #TODO: Check ack in response
        status = True
        if(log):
            html_log += "Connected in "+ str(res_time) +" ms<br>"
    except(requests.exceptions.ReadTimeout,
            requests.exceptions.ConnectTimeout):
        status = False
        if(log):
            html_log += "Connection Timed out.<br>"
    except requests.exceptions.InvalidURL:
        status = False
        if(log):
            html_log += "Invalid Address.<br>"
    except:
        status = False
        print(sys.exc_info())
        if(log):
            html_log += "Connection Error.<br>"

        
def close():
    call_action('stop')
    quit()

def connect(new_ip):
    global ip_address, html_log
    ip_address = new_ip
    html_log += "Connecting to '" + new_ip + "'<br>"
    threading.Thread(name='action_daemon', target=ping_connection, daemon=True, args=(True,)).start()

def create_log_box(manager):
    return pygame_gui.elements.ui_text_box.UITextBox(html_text=html_log,
        relative_rect=pygame.Rect((50, 125), (300, 300)), manager=manager)

######### MAIN ########

connect(ip_address);
pygame.init()
pygame.display.set_caption('Rover Control')

screen = pygame.display.set_mode((720, 480))
clock = pygame.time.Clock()

######## GUI ##############
manager = pygame_gui.UIManager((800, 600))

rect = pygame.Rect((444, 224), (32, 32))
image = pygame.Surface((32, 32))
image.fill(WHITE)

hello_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((220, 25), (100, 30)),
        text='Connect', manager=manager)

address_box = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(
        relative_rect=pygame.Rect((50, 25), (150, 30)), manager= manager)
address_box.set_allowed_characters(['.','0','1','2','3','4','5','6','7','8','9'])
address_box.set_text(ip_address)
address_box.set_text_length_limit(15)

log_box = create_log_box(manager)

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
            rect.x = 444
            rect.y = 224
            if status:
                #Only Move if is connected
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
            rect.x = 444
            rect.y = 224
            if event.key in [pygame.K_UP,pygame.K_DOWN,pygame.K_LEFT,pygame.K_RIGHT] and status:
                threading.Thread(name='action_daemon', target=call_action, 
                    daemon=True, args=('stop',)).start()
        #Independent Events
        if event.type == pygame.USEREVENT:
             if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                 if event.ui_element == hello_button:
                    connect(address_box.get_text()) 
        manager.process_events(event)
    
    ## Re create log box
    log_box.kill()
    log_box = create_log_box(manager)

    ## Main Cycle Calls
    manager.update(time_delta)
    screen.fill(BLACK)
    screen.blit(image, rect)
    manager.draw_ui(screen)

    pygame.display.update()
