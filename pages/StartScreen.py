from pages import Base, Utils, Editor, Welcome
from engine import SessionEngine, RenderEngine
from dataforge import console

class StartScreen(Base):
    def __init__(self):
        self.title = "NanoCode"
        self.content = "Loading workspace"
        
    def render(self, sc):
        sc.addstr(Utils.centerY(),Utils.centerX(self.title), self.title)
        sc.addstr(Utils.centerY()+1,Utils.centerX(self.content), self.content)
        
        session = SessionEngine.Session()
        if session.config.get("workspace").get("open", False):
            RenderEngine.open_page(Editor.page)
            console.info("Opening workspace")
        else:
            RenderEngine.open_page(Welcome.page)
            console.info("No workspace found, resetting workspace configuration")
            session.config.workspace["open"] = False
            session.config.workspace["path"] = None
            session.config.workspace["files"] = []
            session.config.save()
        
    def handle_input(self, key):
        pass
    
page = StartScreen()
    