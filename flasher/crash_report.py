import traceback
import json
import time

def capture_error(error, context="general"):
    report = {
        "time": time.time(),
        "context": context,
        "error": str(error),
        "trace": traceback.format_exc()
    }

    with open("crash_report.json", "w") as f:
        json.dump(report, f, indent=4)

    print("❌ Crash report saved")
