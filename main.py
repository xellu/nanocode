import os
import time
import threading

from pages import Welcome
from pages import Utils
from pages.Components import NavBar, Menus

from dataforge import config
from dataforge.core import notification

from engine import RenderEngine, InputEngine, Actions

cfg = config.Config("data/config.json")
components = [
        NavBar.component,
        Menus.file, Menus.view
    ]

required_fields = ["version", "screenX", "screenY", "theme"]
for field in required_fields:
    if not hasattr(cfg, field): raise notification.warn(f"Config file is corrupted, missing required field: {field}")

#STARTUP----------------------------------------------------
def main():
    threading.Thread(target=render.start).start()
    threading.Thread(target=inputs.start).start()

render = RenderEngine.RenderEngine(Welcome.page, components=components, config=cfg)
inputs = InputEngine.InputEngine(engine=render, delay_ms=0)
Utils.engine = render

main()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    Actions.quit()
    
#-----------------------------------------------------------