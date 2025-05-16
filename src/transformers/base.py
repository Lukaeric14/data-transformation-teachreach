"""
Base transformer class for data transformation operations.
"""
import pandas as pd
from abc import ABC, abstractmethod


class BaseTransformer(ABC):
    """
    Abstract base class for data transformers.
    All specific transformers should inherit from this class.
    """

    def __init__(self, mapping=None, api_key=None):
        """
        Initialize the transformer with a mapping dictionary and API key.
        
        Args:
            mapping (dict, optional): A dictionary mapping input fields to output fields
            api_key (str, optional): API key for services like OpenAI
        """
        self.mapping = mapping or {}
        self.api_key = api_key
        
    @abstractmethod
    def transform(self, data):
        """
        Transform the input data according to the mapping.
        
        Args:
            data: The input data to transform.
            
        Returns:
            The transformed data.
        """
        pass

    def validate_input(self, data):
        """
        Validate the input data.
        
        Args:
            data: The input data to validate.
            
        Returns:
            bool: True if valid, False otherwise.
        """
        return True
    
    def validate_output(self, transformed_data):
        """
        Validate the output data.
        
        Args:
            transformed_data: The transformed data to validate.
            
        Returns:
            bool: True if valid, False otherwise.
        """
        return True
