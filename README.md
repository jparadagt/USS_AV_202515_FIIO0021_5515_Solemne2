# Simulador de Carrera — Secuencial vs Concurrente (Python)

Proyecto para **Paradigmas de Programación** que compara ejecución **secuencial** y **concurrente** en una carrera de vehículos usando `asyncio`.
La idea es observar cómo, al **solapar esperas**, el **tiempo de pared** del modo concurrente se acerca al **máximo** de los tiempos individuales, en lugar de a su **suma**.

![Salida del programa](docs/screenshot.png)

---

## 📁 Estructura real del repo
```
.
├─ main.py         # Punto de entrada (parsea CLI y lanza la comparación)
├─ carrera.py      # Lógica de carrera (async y secuencial), métricas y fábrica de vehículos
├─ models.py       # Jerarquía de vehículos (Vehiculo, Deportivo, Clasico, UsoDiario)
├─ spinner.py      # Animación retro (spinner ASCII) mientras corre la simulación
└─ util.py         # Utilidades (p. ej., pausa_aleatoria)
```

---

## ▶️ Uso
Requisitos: **Python 3.10+** (solo `stdlib`).

Ejecutar con valores por defecto (1000 m, seed 42):
```bash
python main.py
```

Parámetros CLI:
```bash
python main.py --dist 1500     # distancia en metros
python main.py --seed 123      # semilla para reproducibilidad
python main.py --verbose       # log de progreso por vehículo
```

---

## 🧩 Dónde se definen los vehículos
La flota de ejemplo **no** está en `main.py`. Se crea en la **fábrica** `crear_vehiculos_demo()` dentro de `carrera.py`. Ahí puedes:
- Cambiar los modelos,
- Agregar o quitar vehículos,
- O crear otra fábrica y pasarla como `vehiculos_factory`.

```python
# carrera.py
def crear_vehiculos_demo() -> List[Vehiculo]:
    return [
        Deportivo("Nissan GT-R R35"),
        Clasico("Ford Mustang 1967 Fastback"),
        UsoDiario("Toyota Corolla"),
        Deportivo("Porsche 911 Turbo S"),
        Clasico("Jaguar E-Type 1961"),
        UsoDiario("Kia Rio 5"),
    ]
```

Las **clases concretas** `Deportivo`, `Clasico` y `UsoDiario` están en `models.py`, con diferentes parámetros de velocidad base, confiabilidad y variabilidad.

---

## 🧠 Cómo funciona
- **Concurrente (`asyncio`)**: cada vehículo avanza por *ticks* (`step_distance`) y espera `step_delay + maybe_extra_delay`. Las esperas se **solapan**.
- **Secuencial**: mismo modelo pero con `time.sleep`, sin solapamiento.
- **Spinner**: animación `- \ | /` en segundo plano para darle estilo retro.
- **Métricas** que imprime:
  - Tiempo total **secuencial** (pared)
  - Tiempo total **concurrente** (pared) y **% de ahorro**
  - **Suma** de tiempos individuales (ambos modos)
  - **Máximo** tiempo individual (concurrente)
- **Podio**: listas de llegadas ordenadas por **menor tiempo**.

---

## 🧪 Consejos de prueba
- Fija `--seed` para resultados reproducibles.
- Sube `--dist` para carreras más largas.
- Ajusta parámetros en `models.py` (velocidad, varianza, confiabilidad) para ver distintos perfiles.
- Usa `--verbose` para inspeccionar el avance en tiempo real.

---

## 🔧 Extensiones posibles
- Interfaz de línea de comandos más rica (p. ej., `--vehiculos`, `--pista`).
- Integrar *logging* con niveles.
- Exportar resultados a CSV/JSON.
- Visualización con matplotlib o Rich.

---

## 📝 Licencia
MIT — 2025-09-08