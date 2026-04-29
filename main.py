import requests
import csv
import os
from datetime import date, timedelta

yesterday = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
base_currency = "kzt"
symbols = ["usd", "eur", "try", "rub"]
filename = "rates.csv"

# Check if date already exists
if os.path.exists(filename):
    with open(filename, "r") as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            if row and row[0] == yesterday:
                print(f"{yesterday} already exists in CSV, skipping.")
                exit()

# Fetch rates
url = f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@{yesterday}/v1/currencies/{base_currency}.json"
response = requests.get(url)
data = response.json()
rates = data[base_currency]

# Write header if file doesn't exist, then append
file_exists = os.path.exists(filename)
with open(filename, "a", newline="") as f:
    writer = csv.writer(f)
    if not file_exists:
        writer.writerow(["date"] + symbols)
    writer.writerow([yesterday] + [rates[symbol] for symbol in symbols])

print(f"Done! {yesterday} added to {filename}")
