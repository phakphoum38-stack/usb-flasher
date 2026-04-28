import re

ERROR_PATTERNS = {
    "kernel panic": "Kernel crash detected",
    "apfs": "File system issue",
    "nvme": "Storage driver issue",
    "gpu": "Graphics injection problem",
    "oc:": "OpenCore config issue"
}


def analyze_log(log_text: str):
    findings = []

    text = log_text.lower()

    for key, desc in ERROR_PATTERNS.items():
        if key in text:
            findings.append(desc)

    if not findings:
        return ["No critical issues found"]

    return findings
