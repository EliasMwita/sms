import os
import requests
import random
import string
from django.conf import settings

class BeemSMSSender:
    def __init__(self, access_key=None, secret_key=None):
        self.access_key = access_key or getattr(settings, 'BEEM_ACCESS_KEY', '')
        self.secret_key = secret_key or getattr(settings, 'BEEM_SECRET_KEY', '')
        if not self.access_key or not self.secret_key:
            raise ValueError("Beem API credentials (access_key and secret_key) are required")
        self.base_url = "https://apisms.beem.africa/v1/send"
        self.default_message = os.environ.get('MESSAGE', 'Default SMS Message')

    def generate_otp(self, length=6):
        """Generate a random OTP of specified length"""
        return ''.join(random.choices(string.digits, k=length))

    def _prepare_payload(self, recipient, message, sender_id="BEEM"):  # Default to "BEEM"
        """Prepare the SMS payload with recipients array"""
        return {
            "source_addr": sender_id,
            "recipients": [
                {
                    "recipient_id": "1",
                    "dest_addr": str(recipient).replace("+", "")
                }
            ],
            "message": message,
            "encoding": "0"
        }

    def send_sms(self, recipient, message, sender_id="BEEM"):
        """Send a single SMS message"""
        payload = self._prepare_payload(recipient, message, sender_id)
        print("Payload being sent:", payload)
        
        try:
            response = requests.post(
                self.base_url,
                json=payload,
                auth=(self.access_key, self.secret_key),
                headers={'Content-Type': 'application/json'}
            )
            response.raise_for_status()
            return {"status": "success", "data": response.json()}
        except requests.exceptions.RequestException as e:
            error_result = {"status": "error", "message": str(e)}
            if hasattr(e.response, 'text'):
                error_result["response"] = e.response.text
            return error_result

    def send_otp(self, recipient, length=6, sender_id="BEEM"):
        """Send an OTP message"""
        otp = self.generate_otp(length)
        message = f"Your verification code is: {otp}"
        result = self.send_sms(recipient, message, sender_id)
        if result["status"] == "success":
            result["otp"] = otp
        return result

    def send_bulk_sms(self, recipients, message, sender_id="BEEM"):
        """Send SMS to multiple recipients"""
        results = []
        for i, recipient in enumerate(recipients, 1):
            payload = {
                "source_addr": sender_id,
                "recipients": [
                    {
                        "recipient_id": str(i),
                        "dest_addr": str(recipient).replace("+", "")
                    }
                ],
                "message": message,
                "encoding": "0"
            }
            try:
                response = requests.post(
                    self.base_url,
                    json=payload,
                    auth=(self.access_key, self.secret_key),
                    headers={'Content-Type': 'application/json'}
                )
                response.raise_for_status()
                results.append({"recipient": recipient, "status": "success", "data": response.json()})
            except requests.exceptions.RequestException as e:
                error_result = {"status": "error", "message": str(e)}
                if hasattr(e.response, 'text'):
                    error_result["response"] = e.response.text
                results.append({"recipient": recipient, **error_result})
        return results

    def send_two_way_sms(self, recipient, message, callback_url, sender_id="BEEM"):
        """Send two-way SMS with callback"""
        payload = self._prepare_payload(recipient, message, sender_id)
        payload["callback_url"] = callback_url
        
        try:
            response = requests.post(
                self.base_url,
                json=payload,
                auth=(self.access_key, self.secret_key),
                headers={'Content-Type': 'application/json'}
            )
            response.raise_for_status()
            return {"status": "success", "data": response.json()}
        except requests.exceptions.RequestException as e:
            error_result = {"status": "error", "message": str(e)}
            if hasattr(e.response, 'text'):
                error_result["response"] = e.response.text
            return error_result