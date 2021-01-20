import requests
import pygame
import pygame_gui
import threading
import sys

#Settings, Globals & CONSTANTS
timeout = 1 #(seconds)
ip_address = "192.168.20.38"
html_log = "System Started!<br>"
status = False
ping = 0;

FPS = 60
BACKGROUND = (33, 40, 45)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 125, 0)
RED = (125, 0, 0)

#### FUNCTIONS ####

def call_action(action='stop'):
        global html_log,status,ping
        try:
            response = requests.get('http://'+ip_address+'/action='+action,
                    timeout=timeout)
            print("Succeded")
            res_time = response.elapsed.total_seconds() * 1000
            ping = int(res_time)
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
    global html_log,status,ping
    try:
        response = requests.get('http://'+ip_address+'/action=ping',
                    timeout=timeout)
        res_time = response.elapsed.total_seconds() * 1000
        ping = int(res_time)
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



### DRAW FUNCTIONS ###
def draw_status(status,pos):
    if status:
        pygame.draw.circle(screen, GREEN, pos, 10)
    else:
        pygame.draw.circle(screen, RED, pos, 10)

def draw_ping(label):
    label.set_text("Ping: " + str(ping) + "/1000")

######### MAIN ########

connect(ip_address);
pygame.init()
pygame.display.set_caption('Rover Control')

screen = pygame.display.set_mode((720, 480))
clock = pygame.time.Clock()

######## GUI ##############
manager = pygame_gui.UIManager((720, 480))

#Rover Address Box
address_box = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(
        relative_rect=pygame.Rect((20, 20), (200, 30)), manager= manager)
address_box.set_allowed_characters(['.','0','1','2','3','4','5','6','7','8','9'])
address_box.set_text(ip_address)
address_box.set_text_length_limit(15)

#Connect button
rover_connect_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((240, 20), (80, 30)),
        text='Connect', manager=manager)

#General labels
pygame_gui.elements.ui_label.UILabel( 
        relative_rect=pygame.Rect((20, 60), (100, 30)),text='Timeout (ms)', manager=manager)
pygame_gui.elements.ui_label.UILabel( 
        relative_rect=pygame.Rect((20, 100), (100, 30)),text='Turn Speed  ', manager=manager)

#Ping label
ping_label = pygame_gui.elements.ui_label.UILabel( 
        relative_rect=pygame.Rect((220, 60), (140, 30)),text='Ping: 0/0', manager=manager)

#Timeout selector
timeout_selector = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(
        options_list=['0.5','0.7','0.9','1','1.2','1.5','2'],starting_option='1',
        relative_rect=pygame.Rect((140, 60), (60, 30)), manager=manager)

#Turn speed selector
turn_speed_selector = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(
        options_list=['200','100','50','20','10'],starting_option='100',
        relative_rect=pygame.Rect((120, 100), (60, 30)), manager=manager)
#log box
def create_log_box(manager):
    return pygame_gui.elements.ui_text_box.UITextBox(html_text=html_log,
        relative_rect=pygame.Rect((20, 140), (320, 320)), manager=manager)
log_box = create_log_box(manager)

#Camera image
camera_rectangle = pygame.Rect((370,20),(320,240)) 
camera_image = pygame.image.load(r'./data/nosignal.jpg')

#Direction Square
rect = pygame.Rect((444, 410), (32, 32))
image = pygame.Surface((32, 32))
image.fill(WHITE)

#Camera Address Box
camera_box = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(
        relative_rect=pygame.Rect((370, 280), (200, 30)), manager= manager)
camera_box.set_allowed_characters(['.','0','1','2','3','4','5','6','7','8','9'])
camera_box.set_text(ip_address)
camera_box.set_text_length_limit(15)

#Connect button
camera_connect_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((580, 280), (80, 30)),
        text='Connect', manager=manager)





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
            rect.y = 410
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
            rect.y = 410
            if event.key in [pygame.K_UP,pygame.K_DOWN,pygame.K_LEFT,pygame.K_RIGHT] and status:
                threading.Thread(name='action_daemon', target=call_action, 
                    daemon=True, args=('stop',)).start()
        #Independent Events
        if event.type == pygame.USEREVENT:
             if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                 if event.ui_element == rover_connect_button:
                    connect(address_box.get_text()) 
             if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                 if event.ui_element == timeout_selector:
                    timeout = float(event.text)
        manager.process_events(event)
    
    ## Re create log box
    log_box.kill()
    log_box = create_log_box(manager)

    ## Main Cycle Calls
    manager.update(time_delta)
    screen.fill(BACKGROUND)
    screen.blit(image, rect)
    screen.blit(camera_image, camera_rectangle)
    manager.draw_ui(screen)
    ## Draw Functions
    draw_status(status,(340,35))
    draw_status(status,(680,295))
    draw_ping(ping_label)

    pygame.display.update()
