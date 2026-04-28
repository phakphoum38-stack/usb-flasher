import subprocess

def flash_with_rust(img, dev, cb=None):
    process = subprocess.Popen(
        ["rust-flash.exe", img, dev],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    for line in process.stdout:
        line = line.strip()

        if "|" in line:
            try:
                per, sp = line.split("|")
                per = int(float(per.replace("%", "")))
                sp = float(sp.replace("MB/s", ""))

                if cb:
                    cb(per, sp)
            except:
                pass

    return process
