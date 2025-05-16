"""
This module defines the standardized output format for the TeachReach data transformation.
It maps the existing field names to the desired output field names.
"""

# Define the exact output headers in the correct order
DESIRED_OUTPUT_HEADERS = [
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

# Map existing fields to desired output fields
# Format: 'current_field_name': 'desired_output_field_name'
FIELD_MAPPING = {
    # Existing fields that match desired fields
    'teacher_id': 'teacher_id',
    'created_at': 'created_at',
    'current_location_country': 'current_location_country',
    'current_location_city': 'current_location_city',
    'subject': 'subject',
    
    # AI-enriched fields - add direct mappings to preserve these
    'bio': 'bio',
    'preferred_curriculum_experience': 'preferred_curriculum_experience',
    'years_of_teaching_experience': 'years_of_teaching_experience',
    'linkedin_profile_url': 'linkedin_profile_url',
    'preferred_grade_level': 'preferred_grade_level',
    'Nationality': 'Nationality',
    'ID': 'Source ID',
    
    # Fields that need to be renamed
    'name': 'name',
    'Name (b)': 'name',  # Alternative source for name
    'headline': 'headline',
    'Headline (d)': 'headline',
    'Linkedin URL (u)': 'linkedin_profile_url',
    'Preferred age range (V)': 'preferred_grade_level',
    'Email (AC)': 'Email',
    'Source ID (AD)': 'Source ID',
    'School (AA)': 'Current school',
    'school website (AB)': 'School website',
    'country (R)': 'current_location_country',  # Alternative source
    'city (s)': 'current_location_city',  # Alternative source
    'ID (a)': 'teacher_id',  # Alternative source
}

# Fields with default values when missing
DEFAULT_VALUES = {
    'profile_completion_percentage': 0,
    'profile_visibility': 'private',
    'bio': 'No biography provided',  # Updated to provide a meaningful default
    'willing_to_relocate': False,
    'hourly_rate': 0,
    'monthly_salary_expectation': 0,
    'background_check_status': 'not_verified',
    'subjects_count': 1,
    'work_authorization_status': 'unknown',
    'preferred_curriculum_experience': 'Not specified',  # Added meaningful default
    'years_of_teaching_experience': '0',  # Added meaningful default
    'linkedin_profile_url': 'Not provided',  # Added meaningful default
    'preferred_grade_level': 'Elementary',  # Added meaningful default
    'Nationality': 'International',  # Added meaningful default
    'Source ID': 'Unknown',  # Added meaningful default
}

# Fields that should be inferred or calculated
CALCULATED_FIELDS = [
    'preferred_teaching_modes',
    'available_start_date',
    'cv_resume_url',
    'video_intro_url',
    'preferred_curriculum_experience',
    'years_of_teaching_experience',
    'Embeddings',
    'Nationality',
]
