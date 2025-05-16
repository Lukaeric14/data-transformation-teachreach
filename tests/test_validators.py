"""
Tests for the validators module.
"""
import pytest
import pandas as pd
from src.utils.validators import (
    validate_column_existence,
    validate_email_format,
    validate_data_types,
    validate_non_empty
)


class TestValidators:
    """
    Test cases for the validator functions.
    """

    def test_validate_column_existence(self):
        """Test validating column existence in DataFrame."""
        # Create test DataFrame
        test_df = pd.DataFrame({
            'col1': [1, 2, 3],
            'col2': ['a', 'b', 'c'],
            'col3': [True, False, True]
        })

        # Test with all columns existing
        assert validate_column_existence(test_df, ['col1', 'col2', 'col3']) is True

        # Test with some columns missing
        assert validate_column_existence(test_df, ['col1', 'col4']) is False

        # Test with empty required columns
        assert validate_column_existence(test_df, []) is True

    def test_validate_email_format(self):
        """Test validating email format in DataFrame."""
        # Create test DataFrame with emails
        test_df = pd.DataFrame({
            'valid_emails': ['user@example.com', 'another@test.org', None],
            'invalid_emails': ['user@example.com', 'invalid-email', 'another@test'],
            'not_emails': [1, 2, 3]
        })

        # Test with valid emails
        assert validate_email_format(test_df, 'valid_emails') is True

        # Test with invalid emails
        assert validate_email_format(test_df, 'invalid_emails') is False

        # Test with non-existent column
        assert validate_email_format(test_df, 'non_existent') is False

    def test_validate_data_types(self):
        """Test validating data types in DataFrame."""
        # Create test DataFrame
        test_df = pd.DataFrame({
            'integers': [1, 2, 3],
            'strings': ['a', 'b', 'c'],
            'booleans': [True, False, True],
            'mixed': [1, 'b', True],
            'all_na': [None, None, None]
        })

        # Test with matching data types
        assert validate_data_types(test_df, {
            'integers': 'int',
            'strings': 'str',
            'booleans': 'bool'
        }) is True

        # Test with mismatched data types
        assert validate_data_types(test_df, {
            'integers': 'str',
            'strings': 'int'
        }) is False

        # Test with mixed data types
        assert validate_data_types(test_df, {
            'mixed': 'str'
        }) is False

        # Test with non-existent column
        assert validate_data_types(test_df, {
            'non_existent': 'int'
        }) is False

        # Test with all NA column (should pass as NA can be any type)
        assert validate_data_types(test_df, {
            'all_na': 'int'
        }) is True

    def test_validate_non_empty(self):
        """Test validating non-empty fields in DataFrame."""
        # Create test DataFrame
        test_df = pd.DataFrame({
            'all_filled': [1, 2, 3],
            'some_empty': [1, None, 3],
            'all_empty': [None, None, None],
            'empty_strings': ['a', '', 'c']
        })

        # Test with all filled columns
        assert validate_non_empty(test_df, ['all_filled']) is True

        # Test with some empty values
        assert validate_non_empty(test_df, ['some_empty']) is False

        # Test with all empty values
        assert validate_non_empty(test_df, ['all_empty']) is False

        # Test with empty strings
        assert validate_non_empty(test_df, ['empty_strings']) is False

        # Test with non-existent column
        assert validate_non_empty(test_df, ['non_existent']) is False

        # Test with multiple columns
        assert validate_non_empty(test_df, ['all_filled', 'all_filled']) is True
        assert validate_non_empty(test_df, ['all_filled', 'some_empty']) is False
