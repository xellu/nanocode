from pages import Base, Utils
from pages.Utils.MenuBox import MenuBox, TextLine, PromptBox
from engine import RenderEngine
from engine.ThemeEngine import Colors, Loader
from engine import About
import curses
import time

from dataforge import config, console

class Option:
    def __init__(self, label: str, attribute: tuple|str, _type: str, max_value: int=None, min_value: int=None,
            enum: list=[], action: callable=None, live_value: tuple=None, description: str=""):
        
        """
        label (str): The label for the option\n
        attribute (tuple/str): tuple=(object, attribute) the attribute to get the value from\n
        _type (str): an option type\n
        | types (for _type): int, bool, enum, display, display_title, button\n
        max_value (int): the maximum value for an int option\n
        min_value (int): the minimum value for an int option\n
        enum (list): list of strings for an enum option\n
        action (callable): a function to call when the option is selected\n
        live_value (tuple): (callable, attribute:str) updates the value of the option every frame\n
        description (str): a description text of what the option does\n
        """
        self.label = label
        self.value = getattr(attribute[0], attribute[1]) if type(attribute) == tuple else attribute
        self.attribute = attribute
        self.type = _type
        self.enum = [self.value] + enum
        self.enum_index = 0
        self.description = "(i) " + description if description != "" else ""
        
        self.max_value = max_value if max_value != None else 256
        self.min_value = min_value if min_value != None else 0
        
        self.action = action
        
        self.live_value = live_value
        
        self.modified_value = self.value
        
        #remove duplicates from enum
        self.enum = list(dict.fromkeys(self.enum))
    
    def update_live_value(self):
        if self.live_value and self.live_value[0] and self.live_value[1] and hasattr(self.live_value[0](), self.live_value[1]):
            self.value = getattr(self.live_value[0](), self.live_value[1])
            self.modified_value = self.value
        

