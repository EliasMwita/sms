import sys
sys.path.append('/Users/home/Desktop/Shared/project/message/sms/beem_sms_package')
from beem_sms.sms_sender import BeemSMSSender
from decouple import config

def test_send_to_specific_number():
    # Load credentials from .env
    access_key = config('BEEM_ACCESS_KEY')
    secret_key = config('BEEM_SECRET_KEY')
    
    sender = BeemSMSSender(access_key=access_key, secret_key=secret_key)
    recipient = "+255759870734"
    message = "Test message from Django Beem SMS package"
    result = sender.send_sms(recipient, message, sender_id="BEEM")  # Test with "BEEM"
    
    print("Sending SMS to", recipient)
    print("Result:", result)
    if result["status"] == "success":
        print("Message sent successfully! Check the phone to confirm receipt.")
    else:
        print("Failed to send message. Error:", result["message"])
        if "response" in result:
            print("Raw response:", result["response"])

if __name__ == "__main__":
    test_send_to_specific_number()