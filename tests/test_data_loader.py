"""
Tests for the data loader module.
"""
import os
import pytest
import pandas as pd
from src.utils.data_loader import load_csv, save_csv, load_mapping


class TestDataLoader:
    """
    Test cases for the data loader functions.
    """

    def test_load_csv_valid_file(self, tmp_path):
        """Test loading a valid CSV file."""
        # Create test CSV file
        test_file = tmp_path / "test.csv"
        test_df = pd.DataFrame({
            'col1': [1, 2, 3],
            'col2': ['a', 'b', 'c']
        })
        test_df.to_csv(test_file, index=False)

        # Load the CSV file
        loaded_df = load_csv(test_file)

        # Verify data
        assert loaded_df.shape == (3, 2)
        assert list(loaded_df.columns) == ['col1', 'col2']
        assert loaded_df.iloc[0, 0] == 1
        assert loaded_df.iloc[0, 1] == 'a'

    def test_load_csv_file_not_found(self):
        """Test loading a non-existent CSV file."""
        with pytest.raises(FileNotFoundError):
            load_csv("non_existent_file.csv")

    def test_save_csv(self, tmp_path):
        """Test saving a DataFrame to a CSV file."""
        # Create test DataFrame
        test_df = pd.DataFrame({
            'col1': [1, 2, 3],
            'col2': ['a', 'b', 'c']
        })

        # Define output path
        output_file = tmp_path / "output" / "test_output.csv"

        # Save the DataFrame
        saved_path = save_csv(test_df, output_file)

        # Verify file exists
        assert os.path.exists(saved_path)

        # Verify file content
        saved_df = pd.read_csv(saved_path)
        assert saved_df.shape == (3, 2)
        assert list(saved_df.columns) == ['col1', 'col2']
        assert saved_df.iloc[0, 0] == 1
        assert saved_df.iloc[0, 1] == 'a'

    def test_load_mapping_valid_file(self, tmp_path):
        """Test loading mapping from a valid file."""
        # Create test mapping file
        test_file = tmp_path / "test_mapping.txt"
        mapping_content = """input\toutput
First (FP) + Last (FV)\tName (b)
Headline (FS)\tHeadline (d)
Country (B)\tcountry (R)
"""
        with open(test_file, 'w') as f:
            f.write(mapping_content)

        # Load the mapping
        mapping = load_mapping(test_file)

        # Verify mapping
        assert isinstance(mapping, dict)
        assert mapping['First (FP) + Last (FV)'] == 'Name (b)'
        assert mapping['Headline (FS)'] == 'Headline (d)'
        assert mapping['Country (B)'] == 'country (R)'

    def test_load_mapping_file_not_found(self):
        """Test loading mapping from a non-existent file."""
        with pytest.raises(FileNotFoundError):
            load_mapping("non_existent_mapping.txt")
