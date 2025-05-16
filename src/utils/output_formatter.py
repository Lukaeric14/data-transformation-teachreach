"""
Utility to standardize the output format for the TeachReach data transformation.
"""
import pandas as pd
from datetime import datetime
from src.mappings.output_format import (
    DESIRED_OUTPUT_HEADERS,
    FIELD_MAPPING,
    DEFAULT_VALUES,
    CALCULATED_FIELDS
)

def standardize_output(df):
    """
    Standardize the output DataFrame to match the desired format.
    
    Args:
        df (pd.DataFrame): The DataFrame to standardize.
        
    Returns:
        pd.DataFrame: The standardized DataFrame with the correct column order and names.
    """
    # Start with a new DataFrame with the desired columns
    result = pd.DataFrame(columns=DESIRED_OUTPUT_HEADERS)
    
    # Map existing fields to desired output fields
    for src_field, dest_field in FIELD_MAPPING.items():
        if src_field in df.columns and pd.notna(df[src_field]).any():
            # Copy values from source field to destination field
            result[dest_field] = df[src_field]
    
    # Apply default values for missing fields
    for field, default_value in DEFAULT_VALUES.items():
        if field not in result.columns or result[field].isna().all():
            result[field] = default_value
        elif result[field].isna().any():
            # Fill NaN values with default
            result[field] = result[field].fillna(default_value)
    
    # Ensure all calculated fields exist with empty defaults
    for field in CALCULATED_FIELDS:
        if field not in result.columns:
            result[field] = ""
    
    # Ensure teacher_id and created_at fields are always present
    if 'teacher_id' not in result.columns or result['teacher_id'].isna().all():
        if 'teacher_id' in df.columns:
            result['teacher_id'] = df['teacher_id']
        else:
            # This should not happen as teacher_id should always be present
            raise ValueError("teacher_id field is missing from the input DataFrame")
    
    if 'created_at' not in result.columns or result['created_at'].isna().all():
        if 'created_at' in df.columns:
            result['created_at'] = df['created_at']
        else:
            # Add the current timestamp if missing
            result['created_at'] = datetime.now().isoformat()
    
    # Fill any remaining empty fields with empty strings or appropriate defaults
    for field in DESIRED_OUTPUT_HEADERS:
        if field not in result.columns:
            if field in ['subjects_count', 'profile_completion_percentage', 'hourly_rate', 'monthly_salary_expectation']:
                result[field] = 0
            elif field in ['willing_to_relocate']:
                result[field] = False
            else:
                result[field] = ""
    
    # Use preferred name, using 'name' as default and falling back to 'Name (b)' if available
    if 'name' in result.columns and result['name'].isna().any():
        if 'Name (b)' in df.columns:
            # Fill NaN values in 'name' with values from 'Name (b)' where available
            result['name'] = result['name'].fillna(df['Name (b)'])
        else:
            # Fill any remaining NaN values with "Unknown Teacher"
            result['name'] = result['name'].fillna("Unknown Teacher")
    
    # Reorder the columns to match the desired order
    result = result[DESIRED_OUTPUT_HEADERS]
    
    return result
