import subprocess

def flash_with_rust(img, dev, cb=None):
    process = subprocess.Popen(
        ["rust-flash.exe", img, dev],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    for line in process.stdout:
        line = line.strip()

        if "|" in line:
            try:
                p, s = line.split("|")
                p = int(float(p.replace("%", "")))

                if cb:
                    cb(p, 0)
            except:
                pass

    process.wait()

    if process.returncode != 0:
        raise Exception("Flash process failed")
