from django.test import TestCase
from .sms_sender import BeemSMSSender
import os
from unittest.mock import patch, Mock
import json

class BeemSMSTestCase(TestCase):
    def setUp(self):
        # Set environment variables
        os.environ['MESSAGE'] = 'Test Env Message'
        # Initialize sender with test credentials
        self.sender = BeemSMSSender(access_key="test_key", secret_key="test_secret")
        
        # Sample successful response
        self.success_response = {
            "message": "Message sent successfully",
            "code": 100,
            "request_id": "test_request_id"
        }

    def test_default_message(self):
        """Test default message from environment"""
        self.assertEqual(self.sender.default_message, 'Test Env Message')

    def test_generate_otp(self):
        """Test OTP generation"""
        otp = self.sender.generate_otp(6)
        self.assertEqual(len(otp), 6)
        self.assertTrue(otp.isdigit())

    @patch('requests.post')
    def test_send_sms_success(self, mock_post):
        """Test successful single SMS sending"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.success_response
        mock_post.return_value = mock_response

        result = self.sender.send_sms("255123456789", "Test message")
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["data"], self.success_response)
        
        # Verify payload
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertEqual(kwargs['auth'], ("test_key", "test_secret"))
        self.assertEqual(json.loads(kwargs['data'])['dest_addr'], "255123456789")

    @patch('requests.post')
    def test_send_otp(self, mock_post):
        """Test OTP sending"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.success_response
        mock_post.return_value = mock_response

        result = self.sender.send_otp("255123456789")
        self.assertEqual(result["status"], "success")
        self.assertTrue(len(result["otp"]) == 6)
        self.assertTrue(result["otp"].isdigit())

    @patch('requests.post')
    def test_send_bulk_sms(self, mock_post):
        """Test bulk SMS sending"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.success_response
        mock_post.return_value = mock_response

        recipients = ["255123456789", "255987654321"]
        results = self.sender.send_bulk_sms(recipients, "Bulk test")
        
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["status"], "success")
        self.assertEqual(mock_post.call_count, 2)

    @patch('requests.post')
    def test_send_two_way_sms(self, mock_post):
        """Test two-way SMS sending"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.success_response
        mock_post.return_value = mock_response

        callback_url = "https://test.com/callback"
        result = self.sender.send_two_way_sms("255123456789", "Two-way test", callback_url)
        
        self.assertEqual(result["status"], "success")
        args, kwargs = mock_post.call_args
        payload = json.loads(kwargs['data'])
        self.assertEqual(payload["callback_url"], callback_url)

    @patch('requests.post')
    def test_send_sms_failure(self, mock_post):
        """Test SMS sending failure handling"""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.raise_for_status.side_effect = Exception("Bad request")
        mock_post.return_value = mock_response

        result = self.sender.send_sms("255123456789", "Test message")
        self.assertEqual(result["status"], "error")
        self.assertIn("message", result)
