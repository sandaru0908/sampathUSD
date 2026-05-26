from playwright.sync_api import sync_playwright
import json
import requests   # 👈 ONLY NEW ADDITION

URL = "https://www.sampath.lk/api/exchange-rates"

GOOGLE_SHEET_URL = "https://script.google.com/macros/s/AKfycbyNSUJgXxvXRmn9fbr641poBZGS6jr3u4HWd9SXf1QQLb2wmTfGaI0uOAgvZUvvSYk/exec"


def get_usd_ttbuy():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120"
        )

        page = context.new_page()
        response = page.goto(URL, wait_until="networkidle")

        text = response.text()
        browser.close()

        data = json.loads(text)

        for item in data["data"]:
            if item["CurrCode"] == "USD":
                return item["TTBUY"]


value = get_usd_ttbuy()

print(value)

# 👇 ONLY NEW PART (SEND TO SHEET)
if value:
    requests.get(GOOGLE_SHEET_URL, params={"value": value})
