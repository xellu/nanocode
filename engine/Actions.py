import os
from dataforge import console

def quit():
    console.info("Application shutting down")
    os._exit(0)
    