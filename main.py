from playwright.sync_api import sync_playwright
import json
import os
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

URL = "https://www.sampath.lk/api/exchange-rates"
FILE = "rate.txt"


# ---------- GET USD RATE ----------
def get_usd_ttbuy():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120"
        )

        page = context.new_page()
        response = page.goto(URL)

        text = response.text()
        browser.close()

        data = json.loads(text)

        for item in data["data"]:
            if item["CurrCode"] == "USD":
                return float(item["TTBUY"])


# ---------- EMAIL ----------
def send_email(old, new):
    diff = new - old
    direction = "UP 📈" if diff > 0 else "DOWN 📉"

    oldFmt = f"{old:.2f}"
    newFmt = f"{new:.2f}"
    diffFmt = f"{abs(diff):.2f}"

    msg = MIMEText(
        "USD RATE ALERT (Sampath Bank)\n\n"
        "Previous Rate: " + oldFmt + " LKR\n"
        "Current Rate: " + newFmt + " LKR\n\n"
        "Change Amount: " + diffFmt + " LKR\n"
        "Status: " + direction + "\n\n"
        "Checked Time: " + str(datetime.now())
    )

    msg["Subject"] = f"USD Rate {direction}"
    msg["From"] = os.getenv("EMAIL_USER")
    msg["To"] = "sandaru0908@gmail.com"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASS"))
    server.send_message(msg)
    server.quit()


# ---------- LOAD PREVIOUS ----------
def load_old():
    if not os.path.exists(FILE):
        return None
    return float(open(FILE).read().strip())


# ---------- SAVE NEW ----------
def save_new(value):
    with open(FILE, "w") as f:
        f.write(str(value))


# ---------- MAIN ----------
new_rate = get_usd_ttbuy()
old_rate = load_old()

print("OLD:", old_rate)
print("NEW:", new_rate)

if old_rate is not None and old_rate != new_rate:
    send_email(old_rate, new_rate)

save_new(new_rate)
