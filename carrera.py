from __future__ import annotations
import asyncio
import time
from typing import Callable, List, Tuple, Optional
from models import Vehiculo, Deportivo, Clasico, UsoDiario

ProgressCb = Optional[Callable[[str, float], None]]


async def _carrera_corutina(
    vehiculo: Vehiculo,
    distancia_total: float,
    report: ProgressCb = None,
) -> Tuple[str, float, float]:
    restante = distancia_total
    start = time.perf_counter()

    while restante > 0:
        d = vehiculo.step_distance()
        restante -= d
        delay = vehiculo.step_delay() + vehiculo.maybe_extra_delay()
        await asyncio.sleep(delay)
        if report:
            avanz = max(distancia_total - max(restante, 0), 0)
            report(vehiculo.name, min(avanz, distancia_total))

    total = time.perf_counter() - start
    return (vehiculo.name, total, distancia_total)


async def carrera_concurrente(
    vehiculos: List[Vehiculo],
    distancia_total: float = 1000.0,
    on_progress: ProgressCb = None,
) -> List[Tuple[str, float]]:
    tareas = [
        _carrera_corutina(v, distancia_total, on_progress) for v in vehiculos
    ]
    resultados: List[Tuple[str, float, float]] = []
    for fut in asyncio.as_completed(tareas):
        nombre, t, dist = await fut
        resultados.append((nombre, t, dist))
    return [(n, t) for (n, t, _) in resultados]


def carrera_secuencial(
    vehiculos: List[Vehiculo],
    distancia_total: float = 1000.0,
    on_progress: ProgressCb = None,
) -> List[Tuple[str, float]]:
    import time as _t
    resultados: List[Tuple[str, float]] = []

    def sync_run(v: Vehiculo) -> float:
        restante = distancia_total
        start = _t.perf_counter()
        while restante > 0:
            d = v.step_distance()
            restante -= d
            delay = v.step_delay() + v.maybe_extra_delay()
            _t.sleep(delay)
            if on_progress:
                avanz = max(distancia_total - max(restante, 0), 0)
                on_progress(v.name, min(avanz, distancia_total))
        return _t.perf_counter() - start

    for v in vehiculos:
        t = sync_run(v)
        resultados.append((v.name, t))
    return resultados


def imprimir_podio(resultados: List[Tuple[str, float]], titulo: str) -> None:
    print(f"\n=== {titulo} ===")

    # Ordenar por tiempo (menor a mayor)
    resultados_ordenados = sorted(resultados, key=lambda x: x[1])
    ancho_nombre = max((len(n) for n, _ in resultados_ordenados), default=12)

    for i, (n, t) in enumerate(resultados_ordenados, 1):
        print(f"{i:>2}º  {n:<{ancho_nombre}}  tiempo: {t:6.3f} s")


def comparar_versiones(
    vehiculos_factory: Callable[[], List[Vehiculo]],
    distancia_total: float = 1000.0,
    verbose: bool = False,
) -> None:
    # Secuencial
    vehiculos_seq = vehiculos_factory()
    t0 = time.perf_counter()
    res_seq = carrera_secuencial(
        vehiculos_seq,
        distancia_total=distancia_total,
        on_progress=(lambda n, d: None) if not verbose else
        (lambda n, d: print(f"[SEQ] {n} -> {d:.1f} m")))
    total_seq = time.perf_counter() - t0

    # Concurrente
    vehiculos_conc = vehiculos_factory()
    t1 = time.perf_counter()
    res_conc = asyncio.run(
        carrera_concurrente(vehiculos_conc,
                            distancia_total=distancia_total,
                            on_progress=(lambda n, d: None) if not verbose else
                            (lambda n, d: print(f"[CON] {n} -> {d:.1f} m"))))
    total_conc = time.perf_counter() - t1

    print()  # Salto de linea
    imprimir_podio(res_seq, "Llegada (SECUENCIAL)")
    imprimir_podio(res_conc, "Llegada (CONCURRENTE)")

    suma_seq = sum(t for _, t in res_seq)
    suma_conc = sum(t for _, t in res_conc)
    max_conc = max(t for _, t in res_conc)
    ahorro = (1 - (total_conc / total_seq)) * 100 if total_seq > 0 else 0.0

    print("\n=== Métricas ===")
    print(f"Tiempo total SECUENCIAL (pared): {total_seq:.3f} s")
    print(
        f"Tiempo total CONCURRENTE (pared): {total_conc:.3f} s   (ahorro: {ahorro:.1f}%)"
    )
    print(f"Suma de tiempos individuales (SEQ): {suma_seq:.3f} s")
    print(f"Suma de tiempos individuales (CON): {suma_conc:.3f} s")
    print(f"Máximo tiempo individual (CON): {max_conc:.3f} s")
    print("\nObservación:")
    print(
        "- En SECUENCIAL, el tiempo de pared crece ~ con la SUMA de los tiempos de cada vehículo."
    )
    print(
        "- En CONCURRENTE, el tiempo de pared se acerca al MÁXIMO de los tiempos individuales (esperas solapadas)."
    )


def crear_vehiculos_demo() -> List[Vehiculo]:
    return [
        Deportivo("Nissan GT-R R35"),
        Clasico("Ford Mustang 1967 Fastback"),
        UsoDiario("Toyota Corolla"),
        Deportivo("Porsche 911 Turbo S"),
        Clasico("Jaguar E-Type 1961"),
        UsoDiario("Kia Rio 5"),
    ]
