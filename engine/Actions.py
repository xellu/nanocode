import os
from pages.Settings import page as theme_page
from engine import RenderEngine

def quit():
    print("Exiting")
    os._exit(0)
    
def theme_menu():
    RenderEngine.open_page(theme_page)