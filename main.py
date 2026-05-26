from playwright.sync_api import sync_playwright
import requests

URL = "https://www.sampath.lk/api/exchange-rates"
SHEET = "https://script.google.com/macros/s/AKfycbyNSUJgXxvXRmn9fbr641poBZGS6jr3u4HWd9SXf1QQLb2wmTfGaI0uOAgvZUvvSYk/exec"


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    response = page.goto(URL, wait_until="domcontentloaded")
    data = response.json()

    browser.close()

    for item in data["data"]:
        if item["CurrCode"] == "USD":
            value = item["TTBUY"]
            print("USD:", value)

            requests.get(SHEET, params={"value": value})
            break
