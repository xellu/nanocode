class Base:
    def __init__(self):
        self.text = "Base page"
        
    def render(self, sc):
        sc.addstr(0,0, self.text)
        
    def handle_input(self, key):
        print(f"Key pressed: {chr(key)}")