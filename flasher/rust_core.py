import subprocess

def flash_with_rust(img, dev, cb=None):
    p = subprocess.Popen(
        ["rust-flash.exe", img, dev],
        stdout=subprocess.PIPE,
        text=True
    )

    for line in p.stdout:
        if "|" in line:
            per, sp = line.split("|")
            per = int(float(per.replace("%","")))
            sp = float(sp.replace("MB/s",""))
            if cb:
                cb(per, sp)

    return p
