from pages import Base, Utils
import curses
from dataforge import config
from dataforge.database import Item
from pages.Components import Menus
from pages import Settings
from engine.ThemeEngine import Colors
from engine import RenderEngine

cfg = config.Config("data/config.json")

class NavBar(Base):
    def __init__(self):
        self.quick_menu = [
            Item(name="File", display_key = "ALT+F", key = [422], action = self.file_menu),
            Item(name="View", display_key = "ALT+V", key = [438], action = self.view_menu),
            Item(name="Settings", display_key = "ALT+S", key = [435], action = self.settings_page)
        ]

        self.nav_menu = ""
        for i in self.quick_menu:
            self.nav_menu += f"   [{i.display_key}] {i.name} "
        
    def settings_page(self):
        if RenderEngine.instance.page != Settings.page:
            Settings.page.open(RenderEngine.instance.page)
        else:
            RenderEngine.open_page(Settings.page.return_page)
        
    def file_menu(self):
        Menus.toggle("file")
        
    def view_menu(self):
        Menus.toggle("view")
        
    def render(self, sc):
        sc.addstr(0,0, " "*Utils.screenX(), curses.color_pair(Colors.accent_bg))
        sc.addstr(0,1, 
            f"NanoCode", curses.color_pair(Colors.accent_bg))
        sc.addstr(0,Utils.endX(self.nav_menu), self.nav_menu, curses.color_pair(Colors.accent_bg))
        
    def handle_input(self, key):
        print(f"DEBUG: key {chr(key)}/{key}      (!) remove in production (in navbar component)")   
        
        for item in self.quick_menu:
            if key in item.key:
                item.action()
                return True
            
             
component = NavBar()