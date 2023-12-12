from pages import Base, Utils

class Settings(Base):
    def __init__(self):
        super().__init__()
        self.title = "Settings"
        self.content = "This is a placeholder for the settings page."
        
    def render(self, sc):
        sc.addstr(Utils.centerY(),Utils.centerX(self.title), self.title)
        sc.addstr(Utils.centerY()+1,Utils.centerX(self.content), self.content)
    
    def handle_input(self, key):
        pass
    
page = Settings()