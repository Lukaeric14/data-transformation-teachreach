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
    # Fields that are typically numbers or specific strings
    'teacher_id': '',  # Should be generated
    'name': '', # AI will fill, default to empty if fails
    'subject': '', # AI will fill, default to empty if fails
    'headline': '', # AI will fill, default to empty if fails
    'bio': '', # AI will fill, default to empty if fails
    'profile_completion_percentage': None, # Must be empty
    'profile_visibility': None,          # Must be empty
    'preferred_teaching_modes': None,    # Must be empty
    'willing_to_relocate': None,         # Must be empty
    'hourly_rate': None,                 # Must be empty
    'monthly_salary_expectation': None,  # Must be empty
    'available_start_date': None,        # Must be empty
    'cv_resume_url': None,               # Must be empty
    'video_intro_url': None,             # Must be empty
    'preferred_curriculum_experience': '', # AI will fill, default to empty if fails
    'years_of_teaching_experience': '0', # AI will fill, default to '0'
    'work_authorization_status': None,   # Must be empty
    'current_location_country': '', # AI will fill, default to empty if fails
    'current_location_city': '',    # AI will fill, default to empty if fails
    'background_check_status': None,     # Must be empty
    'linkedin_profile_url': '',  # AI will fill, default to empty if 'Not provided' is not desired
    'preferred_grade_level': '', # AI will fill, default to empty if fails
    'subjects_count': 0, # Default to 0, can be updated by AI/logic
    'created_at': '', # Should be generated
    'Embeddings': '', # Can be empty
    'Nationality': '', # AI will fill, default to empty if fails
    'Current school': '', # Optional, can be empty. If AI adds, it should be meaningful.
    'School website': '', # Optional, can be empty.
    'Email': '',           # Optional, can be empty.
    'Source ID': '' # Mapped directly from 'ID', default to empty if 'ID' is missing
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
