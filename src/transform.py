"""
Main script for transforming TeachReach teacher data.
"""
import os
import argparse
import pandas as pd
from dotenv import load_dotenv
from src.utils.data_loader import load_csv, save_csv, load_mapping
from src.transformers.teacher_data import TeacherDataTransformer
from src.config import (
    INPUT_FILE,
    OUTPUT_FILE,
    MAPPING_FILE,
    CLEAN_FIELD_MAPPINGS
)


def main(input_file=None, output_file=None, mapping_file=None):
    """
    Run the data transformation process.
    
    Args:
        input_file (str, optional): Path to the input CSV file.
        output_file (str, optional): Path to the output CSV file.
        mapping_file (str, optional): Path to the mapping file.
    """
    # Use provided paths or defaults from config
    input_file = input_file or INPUT_FILE
    output_file = output_file or OUTPUT_FILE
    mapping_file = mapping_file or MAPPING_FILE

    print(f"Starting transformation process...")
    print(f"- Input file: {input_file}")
    print(f"- Output file: {output_file}")
    print(f"- Mapping file: {mapping_file}")

    # Load the mapping
    try:
        if os.path.exists(mapping_file):
            print("Loading field mappings from file...")
            mapping = load_mapping(mapping_file)
        else:
            print("Mapping file not found, using default mappings...")
            mapping = CLEAN_FIELD_MAPPINGS
            
        print(f"Loaded {len(mapping)} field mappings.")
    except Exception as e:
        print(f"Error loading mapping: {e}")
        print("Using default mappings...")
        mapping = CLEAN_FIELD_MAPPINGS

    # Load the input data
    try:
        print("Loading input data...")
        input_data = load_csv(input_file)
        print(f"Loaded {len(input_data)} records from input file.")
    except Exception as e:
        print(f"Error loading input data: {e}")
        return

    # Load API key from environment
    load_dotenv()
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Error: No OpenAI API key found. Please set OPENAI_API_KEY in your environment.")
        return
    
    # Initialize the transformer with API key
    transformer = TeacherDataTransformer(mapping, api_key=api_key)

    # Transform the data
    try:
        print("Transforming data...")
        transformed_data = transformer.transform(input_data)
        print(f"Transformed {len(transformed_data)} records.")
    except Exception as e:
        print(f"Error during transformation: {e}")
        return

    # Save the transformed data
    try:
        print(f"Saving transformed data to {output_file}...")
        save_csv(transformed_data, output_file, index=False)
        print("Transformation complete!")
    except Exception as e:
        print(f"Error saving transformed data: {e}")
        return


if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Transform TeachReach data")
    parser.add_argument("--input", help="Path to input CSV file")
    parser.add_argument("--output", help="Path to output CSV file")
    parser.add_argument("--mapping", help="Path to mapping file")
    args = parser.parse_args()

    # Run the transformation
    main(args.input, args.output, args.mapping)
