#!/usr/bin/env python3
"""
Test script to verify the updated email content for Cognizant Pre-Placement Talk
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_email_template():
    """Test the email template with new event details"""
    
    # Sample data
    name = "John Smith"
    prn_number = "PRN001"
    event_name = os.getenv('EVENT_NAME', 'Cognizant Pre-Placement Talk - Batch 2026')
    event_date = os.getenv('EVENT_DATE', '18th September 2025')
    event_location = os.getenv('EVENT_LOCATION', 'Main Auditorium')
    
    # Email body template (same as in app.py)
    body = f"""
Dear {name},

Welcome to {event_name}!

Your unique QR code is attached to this email. Please follow these instructions carefully:

🎫 QR CODE INSTRUCTIONS:
1. Save the QR code image to your phone
2. Present the QR code at the event entrance for scanning
3. Each QR code can only be used ONCE - please do not share it
4. Keep your phone charged and QR code easily accessible

📅 EVENT DETAILS:
- Event: {event_name}
- Date: {event_date}
- Location: {event_location}
- Your PRN: {prn_number}

👔 DRESS CODE - MANDATORY:
- Formals with blazers are COMPULSORY
- Professional business attire required
- No casual wear will be permitted

🆔 ENTRY REQUIREMENTS:
- College ID card is MANDATORY for entry
- QR code must be presented along with ID card
- Both documents will be verified at the entrance

⏰ IMPORTANT GUIDELINES:
- Arrive 15 minutes before the event starts
- Entry may be denied without proper dress code
- Keep your QR code and ID card ready for quick verification
- Late arrivals may not be permitted entry
- Contact support if you have any issues

This is a professional corporate event. Please ensure you follow all guidelines for a smooth entry process.

We look forward to seeing you at the event!

Best regards,
Event Management Team
    """
    
    print("=" * 80)
    print("EMAIL CONTENT PREVIEW")
    print("=" * 80)
    print(body)
    print("=" * 80)
    
    # Verify key elements are present
    required_elements = [
        "Cognizant Pre-Placement Talk - Batch 2026",
        "18th September 2025",
        "Formals with blazers are COMPULSORY",
        "College ID card is MANDATORY",
        "professional corporate event"
    ]
    
    print("\nVERIFICATION CHECKLIST:")
    print("-" * 40)
    
    all_present = True
    for element in required_elements:
        if element in body:
            print(f"✓ {element}")
        else:
            print(f"✗ {element}")
            all_present = False
    
    print("-" * 40)
    if all_present:
        print("🎉 All required elements are present in the email!")
        return True
    else:
        print("❌ Some required elements are missing!")
        return False

if __name__ == '__main__':
    success = test_email_template()
    if success:
        print("\n✅ Email template test PASSED")
    else:
        print("\n❌ Email template test FAILED")
