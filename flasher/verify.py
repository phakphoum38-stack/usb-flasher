import hashlib

def sha(path):
    h = hashlib.sha256()
    with open(path,"rb") as f:
        while c:=f.read(1024*1024):
            h.update(c)
    return h.hexdigest()

def verify_flash(a,b):
    return sha(a)==sha(b)
