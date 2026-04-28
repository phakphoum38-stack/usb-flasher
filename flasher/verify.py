def quick_verify(img, dev):
    """
    Verify เฉพาะช่วงต้น (เร็วมาก)
    """
    try:
        with open(img, "rb") as f1, open(dev, "rb") as f2:
            return f1.read(1024 * 1024) == f2.read(1024 * 1024)
    except:
        return False


# optional: เผื่ออยากใช้แบบเต็มในอนาคต
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

def full_verify(a, b):
    try:
        return sha(a) == sha(b)
    except:
        return False
