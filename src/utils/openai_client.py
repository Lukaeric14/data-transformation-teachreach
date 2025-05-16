"""
OpenAI API client for inferring fields in the teacher data transformation.
"""
import os
import json
import openai
from typing import List, Dict, Any, Optional


class OpenAIClient:
    """
    Client for inferring values using OpenAI's API.
    """
    
    def __init__(self, api_key=None):
        """
        Initialize the OpenAI client.
        
        Args:
            api_key (str, optional): OpenAI API key. If not provided, will attempt to use OPENAI_API_KEY environment variable.
        """
        if not api_key:
            api_key = os.environ.get("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("No OpenAI API key provided and OPENAI_API_KEY not found in environment. Please provide an API key.")
        
        # Store the API key
        self.api_key = api_key
        
        # Initialize OpenAI client with the API key
        self.client = openai.OpenAI(api_key=api_key)
            
    def infer_field(self, field_name: str, teacher_data: Dict[str, Any]) -> Any:
        """
        Infer a field value using OpenAI's API.
        
        Args:
            field_name (str): The name of the field to infer.
            teacher_data (dict): Data about the teacher to base the inference on.
            
        Returns:
            The inferred value for the specified field.
        """
        if not self.api_key:
            return self._get_fallback_value(field_name)
            
        try:
            # Prepare a prompt based on the field we want to infer
            prompt = self._create_prompt(field_name, teacher_data)
            
            # Call the OpenAI API
            client = openai.OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model="gpt-4.1-nano",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant for inferring information about teachers based on their profile data. Respond only with the requested information, no explanations."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=150
            )
            
            # Extract and parse the result
            result = response.choices[0].message.content.strip()
            return self._parse_result(field_name, result)
            
        except Exception as e:
            print(f"Error inferring {field_name} using OpenAI API: {e}")
            return self._get_fallback_value(field_name)
    
    def infer_multiple_fields(self, field_names: List[str], teacher_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Infer multiple field values in a single API call for efficiency.
        
        Args:
            field_names (list): List of field names to infer.
            teacher_data (dict): Data about the teacher to base the inference on.
            
        Returns:
            dict: A dictionary mapping field names to their inferred values.
        """
        if not self.api_key:
            return {field: self._get_fallback_value(field) for field in field_names}
            
        try:
            # Prepare a prompt for all fields
            prompt = self._create_multi_field_prompt(field_names, teacher_data)
            
            # Call the OpenAI API
            client = openai.OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model="gpt-4.1-nano",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant for inferring information about teachers based on their profile data. Respond in JSON format with the requested fields."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=300,
                response_format={"type": "json_object"}
            )
            
            # Extract and parse the JSON result
            result = response.choices[0].message.content.strip()
            result_dict = json.loads(result)
            
            # Make sure all requested fields are present
            for field in field_names:
                if field not in result_dict:
                    result_dict[field] = self._get_fallback_value(field)
                    
            return result_dict
            
        except Exception as e:
            print(f"Error inferring multiple fields using OpenAI API: {e}")
            return {field: self._get_fallback_value(field) for field in field_names}
    
    def _create_prompt(self, field_name: str, teacher_data: Dict[str, Any]) -> str:
        """
        Create a prompt for inferring a specific field.
        
        Args:
            field_name (str): The name of the field to infer.
            teacher_data (dict): Data about the teacher.
            
        Returns:
            str: The prompt to send to the OpenAI API.
        """
        # Create a summary of the teacher data to include in the prompt
        data_summary = self._summarize_teacher_data(teacher_data)
        
        # Field-specific prompts
        prompts = {
            "Years of experience (P)": f"Based on the following teacher profile, infer their years of teaching experience as a simple number:\n\n{data_summary}\n\nYears of experience:",
            
            "Subject (Array) (c)": f"Based on the following teacher profile, what subjects do they most likely teach? Provide up to 3 subjects, comma-separated:\n\n{data_summary}\n\nSubjects:",
            
            "Preferred curriculumn (O)": f"Based on the following teacher profile, infer their preferred teaching curriculum. Choose one from: IB, British, American, SABIS, or Other.\n\n{data_summary}\n\nPreferred curriculum:",
            
            "Nationality (Z)": f"Based on the following teacher profile, infer their nationality (provide just the nationality, e.g., 'British', 'American', etc.):\n\n{data_summary}\n\nNationality:"
        }
        
        # Return the appropriate prompt or a generic one if the field is not recognized
        return prompts.get(
            field_name,
            f"Based on the following teacher profile, infer the {field_name}:\n\n{data_summary}\n\n{field_name}:"
        )
    
    def _create_multi_field_prompt(self, field_names: List[str], teacher_data: Dict[str, Any]) -> str:
        """
        Create a prompt for inferring multiple fields at once.
        
        Args:
            field_names (list): The names of the fields to infer.
            teacher_data (dict): Data about the teacher.
            
        Returns:
            str: The prompt to send to the OpenAI API.
        """
        data_summary = self._summarize_teacher_data(teacher_data)
        
        # Comprehensive field descriptions with strict formatting and content rules
        field_instructions_map = {
            'name': "Full name (e.g., 'Jane Doe'), trying to extract from text. Should not be 'Unknown Teacher'. Minimum two words.",
            'subject': "Primary subject(s) taught by the teacher (e.g., 'Mathematics', 'Physics', 'English, History'). List up to 3 if applicable, comma-separated. ABSOLUTELY CRITICAL: The subject must NOT be 'General Education'. If 'General Education' seems applicable, pick a more specific core subject like 'Elementary Education' or 'Primary Subjects' or if possible, infer a specific subject like 'Mathematics' or 'English' based on other context.",
            'headline': "A concise, professional headline for the teacher (2-7 words, e.g., 'Experienced IB Chemistry Educator'). Not just 'Teacher'.",
            'bio': """A professional summary of the teacher's experience (target 70-150 words).

**CRITICAL PRIVACY REQUIREMENTS (MANDATORY)**:
1. ABSOLUTELY DO NOT include any proper nouns, names of people, institutions, schools, organizations, or locations.
2. ALL NAMES MUST BE REMOVED - no specific teacher names, supervisor names, institution names, or organization names.
3. Use only general terms like 'educational institution', 'learning center', or 'academic organization'.
4. Focus exclusively on skills, teaching philosophies, curriculum types, and pedagogical approaches.
5. ZERO IDENTIFYING INFORMATION - no cities, regions, specific years, certifications with provider names, or specific courses.

Format as a general professional summary with ABSOLUTELY NO identifying specifics. 
For example: "Experienced educator specializing in mathematics with over 10 years in international curricula including IB and American frameworks. Focused on student-centered learning with strong assessment skills."

VIOLATION OF THESE REQUIREMENTS IS UNACCEPTABLE.""",
            'preferred_curriculum_experience': "Comma-separated list of preferred curricula. Valid options ONLY: British, American, IB, Indian, CBSE, ICSE, UAE. If 'Indian', specify 'CBSE' or 'ICSE' if context allows, otherwise 'Indian' is fine. (e.g., 'British, IB'). If no specific curriculum is mentioned or inferable from the text, try to select a common one from these valid options (e.g., 'American', 'British', 'IB') if any general educational context is available. If truly no curriculum can be determined, respond with 'Not Specified'.",
            'years_of_teaching_experience': "Total number of years of teaching experience as an integer (e.g., 7 or 12).",
            'current_location_country': "Current country of residence (e.g., 'United Arab Emirates', 'India'). Do not use 'Unknown'. If not clearly stated or inferable, use 'Not Specified'.",
            'current_location_city': "Current city of residence (e.g., 'Dubai', 'Mumbai'). Do not use 'Unknown'. If not clearly stated or inferable, use 'Not Specified'.",
            'linkedin_profile_url': "LinkedIn profile URL (e.g., 'https://linkedin.com/in/username'). Prefer a URL directly from the data. If none is present, create a reasonable URL based on the name. ONLY return the URL itself, do not include explanatory text or formatting. e.g., 'https://linkedin.com/in/jane-doe' not 'LinkedIn: https://linkedin.com/in/jane-doe'.",
            'preferred_grade_level': """Comma-separated list of preferred grade levels or ranges. Choose ONLY from these EXACT options: 
American/IB/UAE-like: KG, Kindergarten, Elementary, Middle School, High School, Grade 1, Grade 2, Grade 3, Grade 4, Grade 5, Grade 6, Grade 7, Grade 8, Grade 9, Grade 10, Grade 11, Grade 12. 
Ranges like: KG - Grade 5, Grade 1-5, Grade 6-10, Grade 11-12, Grade 6-9, Grade 10-12, Grade 1-6, Grade 1-4, Grade 1-3, Grade 1-2, Grade 2-5, Grade 3-5. 
British-like: FS1, FS2, Year 1, Year 2, Year 3, Year 4, Year 5, Year 6, Year 7, Year 8, Year 9, Year 10, Year 11, Year 12, Year 13. 
Ranges like: Year 1-2, Year 3-6, Year 7-9, Year 10-11, Year 12-13, Year 1-4, Year 4-6. 
Indian-like: Pre-Primary, Primary, Middle, Secondary, Senior Secondary. 

IMPORTANT: This is a required field - NEVER leave it empty. If no specific grade level is mentioned or inferable, choose 'Elementary' or 'Primary' as a safe default.""",
            'Nationality': "The teacher's nationality as a common demonym (e.g., 'Irish', 'British', 'Indian'). MUST PROVIDE A VALUE - this is a required field. If the nationality isn't explicitly stated, make your best inference based on name, location, language, or other context clues. If truly unable to determine, use 'International' or a general regional term like 'European', 'Middle Eastern', 'Asian', etc. DO NOT leave this blank or use 'Unknown'. Format as a single word or short phrase only.",
            'Current school': "The current educational institution where the teacher works. DO NOT INCLUDE if not explicitly stated in source data - leave blank rather than inventing.",
            'School website': "URL of the school website. DO NOT INCLUDE if not explicitly stated in source data - leave blank rather than inventing.",
            'Email': "Teacher's email address. DO NOT INCLUDE if not explicitly stated in source data - leave blank rather than inventing.",
            'Source ID': "This field should not be inferred by AI. It is mapped directly from input data ID."
        }

        fields_to_request = []
        field_specific_instructions_text = ""
        for field_name in field_names:
            # Skip Source ID from AI inference as it's directly mapped
            if field_name == 'Source ID':
                continue
            instruction = field_instructions_map.get(field_name, f"Infer a suitable value for '{field_name}'.")
            fields_to_request.append(f"'{field_name}'")
            field_specific_instructions_text += f"\n- For '{field_name}': {instruction}"

        if not fields_to_request:
            # This case should ideally not happen if field_names are passed correctly
            return "No valid fields requested for AI inference."

        requested_fields_str = ", ".join(fields_to_request)

        prompt = f"""You are an expert data enrichment AI. Based on the following teacher profile, infer the values for these specific fields: {requested_fields_str}.

Teacher information summary:
{data_summary}

Strictly follow these instructions for EACH field:
{field_specific_instructions_text}

Provide your response as a single, valid JSON object containing only the requested fields as keys and their inferred values. Ensure the JSON is well-formed.
Example for different fields: {{"name": "Jane Doe", "Nationality": "British", "years_of_teaching_experience": 5, "preferred_grade_level": "Elementary, Middle School"}}
"""
        return prompt
    
    def _summarize_teacher_data(self, teacher_data: Dict[str, Any]) -> str:
        """
        Create a summary of the teacher data to use in prompts.
        
        Args:
            teacher_data (dict): Data about the teacher.
            
        Returns:
            str: A summary of the teacher data.
        """
        # Extract key information from the teacher data
        summary_lines = []
        
        # Add name if available
        if 'first_name' in teacher_data and 'last_name' in teacher_data:
            name = f"{teacher_data.get('first_name', '')} {teacher_data.get('last_name', '')}".strip()
            if name:
                summary_lines.append(f"Name: {name}")
        
        # Add headline if available
        if 'headline' in teacher_data and teacher_data['headline']:
            summary_lines.append(f"Headline: {teacher_data['headline']}")
        
        # Add location if available
        location = []
        if 'city' in teacher_data and teacher_data['city']:
            location.append(teacher_data['city'])
        if 'country' in teacher_data and teacher_data['country']:
            location.append(teacher_data['country'])
        if location:
            summary_lines.append(f"Location: {', '.join(location)}")
        
        # Add organization if available
        if 'organization_name' in teacher_data and teacher_data['organization_name']:
            summary_lines.append(f"Current School/Organization: {teacher_data['organization_name']}")
        
        # Add employment history
        employment_history = []
        for key in teacher_data:
            if 'employment_history' in key and '/title' in key and teacher_data[key]:
                # Extract index and corresponding date info
                parts = key.split('/')
                if len(parts) >= 3:
                    index = parts[1]
                    start_date_key = f"employment_history/{index}/start_date"
                    org_name_key = f"employment_history/{index}/organization_name"
                    
                    title = teacher_data[key]
                    start_date = teacher_data.get(start_date_key, '')
                    org_name = teacher_data.get(org_name_key, '')
                    
                    job_entry = f"{title}"
                    if org_name:
                        job_entry += f" at {org_name}"
                    if start_date:
                        job_entry += f" (from {start_date})"
                    
                    employment_history.append(job_entry)
        
        if employment_history:
            summary_lines.append("Employment History:")
            for job in employment_history[:5]:  # Limit to 5 entries
                summary_lines.append(f"- {job}")
            if len(employment_history) > 5:
                summary_lines.append(f"- ... and {len(employment_history) - 5} more positions")
        
        # Add any other relevant fields
        for key, value in teacher_data.items():
            if (key in ['departments/0', 'functions/0'] and value and 
                not any(key in line for line in summary_lines)):
                summary_lines.append(f"{key.split('/')[0].title()}: {value}")
        
        return "\n".join(summary_lines)
    
    def _parse_result(self, field_name: str, result: str) -> Any:
        """
        Parse the result from OpenAI API based on the field type.
        
        Args:
            field_name (str): The name of the field.
            result (str): The result from the OpenAI API.
            
        Returns:
            The parsed result.
        """
        if not result:
            return self._get_fallback_value(field_name)
            
        # Field-specific parsing
        if field_name == "Years of experience (P)":
            # Extract a number from the result
            import re
            numbers = re.findall(r'\d+', result)
            if numbers:
                try:
                    return int(numbers[0])
                except ValueError:
                    pass
            return 5  # Fallback
            
        elif field_name == "Subject (Array) (c)":
            # Parse comma-separated subjects
            subjects = [s.strip() for s in result.split(',')]
            return subjects
            
        # For other fields, return as is
        return result
    
    def _get_fallback_value(self, field_name: str) -> Any:
        """
        Get a fallback value for a field if the API call fails.
        
        Args:
            field_name (str): The name of the field.
            
        Returns:
            A fallback value appropriate for the field.
        """
        fallbacks = {
            "Years of experience (P)": 5,
            "Subject (Array) (c)": ["General Education"],
            "Preferred curriculumn (O)": "British",
            "Nationality (Z)": "International"
        }
        
        return fallbacks.get(field_name, "Unknown")
