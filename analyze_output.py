"""
Script to analyze the transformed output file and compare it with expected specifications.
"""
import os
import pandas as pd
from src.utils.data_loader import load_csv

def analyze_output_file():
    """Analyze the transformed output file and print detailed information."""
    # Check if the output file exists
    output_file = 'data/processed/transformed_output.csv'
    if not os.path.exists(output_file):
        print(f"Output file {output_file} does not exist.")
        return
        
    # Load the transformed output file
    transformed_data = load_csv(output_file)
    
    print("\n" + "="*80)
    print("TRANSFORMATION OUTPUT ANALYSIS")
    print("="*80)
    
    print(f"\nExamining actual output file with {len(transformed_data)} records")
    print(f"Columns: {transformed_data.columns.tolist()}")
    
    # Check header names
    header_check = {'correct': [], 'incorrect': [], 'missing': []}
    expected_headers = [
        'ID (a)',
        'Name (b)',
        'Headline (d)',
        'country (R)',
        'city (s)',
        'Linkedin URL (u)',
        'School (AA)',
        'school website (AB)',
        'Email (AC)',
        'Source ID (AD)',
        'Years of experience (P)',
        'Subject (Array) (c)',
        'Preferred curriculumn (O)',
        'Nationality (Z)',
        'Preferred age range (V)',
        'teacher_id'
    ]
    
    for header in expected_headers:
        if header in transformed_data.columns:
            header_check['correct'].append(header)
        else:
            header_check['missing'].append(header)
    
    for header in transformed_data.columns:
        if header not in expected_headers and header != 'created_at':
            header_check['incorrect'].append(header)
    
    print(f"\nHeader check results:")
    print(f"Correct headers: {header_check['correct']}")
    print(f"Missing headers: {header_check['missing']}")
    print(f"Unexpected headers: {header_check['incorrect']}")
    
    # Check for duplicate headers (case-insensitive)
    header_lower = [h.lower() for h in transformed_data.columns]
    duplicates = []
    for h in header_lower:
        if header_lower.count(h) > 1 and h not in duplicates:
            duplicates.append(h)
    print(f"\nDuplicate headers (case-insensitive): {duplicates}")
    
    # Check for potential duplicate fields (different casing)
    case_inconsistencies = {}
    for header in transformed_data.columns:
        header_lower = header.lower()
        if header_lower in case_inconsistencies:
            case_inconsistencies[header_lower].append(header)
        else:
            case_inconsistencies[header_lower] = [header]
    
    potential_issues = {k: v for k, v in case_inconsistencies.items() if len(v) > 1}
    if potential_issues:
        print("\nPotential case inconsistency issues:")
        for base, variants in potential_issues.items():
            print(f"  {base}: {variants}")
    
    # Check sample data
    print(f"\nSample data (first row):")
    if len(transformed_data) > 0:
        for col in transformed_data.columns:
            value = transformed_data.iloc[0][col]
            print(f"{col}: {value}")
        
    # Validate required fields are filled
    empty_counts = {}
    for col in transformed_data.columns:
        empty_count = transformed_data[col].isna().sum()
        if empty_count > 0:
            empty_counts[col] = empty_count
    
    print(f"\nFields with empty values: {empty_counts}")
    
    # Check data consistency
    print("\nData consistency checks:")
    
    # Check Name field
    if 'Name (b)' in transformed_data.columns:
        unknown_count = (transformed_data['Name (b)'] == 'Unknown Teacher').sum()
        print(f"  Records with 'Unknown Teacher' name: {unknown_count} of {len(transformed_data)}")
    
    # Check for country/location fields
    loc_fields = [col for col in transformed_data.columns if 'country' in col.lower()]
    for field in loc_fields:
        unknown_count = (transformed_data[field] == 'Unknown').sum()
        print(f"  Records with 'Unknown' {field}: {unknown_count} of {len(transformed_data)}")
    
    print("="*80)

if __name__ == "__main__":
    analyze_output_file()
