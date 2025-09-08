import sys
import threading
import time


class Spinner:

    def __init__(self, delay=0.1):
        self.spinner_cycle = ['-', '\\', '|', '/']
        self.delay = delay
        self.running = False
        self._thread = None

    def _spin(self):
        while self.running:
            for ch in self.spinner_cycle:
                sys.stdout.write(f"\r{ch} Corriendo la carrera...")
                sys.stdout.flush()
                time.sleep(self.delay)

    def start(self):
        if not self.running:
            self.running = True
            self._thread = threading.Thread(target=self._spin, daemon=True)
            self._thread.start()

    def stop(self):
        self.running = False
        if self._thread:
            self._thread.join()
        # limpiar línea
        sys.stdout.write("\r✔ Carrera finalizada!          \n")
        sys.stdout.flush()
