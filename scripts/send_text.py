"""
send_text.py — Send SMS via Twilio
Usage: python send_text.py --to "+14405559876" --message "Your message here"

Requires:
  pip install twilio python-dotenv
  .env file with TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER
"""

import argparse
import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
FROM_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")


def send_sms(to_number: str, message: str) -> None:
    if not all([ACCOUNT_SID, AUTH_TOKEN, FROM_NUMBER]):
        raise ValueError(
            "Missing Twilio credentials. Check your .env file.\n"
            "See tools/twilio_setup.md for instructions."
        )

    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    msg = client.messages.create(
        body=message,
        from_=FROM_NUMBER,
        to=to_number,
    )
    print(f"Message sent! SID: {msg.sid} | To: {to_number}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send an SMS via Twilio")
    parser.add_argument("--to", required=True, help="Recipient phone number (e.g. +14405551234)")
    parser.add_argument("--message", required=True, help="Text message body")
    args = parser.parse_args()

    send_sms(args.to, args.message)
