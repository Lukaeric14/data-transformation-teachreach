"""
Utility functions for validating data.
"""
import pandas as pd
import re


def validate_column_existence(df, required_columns):
    """
    Validate that a DataFrame contains all required columns.
    
    Args:
        df (pandas.DataFrame): The DataFrame to validate.
        required_columns (list): List of required column names.
        
    Returns:
        bool: True if all required columns exist, False otherwise.
    """
    return all(col in df.columns for col in required_columns)


def validate_email_format(df, email_column):
    """
    Validate that all values in a column are valid email addresses.
    
    Args:
        df (pandas.DataFrame): The DataFrame to validate.
        email_column (str): The name of the column containing email addresses.
        
    Returns:
        bool: True if all values are valid emails or empty, False otherwise.
    """
    if email_column not in df.columns:
        return False
    
    # Simple regex for email validation
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    # Check each non-empty email
    for email in df[email_column].dropna():
        if not re.match(email_pattern, str(email)):
            return False
    
    return True


def validate_data_types(df, column_types):
    """
    Validate that columns in a DataFrame have the expected data types.
    
    Args:
        df (pandas.DataFrame): The DataFrame to validate.
        column_types (dict): Dictionary mapping column names to expected data types.
        
    Returns:
        bool: True if all columns have the expected data types, False otherwise.
    """
    for column, dtype in column_types.items():
        if column not in df.columns:
            return False
        
        # Skip validation for columns with all NA values
        if df[column].isna().all():
            continue
        
        # Check if column can be cast to the specified type
        try:
            # First check original types before casting
            original_values = df[column].dropna()
            
            # For string type, ensure all values are either strings or can be converted to strings
            if dtype == 'str':
                # Check if all non-null values are strings
                if not all(isinstance(val, str) or 
                          (isinstance(val, (int, float, bool)) and str(val) == val) 
                          for val in original_values):
                    return False
            
            # For numeric types, ensure all values are numeric
            elif dtype in ['int', 'float']:
                if not all(isinstance(val, (int, float)) for val in original_values):
                    return False
            
            # For boolean type, ensure all values are boolean
            elif dtype == 'bool':
                if not all(isinstance(val, bool) for val in original_values):
                    return False
            
            # Try to cast the series as a final check
            pd.Series(original_values).astype(dtype)
            
        except (ValueError, TypeError):
            return False
    
    return True


def validate_non_empty(df, required_non_empty_columns):
    """
    Validate that required columns in a DataFrame are not empty.
    
    Args:
        df (pandas.DataFrame): The DataFrame to validate.
        required_non_empty_columns (list): List of columns that should not be empty.
        
    Returns:
        bool: True if all required columns are not empty, False otherwise.
    """
    for column in required_non_empty_columns:
        if column not in df.columns:
            return False
        
        if df[column].isna().any() or (df[column] == '').any():
            return False
    
    return True
