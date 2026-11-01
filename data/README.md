# Data policy

The default dataset is synthetic. It represents repeated ADC readings at known
reference pressure points so the software workflow can be tested without the
original optical setup.

The generated data includes a deliberately small nonlinearity and random
noise. This does not establish the transfer function of the real sensor. To
replace it with real measurements, record the reference pressure, raw ADC
value, replicate number, photodetector setup, ADC resolution, sampling rate,
and environmental conditions.

