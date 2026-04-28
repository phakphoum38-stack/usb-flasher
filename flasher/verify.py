import hashlib

def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            c = f.read(1024 * 1024)
            if not c:
                break
            h.update(c)
    return h.hexdigest()

def verify_flash(a, b):
    try:
        return sha(a) == sha(b)
    except:
        return False
