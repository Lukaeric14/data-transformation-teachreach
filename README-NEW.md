# TeachReach Data Transformation

## Overview
The TeachReach Data Transformation project is a system for processing, cleaning, and transforming educational data, specifically teacher profiles. It converts complex nested teacher profile data into a structured format suitable for analytics, reporting, and visualization.

## Features
- Mapping-based data transformation from complex to simplified structure
- Field name normalization and standardization
- AI-powered field inference using OpenAI API for missing values
- Validation of input and output data
- Comprehensive logging and error handling
- Test-driven development approach

## Project Structure
```
data-transformation-teachReach/
├── README.md                   # Project documentation
├── requirements.txt            # Project dependencies
├── mappings.md                 # Field mappings
├── src/                        # Source code
│   ├── __init__.py             # Make src a package
│   ├── config.py               # Configuration settings
│   ├── transform.py            # Main transformation script
│   ├── transformers/           # Data transformation modules
│   │   ├── __init__.py
│   │   ├── base.py             # Base transformer class
│   │   └── teacher_data.py     # Teacher data transformer
│   └── utils/                  # Utility functions
│       ├── __init__.py
│       ├── data_loader.py      # Data loading utilities
│       ├── openai_client.py    # OpenAI API client for inference
│       └── validators.py       # Data validation utilities
├── data/                       # Data directory
│   ├── raw/                    # Raw data files
│   │   └── inputv2.csv         # Input data file
│   └── processed/              # Processed data files
│       └── output.csv          # Output data file
├── tests/                      # Test directory
│   ├── __init__.py
│   ├── test_data_loader.py
│   ├── test_openai_client.py
│   ├── test_teacher_data_transformer.py
│   └── test_validators.py
└── examples/                   # Example scripts
    └── basic_transformation.py # Basic transformation example
```

## Installation

```bash
# Clone the repository
git clone https://github.com/username/data-transformation-teachReach.git
cd data-transformation-teachReach

# Create and activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Setup

The project uses the OpenAI API for field inference. You'll need to set up your API key:

1. Get an API key from OpenAI (https://platform.openai.com/)
2. Create a `.env` file in the project root with:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

### Basic Usage

Run the main transformation script:

```bash
python -m src.transform
```

This will read data from the default input file (`data/raw/inputv2.csv`), transform it according to the mappings in `mappings.md`, and save the result to `data/processed/transformed_output.csv`.

### Custom Input/Output Paths

```bash
python -m src.transform --input /path/to/input.csv --output /path/to/output.csv --mapping /path/to/mappings.md
```

### Python API

```python
from src.utils.data_loader import load_csv, save_csv, load_mapping
from src.transformers.teacher_data import TeacherDataTransformer

# Load data and mappings
input_data = load_csv('data/raw/inputv2.csv')
mapping = load_mapping('mappings.md')

# Initialize transformer with OpenAI API key
transformer = TeacherDataTransformer(mapping, api_key='your_openai_api_key')

# Transform data
transformed_data = transformer.transform(input_data)

# Save results
save_csv(transformed_data, 'data/processed/output.csv', index=False)
```

## Testing

The project uses pytest for testing. Run the tests with:

```bash
python -m pytest tests/
```

For more detailed output:

```bash
python -m pytest tests/ -v
```

With coverage report:

```bash
python -m pytest tests/ --cov=src --cov-report=term-missing
```

## Field Mappings

Field mappings are defined in `mappings.md` and follow this format:

```
input	output
-	ID (a)
First (FP) + Last (FV)	Name (b)
Headline (FS)	Headline (d)
Country (B)	country (R)
```

There are three types of input mappings:
1. Direct field mappings (e.g., `Country (B)` → `country (R)`)
2. Combined field mappings (e.g., `First (FP) + Last (FV)` → `Name (b)`)
3. AI-inferred fields (e.g., `AI` → `Years of experience (P)`)

## Adding New Transformers

To add a new transformer:

1. Create a new module in the `src/transformers/` directory
2. Extend the `BaseTransformer` class
3. Implement the required methods
4. Add corresponding tests in the `tests/` directory

## License

MIT
