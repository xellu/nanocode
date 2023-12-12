from pages import Base
from pages import Utils
from engine.ThemeEngine import Colors
import time
import curses

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
        
    def render(self, sc):
        for i, line in enumerate(self.ascii_art.splitlines()):
            sc.addstr(i+5, Utils.centerX(line), line, curses.color_pair(Colors.accent))
        
        
        #if blink then render a cursor
        if (self.animation_meta["blink"] and self.animation_meta["state"] == "waiting") or self.animation_meta["state"] in ["writing", "deleting"]:
            sc.addstr(len(self.ascii_art.splitlines())+5, Utils.centerX(self.animation_meta["text"]),
                " "*len(self.animation_meta["text"])+"█")
            
        sc.addstr(len(self.ascii_art.splitlines())+5, Utils.centerX(self.animation_meta["text"]),
            self.animation_meta["text"])
        
        
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
            
        
           
    
    def handle_input(self, key):
        pass
    
page = Welcome()