"""Generate a transparent synthetic calibration dataset."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import numpy as np


def generate_dataset(
    output_path: Path,
    pressures_kpa: tuple[float, ...] = (0.0, 10.0, 20.0, 30.0, 40.0, 50.0),
    repeats: int = 8,
    seed: int = 11,
) -> None:
    """Write deterministic synthetic reference-pressure and ADC readings.

    The response includes small quadratic nonlinearity and Gaussian noise to
    make the calibration report more realistic. It is not a physical model of
    a particular optical-fiber sensor.
    """

    if repeats < 2:
        raise ValueError("repeats must be at least 2 for validation samples")

    rng = np.random.default_rng(seed)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, float | int]] = []
    for pressure in pressures_kpa:
        for replicate in range(1, repeats + 1):
            ideal_adc = 410.0 + 2.25 * pressure + 0.0012 * pressure**2
            noisy_adc = ideal_adc + float(rng.normal(0.0, 1.5))
            rows.append(
                {
                    "reference_pressure_kpa": pressure,
                    "raw_adc": round(noisy_adc, 5),
                    "replicate": replicate,
                }
            )

    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("data/generated_synthetic_calibration.csv"))
    parser.add_argument("--seed", type=int, default=11)
    args = parser.parse_args()
    generate_dataset(args.output, seed=args.seed)
    print(f"Wrote synthetic dataset to {args.output}")


if __name__ == "__main__":
    main()

