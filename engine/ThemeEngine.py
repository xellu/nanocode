import curses
import os
from dataforge import config
from dataforge.core import notification

class ThemeLoader:
    def __init__(self):
        self.colors = {
            "WHITE": curses.COLOR_WHITE,
            "BLACK": curses.COLOR_BLACK,
            "RED": curses.COLOR_RED,
            "GREEN": curses.COLOR_GREEN,
            "YELLOW": curses.COLOR_YELLOW,
            "BLUE": curses.COLOR_BLUE,
            "MAGENTA": curses.COLOR_MAGENTA,
            "CYAN": curses.COLOR_CYAN,
        }
    
    def get_themes(self):
        out = []
        for theme in os.listdir("data/themes"):
            if theme.endswith(".theme.json"):
               if self.validate_theme(theme.replace(".theme.json", "")):
                    out.append((theme, self.get_theme_data(theme.replace(".theme.json", ""))))
        return out
    
    def get_theme_names(self):
        themes = self.get_themes()
        out = []
        for t in themes:
            out.append(t[0].replace(".theme.json", ""))
        return out
    
    def validate_theme(self, name):
        f = config.Config("data/themes/" + name + ".theme.json")
        required_fields = ["name", "author", "colors", "syntax"]
        for field in required_fields:
            if not hasattr(f, field): return (False, f"Missing field for {field}")
        
        return (True, None)
    
    def get_theme_data(self, name):
        f = config.Config("data/themes/" + name + ".theme.json")
        return f
            
    def to_colors(self, text_colors):
        out = {}
        for color in text_colors:
            out[color] = self.colors.get(text_colors.get(color))
        return out
    
    def load_from_config(self):
        cfg = config.Config("data/config.json")
        theme = cfg.Get("theme")
        path = "data/themes/" + theme + ".theme.json"
        if not os.path.exists(path):
            raise FileNotFoundError(f"Theme file not found in {path}")
        
        validation = self.validate_theme(theme)
        if not validation[0]:
            raise notification.warn(f"Theme file {theme} is corrupted: {validation[1]}")
        
        colors = self.to_colors( self.get_theme_data(theme).colors )
        curses.init_pair(Colors.normal, colors.get("foreground"), colors.get("background"))
        curses.init_pair(Colors.reverse, colors.get("background"), colors.get("foreground"))
        curses.init_pair(Colors.accent, colors.get("accent"), colors.get("background"))
        curses.init_pair(Colors.accent_bg, colors.get("background"), colors.get("accent"))
        curses.init_pair(Colors.warning, colors.get("warning"), colors.get("background"))
        curses.init_pair(Colors.warning_bg, colors.get("background"), colors.get("warning"))
        curses.init_pair(Colors.menu_pointer, colors.get("accent") if colors.get("background") == colors.get("pointer") else colors.get("background"), colors.get("pointer"))
        
      
class Colors:
    normal = 1
    reverse = 2
    accent = 3
    accent_bg = 4
    warning = 5
    warning_bg = 6
    menu_pointer = 7
  
Loader = ThemeLoader()
