"""
bulk_outreach.py — Send personalized outreach texts to a list of leads
Usage: python bulk_outreach.py --csv leads/contacts.csv --template text

Requires:
  pip install twilio python-dotenv pandas
  .env file with Twilio credentials (see tools/twilio_setup.md)
  leads/contacts.csv with columns: name, business, phone, email, web_status
"""

import argparse
import os
import time
import pandas as pd
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
FROM_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

# Template messages — personalized with {name} and {business}
TEMPLATES = {
    "cold": (
        "Hi {name}, I'm a local web designer in Oberlin. I noticed {business} "
        "doesn't have a website yet. I build simple sites starting at $299 that "
        "help customers find you on Google. Want me to send a free mockup? No commitment."
    ),
    "followup": (
        "Hey {name}, just following up about a website for {business}. "
        "Happy to do a free sample so you can see what it'd look like before deciding anything."
    ),
    "facebook": (
        "Hey {name}! {business} has a great Facebook page — a website gives you "
        "something permanent + helps Google find you. Sites start at $299. Want to see an example?"
    ),
}


def send_bulk_texts(csv_path: str, template_key: str, delay_seconds: int = 10) -> None:
    if template_key not in TEMPLATES:
        raise ValueError(f"Template '{template_key}' not found. Choose from: {list(TEMPLATES.keys())}")

    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    df = pd.read_csv(csv_path)

    required_cols = {"name", "business", "phone"}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"CSV must have columns: {required_cols}")

    sent = 0
    failed = 0

    for _, row in df.iterrows():
        phone = str(row["phone"]).strip()
        if not phone.startswith("+"):
            phone = "+1" + phone.replace("-", "").replace("(", "").replace(")", "").replace(" ", "")

        message = TEMPLATES[template_key].format(
            name=row.get("name", "there"),
            business=row["business"],
        )

        try:
            msg = client.messages.create(body=message, from_=FROM_NUMBER, to=phone)
            print(f"[OK] Sent to {row['business']} ({phone}) | SID: {msg.sid}")
            sent += 1
            time.sleep(delay_seconds)  # Rate limiting — be respectful
        except Exception as e:
            print(f"[FAIL] {row['business']} ({phone}): {e}")
            failed += 1

    print(f"\nDone. Sent: {sent} | Failed: {failed}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send bulk personalized SMS outreach")
    parser.add_argument("--csv", required=True, help="Path to leads CSV file")
    parser.add_argument(
        "--template",
        default="cold",
        choices=list(TEMPLATES.keys()),
        help="Message template to use",
    )
    parser.add_argument(
        "--delay",
        type=int,
        default=10,
        help="Seconds to wait between messages (default: 10)",
    )
    args = parser.parse_args()

    bulk_send_texts(args.csv, args.template, args.delay)