class Settings(Base):
    def __init__(self):
        super().__init__()
        self.return_page = None
        self.config = config.Config("data/config.json")
        self.changed = False
        self.changed_expire = 0
        self.guide = "[UP/DOWN] Navigate   [LEFT/RIGHT] Change Value   [ENTER] Press Button   [ESC] Reset Value"
        self.guide_2 = "[S] Save changes   [D] Discard changes"
        
        self.prompt = PromptBox("Path", [TextLine("Enter a path to open")], callback=Utils.open_url, width=30)
        
        self.options = [
            Option("Interface", None, "display_title"),
            Option("Screen Width", (self.config, "screenX"), "int", min_value=120, max_value=300, description="The width of the screen in characters"),
            Option("Screen Height", (self.config, "screenY"), "int", min_value=28, max_value=300, description="The height of the screen in characters"),
            Option("Theme", (self.config, "theme"), "enum", enum=Loader.get_theme_names(), description="Color appearance of the application"),
            Option("Show FPS", (self.config, "showFps"), "bool", description="Shows the framerate in the top left corner of the screen"),
            Option("", None, "display"),
            
            Option("Editor", None, "display_title"),
            Option("Tab Indent", (self.config, "tabIndent"), "int", min_value=1, description="Amount of spaces to indent when pressing tab"),
            Option("Gutter", (self.config, "gutter"), "bool", description="Highlights empty spaces at the end of the line"),
            Option("Line Numbers", (self.config, "lineNumbers"), "bool", description="Shows line numbers on the left side of the editor"),
            Option("", None, "display"),
            
            Option("Software", None, "display_title"),
            Option("Version", About.version, "display", description="Version of the application"),
            Option("Framerate", None, "display", description="The amount of times the screen is updated per second", live_value=(RenderEngine.get_instance, "fps")),
            Option("Author", "@xellu", "button", description="Open github profile", action=lambda: Utils.open_url("https://github.com/xellu")),
            Option("Repository", "github.com/xellu/nanocode", "button", description="Open the github repository", action=lambda: Utils.open_url("https://github.com/xellu/nanocode"))   
        ]
        
        self.selection = 1
        
        self.prompt.open()
        
    def render(self, sc):
        if self.prompt.is_confirmed():
            sc.addstr(2,2,self.prompt.output()) 
            
        return
        
        sc.addstr(2,0, "="*Utils.screenX(), curses.color_pair(Colors.accent))
        sc.addstr(2,Utils.centerX("a Settings a"), "[ Settings ]", curses.color_pair(Colors.accent))
        sc.addstr(Utils.screenY()-1, 0, " "*Utils.screenX(), curses.color_pair(Colors.accent_bg))
        sc.addstr(Utils.screenY(), 0, " "*Utils.screenX(), curses.color_pair(Colors.accent_bg))
        sc.addstr(Utils.screenY(), Utils.centerX(self.guide), self.guide, curses.color_pair(Colors.accent_bg))
        sc.addstr(Utils.screenY()-2, Utils.centerX(self.guide_2), self.guide_2, curses.color_pair(Colors.accent))
    
        if self.changed and self.changed_expire >= time.time():
            menu = MenuBox(
                f"Settings Saved ({self.changed_expire - time.time():.0f}s)",
                lines = [
                    TextLine("To apply changes, you'll need", center=True),
                    TextLine("to restart the application", center=True),
                    TextLine(""),
                    TextLine("Press enter to dismiss", center=True)
                ],
                width=31,
                warning=True
            )
            menu.render(sc)
    
        y = 4
        max_y = Utils.screenY()-8
        for i in range(0, max_y-y):
            try:
                opt = self.options[i]
            except IndexError: break
            
            if self.selection == i:
                tooltip = opt.description[:Utils.screenX()-1]
                sc.addstr(y+i, 3, opt.label, curses.color_pair(Colors.accent_bg))
                sc.addstr(y+i, 2, ">", curses.color_pair(Colors.menu_pointer))
                sc.addstr(Utils.screenY()-1, Utils.centerX(tooltip), tooltip, curses.color_pair(Colors.accent_bg))
            else:
                sc.addstr(y+i, 3, opt.label, curses.color_pair(Colors.accent_bg if opt.type == "display_title" else Colors.accent))
            
            if opt.modified_value != None:
                value = str(opt.modified_value)
                if type(value) == bool:
                    value = "Enabled" if value else "Disabled"
                    
                if opt.modified_value != opt.value:
                    value += "*"
                    
                sc.addstr(y+i, 3+len(opt.label)+1, value)
        
    
    def handle_input(self, key):
        opt = self.options[self.selection]
        if key == curses.KEY_UP:
            self.selection -= 1
            if self.selection < 0:
                self.selection = len(self.options)-1
            
            while self.options[self.selection].type in ["display_title", "display"]: #skip all text elements
                self.selection -= 1 
                
        if key == curses.KEY_DOWN:
            self.selection += 1
            if self.selection > len(self.options)-1:
                self.selection = 0
            
            while self.options[self.selection].type in ["display_title", "display"]: #skip all text elements
                self.selection += 1
                
        if key == curses.KEY_LEFT:
            if opt.type == "int":
                opt.modified_value -= 1
                if opt.modified_value < opt.min_value:
                    opt.modified_value = opt.min_value
                    
            if opt.type == "enum":
                opt.enum_index -= 1
                if opt.enum_index < 0:
                    opt.enum_index = len(opt.enum)-1
                opt.modified_value = opt.enum[opt.enum_index]
                    
            if opt.type == "bool":
                opt.modified_value = not opt.modified_value
                
        if key == curses.KEY_RIGHT:
            if opt.type == "int":
                opt.modified_value += 1
                if opt.modified_value > opt.max_value:
                    opt.modified_value = opt.max_value
                    
            if opt.type == "enum":
                opt.enum_index += 1
                if opt.enum_index > len(opt.enum)-1:
                    opt.enum_index = 0
                opt.modified_value = opt.enum[opt.enum_index]
                
            if opt.type == "bool":
                opt.modified_value = not opt.modified_value
    
        if key in [27, 7]: #escape
            if opt.type != "enum":
                opt.modified_value = opt.value
            else:
                opt.enum_index = opt.enum.index(opt.value)
                opt.modified_value = opt.enum[opt.enum_index]
    
        if key in [10, 459, 13]: #enter
            if self.changed:
                self.changed = False
                return
                
            if opt.action != None:
                opt.action()
            elif opt.type == "bool":
                opt.modified_value = not opt.modified_value
                
        if key in [115, 83]: #s
            console.info("Updated configuration")
            for o in self.options:
                if o.modified_value != None and o.live_value == None:
                    o.value = o.modified_value
                    if type(o.attribute) == tuple:
                        setattr(o.attribute[0], o.attribute[1], o.modified_value)
                    
                    
            self.config.save()
            self.config = config.Config("data/config.json")
                    
            self.changed = True
            self.changed_expire = time.time() + 5
            
        if key in [100, 68]: #d
            self.changed = False
            self.changed_expire = 0
            for o in self.options:
                if o.modified_value != None:
                    o.modified_value = o.value
    
    def open(self, _page):
        self.return_page = _page
        RenderEngine.open_page(page)
    
page = Settings()