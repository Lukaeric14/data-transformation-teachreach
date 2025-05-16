"""
Tests for the teacher data transformer.
"""
import pytest
import pandas as pd
import uuid
from datetime import datetime
from unittest.mock import patch, MagicMock
from src.transformers.teacher_data import TeacherDataTransformer
from src.utils.openai_client import OpenAIClient


class TestTeacherDataTransformer:
    """
    Test cases for the TeacherDataTransformer.
    """

    @pytest.fixture
    def sample_input_data(self):
        """Fixture to provide sample input data."""
        return pd.DataFrame({
            'first_name': ['John', 'Jane', 'Alex'],
            'last_name': ['Doe', 'Smith', 'Johnson'],
            'headline': ['Math Teacher', 'Science Teacher', 'English Teacher'],
            'country': ['United Arab Emirates', 'United Kingdom', 'United States'],
            'city': ['Dubai', 'London', 'New York'],
            'email': ['john.doe@example.com', 'jane.smith@example.com', 'alex.johnson@example.com'],
            'linkedin_url': ['http://linkedin.com/in/johndoe', 'http://linkedin.com/in/janesmith', 'http://linkedin.com/in/alexjohnson'],
            'organization_name': ['GEMS Education', 'British School', 'American Academy'],
            'organization_website': ['gemseducation.com', 'britishschool.uk', 'americanacademy.edu']
        })

    @pytest.fixture
    def sample_mapping(self):
        """Fixture to provide sample mapping."""
        return {
            'first_name + last_name': 'name',
            'headline': 'headline',
            'country': 'current_location_country',
            'city': 'current_location_city',
            'email': 'Email',
            'linkedin_url': 'Linkedin URL',
            'organization_name': 'School',
            'organization_website': 'school website'
        }

    def test_initialization(self, sample_mapping):
        """Test initialization of transformer."""
        transformer = TeacherDataTransformer(sample_mapping)
        
        # Verify mapping is set correctly
        assert transformer.mapping == sample_mapping
        
        # Verify required columns are set
        assert 'teacher_id' in transformer.required_output_columns
        assert 'name' in transformer.required_output_columns
        assert 'current_location_country' in transformer.required_output_columns
        assert 'current_location_city' in transformer.required_output_columns

    def test_transform_basic(self, sample_input_data, sample_mapping):
        """Test basic transformation functionality."""
        transformer = TeacherDataTransformer(sample_mapping)
        
        # Transform the data
        transformed_data = transformer.transform(sample_input_data)
        
        # Verify basic properties of the transformed data
        assert isinstance(transformed_data, pd.DataFrame)
        assert len(transformed_data) == len(sample_input_data)
        
        # Verify required columns exist
        for col in transformer.required_output_columns:
            assert col in transformed_data.columns
            
        # Verify mapped fields were transformed correctly
        assert transformed_data.iloc[0]['name'] == 'John Doe'
        assert transformed_data.iloc[0]['headline'] == 'Math Teacher'
        assert transformed_data.iloc[0]['current_location_country'] == 'United Arab Emirates'
        assert transformed_data.iloc[0]['current_location_city'] == 'Dubai'
        assert transformed_data.iloc[0]['Email'] == 'john.doe@example.com'
        assert transformed_data.iloc[0]['School'] == 'GEMS Education'

    def test_validate_input(self, sample_input_data):
        """Test input validation."""
        transformer = TeacherDataTransformer()
        
        # Valid input
        assert transformer.validate_input(sample_input_data) is True
        
        # Invalid input: not a DataFrame
        assert transformer.validate_input("not a dataframe") is False
        
        # Invalid input: empty DataFrame
        assert transformer.validate_input(pd.DataFrame()) is False

    def test_validate_output(self):
        """Test output validation."""
        transformer = TeacherDataTransformer()
        
        # Valid output
        valid_output = pd.DataFrame({
            'teacher_id': ['123'],
            'name': ['John Doe'],
            'subject': ['Math'],
            'headline': ['Math Teacher'],
            'current_location_country': ['UAE'],
            'current_location_city': ['Dubai']
        })
        assert transformer.validate_output(valid_output) is True
        
        # Invalid output: not a DataFrame
        assert transformer.validate_output("not a dataframe") is False
        
        # Invalid output: empty DataFrame
        assert transformer.validate_output(pd.DataFrame()) is False
        
        # Invalid output: missing required column
        invalid_output = pd.DataFrame({
            'teacher_id': ['123'],
            'name': ['John Doe'],
            # 'subject' is missing
            'headline': ['Math Teacher'],
            'current_location_country': ['UAE'],
            'current_location_city': ['Dubai']
        })
        assert transformer.validate_output(invalid_output) is False

    def test_transform_with_missing_fields(self, sample_mapping):
        """Test transformation with missing input fields."""
        # Input with missing fields
        input_data = pd.DataFrame({
            'first_name': ['John', 'Jane', None],
            'last_name': ['Doe', None, 'Johnson'],
            'headline': ['Math Teacher', None, 'English Teacher'],
            # country is completely missing
            'city': ['Dubai', 'London', None],
        })
        
        transformer = TeacherDataTransformer(sample_mapping)
        
        # Transform the data
        transformed_data = transformer.transform(input_data)
        
        # Verify defaults were applied
        assert transformed_data.iloc[1]['name'].startswith('Jane')  # last name might be default
        assert pd.notna(transformed_data.iloc[2]['name'])  # Should have a default first name
        assert pd.notna(transformed_data.iloc[1]['headline'])  # Should have default headline
        
        # All records should have current_location_country filled with defaults
        assert all(pd.notna(transformed_data['current_location_country']))
        
        # Missing city for third record should be filled
        assert pd.notna(transformed_data.iloc[2]['current_location_city'])

    @patch.object(OpenAIClient, 'infer_multiple_fields')
    def test_infer_fields(self, mock_infer_fields, sample_input_data):
        """Test the field inference functionality with mocked OpenAI client."""
        # Set up mock return value for OpenAI client
        mock_infer_fields.return_value = {
            'Years of experience (P)': 10,
            'Subject (Array) (c)': ['Mathematics', 'Physics'],
            'Preferred curriculumn (O)': 'British',
            'Nationality (Z)': 'British'
        }
        
        # Add AI inference mapping
        mapping = {
            'first_name + last_name': 'name',
            'headline': 'headline',
            'country': 'current_location_country',
            'city': 'current_location_city',
            'AI': 'Years of experience (P)',
            'AI': 'Subject (Array) (c)',
            'AI': 'Preferred curriculumn (O)',
            'AI': 'Nationality (Z)'
        }
        
        transformer = TeacherDataTransformer(mapping)
        
        # Transform the data
        transformed_data = transformer.transform(sample_input_data)
        
        # Verify OpenAI client was called correctly
        assert mock_infer_fields.call_count > 0
        for call_args in mock_infer_fields.call_args_list:
            args, kwargs = call_args
            # Check that we're passing expected field names
            assert set(args[0]) & {'Years of experience (P)', 'Subject (Array) (c)', 
                                  'Preferred curriculumn (O)', 'Nationality (Z)'}
            # Check we're passing teacher data as a dict
            assert isinstance(args[1], dict)
        
        # Verify inferred fields were properly applied to output
        if 'Years of experience (P)' in transformed_data.columns:
            assert transformed_data['Years of experience (P)'].iloc[0] == 10
            
        if 'Subject (Array) (c)' in transformed_data.columns:
            assert transformed_data['Subject (Array) (c)'].iloc[0] == ['Mathematics', 'Physics']
            
        if 'Preferred curriculumn (O)' in transformed_data.columns:
            assert transformed_data['Preferred curriculumn (O)'].iloc[0] == 'British'
            
        if 'Nationality (Z)' in transformed_data.columns:
            assert transformed_data['Nationality (Z)'].iloc[0] == 'British'

    def test_get_default_value(self):
        """Test the default value generation."""
        transformer = TeacherDataTransformer()
        
        # Test default values for required fields
        assert transformer._get_default_value('teacher_id') is not None
        assert transformer._get_default_value('name') == 'Unknown Teacher'
        assert transformer._get_default_value('subject') == 'General Education'
        assert transformer._get_default_value('headline') == 'Teacher'
        assert transformer._get_default_value('current_location_country') == 'Unknown'
        assert transformer._get_default_value('current_location_city') == 'Unknown'
        
        # Test default value for non-required field
        assert transformer._get_default_value('non_existent_field') is None

    def test_get_output_columns(self, sample_mapping):
        """Test getting output columns."""
        transformer = TeacherDataTransformer(sample_mapping)
        
        output_columns = transformer.get_output_columns()
        
        # Verify all mapped output fields are included
        for output_field in sample_mapping.values():
            assert output_field in output_columns
            
        # Verify required columns are included
        for col in transformer.required_output_columns:
            assert col in output_columns
            
        # Verify created_at is included
        assert 'created_at' in output_columns
