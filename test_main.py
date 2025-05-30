import unittest
from unittest.mock import patch, MagicMock, call
import json
import os
import sys
from io import StringIO
from main import send_message_to_grok, stream_output
import requests

class TestGrokChat(unittest.TestCase):
    def setUp(self):
        """Set up test environment variables and common test data"""
        os.environ['XAI_API_KEY'] = 'test_api_key'
        self.conversation_history = [{
            "role": "system",
            "content": "You are a genius AI assistant with PhDs in Mathematics and Computer Science."
        }]
        self.test_message = "What is Python?"

    def test_send_message_to_grok_success(self):
        """Test successful API call to Grok"""
        mock_response = {
            "choices": [{
                "message": {
                    "content": "Python is a high-level programming language.",
                    "role": "assistant"
                }
            }]
        }

        with patch('requests.post') as mock_post:
            # Configure the mock
            mock_post.return_value.json.return_value = mock_response
            mock_post.return_value.raise_for_status = MagicMock()

            # Call the function
            response = send_message_to_grok(self.test_message, self.conversation_history)

            # Verify the response
            self.assertEqual(response, mock_response)
            
            # Verify the API was called with correct parameters
            mock_post.assert_called_once()
            call_kwargs = mock_post.call_args.kwargs
            
            # Check headers
            self.assertEqual(call_kwargs['headers']['Authorization'], 'Bearer test_api_key')
            self.assertEqual(call_kwargs['headers']['Content-Type'], 'application/json')
            
            # Check payload
            payload = call_kwargs['json']
            self.assertEqual(payload['model'], 'grok-3-latest')
            self.assertEqual(payload['search_parameters']['mode'], 'auto')
            self.assertTrue(any(msg['content'] == self.test_message for msg in payload['messages']))

    def test_send_message_to_grok_api_error(self):
        """Test API error handling"""
        with patch('requests.post') as mock_post:
            # Configure the mock to raise a RequestException
            mock_post.side_effect = requests.exceptions.RequestException("API Error")
            
            # Capture stdout to check error message
            captured_output = StringIO()
            sys.stdout = captured_output
            
            try:
                # Call the function
                response = send_message_to_grok(self.test_message, self.conversation_history)
                
                # Verify the response is None when there's an error
                self.assertIsNone(response)
                
                # Verify error message was printed
                self.assertIn("Error: API Error", captured_output.getvalue())
            finally:
                sys.stdout = sys.__stdout__

    def test_send_message_to_grok_missing_api_key(self):
        """Test behavior when API key is missing"""
        # Remove API key from environment
        if 'XAI_API_KEY' in os.environ:
            del os.environ['XAI_API_KEY']

        with patch('requests.post') as mock_post:
            # Configure mock to return a 401 error
            mock_post.side_effect = requests.exceptions.RequestException("401 Client Error: Unauthorized")
            
            response = send_message_to_grok(self.test_message, self.conversation_history)
            self.assertIsNone(response)

    def test_stream_output(self):
        """Test the streaming output functionality"""
        test_message = "Hello, World!"
        expected_output = "\nGrok: Hello, World!\n"

        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            with patch('time.sleep') as mock_sleep:  # Mock sleep to speed up test
                stream_output(test_message)
                
                # Verify sleep was called for each character
                self.assertEqual(mock_sleep.call_count, len(test_message))
                
                # Verify each sleep call was with 0.02 seconds
                mock_sleep.assert_has_calls([call(0.02) for _ in test_message])
        finally:
            sys.stdout = sys.__stdout__  # Restore stdout

        # Verify the complete output
        self.assertEqual(captured_output.getvalue(), expected_output)

if __name__ == '__main__':
    unittest.main()
