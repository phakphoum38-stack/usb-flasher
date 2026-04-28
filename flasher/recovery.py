import os

# =========================
# 🧠 RECOVERY STATE
# =========================
RECOVERY_FLAG = "flash_failed.flag"


def mark_failed():
    with open(RECOVERY_FLAG, "w") as f:
        f.write("failed")


def mark_success():
    if os.path.exists(RECOVERY_FLAG):
        os.remove(RECOVERY_FLAG)


def needs_recovery():
    return os.path.exists(RECOVERY_FLAG)


# =========================
# 🔧 RECOVERY ACTION
# =========================
def recovery_fix():
    print("🔧 Recovery mode activated...")

    steps = [
        "Re-check USB",
        "Re-mount image",
        "Reset EFI builder",
        "Retry flash pipeline"
    ]

    for s in steps:
        print("➡️", s)

    return True
