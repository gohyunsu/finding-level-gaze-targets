# Contributing

Contributions that improve portability, documentation, or test coverage are
welcome. Changes to experimental definitions or reported values must keep the
study configuration, machine-readable result registry, README, and independent
validator synchronized.

## Development setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
python verify_results.py
python scripts/render_readme_assets.py --check
pytest -q
```

Do not commit source datasets, clinical records, patient-level outputs, caches,
model checkpoints, radiographs, report text, or manuscript files. Keep every
learned preprocessing and calibration step within the corresponding training or
validation partition.
