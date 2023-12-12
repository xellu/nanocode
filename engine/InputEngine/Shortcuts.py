from dataforge.database import Item
from engine import Actions
import curses

class Shortcuts:
    def __init__(self):
        self.actions = [
            Item(desc="Exit program on CTRL+Q", shift=False, keys=["q", "Q"], func=Actions.quit),
            Item(desc="Open theme menu on CTRL+T", shift=False, keys=["t", "T"], func=Actions.theme_menu),
        
        ]
        

    def process(self, key, shift:bool):
        # Check if Ctrl key is pressed

        for action in self.actions:
            if key in action.keys and shift == action.shift: 
                action.func()
                print("Executed Ctrl shortcut")
                return
