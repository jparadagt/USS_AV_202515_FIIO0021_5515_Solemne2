import time
import random


def pausa_aleatoria(min: float = 0.0, max: float = 0.1):
  time.sleep(random.uniform(min, max))
