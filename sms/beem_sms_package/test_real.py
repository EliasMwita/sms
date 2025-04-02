from beem_sms.sms_sender import BeemSMSSender

def test_real_sms():
    # Use your real Beem Africa credentials
    sender = BeemSMSSender(
        access_key="your_real_access_key",
        secret_key="your_real_secret_key"
    )
    
    # Test single SMS
    result = sender.send_sms("255123456789", "Test message from Beem SMS")
    print("Single SMS result:", result)
    
    # Test OTP
    result = sender.send_otp("255123456789")
    print("OTP result:", result)
    
    # Test bulk SMS
    result = sender.send_bulk_sms(
        ["255123456789", "255987654321"],
        "Bulk test message"
    )
    print("Bulk SMS result:", result)
    
    # Test two-way SMS
    result = sender.send_two_way_sms(
        "255123456789",
        "Please reply to this message",
        "https://your-callback-url.com"
    )
    print("Two-way SMS result:", result)

if __name__ == "__main__":
    test_real_sms()