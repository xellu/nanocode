import os
# import curses
from dataforge.config import Config

config = Config("data/config.json")

def centerX(x: str):
    return int( screenX() / 2 ) - int( len(x) /2 )
    
def centerY():
    return int(screenY() / 2)

def centerYX():
    return (centerY(), centerX())

def endX(x):
    lenx = len(x)
    w = screenX()
    return int(w - lenx)

def screenX():
    return config.screenX

def screenY():
    return config.screenY

def open_url(url):
    os.system(f"start \"\" {url}")