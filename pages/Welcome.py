import os
import time
import curses

from pages import Base
from pages import Utils
from engine.ThemeEngine import Colors
from engine.SessionEngine import Session

from engine import FileManager
from pages.Utils.MenuBox import MenuBox, TextLine

class Option:
    def __init__(self, label, action = None):
        self.label = label
        self.action = action

class Welcome(Base):
    def __init__(self):
        self.ascii_art = """
   _  __               _____        __   
  / |/ /__ ____  ___  / ___/__  ___/ /__ 
 /    / _ `/ _ \/ _ \/ /__/ _ \/ _  / -_)
/_/|_/\_,_/_//_/\___/\___/\___/\_,_/\__/ 
"""
        self.animation = [
            "Faster way to Code",
            "Faster way to Write",
            "Faster way to Create",
            "Faster way to Edit",
            "Faster way to Develop",
            "Faster way to Develop Software",
            "Faster way to Develop Games",
            "Faster way to Develop Websites",   
            "Faster way to Develop Apps",
            "Faster way to Develop Anything",
            "Faster way to Develop Everything",
        ]
        self.animation_meta = {
            "index": 0,
            "wait": 5,
            "next": time.time()+5,
            "next_char": 0,
            "state": "writing",
            "text": "",
            "next_blink": 0,
            "blink": False
        }
        
        self.session = Session()
        
        self.recent = self.session.get_data().get("recent")
        
        self.selection = 0
        self.options = [
            TextLine("Start", center=True),
            
            TextLine("New File", action=lambda: FileManager.file.new()),
            TextLine("Open File", action=lambda: FileManager.file.open()),
            TextLine("Open Folder", action=lambda: FileManager.file.open_workspace()),
            TextLine(""),
                        
            TextLine("Recent", center=True)] + self.get_recents()
        
    def get_recents(self):
        if len(self.recent) > 5:
            self.recents = self.recent[:5]
            cfg = self.session.get_data()
            cfg.set("recent", self.recents)
            cfg.save()
            
        out = []
        for r in self.recent:
            #get file/folder name
            try:
                label = str(os.path.basename(r.get("path")))
            except:
                label = "Unknown"
            
            out.append(TextLine(label, action = lambda: FileManager.file.open_workspace(r.get("path"))))
        return out
        
    def render(self, sc):
        for i, line in enumerate(self.ascii_art.splitlines()):
            sc.addstr(i+5, Utils.centerX(line), line, curses.color_pair(Colors.accent))
        
        center = Utils.centerX(" "*15)
        
        #if blink then render a cursor
        if (self.animation_meta["blink"] and self.animation_meta["state"] == "waiting") or self.animation_meta["state"] in ["writing", "deleting"]:
            sc.addstr(len(self.ascii_art.splitlines())+5, Utils.centerX(self.animation_meta["text"]),
                " "*len(self.animation_meta["text"])+"█")
            
        sc.addstr(len(self.ascii_art.splitlines())+5, Utils.centerX(self.animation_meta["text"]),
            self.animation_meta["text"])
        
        #MENU ANIMATION----------------------------------------------------------
        
        #if state is writing and text == animation[index] then state = waiting
        if self.animation_meta["state"] == "writing" and self.animation_meta["text"] == self.animation[self.animation_meta["index"]]:
            self.animation_meta["state"] = "waiting"
            self.animation_meta["next"] = time.time()+self.animation_meta["wait"]
        
        #if state is writing and time.time() >= next_char then add a character to the text
        if self.animation_meta["state"] == "writing" and time.time() >= self.animation_meta["next_char"]:
            self.animation_meta["text"] += self.animation[self.animation_meta["index"]][len(self.animation_meta["text"])]
            self.animation_meta["next_char"] = time.time()+0.05
            
        #if state is waiting and time.time() >= next then state = deleting
        if self.animation_meta["state"] == "waiting" and time.time() >= self.animation_meta["next"]:
            self.animation_meta["state"] = "deleting"
            self.animation_meta["next"] = time.time()+self.animation_meta["wait"]
            
        #if state is deleting and text == "" then state = writing, index = index+1
        if self.animation_meta["state"] == "deleting" and self.animation_meta["text"] == "":
            self.animation_meta["state"] = "writing"
            self.animation_meta["index"] = (self.animation_meta["index"]+1)%len(self.animation)
            
        #if state is deleting and time.time() >= next_char then remove a character from the text
        if self.animation_meta["state"] == "deleting" and time.time() >= self.animation_meta["next_char"]:
            self.animation_meta["text"] = self.animation[self.animation_meta["index"]][:len(self.animation_meta["text"])-1]
            self.animation_meta["next_char"] = time.time()+0.05
        
        #if time.time() >= next_blink then set blink = not blink, next_blink = time.time()+0.5
        if time.time() >= self.animation_meta["next_blink"]:
            self.animation_meta["blink"] = not self.animation_meta["blink"]
            self.animation_meta["next_blink"] = time.time()+0.5
           
        #START MENU---------------------------------------------------------------
        
        for i, line in enumerate(self.options):
            sc.addstr(Utils.centerY()+i, center, line.text, curses.color_pair(Colors.accent_bg if line.center else Colors.accent))

            
            if i == self.selection:
                sc.addstr(Utils.centerY()+i, center-2, "> ", curses.color_pair(Colors.menu_pointer))
    
    def handle_input(self, key):
        if key == curses.KEY_UP:
            self.selection -= 1
            if self.selection < 0:
                self.selection = len(self.options) - 1
        
        if key == curses.KEY_DOWN:
            self.selection += 1
            if self.selection > len(self.options) - 1:
                self.selection = 0
                
        if key == 10 or key == 459 or key == 13:
            if self.options[self.selection].action != None:
                self.options[self.selection].action()
    
page = Welcome()