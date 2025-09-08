from __future__ import annotations
import random
from dataclasses import dataclass, field
from typing import List

__all__ = ["Vehiculo", "Deportivo", "Clasico", "UsoDiario"]


@dataclass
class Vehiculo:
    """
    Clase base para vehículos.
    - name: nombre del vehículo
    - base_speed: velocidad base (m/s) en cada "paso" o intervalo
    - reliability: probabilidad de NO sufrir micro-retraso (0..1)
    - variance: variabilidad de la distancia por paso (ruido aleatorio)
    """
    name: str
    base_speed: float = 18.0
    reliability: float = 0.92
    variance: float = 0.15
    events: List[str] = field(default_factory=list, repr=False)

    def step_distance(self) -> float:
        noise = random.uniform(-self.variance, self.variance)
        return max(0.0, self.base_speed * (1.0 + noise))

    def step_delay(self) -> float:
        return random.uniform(0.08, 0.12)

    def maybe_extra_delay(self) -> float:
        if random.random() > self.reliability:
            extra = random.uniform(0.05, 0.25)
            self.events.append(
                f"{self.name} sufre micro-retraso de {extra:.3f}s")
            return extra
        return 0.0


class Deportivo(Vehiculo):
    """Más rápido pero un poco menos confiable; ocasional 'nitro'."""

    def __init__(self, name: str):
        super().__init__(name=name,
                         base_speed=23.0,
                         reliability=0.88,
                         variance=0.18)

    def step_distance(self) -> float:
        d = super().step_distance()
        if random.random() < 0.10:  # nitro
            return d * 2.0
        return d

    def step_delay(self) -> float:
        return random.uniform(0.07, 0.10)


class Clasico(Vehiculo):
    """Más estable y confiable; menor velocidad máxima."""

    def __init__(self, name: str):
        super().__init__(name=name,
                         base_speed=16.0,
                         reliability=0.97,
                         variance=0.10)

    def step_delay(self) -> float:
        return random.uniform(0.09, 0.13)


class UsoDiario(Vehiculo):
    """Equilibrado."""

    def __init__(self, name: str):
        super().__init__(name=name,
                         base_speed=19.0,
                         reliability=0.93,
                         variance=0.12)
