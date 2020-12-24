import requests
import tkinter as tk

pressed_key = 'none';
relesed_key = 'none';

def call_action():
        try:
            response = requests.get('http://192.168.20.38/action=forward', timeout=1)
            print("Success!")
        except:
            print("Error!")

window = tk.Tk()

def key_pressed(event):
    global pressed_key
    if (pressed_key != event.keysym):
        pressed_key = event.keysym
        print(pressed_key)
        if(pressed_key == 'Escape'):
            window.destroy()
    
def key_relesed(event):
    global relesed_key
    if (relesed_key != event.keysym):
        relesed_key = event.keysym
        print("keyRelese:"+ relesed_key)

window.bind("<Key>",key_pressed)
window.bind("<KeyRelease>",key_relesed)

window.mainloop()
