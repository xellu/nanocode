# import os
# import curses

engine = None

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
    return engine.config.screenX

def screenY():
    return engine.config.screenY