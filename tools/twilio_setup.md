# Twilio Setup — SMS Outreach Tool

Twilio lets you send text messages programmatically. Claude can send texts on your behalf once this is set up.

---

## Step 1: Create a Twilio Account

1. Go to [twilio.com](https://www.twilio.com) and sign up (free trial gives you $15 credit)
2. Verify your phone number
3. Get a Twilio phone number (free in trial, ~$1/mo after)

---

## Step 2: Get Your Credentials

In the Twilio Console:
- **Account SID** — looks like `ACxxxxxxxxxxxxxxx`
- **Auth Token** — looks like a long random string
- **Your Twilio Phone Number** — e.g., `+14405551234`

Store these in a `.env` file (NEVER commit this to git):
```
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=+1XXXXXXXXXX
```

---

## Step 3: Install Twilio Python Library

```bash
pip install twilio python-dotenv
```

---

## Step 4: Send a Text (Python Script)

The file `scripts/send_text.py` is ready to use. Run it like this:

```bash
python scripts/send_text.py --to "+14405559876" --message "Hi, this is [Your Name]..."
```

---

## Costs (After Free Trial)
- SMS in US: ~$0.0079/message (~$8 per 1,000 texts)
- Phone number: ~$1.15/month
- Very cheap for cold outreach

---

## Important — SMS Compliance (A2P 10DLC)
- You must register your business with Twilio for A2P 10DLC compliance
- For local/small outreach (under 200 texts/day), the free trial and unregistered number works fine to start
- Register at: Twilio Console → Messaging → Regulatory Compliance

---

## Alternative: Text Manually First
If you don't want to set up Twilio yet, just copy the templates from `outreach/text_templates.md` and send manually from your phone. Claude can draft the messages for you.
