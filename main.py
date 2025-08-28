from google_play_scraper import reviews_all, Sort
from datetime import datetime, timedelta
import pandas as pd
from twilio.rest import Client
import pytz
import os

# ====== CONFIG ======
APP_ID = "in.gov.tnsedstudent.tnemis"
DAYS = 1  

TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH = os.getenv("TWILIO_AUTH")
TWILIO_NUMBER = os.getenv("TWILIO_NUMBER")
MY_NUMBER = os.getenv("MY_NUMBER")

# ====== FETCH REVIEWS ======
all_reviews = reviews_all(APP_ID, lang="en", country="in", sort=Sort.NEWEST)
df = pd.DataFrame(all_reviews)

# Keep only last 24 hours (IST)
ist = pytz.timezone("Asia/Kolkata")
df['at'] = pd.to_datetime(df['at']).dt.tz_convert(ist)
yesterday = datetime.now(ist) - timedelta(days=DAYS)
df = df[df['at'] >= yesterday]

# ====== FORMAT MESSAGE ======
today_str = datetime.now(ist).strftime("%Y-%m-%d")
if df.empty:
    message_text = f"📢 No new reviews found on {today_str}."
else:
    message_text = f"You got {len(df)} new reviews on {today_str}."

# ====== SEND TO WHATSAPP ======
if all([TWILIO_SID, TWILIO_AUTH, TWILIO_NUMBER, MY_NUMBER]):
    client = Client(TWILIO_SID, TWILIO_AUTH)
    client.messages.create(
        from_=TWILIO_NUMBER,
        body=message_text,
        to=MY_NUMBER
    )
    print("✅ WhatsApp message sent!")
else:
    print("⚠️ Missing environment variables. Please set TWILIO_SID, TWILIO_AUTH, TWILIO_NUMBER, MY_NUMBER.")
