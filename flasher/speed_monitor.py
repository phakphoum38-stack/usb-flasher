import time

class SpeedMonitor:
    def __init__(self):
        self.start_time = None
        self.last_bytes = 0

    def start(self):
        self.start_time = time.time()
        self.last_bytes = 0

    def update(self, written_bytes):
        now = time.time()
        elapsed = now - self.start_time

        if elapsed == 0:
            return 0

        speed = written_bytes / elapsed / (1024 * 1024)  # MB/s

        return round(speed, 2)
