import time

class SpeedMonitor:
    def __init__(self):
        self.start = time.time()
        self.bytes_written = 0

    def update(self, chunk):
        self.bytes_written += chunk
        elapsed = time.time() - self.start

        if elapsed > 0:
            speed = self.bytes_written / elapsed / (1024 * 1024)
            return round(speed, 2)
        return 0
