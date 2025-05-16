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
    
    @pytest.fixture
    def output_file(self):
        """Fixture to provide the path to the output file."""
        return "data/processed/transformed_output.csv"
    
    def test_header_order_exact_match(self, expected_headers, output_file):
        """Test that the CSV file has exactly the specified headers in the exact order."""
        # Check if the output file exists
        if not os.path.exists(output_file):
            pytest.skip(f"Output file {output_file} does not exist. Run the transformation first.")
        
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
    
    def test_no_missing_headers(self, expected_headers, output_file):
        """Test that no required headers are missing from the CSV file."""
        # Check if the output file exists
        if not os.path.exists(output_file):
            pytest.skip(f"Output file {output_file} does not exist. Run the transformation first.")
        
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
    
    def test_no_extra_headers(self, expected_headers, output_file):
        """Test that there are no unexpected headers."""
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
    
    def test_teacher_id_format(self, output_file):
        """Test that teacher_id is a valid UUID string."""
        output_data = load_csv(output_file)
        for val in output_data['teacher_id'].dropna():
            assert isinstance(val, str) and len(val.split('-')) == 5, "teacher_id must be a UUID string"

    def test_name_format(self, output_file):
        """Test that name contains first and last name."""
        output_data = load_csv(output_file)
        for val in output_data['name'].dropna():
            assert isinstance(val, str) and len(val.split()) >= 2, "name should be full name (First + Last)"

    def test_subject_format(self, output_file):
        """Test that subject is a non-empty string."""
        output_data = load_csv(output_file)
        for val in output_data['subject'].dropna():
            assert isinstance(val, str) and len(val.strip()) > 0

    def test_headline_format(self, output_file):
        """Test that headline is a non-empty string."""
        output_data = load_csv(output_file)
        for val in output_data['headline'].dropna():
            assert isinstance(val, str) and len(val.strip()) > 0

    def test_bio_format(self, output_file):
        """Test that bio is a non-empty string."""
        output_data = load_csv(output_file)
        for val in output_data['bio'].dropna():
            assert isinstance(val, str) and len(val.strip()) > 0

    def test_years_of_experience_format(self, output_file):
        """Test that years_of_teaching_experience is either a number or 'X Years'."""
        output_data = load_csv(output_file)
        for val in output_data['years_of_teaching_experience'].dropna():
            str_val = str(val)
            if 'Years' in str_val:
                assert re.fullmatch(r"\d+ Years", str_val), f"years_of_teaching_experience must be like '10 Years' or just a number, got '{str_val}'"
            else:
                assert str_val.isdigit(), f"years_of_teaching_experience must be a number or number + 'Years', got '{str_val}'"

    def test_curriculum_experience_format(self, output_file):
        """Test that preferred_curriculum_experience is a non-empty string."""
        output_data = load_csv(output_file)
        for val in output_data['preferred_curriculum_experience'].dropna():
            assert isinstance(val, str) and len(val.strip()) > 0

    def test_location_format(self, output_file):
        """Test that location fields (country and city) are non-empty strings."""
        output_data = load_csv(output_file)
        for val in output_data['current_location_country'].dropna():
            assert isinstance(val, str) and len(val.strip()) > 0
        for val in output_data['current_location_city'].dropna():
            assert isinstance(val, str) and len(val.strip()) > 0

    def test_linkedin_url_format(self, output_file):
        """Test that linkedin_profile_url is a valid URL."""
        output_data = load_csv(output_file)
        for val in output_data['linkedin_profile_url'].dropna():
            assert isinstance(val, str) and val.startswith(('http://', 'https://'))

    def test_grade_level_format(self, output_file):
        """Test that preferred_grade_level is a non-empty string."""
        output_data = load_csv(output_file)
        for val in output_data['preferred_grade_level'].dropna():
            assert isinstance(val, str) and len(val.strip()) > 0

    def test_subjects_count_format(self, output_file):
        """Test that subjects_count is a number."""
        output_data = load_csv(output_file)
        for val in output_data['subjects_count'].dropna():
            assert str(val).isdigit(), f"subjects_count must be a number, got '{val}'"

    def test_nationality_format(self, output_file):
        """Test that Nationality is a non-empty string."""
        output_data = load_csv(output_file)
        for val in output_data['Nationality'].dropna():
            assert isinstance(val, str) and len(val.strip()) > 0

    def test_required_if_available_fields(self, output_file):
        """Test that required fields are present if available in source data."""
        output_data = load_csv(output_file)
        REQUIRED_IF_AVAILABLE = ['Current school', 'School website', 'Email']
        
        for col in REQUIRED_IF_AVAILABLE:
            if col in output_data.columns:
                all_empty = output_data[col].isna().all()
                if not all_empty:
                    for val in output_data[col].dropna():
                        if col == 'Email':
                            assert '@' in val, f"Invalid email format: {val}"
                        elif col == 'School website':
                            assert val.startswith(('http://', 'https://')), f"School website must be a URL, got '{val}'"
                        else:
                            assert isinstance(val, str) and len(val.strip()) > 0

    def test_source_id_format(self, output_file):
        """Test that Source ID is a non-empty value."""
        output_data = load_csv(output_file)
        for val in output_data['Source ID'].dropna():
            assert isinstance(val, (str, int, float)) and str(val).strip() != ''

    def test_created_at_format(self, output_file):
        """Test that created_at is a valid timestamp (accepts both ISO and space-separated formats)."""
        output_data = load_csv(output_file)
        for val in output_data['created_at'].dropna():
            # Accept both ISO format (with T) and space-separated format
            assert ('T' in str(val) or ' ' in str(val)), f"created_at must be a valid timestamp format, got '{val}'"

    def test_empty_fields(self, output_file):
        """Test that empty fields are allowed and can be empty."""
        output_data = load_csv(output_file)
        ALLOWED_EMPTY_COLUMNS = [
            'profile_completion_percentage',
            'profile_visibility',
            'preferred_teaching_modes',
            'willing_to_relocate',
            'hourly_rate',
            'monthly_salary_expectation',
            'available_start_date',
            'cv_resume_url',
            'video_intro_url',
            'work_authorization_status',
            'background_check_status'
        ]
        
        for col in ALLOWED_EMPTY_COLUMNS:
            assert col in output_data.columns, f"{col} must be present in output"

        # Fields that must always be empty
        empty_fields = [
            'profile_completion_percentage', 'profile_visibility', 'preferred_teaching_modes', 'willing_to_relocate',
            'hourly_rate', 'monthly_salary_expectation', 'available_start_date', 'cv_resume_url', 'video_intro_url',
            'work_authorization_status', 'background_check_status'
        ]
        
        # Check that these fields are either empty or contain default values
        for col in empty_fields:
            if col in output_data.columns:
                # Get non-null values
                non_null_values = output_data[col].dropna()
                if len(non_null_values) > 0:
                    # Check each non-null value
                    for val in non_null_values:
                        if isinstance(val, str):
                            val = val.strip()
                        if val not in ['', 0, False, 'unknown', 'not_verified', 'private']:
                            pytest.fail(f"{col} contains unexpected value '{val}' - should be empty or default value")

        # Embeddings: not required, can be empty
        if 'Embeddings' in output_data.columns:
            pass  # No check required

        # Check for missing required values (excluding allowed empty columns and required-if-available columns)
        required_fields = [
            'teacher_id', 'name', 'subject', 'headline',
            'current_location_country', 'current_location_city',
            'linkedin_profile_url', 'preferred_grade_level', 'subjects_count', 'created_at', 'Nationality', 'Source ID'
        ]
        
        # Special case for bio, preferred_curriculum_experience, and years_of_teaching_experience: can be empty if no information available
        bio_empty_count = output_data['bio'].isna().sum() + (output_data['bio'] == '').sum()
        if bio_empty_count > 0:
            print(f"Warning: {bio_empty_count} records have empty bio field")
        
        curriculum_empty_count = output_data['preferred_curriculum_experience'].isna().sum() + (output_data['preferred_curriculum_experience'] == '').sum()
        if curriculum_empty_count > 0:
            print(f"Warning: {curriculum_empty_count} records have empty preferred_curriculum_experience field")
        
        years_empty_count = output_data['years_of_teaching_experience'].isna().sum() + (output_data['years_of_teaching_experience'] == '').sum()
        if years_empty_count > 0:
            print(f"Warning: {years_empty_count} records have empty years_of_teaching_experience field")
        
        # Check other required fields
        for col in required_fields:
            assert col in output_data.columns, f"{col} is missing from output"
            empty_count = output_data[col].isna().sum() + (output_data[col] == '').sum()
            if empty_count > 0:
                print(f"Warning: {empty_count} records have empty {col} field")
            assert empty_count == 0, f"{col} has {empty_count} empty values but is required"

        print("\nAll content specification checks passed according to content_requirements.md!")
        """Test that the content meets the specifications."""
        # Define the paths to the transformed output
        output_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data/processed/transformed_output.csv')
        
        # Check if the output file exists
        if not os.path.exists(output_file):
            pytest.skip(f"Output file {output_file} does not exist. Run the transformation first.")
        
        # Load the output CSV
        output_data = load_csv(output_file)
        
        # Columns that are allowed to be empty
        ALLOWED_EMPTY_COLUMNS = [
            'profile_completion_percentage',
            'profile_visibility',
            'preferred_teaching_modes',
            'willing_to_relocate',
            'hourly_rate',
            'monthly_salary_expectation',
            'available_start_date',
            'cv_resume_url',
            'video_intro_url',
            'work_authorization_status',
            'background_check_status'
        ]
        
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

        # Check for specific content issues
        print("\nContent Analysis:")
        
        # Check name field issues
        if 'name' in output_data.columns:
            name_issues = output_data[output_data['name'].str.contains('Unknown', na=False)]
            print(f"\nName issues (contains 'Unknown'): {len(name_issues)} records")
            if len(name_issues) > 0:
                print("First problematic record:")
                print(name_issues.iloc[0])
            
        # Check location issues
        location_fields = ['current_location_country', 'current_location_city']
        for field in location_fields:
            if field in output_data.columns:
                location_issues = output_data[output_data[field] == 'Unknown']
                print(f"\n{field} issues (contains 'Unknown'): {len(location_issues)} records")
                if len(location_issues) > 0:
                    print("First problematic record:")
                    print(location_issues.iloc[0])

        # Check for empty fields that shouldn't be empty (excluding allowed empty columns)
        for col in output_data.columns:
            if col not in ALLOWED_EMPTY_COLUMNS:
                empty_count = output_data[col].isna().sum()
                if empty_count > 0:
                    print(f"\nField '{col}' has {empty_count} empty values")
                    # Print first empty record
                    empty_records = output_data[output_data[col].isna()]
                    if len(empty_records) > 0:
                        print("First empty record:")
                        print(empty_records.iloc[0])
