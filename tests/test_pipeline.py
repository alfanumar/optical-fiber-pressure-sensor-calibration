from pathlib import Path

from sensor_calibration.generate_data import generate_dataset
from sensor_calibration.report import analyze_dataset


def test_generated_dataset_can_be_analyzed(tmp_path: Path):
    data_path = tmp_path / "synthetic.csv"
    output_dir = tmp_path / "results"
    generate_dataset(data_path, seed=3)
    report = analyze_dataset(data_path, output_dir)

    assert report["sample_count"] == 48
    assert report["calibration_sample_count"] == 42
    assert report["validation_sample_count"] == 6
    assert (output_dir / "calibration_report.json").exists()
    assert (output_dir / "calibration_report.png").exists()

