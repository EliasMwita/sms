from beem_sms.sms_sender import BeemSMSSender
import os

def test_send_to_specific_number():
    # Set your real Beem Africa credentials (preferably via environment variables)
    access_key = os.environ.get('BEEM_ACCESS_KEY', 'your_real_access_key')
    secret_key = os.environ.get('BEEM_SECRET_KEY', 'your_real_secret_key')
    
    # Initialize the sender
    sender = BeemSMSSender(access_key=access_key, secret_key=secret_key)
    
    # Format the number in international format (Tanzania)
    recipient = "+255753107784"  # Converted from 0753107784
    
    # Send the test message
    message = "Test message from Django Beem SMS package"
    result = sender.send_sms(recipient, message)
    
    # Print the result
    print("Sending SMS to", recipient)
    print("Result:", result)
    
    # Check if the message was sent successfully
    if result["status"] == "success":
        print("Message sent successfully! Check the phone to confirm receipt.")
    else:
        print("Failed to send message. Error:", result["message"])

if __name__ == "__main__":
    test_send_to_specific_number()