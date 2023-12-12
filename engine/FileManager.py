import os

class FileManager:
    def __init__(self):
        pass
    
    def new(self):
        pass
    
    def new_workspace(self):
        pass
    
    def open(self):
        pass
    
    def open_workspace(self, path: str = None):
        pass
    
    def save(self):
        pass
    
    def save_as(self):
        pass
    
class File:
    def __init__(self, path):
        self.path = path
        self.contents = []
        
    def load(self, content: str = None):
        if os.exists(self.path) or content != None:
            if content != None:
                data = content
            else:
                data = open(self.path, "r").read()
            lines = data.splitlines()
            
            for line in lines:
                self.contents.append(line.split(""))
                
        else:
            self.load("File was deleted or was moved")
            
    
file = FileManager()