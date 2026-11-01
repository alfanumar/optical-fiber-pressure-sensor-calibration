import numpy as np
import pytest

from sensor_calibration.calibration import fit_linear_calibration, regression_metrics


def test_linear_fit_recovers_known_model():
    adc = np.array([100.0, 200.0, 300.0])
    pressure = 0.05 * adc - 5.0
    model = fit_linear_calibration(adc, pressure)

    assert model.slope == pytest.approx(0.05)
    assert model.intercept == pytest.approx(-5.0)
    assert np.allclose(model.predict(adc), pressure)


def test_metrics_are_zero_for_perfect_prediction():
    values = np.array([0.0, 1.0, 2.0])
    metrics = regression_metrics(values, values)

    assert metrics["mae_kpa"] == pytest.approx(0.0)
    assert metrics["rmse_kpa"] == pytest.approx(0.0)
    assert metrics["max_abs_error_kpa"] == pytest.approx(0.0)
    assert metrics["r2"] == pytest.approx(1.0)


def test_constant_adc_is_rejected():
    with pytest.raises(ValueError):
        fit_linear_calibration(np.array([100.0, 100.0]), np.array([0.0, 1.0]))

