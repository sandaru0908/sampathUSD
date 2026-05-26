from playwright.sync_api import sync_playwright
import json
import requests

URL = "https://www.sampath.lk/api/exchange-rates"
GOOGLE_SHEET_URL = "https://script.google.com/macros/s/AKfycbyNSUJgXxvXRmn9fbr641poBZGS6jr3u4HWd9SXf1QQLb2wmTfGaI0uOAgvZUvvSYk/exec"


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(URL, wait_until="networkidle")

    data = json.loads(page.text_content("body"))
    browser.close()

    for item in data["data"]:
        if item["CurrCode"] == "USD":
            value = item["TTBUY"]
            print("USD TTBUY:", value)

            requests.get(GOOGLE_SHEET_URL, params={"value": value})
            break
