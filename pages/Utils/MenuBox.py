from pages import Utils
import curses
from engine.ThemeEngine import Colors

class TextLine:
    def __init__(self, text: str, center: bool = False, action = None):
        self.text = text
        self.center = center
        self.action = action
        
class MenuBox:
    def __init__(self, title, lines: list, width: int = 20, outline: bool=True, highlight_index: int = None, warning: bool = False):
        self.title = f"[ {title} ]"
        self.lines = lines
        self.outline = outline
        self.width = width
        self.highlight_index = highlight_index
        self.warning = warning
        
        self.color_bg = Colors.warning_bg if self.warning else Colors.accent_bg
        self.color_fg = Colors.warning if self.warning else Colors.accent
        
        self.startY = int(Utils.centerY() - (len(lines) / 2))
        self.endY = self.startY + len(lines)
        self.startX = Utils.centerX("x"*width)
        self.endX = self.startX + width
        
    def render(self, sc):
        # Draw outline
        if self.outline:
            for y in range(self.startY+1, self.endY+1):
                sc.addstr(y, self.startX-1, "*", curses.color_pair(self.color_bg))
                sc.addstr(y, self.endX, "*", curses.color_pair(self.color_bg))
            for x in range(self.startX-1, self.endX+1):
                sc.addstr(self.startY, x, "#", curses.color_pair(self.color_bg))
                sc.addstr(self.endY+1, x, "#", curses.color_pair(self.color_bg))
            
        # Draw title
        sc.addstr(self.startY, Utils.centerX(self.title), self.title, curses.color_pair(self.color_bg))
        
        # Draw lines
        for line in self.lines:
            if self.highlight_index == self.lines.index(line):
                sc.addstr(self.startY + self.lines.index(line) + 1, self.startX-1, "> ", curses.color_pair(Colors.menu_pointer))
                sc.addstr(self.startY + self.lines.index(line) + 1, self.endX-1, " <", curses.color_pair(Colors.menu_pointer))
                
            sc.addstr(self.startY + self.lines.index(line) + 1, self.startX, " "*self.width, curses.color_pair(self.color_bg))
            if line.center:
                sc.addstr(self.startY + self.lines.index(line) + 1, Utils.centerX(line.text), line.text, curses.color_pair(self.color_bg))
            else:
                sc.addstr(self.startY + self.lines.index(line) + 1, self.startX + 1, line.text, curses.color_pair(self.color_bg))
        