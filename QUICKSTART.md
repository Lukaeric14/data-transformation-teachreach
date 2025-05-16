# Quick Start Guide

## 1. Install Dependencies

```bash
brew install python3
pip3 install pandas pytest
```

## 2. Run Transformation

```bash
python3 src/transform.py
```

## 3. Run Tests

```bash
pytest tests/test_output_specifications.py -v
```

## 4. View Output

The transformed data will be saved in:
- `data/processed/transformed_output.csv`
