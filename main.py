from dataforge import config
from dataforge.core import notification

try:
    cfg = config.Config("data/config.json")
    required_fields = ["screenX", "screenY", "theme", "tabIndent"]
    for field in required_fields:
        if not hasattr(cfg, field): raise notification.error(f"Config file is corrupted, missing required field: {field}")
except:
    raise notification.error(f"Config file is corrupted, unable to load")



import os
import time
import threading

from pages import StartScreen
from pages import Utils
from pages.Components import NavBar, Menus

from engine import RenderEngine, InputEngine, Actions, SessionEngine


components = [
    NavBar.component,
    Menus.file, Menus.view
]


SessionEngine.Session()

#STARTUP----------------------------------------------------
def main():
    threading.Thread(target=render.start).start()
    threading.Thread(target=inputs.start).start()

render = RenderEngine.RenderEngine(StartScreen.page, components=components, config=cfg)
inputs = InputEngine.InputEngine(engine=render, delay_ms=0)
Utils.engine = render

main()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    # print("Use CTRL+Q to exit")
    Actions.quit()    
#-----------------------------------------------------------