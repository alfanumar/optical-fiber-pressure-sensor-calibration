"""Calibration fitting and validation metrics."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class LinearCalibration:
    """Model for estimating pressure from a raw ADC value."""

    slope: float
    intercept: float

    def predict(self, raw_adc: np.ndarray | float) -> np.ndarray:
        return self.slope * np.asarray(raw_adc, dtype=float) + self.intercept

    @property
    def equation(self) -> str:
        return f"pressure_kpa = {self.slope:.8f} * raw_adc + {self.intercept:.8f}"


def fit_linear_calibration(raw_adc: np.ndarray, reference_pressure: np.ndarray) -> LinearCalibration:
    """Fit pressure = slope * ADC + intercept using least squares."""

    raw_adc = np.asarray(raw_adc, dtype=float)
    reference_pressure = np.asarray(reference_pressure, dtype=float)
    if raw_adc.size != reference_pressure.size or raw_adc.size < 2:
        raise ValueError("ADC and reference arrays must have the same size >= 2")
    if np.allclose(raw_adc, raw_adc[0]):
        raise ValueError("Calibration requires varying ADC values")

    design = np.column_stack((raw_adc, np.ones(raw_adc.size)))
    slope, intercept = np.linalg.lstsq(design, reference_pressure, rcond=None)[0]
    return LinearCalibration(float(slope), float(intercept))


def regression_metrics(reference_pressure: np.ndarray, predicted_pressure: np.ndarray) -> dict[str, float]:
    """Return common regression and absolute-error metrics."""

    reference_pressure = np.asarray(reference_pressure, dtype=float)
    predicted_pressure = np.asarray(predicted_pressure, dtype=float)
    errors = predicted_pressure - reference_pressure
    ss_res = float(np.sum(errors**2))
    ss_tot = float(np.sum((reference_pressure - np.mean(reference_pressure)) ** 2))
    return {
        "mae_kpa": float(np.mean(np.abs(errors))),
        "rmse_kpa": float(np.sqrt(np.mean(errors**2))),
        "max_abs_error_kpa": float(np.max(np.abs(errors))),
        "r2": 1.0 - ss_res / ss_tot if ss_tot else 0.0,
    }

