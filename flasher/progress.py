import time
import threading

class ProgressEmitter:
    def __init__(self, callback=None):
        self.callback = callback
        self.progress = 0

    def start(self, total=100):
        def run():
            for i in range(total + 1):
                time.sleep(0.02)  # smooth effect
                self.progress = i

                if self.callback:
                    self.callback(i)

        threading.Thread(target=run, daemon=True).start()
