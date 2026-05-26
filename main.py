import requests

# Google Apps Script Web App URL
GOOGLE_SHEET_URL = "https://script.google.com/macros/s/AKfycbyNSUJgXxvXRmn9fbr641poBZGS6jr3u4HWd9SXf1QQLb2wmTfGaI0uOAgvZUvvSYk/exec"


def get_usd_ttbuy():
    try:
        r = requests.get("https://www.sampath.lk/api/exchange-rates", timeout=10)
        r.raise_for_status()
        data = r.json()

        for item in data["data"]:
            if item["CurrCode"] == "USD":
                return item["TTBUY"]

    except Exception as e:
        print("Error fetching exchange rate:", e)

    return None


def send_to_sheet(value):
    try:
        response = requests.get(GOOGLE_SHEET_URL, params={"value": value}, timeout=10)
        print("Sheet response:", response.text)
    except Exception as e:
        print("Error sending to sheet:", e)


def main():
    ttbuy = get_usd_ttbuy()

    print("USD TTBUY:", ttbuy)

    if ttbuy:
        send_to_sheet(ttbuy)
    else:
        print("No value found")


if __name__ == "__main__":
    main()
