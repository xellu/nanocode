import curses
import os
from pages import Base, Editor

from dataforge.core import notification
from engine import ThemeEngine
import time

instance = None

class RenderEngine:
    def __init__(self, start_page = None, components = [], config = None):
        global instance
        instance = self
        
        self.page = Base() if not start_page else start_page # A default page to show on startup
        self.components = components
        self.sc = None
        self.config = config
        self.fps = 0
        self.framerate = {
            "frames": 0,
            "reset": time.time()
        }
        
        
        if not self.config: raise notification.warn("No config was provided")
        
        
    def start(self):
        curses.wrapper(self.loop)
    
    
    def render(self, sc):
        #render a page
        self.page.render(sc)
        
        if self.page == Editor.page:
            curses.curs_set(2)
        else:        
            curses.curs_set(0)

        #render components
        for c in self.components:
            c.render(sc)      
      
    def loop(self, sc):
        self.sc = sc
        curses.start_color()
        ThemeEngine.Loader.load_from_config()
        
        while True:
            #clear screen
            sc.clear()
            
            #rendering logic
            self.render(sc)
            
            if self.config.get("showFps"):
                sc.addstr(1, 0, f"FPS: {self.fps}")
                            
            #update screen
            sc.refresh()
            
            #calculate fps
            self.framerate["frames"] += 1
            if time.time() >= self.framerate["reset"]:
                self.fps = self.framerate["frames"]
                self.framerate["frames"] = 0
                self.framerate["reset"] = time.time() + 1
        
def get_instance():
    return instance
            
def open_page(page):
    instance.page = page