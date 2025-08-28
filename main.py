from google_play_scraper import reviews_all, Sort
from datetime import datetime, timedelta
import pandas as pd
from twilio.rest import Client
import pytz

# ====== CONFIG ======
APP_ID = "in.gov.tnsedstudent.tnemis"
DAYS = 1  # last 24 hrs
TWILIO_SID = "YOUR_TWILIO_SID"
TWILIO_AUTH = "YOUR_TWILIO_AUTH"
TWILIO_NUMBER = "whatsapp:+14155238886"  # Twilio sandbox number
MY_NUMBER = "whatsapp:+91XXXXXXXXXX"     # your WhatsApp

# ====== FETCH REVIEWS ======
all_reviews = reviews_all(APP_ID, lang="en", country="in", sort=Sort.NEWEST)
df = pd.DataFrame(all_reviews)

# Keep only last 24 hours (IST)
ist = pytz.timezone("Asia/Kolkata")
df['at'] = pd.to_datetime(df['at']).dt.tz_convert(ist)
yesterday = datetime.now(ist) - timedelta(days=DAYS)
df = df[df['at'] >= yesterday]

# Keep only required columns
df = df[['at', 'userName', 'content']]

# ====== FORMAT MESSAGE ======
today_str = datetime.now(ist).strftime("%Y-%m-%d")
if df.empty:
    message_text = f"📢 No new reviews found on {today_str}."
else:
    lines = [f"📅 Reviews for {today_str}\nYou got {len(df)} new reviews:\n"]
    for i, row in enumerate(df.itertuples(), start=1):
        lines.append(
            f"{i}) Name: {row.userName}\n   Review: {row.content}\n"
        )
    message_text = "\n".join(lines)

# ====== SEND TO WHATSAPP ======
client = Client(TWILIO_SID, TWILIO_AUTH)
client.messages.create(
    from_=TWILIO_NUMBER,
    body=message_text,
    to=MY_NUMBER
)

print("✅ WhatsApp message sent!")
