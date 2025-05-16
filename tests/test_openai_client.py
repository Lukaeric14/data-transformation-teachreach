"""
Tests for the OpenAI client.
"""
import pytest
from unittest.mock import patch, MagicMock
from src.utils.openai_client import OpenAIClient


class TestOpenAIClient:
    """
    Test cases for the OpenAIClient.
    """

    @pytest.fixture
    def sample_teacher_data(self):
        """Fixture to provide sample teacher data."""
        return {
            'first_name': 'John',
            'last_name': 'Doe',
            'headline': 'Math Teacher',
            'country': 'United Arab Emirates',
            'city': 'Dubai',
            'email': 'john.doe@example.com',
            'linkedin_url': 'http://linkedin.com/in/johndoe',
            'organization_name': 'GEMS Education',
            'organization_website': 'gemseducation.com'
        }

    def test_initialization(self):
        """Test initialization of client."""
        # Initialize with no API key
        client = OpenAIClient()
        assert client.api_key is None
        
        # Initialize with API key
        client = OpenAIClient("test_api_key")
        assert client.api_key == "test_api_key"

    def test_summarize_teacher_data(self, sample_teacher_data):
        """Test summarizing teacher data for prompts."""
        client = OpenAIClient("test_api_key")
        summary = client._summarize_teacher_data(sample_teacher_data)
        
        # Check if summary contains key information
        assert "John Doe" in summary
        assert "Math Teacher" in summary
        assert "Dubai" in summary
        assert "United Arab Emirates" in summary
        assert "GEMS Education" in summary

    def test_get_fallback_value(self):
        """Test getting fallback values for fields."""
        client = OpenAIClient()
        
        # Test fallback values for known fields
        assert client._get_fallback_value("Years of experience (P)") == 5
        assert client._get_fallback_value("Subject (Array) (c)") == ["General Education"]
        assert client._get_fallback_value("Preferred curriculumn (O)") == "British"
        assert client._get_fallback_value("Nationality (Z)") == "International"
        
        # Test fallback value for unknown field
        assert client._get_fallback_value("Unknown Field") == "Unknown"

    @patch('openai.OpenAI')
    def test_infer_field_with_api(self, mock_openai, sample_teacher_data):
        """Test inferring a field using the OpenAI API."""
        # Mock OpenAI API response
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "10"
        
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        
        mock_openai.return_value = mock_client
        
        # Test inference
        client = OpenAIClient("test_api_key")
        result = client.infer_field("Years of experience (P)", sample_teacher_data)
        
        # Verify API was called with appropriate parameters
        mock_client.chat.completions.create.assert_called_once()
        call_args = mock_client.chat.completions.create.call_args[1]
        
        assert call_args["model"] == "gpt-4.1-nano"
        assert len(call_args["messages"]) == 2
        assert call_args["messages"][0]["role"] == "system"
        assert call_args["messages"][1]["role"] == "user"
        assert "Years of experience" in call_args["messages"][1]["content"]
        
        # Verify result was parsed correctly
        assert result == 10

    @patch('openai.OpenAI')
    def test_infer_multiple_fields(self, mock_openai, sample_teacher_data):
        """Test inferring multiple fields in a single API call."""
        # Mock OpenAI API response
        mock_response = MagicMock()
        mock_response.choices[0].message.content = '''
        {
            "Years of experience (P)": 10,
            "Subject (Array) (c)": "Mathematics, Physics, Computer Science",
            "Preferred curriculumn (O)": "British",
            "Nationality (Z)": "British"
        }
        '''
        
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        
        mock_openai.return_value = mock_client
        
        # Test inference
        client = OpenAIClient("test_api_key")
        fields = [
            "Years of experience (P)",
            "Subject (Array) (c)",
            "Preferred curriculumn (O)",
            "Nationality (Z)"
        ]
        
        result = client.infer_multiple_fields(fields, sample_teacher_data)
        
        # Verify API was called once with appropriate parameters
        mock_client.chat.completions.create.assert_called_once()
        call_args = mock_client.chat.completions.create.call_args[1]
        
        assert call_args["model"] == "gpt-4.1-nano"
        assert call_args["response_format"] == {"type": "json_object"}
        
        # Verify results were parsed correctly
        assert "Years of experience (P)" in result
        assert "Subject (Array) (c)" in result
        assert "Preferred curriculumn (O)" in result
        assert "Nationality (Z)" in result

    def test_infer_field_no_api_key(self, sample_teacher_data):
        """Test inferring a field without an API key returns fallback values."""
        client = OpenAIClient()  # No API key
        
        # Infer a field
        result = client.infer_field("Years of experience (P)", sample_teacher_data)
        
        # Verify fallback value was returned
        assert result == 5

    def test_infer_multiple_fields_no_api_key(self, sample_teacher_data):
        """Test inferring multiple fields without an API key returns fallback values."""
        client = OpenAIClient()  # No API key
        
        fields = [
            "Years of experience (P)",
            "Subject (Array) (c)",
            "Preferred curriculumn (O)",
            "Nationality (Z)"
        ]
        
        # Infer multiple fields
        result = client.infer_multiple_fields(fields, sample_teacher_data)
        
        # Verify fallback values were returned
        assert result["Years of experience (P)"] == 5
        assert result["Subject (Array) (c)"] == ["General Education"]
        assert result["Preferred curriculumn (O)"] == "British"
        assert result["Nationality (Z)"] == "International"
