import curses

from pages.Components.Base import MenuBase as Base
from pages.Utils.MenuBox import MenuBox, TextLine
from engine.ThemeEngine import Colors
from engine import Actions, FileManager

class ViewMenu(Base):
    def __init__(self):
        self.id = "view"
        self.show = False
        
        self.selection = 0
        self.options = [
            TextLine("[Enabled ]  Line numbers"),
            TextLine("[Disabled]        Gutter"),
            TextLine("[CTRL+T]          Themes"),
            TextLine("[CTRL+R]          Reload"),
            TextLine("                        "),
            TextLine(f"[ESC]             Close", action=self.close)
        ]
    
    def render(self, sc):
        if not self.show: return
        menu = MenuBox(
            title = "View",
            lines = self.options,
            width=26,
            highlight_index=self.selection
        )
        
        menu.render(sc)
    
    def handle_input(self, key):
        if self.show == False: return
        
        if key == 27: #close menu using escape
            self.close()
        
        if key in [curses.KEY_UP, curses.KEY_LEFT]:
            self.selection -= 1
            if self.selection < 0:
                self.selection = len(self.options) - 1
            
        if key in [curses.KEY_DOWN, curses.KEY_RIGHT]:
            self.selection += 1
            if self.selection > len(self.options) - 1:
                self.selection = 0
                
        if key == 32 or key == 10 or key == 459 or key == 13:
            if self.options[self.selection].action != None:
                self.options[self.selection].action()
        return True
    
    def open(self):
        self.show = True
        
    def close(self):
        self.show = False

class FileMenu(Base):
    def __init__(self):
        self.id = "file"
        self.show = False
        
        self.selection = 0
        self.options = [
            TextLine("[CTRL+N]                   New", action=FileManager.file.new),
            TextLine("[CTRL+O]                  Open", action=FileManager.file.open),
            TextLine("[CTRL+SHIFT+O]  Open Workspace", action=FileManager.file.open),
            TextLine("[CTRL+S]                  Save", action=FileManager.file.save),
            TextLine("[CTRL+SHIFT+S]         Save as", action=FileManager.file.save_as),
            TextLine("[CTRL+Q]                  Quit", action=Actions.quit),
            TextLine("                              "),   
            TextLine("[ESC]                    Close", action=self.close)
        ]
    
    def render(self, sc):
        if not self.show: return
        
        menu = MenuBox(
            title = "File",
            lines = self.options,
            width=32,
            highlight_index=self.selection
        )
        
        menu.render(sc)
        
    
    def handle_input(self, key):
        if self.show == False: return
        
        if key == 27: #close menu using escape
            self.close()
        
        if key in [curses.KEY_UP, curses.KEY_LEFT]:
            self.selection -= 1
            if self.selection < 0:
                self.selection = len(self.options) - 1
            
        if key in [curses.KEY_DOWN, curses.KEY_RIGHT]:
            self.selection += 1
            if self.selection > len(self.options) - 1:
                self.selection = 0
        
        if key == 32 or key == 10 or key == 459 or key == 13:
            if self.options[self.selection].action != None:
                    self.options[self.selection].action()
        return True
        
    
    def open(self):
        self.show = True
        
    def close(self):
        self.show = False
        
view = ViewMenu()
file = FileMenu()

menus = [view, file]
current = None

def open(menu_id: str):
    global current
    
    if current: current.close() #prevent multiple menus from being open at once
    try:
        current = next(menu for menu in menus if menu.id == menu_id)
        current.open()
    except:
        current = None
        raise Exception(f"Menu '{menu_id}' not found")
    
def close():
    global current
    if current: current.close()
    current = None
    
def toggle(menu_id: str):
    global current
    if current:
        if current.id == menu_id:
            close()
        else:
            open(menu_id)
    else:
        open(menu_id)