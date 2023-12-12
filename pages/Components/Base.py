from pages import Utils
import curses

class MenuBase:
    def __init__(self):
        self.id = "base"
        self.show = False
        
    def render(self, sc):
        sc.addstr(Utils.centerY(),Utils.centerX(self.id), self.id, curses.A_REVERSE)
        
    def handle_input(self, key):
        pass
    
    def open(self):
        self.show = True
    
    def close(self):
        self.show = False
    
    