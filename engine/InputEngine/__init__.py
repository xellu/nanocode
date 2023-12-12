import time
import curses
import keyboard
import threading
from engine.InputEngine import Shortcuts

class InputEngine:
    def __init__(self, delay_ms = 100, engine = None):
        self.delay = delay_ms / 1000
        self.engine = engine

    def start(self):
        if not self.engine: raise Exception("No base engine provided to InputEngine")
        threading.Thread(target=self.control_loop).start()
        curses.wrapper(self.loop)        
    
    def loop(self, sc):
        
        while True: 
            key = sc.getch()

            block = []
            for c in self.engine.components: #send an input to the components
                block.append(c.handle_input(key))
       
            if not (True in block):
                self.engine.page.handle_input(key) #send an input to the page
    
            
                
            if self.delay > 0:
                time.sleep(self.delay)
            
    def control_loop(self):
        shortcut = Shortcuts.Shortcuts()
        while True:
            key = keyboard.read_key()
            shortcut.process(key, keyboard.is_pressed("ctrl"), keyboard.is_pressed("shift")) #send an input to ctrl shortcuts
            time.sleep(0.05)