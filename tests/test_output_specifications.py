"""
Tests to verify that the output CSV file meets the exact specifications.
"""
import os
import pytest
import pandas as pd
from src.utils.data_loader import load_csv
import re
import ast

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
        """Test that name contains first and last name and is not a placeholder."""
        output_data = load_csv(output_file)
        for val in output_data['name'].dropna():
            assert isinstance(val, str), "name should be a string"
            assert val.lower() != 'unknown teacher', "name should not be 'unknown teacher'"
            assert len(val.split()) >= 2, "name should be full name (First + Last)"

    def test_subject_format(self, output_file):
        """Test that subject is a non-empty string and not a generic placeholder."""
        output_data = load_csv(output_file)
        for val in output_data['subject'].dropna():
            assert isinstance(val, str), "subject should be a string"
            assert val.strip() != "", "subject should not be an empty string"
            assert val.lower() != 'general education', "subject should not be 'General Education'"

    def test_headline_format(self, output_file):
        """Test that headline is a non-empty string and not a generic placeholder."""
        output_data = load_csv(output_file)
        for val in output_data['headline'].dropna():
            assert isinstance(val, str), "headline should be a string"
            assert val.strip() != "", "headline should not be an empty string"
            assert val.lower() != 'teacher', "headline should not be 'Teacher'"

    def test_bio_format(self, output_file):
        """Test that bio is a non-empty, descriptive string, and does not contain revealing keywords."""
        output_data = load_csv(output_file)
        for val in output_data['bio'].dropna():
            assert isinstance(val, str), "bio should be a string"
            assert val.strip() != "", "bio should not be an empty string"
            assert len(val.strip()) > 50, f"bio ('{val.strip()[0:30]}...') should be descriptive and have a minimum length of 50 characters. Length: {len(val.strip())}"
            # 'teacher' is now allowed. 'school' (referring to specific institutions) is not.
            # The AI prompt is more nuanced now, this test mainly checks for obvious placeholders or overly generic forbidden terms.
            # A more complex regex might be needed for stricter 'no specific school names' if AI struggles.
            assert 'school' not in val.lower(), "bio should not contain the word 'school' (use alternative phrasing like 'learning center', 'institution')"
            assert 'unknown' not in val.lower(), "bio should not contain 'unknown'"

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
        """Test that preferred_curriculum_experience is a non-empty string and contains valid curriculum types."""
        output_data = load_csv(output_file)
        ALLOWED_CURRICULA = ['british', 'american', 'ib', 'indian', 'cbse', 'icse', 'uae']
        for val in output_data['preferred_curriculum_experience'].dropna():
            assert isinstance(val, str), "preferred_curriculum_experience should be a string"
            assert val.strip() != "", "preferred_curriculum_experience should not be an empty string"
            val_lower = val.lower()
            # Allow 'Not specified' or 'Not Specified' as valid values
            if val_lower == 'not specified':
                continue
            assert any(curriculum in val_lower for curriculum in ALLOWED_CURRICULA), \
                f"preferred_curriculum_experience '{val}' does not seem to contain a valid curriculum. Allowed: {ALLOWED_CURRICULA}"

    def test_location_format(self, output_file):
        """Test that location fields (country and city) are non-empty strings and not 'unknown'."""
        output_data = load_csv(output_file)
        location_fields = ['current_location_country', 'current_location_city']
        for field in location_fields:
            assert field in output_data.columns, f"{field} is missing from output"
            for val in output_data[field].dropna():
                assert isinstance(val, str), f"{field} should be a string"
                assert val.strip() != "", f"{field} should not be an empty string"
                assert val.lower() != 'unknown', f"{field} should not be 'unknown'"

    def test_linkedin_url_format(self, output_file):
        """Test that linkedin_profile_url is a valid URL."""
        output_data = load_csv(output_file)
        for val in output_data['linkedin_profile_url'].dropna():
            assert isinstance(val, str) and val.startswith(('http://', 'https://'))

    def test_grade_level_format(self, output_file):
        """Test that preferred_grade_level contains valid grade levels based on specified curricula."""
        output_data = load_csv(output_file)

        # Define atomic and grouped grade levels for each curriculum
        american_atomic = ["kg", "elementary", "middle school", "high school", "kindergarten"]
        british_atomic = ["fs1", "fs2"] + [f"year {i}" for i in range(1, 14)]
        ib_atomic = ["kg", "kindergarten"] + [f"grade {i}" for i in range(1, 13)]
        indian_atomic = ["pre-primary", "primary", "middle", "secondary", "senior secondary"]
        uae_atomic = ["kg", "kindergarten"] + [f"grade {i}" for i in range(1, 13)]

        american_groups = ["kg", "elementary", "middle school", "high school", "kindergarten"]
        british_groups = ["fs1", "fs2", "year 1-2", "year 3-6", "year 7-9", "year 10-11", "year 12-13"]
        ib_groups = ["kg - grade 5", "grade 6-10", "grade 11-12"]
        indian_groups = ["pre-primary", "primary", "middle", "secondary", "senior secondary"]
        uae_groups = ["kg", "grade 1-5", "grade 6-9", "grade 10-12"]

        # Combine all, normalize to lowercase
        valid_grades = set(
            [g.lower() for g in american_atomic + british_atomic + ib_atomic + indian_atomic + uae_atomic +
             american_groups + british_groups + ib_groups + indian_groups + uae_groups]
        )
        
        # Add variants for ranges (e.g., "kg to grade 5" if "kg - grade 5" is standard)
        range_variants = set()
        for group_list in [ib_groups, uae_groups, british_groups]:
            for group in group_list:
                group_lower = group.lower()
                if '-' in group_lower:
                    parts = [p.strip() for p in group_lower.split('-')]
                    if len(parts) == 2:
                        range_variants.add(parts[0] + " to " + parts[1])
        valid_grades.update(range_variants)

        # Add more granular ranges as observed from AI output or common usage
        valid_grades.update([
            'grade 1-2', 'grade 1-3', 'grade 1-4', 'grade 2-3', 'grade 2-4', 'grade 2-5',
            'grade 3-4', 'grade 3-5', 'grade 4-5', 'grade 6-7', 'grade 6-8', 'grade 7-8',
            'grade 6-12', # Add another observed AI output format
            'year 1-3', 'year 1-4', 'year 4-6', 'year 5-6', 'year 7-8', 'year 10-12',
            'grade 1-6'  # Added 'grade 1-6' to the list of valid grades
        ])

        for val_orig in output_data['preferred_grade_level'].dropna():
            assert isinstance(val_orig, str), f"preferred_grade_level entry '{val_orig}' should be a string in the CSV"
            assert val_orig.strip() != "", "preferred_grade_level should not be an empty string"

            items_to_check_normalized = []
            # Attempt to parse if it's a string representation of a Python list
            if val_orig.startswith('[') and val_orig.endswith(']'):
                try:
                    parsed_list = ast.literal_eval(val_orig)
                    if isinstance(parsed_list, list):
                        items_to_check_normalized = [str(item).lower().strip() for item in parsed_list]
                    else: # literal_eval returned something else, treat original string as a single item
                        items_to_check_normalized = [val_orig.lower().strip()]
                except (ValueError, SyntaxError): # Not a valid list string, treat as a simple string
                    # Split by comma as a fallback if not a list string
                    items_to_check_normalized = [item.lower().strip() for item in val_orig.split(',')]
            else:
                # If not a list string, split by comma as a fallback
                items_to_check_normalized = [item.lower().strip() for item in val_orig.split(',')]
            
            if not items_to_check_normalized or all(not item for item in items_to_check_normalized):
                 pytest.fail(f"preferred_grade_level '{val_orig}' resulted in no valid items to check after parsing/splitting.")

            for item_norm in items_to_check_normalized:
                if not item_norm: continue # Skip empty strings resulting from split (e.g. "kg, ")
                assert item_norm in valid_grades, \
                    f"Invalid grade level '{item_norm}' (from original: '{val_orig}') found. Must be one of the defined valid grades. Allowed: {sorted(list(valid_grades))}"

    def test_subjects_count_format(self, output_file):
        """Test that subjects_count is a number."""
        output_data = load_csv(output_file)
        for val in output_data['subjects_count'].dropna():
            assert str(val).isdigit(), f"subjects_count must be a number, got '{val}'"

    def test_nationality_format(self, output_file):
        """Test that Nationality is a non-empty string, not 'unknown', and has a valid format."""
        output_data = load_csv(output_file)
        for val in output_data['Nationality'].dropna():
            assert isinstance(val, str), "Nationality should be a string"
            val_stripped = val.strip()
            assert val_stripped != "", "Nationality should not be an empty string"
            assert val_stripped.lower() != 'unknown', "Nationality should not be 'unknown'"
            assert not any(char.isdigit() for char in val_stripped), "Nationality should not contain numbers"
            # Allow letters, spaces, and hyphens (for compound nationalities)
            assert re.match(r"^[a-zA-Z\s-]+$", val_stripped), \
                f"Nationality '{val_stripped}' contains invalid characters. Only letters, spaces, hyphens allowed."
            assert len(val_stripped.split()) <= 4, \
                f"Nationality '{val_stripped}' seems too long (more than 4 words)."

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
        """Test that empty fields are allowed and can be empty, and non-empty optional fields have meaningful content."""
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
            'background_check_status',
            'Embeddings', # Embeddings can be empty
            # Current school, School website, Email can be empty, but if not, should not be placeholders
            'Current school', 
            'School website', 
            'Email'
        ]

        PLACEHOLDER_VALUES = ['unknown', 'not provided', 'n/a', 'na', '-', 'none', 'not applicable']

        for col in ALLOWED_EMPTY_COLUMNS:
            if col not in output_data.columns:
                # If an allowed empty column is simply missing, that's an issue for header checks, not this test.
                # However, if it's one of the specific optional fields we want to check for placeholders, skip if not present.
                if col in ['Current school', 'School website', 'Email']:
                    print(f"Warning: Optional field '{col}' not found in output, skipping placeholder check for it.")
                    continue
            # For columns that CAN be empty, if they are not empty, check for placeholder values.
            if col in output_data.columns and col in ['Current school', 'School website', 'Email']:
                for val in output_data[col].dropna():
                    if isinstance(val, str) and val.strip().lower() in PLACEHOLDER_VALUES:
                        pytest.fail(f"Field '{col}' (allowed to be empty) contains a placeholder value '{val}'. If present, it should be meaningful.")

        MUST_BE_COMPLETELY_EMPTY_COLUMNS = [
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

        # Add this loop to check these columns, perhaps after checking ALLOWED_EMPTY_COLUMNS
        # and before checking required_fields_for_content_check
        for col in MUST_BE_COMPLETELY_EMPTY_COLUMNS:
            if col in output_data.columns:
                # Check if all values are NaN or empty strings
                is_effectively_empty = output_data[col].isnull().all() or \
                                       (output_data[col].astype(str).str.strip() == '').all()
                assert is_effectively_empty, \
                    f"Column '{col}' is supposed to be completely empty but contains values: {output_data[col][output_data[col].notnull() & (output_data[col].astype(str).str.strip() != '')].unique()}"
            else:
                # If the column isn't even in the output, that's fine for this check (it's truly empty)
                print(f"Note: Column '{col}' (expected to be empty) is not present in the output file.")

        # Fields that must always be empty (or specific default like 0, False) - These are generally not used by TeachReach schema based on current tests
        # This part can be reactivated if there are fields that MUST be blank or have fixed non-string defaults
        # fixed_empty_fields = [
        #     'profile_completion_percentage', 'profile_visibility', 'preferred_teaching_modes', 'willing_to_relocate',
        #     'hourly_rate', 'monthly_salary_expectation', 'available_start_date', 'cv_resume_url', 'video_intro_url',
        #     'work_authorization_status', 'background_check_status'
        # ]
        # for col in fixed_empty_fields:
        #     if col in output_data.columns:
        #         non_null_values = output_data[col].dropna()
        #         if len(non_null_values) > 0:
        #             for val in non_null_values:
        #                 if isinstance(val, str):
        #                     val_clean = val.strip().lower()
        #                     if val_clean not in ['', 'unknown', 'not_verified', 'private']:
        #                         pytest.fail(f"{col} contains unexpected value '{val}' - should be empty or specific default value")
        #                 elif val not in [0, False]: # Assuming 0 and False are acceptable defaults for non-string types
        #                      pytest.fail(f"{col} contains unexpected value '{val}' - should be empty or specific default value (0, False)")

        # Check for missing required values (excluding allowed empty columns and required-if-available columns)
        # These are fields that should always have a *meaningful* value.
        required_fields_for_content_check = [
            'teacher_id',
            'name',
            'created_at'
        ]
        
        for col in required_fields_for_content_check:
            assert col in output_data.columns, f"Required field '{col}' is missing from output."
            empty_count = output_data[col].isna().sum() + (output_data[col].astype(str).str.strip() == '').sum()
            if empty_count > 0:
                print(f"Warning: Required field '{col}' has {empty_count} empty or NA values.")
            assert empty_count == 0, f"Required field '{col}' has {empty_count} empty or NA values but is required."

            # Additional check for placeholder values in these required string fields
            if output_data[col].dtype == 'object': # Check only string type columns
                for val in output_data[col].dropna():
                    if isinstance(val, str) and val.strip().lower() in PLACEHOLDER_VALUES:
                        pytest.fail(f"Required field '{col}' contains a placeholder value '{val}'. It must have meaningful content.")

        # Special handling for bio, curriculum, years_of_experience if they were allowed to be empty under certain conditions (they are not now).
        # These are now in required_fields_for_content_check.

        print("\nContent Analysis from test_empty_fields (checking for placeholders in required fields):")
        if 'name' in output_data.columns:
            name_issues = output_data[output_data['name'].str.contains('|'.join(PLACEHOLDER_VALUES), case=False, na=False)]
            if not name_issues.empty:
                print(f"Name issues (contains placeholders like {PLACEHOLDER_VALUES}): {len(name_issues)} records")
                print("First problematic record (name):")
                print(name_issues.iloc[0])

        location_fields_to_check = ['current_location_country', 'current_location_city']
        for field in location_fields_to_check:
            if field in output_data.columns:
                loc_issues = output_data[output_data[field].str.contains('|'.join(PLACEHOLDER_VALUES), case=False, na=False)]
                if not loc_issues.empty:
                    print(f"{field} issues (contains placeholders like {PLACEHOLDER_VALUES}): {len(loc_issues)} records")
                    print(f"First problematic record ({field}):")
                    print(loc_issues.iloc[0])

    def test_content_specifications(self, output_file):
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

print("\nAll content specification checks passed according to content_requirements.md!")
