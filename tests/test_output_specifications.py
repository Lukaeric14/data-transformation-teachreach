"""
Tests to verify that the output CSV file meets the exact specifications.
"""
import os
import pytest
import pandas as pd
from src.utils.data_loader import load_csv

class TestOutputSpecifications:
    """
    Test class to verify output CSV specifications.
    """
    
    @pytest.fixture
    def expected_headers(self):
        """Fixture providing the exact expected headers in the correct order."""
        return [
            'teacher_id',
            'name',
            'subject',
            'headline',
            'bio',
            'profile_completion_percentage',
            'profile_visibility',
            'preferred_teaching_modes',
            'willing_to_relocate',
            'hourly_rate',
            'monthly_salary_expectation',
            'available_start_date',
            'cv_resume_url',
            'video_intro_url',
            'preferred_curriculum_experience',
            'years_of_teaching_experience',
            'work_authorization_status',
            'current_location_country',
            'current_location_city',
            'background_check_status',
            'linkedin_profile_url',
            'preferred_grade_level',
            'subjects_count',
            'created_at',
            'Embeddings',
            'Nationality',
            'Current school',
            'School website',
            'Email',
            'Source ID'
        ]
    
    def test_header_order_exact_match(self, expected_headers):
        """Test that the CSV file has exactly the specified headers in the exact order."""
        # Define the paths to the transformed output
        output_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data/processed/transformed_output.csv')
        
        # Check if the output file exists
        if not os.path.exists(output_file):
            pytest.skip(f"Output file {output_file} does not exist. Run the transformation first.")
        
        # Load the output CSV
        output_data = load_csv(output_file)
        
        # Get actual headers
        actual_headers = output_data.columns.tolist()
        
        # First, check that the length matches
        assert len(actual_headers) == len(expected_headers), \
            f"Expected {len(expected_headers)} headers, but got {len(actual_headers)}. " \
            f"Difference: {set(expected_headers).symmetric_difference(set(actual_headers))}"
        
        # Then check each header in order
        for i, (expected, actual) in enumerate(zip(expected_headers, actual_headers)):
            assert expected == actual, \
                f"Header mismatch at position {i}. Expected '{expected}', but got '{actual}'"
    
    def test_no_missing_headers(self, expected_headers):
        """Test that no expected headers are missing."""
        # Define the paths to the transformed output
        output_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data/processed/transformed_output.csv')
        
        # Check if the output file exists
        if not os.path.exists(output_file):
            pytest.skip(f"Output file {output_file} does not exist. Run the transformation first.")
        
        # Load the output CSV
        output_data = load_csv(output_file)
        
        # Get actual headers
        actual_headers = output_data.columns.tolist()
        
        # Check for missing headers
        missing_headers = set(expected_headers) - set(actual_headers)
        assert not missing_headers, f"Missing headers: {missing_headers}"
    
    def test_no_extra_headers(self, expected_headers):
        """Test that there are no unexpected headers."""
        # Define the paths to the transformed output
        output_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data/processed/transformed_output.csv')
        
        # Check if the output file exists
        if not os.path.exists(output_file):
            pytest.skip(f"Output file {output_file} does not exist. Run the transformation first.")
        
        # Load the output CSV
        output_data = load_csv(output_file)
        
        # Get actual headers
        actual_headers = output_data.columns.tolist()
        
        # Check for extra headers
        extra_headers = set(actual_headers) - set(expected_headers)
        assert not extra_headers, f"Unexpected headers: {extra_headers}"
    
    def test_content_specifications(self, expected_headers):
        """Test that the content meets the specifications."""
        # Define the paths to the transformed output
        output_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data/processed/transformed_output.csv')
        
        # Check if the output file exists
        if not os.path.exists(output_file):
            pytest.skip(f"Output file {output_file} does not exist. Run the transformation first.")
        
        # Load the output CSV
        output_data = load_csv(output_file)
        
        # Check required fields have values
        required_fields = [
            'teacher_id',
            'name',
            'created_at'
        ]
        
        for field in required_fields:
            if field in output_data.columns:
                assert not output_data[field].isna().any(), \
                    f"Required field '{field}' has missing values"
        
        # Check teacher_id format (should be a UUID)
        if 'teacher_id' in output_data.columns:
            # Sample check - ensures it's string-like and has correct format
            sample_id = output_data['teacher_id'].iloc[0] if len(output_data) > 0 else None
            if sample_id is not None and pd.notna(sample_id):
                # Simple UUID check: contains hyphens and is the right length
                assert isinstance(sample_id, str), "teacher_id should be a string"
                assert len(sample_id.split('-')) == 5, "teacher_id does not appear to be a valid UUID format"
        
        # Check date fields format
        date_fields = ['created_at', 'available_start_date']
        for field in date_fields:
            if field in output_data.columns and not output_data[field].isna().all():
                # For created_at, check it's in ISO format
                if field == 'created_at':
                    # Take first non-null value
                    first_date = output_data[field].dropna().iloc[0] if len(output_data[field].dropna()) > 0 else None
                    if first_date is not None:
                        assert 'T' in str(first_date), f"'{field}' does not appear to be in ISO format"
        
        # Check percentage fields are in valid range
        percentage_fields = ['profile_completion_percentage']
        for field in percentage_fields:
            if field in output_data.columns and not output_data[field].isna().all():
                non_null_values = output_data[field].dropna()
                if len(non_null_values) > 0:
                    assert non_null_values.min() >= 0 and non_null_values.max() <= 100, \
                        f"'{field}' contains values outside the valid percentage range (0-100)"
        
        # Check URL fields have valid format
        url_fields = ['cv_resume_url', 'video_intro_url', 'linkedin_profile_url']
        for field in url_fields:
            if field in output_data.columns:
                # Check any non-null values start with http:// or https://
                non_null_urls = output_data[field].dropna()
                for url in non_null_urls:
                    if isinstance(url, str) and url.strip():
                        assert url.startswith(('http://', 'https://')), \
                            f"URL in '{field}' does not start with http:// or https://: {url}"
        
        # Check email format
        if 'Email' in output_data.columns:
            non_null_emails = output_data['Email'].dropna()
            for email in non_null_emails:
                if isinstance(email, str) and email.strip():
                    assert '@' in email, f"Invalid email format: {email}"
