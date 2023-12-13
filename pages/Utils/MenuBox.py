from pages import Utils
import curses
from engine.ThemeEngine import Colors
from dataforge.core import notification
import random

class TextLine:
    def __init__(self, text: str, center: bool = False, action = None):
        self.text = text
        self.center = center
        self.action = action
        
class MenuBox:
    def __init__(self, title, lines: list, width: int = 20, outline: bool=True, highlight_index: int = None, warning: bool = False, x: int = None, y: int = None):
        self.title = f"[ {title} ]"
        self.lines = lines
        self.outline = outline
        self.width = width
        self.highlight_index = highlight_index
        self.warning = warning
        self.x = x
        self.y = y
        
        self.color_bg = Colors.warning_bg if self.warning else Colors.accent_bg
        self.color_fg = Colors.warning if self.warning else Colors.accent
        
        
        if x == None:
            self.startX = Utils.centerX("x"*width)
            self.endX = self.startX + width
        else:
            self.startX = x
            self.endX = x + width
        
        if y == None:
            self.startY = int(Utils.centerY() - (len(lines) / 2))
            self.endY = self.startY + len(lines)
        else:
            self.startY = y
            self.endY = y + len(lines)
            
        
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
        if self.x == None:
            sc.addstr(self.startY, Utils.centerX(self.title), self.title, curses.color_pair(self.color_bg))
        else:
            sc.addstr(self.startY, self.x+5, self.title, curses.color_pair(self.color_bg))
        
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
        
class PromptBox:
    def __init__(self, title, lines: list, callback: callable, width: int = 20, outline: bool=True, x:int=None, y:int=None):
        self.title = f"[ {title} ]"
        self.lines = lines + [TextLine(""), TextLine("=input")]
        self.outline = outline
        self.width = width
        self.callback = callback
        self.x = x
        self.y = y
        
        if x == None:
            self.startX = Utils.centerX("x"*width)
            self.endX = self.startX + width
        else:
            self.startX = x
            self.endX = x + width
            
        if y == None:
            self.startY = int(Utils.centerY() - (len(self.lines) / 2))
            self.endY = self.startY + len(self.lines)
        else:
            self.startY = y
            self.endY = y + len(self.lines)

    def open(self):
        if prompt.prompt != None:
            raise notification.warn2("Prompt is already open")
            
        prompt.prompt = self
        
    def close(self):
        if prompt.prompt == self:
            prompt.prompt = None
    
    def is_open(self):
        return prompt.prompt == self
    
    def is_confirmed(self):
        return prompt.confirm
    
    def output(self):
        if self.is_open() or not prompt.confirm: return None
        
        return prompt.input
         
        
class Prompt:
    def __init__(self, prompt: PromptBox=None):
        self.prompt = prompt
        self.input = ""
        self.confirm = False
    
    def render(self, sc):
        p = self.prompt
        if not p:
            return
        
        # Draw outline
        if p.outline:
            for y in range(p.startY+1, p.endY+1):
                sc.addstr(y, p.startX-1, "*", curses.color_pair(Colors.accent_bg))
                sc.addstr(y, p.endX, "*", curses.color_pair(Colors.accent_bg))
            for x in range(p.startX-1, p.endX+1):
                sc.addstr(p.startY, x, "#", curses.color_pair(Colors.accent_bg))
                sc.addstr(p.endY+1, x, "#", curses.color_pair(Colors.accent_bg))
        
        # Draw title
        if p.x == None:
            sc.addstr(p.startY, Utils.centerX(p.title), p.title, curses.color_pair(Colors.accent_bg))
        else:
            sc.addstr(p.startY, p.x+5, p.title, curses.color_pair(Colors.accent_bg))
            
        # Draw lines
        for line in p.lines:
            sc.addstr(p.startY + p.lines.index(line) + 1, p.startX, " "*p.width, curses.color_pair(Colors.accent_bg))
            if line.center:
                sc.addstr(p.startY + p.lines.index(line) + 1, Utils.centerX(line.text), line.text, curses.color_pair(Colors.accent_bg))
            else:
                sc.addstr(p.startY + p.lines.index(line) + 1, p.startX + 1, line.text.replace("=input", self.input), curses.color_pair(Colors.accent_bg))

    
    def handle_input(self, key):
        if not self.prompt: return False
        
        if key == curses.KEY_BACKSPACE or key == 8:
            self.input = self.input[:-1]
        elif key == curses.KEY_ENTER or key == 10 or key == 429:
            self.prompt.callback(self.input)
            self.input = ""
            self.confirm = True
        else:
            self.input += chr(key)
        
        return True
        
prompt = Prompt()