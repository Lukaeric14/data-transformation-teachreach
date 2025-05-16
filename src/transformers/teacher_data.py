"""
Teacher data transformer for TeachReach.
"""
import uuid
import pandas as pd
import numpy as np
from datetime import datetime
from src.transformers.base import BaseTransformer
from src.utils.openai_client import OpenAIClient


class TeacherDataTransformer(BaseTransformer):
    """
    Transformer for teacher data.
    """

    def __init__(self, mapping=None, api_key=None):
        """
        Initialize the teacher data transformer.
        
        Args:
            mapping (dict, optional): A dictionary mapping input fields to output fields.
            api_key (str, optional): OpenAI API key for field inference.
        """
        super().__init__(mapping, api_key)
        
        # Default required output columns
        self.required_output_columns = [
            'teacher_id', 'name', 'subject', 'headline',
            'current_location_country', 'current_location_city',
            'bio', 'preferred_curriculum_experience', 'years_of_teaching_experience', 'linkedin_profile_url'
        ]
        
        # Initialize OpenAI client for AI field inference
        self.openai_client = OpenAIClient(api_key=self.api_key)
        
    def transform(self, data):
        """
        Transform teacher data according to the mapping.
        
        Args:
            data (pandas.DataFrame): The input data to transform.
            
        Returns:
            pandas.DataFrame: The transformed data.
        """
        # Validate input
        if not self.validate_input(data):
            raise ValueError("Invalid input data")
            
        # Create empty output DataFrame with required columns
        output_data = pd.DataFrame(columns=self.get_output_columns())
        
        # Process each input record
        for _, row in data.iterrows():
            transformed_row = self._transform_row(row)
            output_data = pd.concat([output_data, pd.DataFrame([transformed_row])], ignore_index=True)
            
        # Validate output
        if not self.validate_output(output_data):
            raise ValueError("Invalid output data")
            
        return output_data
        
    def _transform_row(self, row):
        """
        Transform a single row of data.
        
        Args:
            row (pandas.Series): The input row to transform.
            
        Returns:
            dict: The transformed row.
        """
        transformed = {}
        
        # Generate a unique ID for the teacher if not present
        transformed['teacher_id'] = str(uuid.uuid4())
        
        # Track AI fields to infer
        ai_fields = []
        
        # Apply each mapping
        for input_field, output_field in self.mapping.items():
            if input_field in row:
                transformed[output_field] = row[input_field]
            elif '+' in input_field:
                # Handle combined fields (e.g., "First (FP) + Last (FV)")
                input_parts = [part.strip() for part in input_field.split('+')]
                combined_value = ' '.join([str(row.get(part, '')) for part in input_parts if row.get(part)])
                transformed[output_field] = combined_value if combined_value else None
            elif input_field.lower() == 'ai':
                # Collect AI-inferred fields to process in batch
                ai_fields.append(output_field)
        
        # Process AI fields in a single API call for efficiency
        if ai_fields:
            # Convert row to dict for OpenAI client
            teacher_data = row.to_dict()
            
            # Get inferred values for all AI fields at once
            inferred_values = self.openai_client.infer_multiple_fields(ai_fields, teacher_data)
            
            # Apply inferred values
            for field, value in inferred_values.items():
                transformed[field] = value
                
        # Fill in default values for missing required fields
        for col in self.required_output_columns:
            if col not in transformed or pd.isna(transformed[col]) or transformed[col] == '':
                transformed[col] = self._get_default_value(col)
                
        # Add timestamp
        transformed['created_at'] = datetime.now().isoformat()
        
        return transformed
        
    def _get_default_value(self, column_name):
        """
        Get a default value for a missing column.
        
        Args:
            column_name (str): The name of the column.
            
        Returns:
            The default value for the column.
        """
        defaults = {
            'teacher_id': lambda: str(uuid.uuid4()),
            'name': lambda: 'Unknown Teacher',
            'subject': lambda: 'General Education',
            'headline': lambda: 'Teacher',
            'current_location_country': lambda: 'Unknown',
            'current_location_city': lambda: 'Unknown',
            'bio': lambda: 'No biography provided',
            'preferred_curriculum_experience': lambda: 'Not specified',
            'years_of_teaching_experience': lambda: '0',
            'linkedin_profile_url': lambda: 'Not provided'
        }
        
        return defaults.get(column_name, lambda: None)()
    
    def get_output_columns(self):
        """
        Get the list of output columns.
        
        Returns:
            list: List of output column names.
        """
        # Convert mapping values to a set of output columns
        output_columns = set(self.mapping.values())
        
        # Add required columns
        for col in self.required_output_columns:
            output_columns.add(col)
            
        # Add additional columns
        output_columns.add('created_at')
        
        return list(output_columns)
        
    def validate_input(self, data):
        """
        Validate the input data.
        
        Args:
            data (pandas.DataFrame): The input data to validate.
            
        Returns:
            bool: True if valid, False otherwise.
        """
        # Check if data is a DataFrame
        if not isinstance(data, pd.DataFrame):
            return False
            
        # Check if data has any rows
        if len(data) == 0:
            return False
            
        return True
        
    def validate_output(self, transformed_data):
        """
        Validate the output data.
        
        Args:
            transformed_data (pandas.DataFrame): The transformed data to validate.
            
        Returns:
            bool: True if valid, False otherwise.
        """
        # Check if transformed_data is a DataFrame
        if not isinstance(transformed_data, pd.DataFrame):
            return False
            
        # Check if transformed_data has any rows
        if len(transformed_data) == 0:
            return False
            
        # Check if all required columns are present
        for col in self.required_output_columns:
            if col not in transformed_data.columns:
                return False
                
        return True
