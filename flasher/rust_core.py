import subprocess

def flash_with_rust(image, device, progress_callback=None):
    cmd = ["rust-flash.exe", image, device]

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    for line in process.stdout:
        line = line.strip()

        if "|" in line:
            percent, speed = line.split("|")
            percent = int(float(percent.replace("%", "")))
            speed = float(speed.replace("MB/s", ""))

            if progress_callback:
                progress_callback(percent, speed)

        if "DONE" in line:
            break

    process.wait()
