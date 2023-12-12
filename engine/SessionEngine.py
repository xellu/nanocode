import os
import json
from dataforge import config


class Session:
    def __init__(self):
        self.template = {
            "workspace": {
                "open": False,
                "path": None,
                "files": []
            },
            "prev_workspace": None
        }
        
        self.repair_config()
        self.config = self.get_data()
        
    def get_data(self):
        if os.path.exists("data/session.json"):
            return config.Config("data/session.json")
        
        open("data/session.json", "w").write(json.dumps(self.template))
        return self.template
    
    def repair_config(self):
        if not os.path.exists("data/session.json"):
            open("data/session.json", "w").write(json.dumps(self.template))
            return
        
        data = config.Config("data/session.json")
        for key in self.template:
            if not hasattr(data, key):
                data.Set(key, self.template[key])
                
        data.save()