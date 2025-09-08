from __future__ import annotations
import argparse
import random
from carrera import comparar_versiones, crear_vehiculos_demo
from spinner import Spinner
from util import pausa_aleatoria


def parse_args():
  p = argparse.ArgumentParser(
      description="Simulación de carrera: secuencial vs concurrente")

  p.add_argument("--dist",
                 type=float,
                 default=1000.0,
                 help="Distancia de carrera en metros (default: 1000)")
  p.add_argument("--seed",
                 type=int,
                 default=42,
                 help="Semilla de aleatoriedad (default: 42)")
  p.add_argument("--verbose",
                 action="store_true",
                 help="Muestra progreso en vivo")

  return p.parse_args()


if __name__ == "__main__":
  args = parse_args()

  random.seed(args.seed)

  pausa_aleatoria(1, 3)
  print(f"Esta será una carrera de {args.dist:.1f} metros...")
  pausa_aleatoria(1, 2)
  print("Se apagan las luces rojas del semáforo...")
  pausa_aleatoria(0.5, 1)
  print("¡Y ARRANCAN!")

  spinner = Spinner()
  spinner.start()  # comienza a girar

  try:
    comparar_versiones(
        vehiculos_factory=crear_vehiculos_demo,
        distancia_total=args.dist,
        verbose=args.verbose,
    )
  finally:
    spinner.stop()
