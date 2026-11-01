# Optical-Fiber Pressure Sensor Calibration and Validation

This project turns raw ADC readings into a transparent calibration workflow
for an optical-fiber pressure sensor prototype:

```text
reference pressure + raw ADC readings -> least-squares calibration
                                          |
                                          v
                              validation metrics and residual plot
```

The pipeline generates repeated synthetic calibration samples, fits a linear
pressure-from-ADC model, holds out one replicate at each pressure point, and
reports MAE, RMSE, maximum absolute error, and R².

This is a software validation project. It does not claim a physical sensor
measurement, confirmed photodetector circuit, calibrated ADC, or optical-fiber
transfer function. The original sensor setup must be measured before real
hardware results are added. See `data/README.md` and `media/README.md`.

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt

python3 -m sensor_calibration.generate_data \
  --output data/generated_synthetic_calibration.csv

python3 -m sensor_calibration.report \
  data/generated_synthetic_calibration.csv \
  --output-dir results

python3 -m pytest -q
```

The analysis produces:

- `results/calibration_report.json` — model equation and metrics;
- `results/calibration_report.png` — fit and residual plots.

## What this demonstrates

- ADC data ingestion and validation;
- linear sensor calibration with least squares;
- repeatability-aware calibration/validation split;
- residual analysis and error metrics;
- a cautious Arduino acquisition template.

## Honest next steps

1. Replace the synthetic CSV with measurements from the real sensor setup.
2. Document the optical coupling, photodetector, ADC resolution, and pressure
   reference instrument.
3. Compare linear and polynomial calibration only after enough real data is
   available.
4. Add uncertainty and hysteresis analysis from increasing/decreasing pressure
   cycles.

