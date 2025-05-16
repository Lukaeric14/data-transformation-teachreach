"""
Utility functions for loading data from various sources.
"""
import os
import pandas as pd


def load_csv(file_path, **kwargs):
    """
    Load data from a CSV file.
    
    Args:
        file_path (str): Path to the CSV file.
        **kwargs: Additional arguments to pass to pandas.read_csv.
        
    Returns:
        pandas.DataFrame: The loaded data.
        
    Raises:
        FileNotFoundError: If the file does not exist.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    return pd.read_csv(file_path, **kwargs)


def save_csv(data, file_path, **kwargs):
    """
    Save data to a CSV file.
    
    Args:
        data (pandas.DataFrame): The data to save.
        file_path (str): Path to the CSV file.
        **kwargs: Additional arguments to pass to pandas.to_csv.
        
    Returns:
        str: The path to the saved file.
    """
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    # Save the data with index=False by default
    if 'index' not in kwargs:
        kwargs['index'] = False
    data.to_csv(file_path, **kwargs)
    
    return file_path


def load_mapping(file_path):
    """
    Load mapping from a mapping file.
    
    Args:
        file_path (str): Path to the mapping file.
        
    Returns:
        dict: A dictionary mapping input fields to output fields.
        
    Raises:
        FileNotFoundError: If the file does not exist.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Mapping file not found: {file_path}")
    
    # For basic text mapping files (tab-separated)
    mapping = {}
    with open(file_path, 'r') as f:
        lines = f.readlines()
        
        # Skip header line
        for line in lines[1:]:
            if not line.strip() or line.startswith('Inferred'):
                continue
                
            parts = line.strip().split('\t')
            if len(parts) >= 2:
                input_field = parts[0].strip()
                output_field = parts[1].strip()
                
                # Skip empty mappings
                if input_field and output_field:
                    mapping[input_field] = output_field
    
    return mapping
