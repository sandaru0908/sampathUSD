import requests

value = 123  # your calculated value

url = "https://script.google.com/macros/s/AKfycbyNSUJgXxvXRmn9fbr641poBZGS6jr3u4HWd9SXf1QQLb2wmTfGaI0uOAgvZUvvSYk/exec"

params = {
    "value": value
}

response = requests.get(url, params=params)

print(response.text)
