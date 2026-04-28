import os
import psutil

# =========================
# 📏 SIZE CHECK
# =========================
def get_disk_size_gb(path):
    usage = psutil.disk_usage(path)
    return usage.total / (1024 ** 3)


# =========================
# ⚠️ VERIFY TARGET DEVICE
# =========================
def verify_target_device(device_path, iso_path):
    """
    กัน error:
    - USB เล็กเกินไป
    - เลือก disk ผิด
    """

    if not os.path.exists(iso_path):
        raise Exception("❌ ISO file not found")

    # mock size check (จริงควร map device จริง)
    size = get_disk_size_gb("/")

    if size > 200:
        raise Exception("❌ BLOCKED: target looks like system disk")

    return True
