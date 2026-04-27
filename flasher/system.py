import platform
import subprocess

def get_cpu_info():
    info = {
        "arch": platform.machine(),
        "system": platform.system(),
        "cpu": platform.processor()
    }

    try:
        if info["system"] == "Windows":
            out = subprocess.check_output(
                "wmic cpu get Name",
                shell=True
            ).decode()
            info["cpu"] = out.split("\n")[1].strip()

        elif info["system"] == "Linux":
            out = subprocess.check_output("lscpu", shell=True).decode()
            for line in out.split("\n"):
                if "Model name" in line:
                    info["cpu"] = line.split(":")[1].strip()

    except:
        pass

    return info


def detect_platform(cpu_name):
    cpu_name = cpu_name.lower()

    if "intel" in cpu_name:
        if "i3" in cpu_name or "i5" in cpu_name:
            return "Intel-Desktop"
        return "Intel"

    if "amd" in cpu_name or "ryzen" in cpu_name:
        return "AMD"

    return "Unknown"
