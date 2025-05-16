"""
Configuration settings for the TeachReach data transformation project.
"""
import os

# Project paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, 'processed')

# Input and output file paths
INPUT_FILE = os.path.join(RAW_DATA_DIR, 'inputv2.csv')
OUTPUT_FILE = os.path.join(PROCESSED_DATA_DIR, 'transformed_output.csv')
MAPPING_FILE = os.path.join(PROJECT_ROOT, 'mappings.md')

# Required fields in the output
REQUIRED_OUTPUT_FIELDS = [
    'teacher_id', 'name', 'subject', 'headline',
    'current_location_country', 'current_location_city'
]

# Field mappings based on the mappings.md file
# These are defaults and will be overridden by the mappings file if it exists
DEFAULT_FIELD_MAPPINGS = {
    '-': 'ID (a)',
    'First (FP) + Last (FV)': 'Name (b)',
    'Headline (FS)': 'Headline (d)',
    'Country (B)': 'country (R)',
    'City (A)': 'city (s)',
    'Linkedin URL (FW)': 'Linkedin URL (u)',
    'organization (U)': 'School (AA)',
    'organization website': 'school website (AB)',
    'Email E': 'Email (AC)',
    'ID': 'Source ID (AD)',
    'AI': 'Years of experience (P)',
    'AI': 'Subject (Array) (c)',
    'AI': 'Preferred curriculumn (O)',
    'AI': 'Nationality (Z)'
}

# Clean column name mappings (remove the parenthetical codes)
def clean_column_name(name):
    """Clean column names by removing parenthetical codes."""
    import re
    return re.sub(r'\s*\([a-zA-Z0-9]+\)\s*$', '', name).strip()

# Apply the cleaning to get clean field mappings
CLEAN_FIELD_MAPPINGS = {
    key: clean_column_name(value) for key, value in DEFAULT_FIELD_MAPPINGS.items()
}
