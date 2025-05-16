# Content Format Requirements

This document outlines the required format for each column in the output CSV file.

## Required Fields

### teacher_id
- Format: UUID (e.g., "32267688-c85d-4eac-9556-34d0b3746807")
- Required: Yes
- Description: Unique identifier for each teacher

### name
- Format: Full name (First + Last)
- Required: Yes
- Description: Full name of the teacher

### subject
- Format: Single subject or comma-separated list
- Required: Yes
- Description: Subject(s) taught by the teacher
- Example: "Mathematics" or "Mathematics, Physics"

### headline
- Format: Text string
- Required: Yes
- Description: Brief description of the teacher's role/position
- Example: "Math Teacher"

### bio
- Format: Text string
- Required: Yes
- Description: Brief biography of the teacher
- Example: "Experienced mathematics educator with 10 years of teaching experience"

### years_of_teaching_experience
- Format: Single number
- Required: Yes
- Description: Total years of teaching experience
- Example: "10"
- Note: Should not be a range (e.g., "5-10")

### preferred_curriculum_experience
- Format: Text string
- Required: Yes
- Description: Preferred curriculum or teaching style
- Example: "British Curriculum", "IB Curriculum"

### current_location_country
- Format: Full country name
- Required: Yes
- Description: Current country of residence
- Example: "United Arab Emirates"

### current_location_city
- Format: Full city name
- Required: Yes
- Description: Current city of residence
- Example: "Dubai"

### linkedin_profile_url
- Format: Full URL
- Required: Yes
- Description: LinkedIn profile URL
- Example: "https://linkedin.com/in/johnsmith"

### preferred_grade_level
- Format: Text string
- Required: Yes
- Description: Preferred grade levels
- Example: "Elementary", "Secondary"

### subjects_count
- Format: Number
- Required: Yes
- Description: Number of subjects taught
- Example: "2"

### Nationality
- Format: Full country name
- Required: Yes
- Description: Teacher's nationality
- Example: "British"

### Current school
- Format: Text string
- Required: Yes - If available in source data
- Description: Current or most recent school
- Example: "GEMS Education"

### School website
- Format: Full URL
- Required: Yes - If available in source data
- Description: School's website URL
- Example: "https://gemseducation.com"

### Email
- Format: Email address
- Required: Yes - If available in source data
- Description: Teacher's email address
- Example: "john.smith@example.com"

### Source ID
- Format: Text/Number
- Required: Yes
- Description: Source identifier for the data

## Optional Fields (Can be empty)

### profile_completion_percentage
- Format: Number followed by "%"
- Required: No
- Description: Percentage of profile completion
- Example: "85%"

### profile_visibility
- Format: Text string
- Required: No
- Description: Profile visibility status
- Example: "Public", "Private"

### preferred_teaching_modes
- Format: Text string
- Required: No
- Description: Preferred teaching modes
- Example: "Online", "In-person"

### willing_to_relocate
- Format: Yes/No
- Required: No
- Description: Willingness to relocate
- Example: "Yes", "No"

### hourly_rate
- Format: Number with currency
- Required: No
- Description: Hourly rate
- Example: "100 AED"

### monthly_salary_expectation
- Format: Number with currency
- Required: No
- Description: Monthly salary expectation
- Example: "20000 AED"

### available_start_date
- Format: Date (YYYY-MM-DD)
- Required: No
- Description: Available start date
- Example: "2025-06-01"

### cv_resume_url
- Format: Full URL
- Required: No
- Description: URL to CV/Resume
- Example: "https://example.com/cv.pdf"

### video_intro_url
- Format: Full URL
- Required: No
- Description: URL to video introduction
- Example: "https://youtube.com/video/123"

### work_authorization_status
- Format: Text string
- Required: No
- Description: Work authorization status
- Example: "Valid", "Pending"

### background_check_status
- Format: Text string
- Required: No
- Description: Background check status
- Example: "Completed", "Pending"

## System Fields

### created_at
- Format: Timestamp
- Required: Yes
- Description: Record creation timestamp
- Example: "2025-05-16T14:10:41+04:00"

### Embeddings
- Format: Vector data
- Required: No 
- Description: AI-generated embeddings for the teacher profile.
