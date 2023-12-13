 
keys = {
    0: ord("?"),
    458: ord("/"),
    463: ord("*"),
    464: ord("-"),
    465: ord("+"),
    459: ord("\n"),
    530: ord("§"),
    460: ord("!"),
    461: ord("ß")
}

def patch_key(key):
    if key in keys:
        return keys[key]
    
    return key