from pages import Base
from pages import Utils

class Welcome(Base):
    def __init__(self):
        super().__init__()
        self.title = "NanoCode"
        self.content = "This is a placeholder for the welcome page."
        
    def render(self, sc):
        sc.addstr(Utils.centerY(),Utils.centerX(self.title), self.title)
        sc.addstr(Utils.centerY()+1,Utils.centerX(self.content), self.content)
    
    def handle_input(self, key):
        pass
    
page = Welcome()