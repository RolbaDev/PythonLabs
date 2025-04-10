import requests, sys
import random as rng
from wallet import Wallet



url = "https://api.nbp.pl/api/exchangerates/tables/A/?format=json"

response = requests.get(url)

if response.status_code == 200:
  resp = response.json()
else:
  print("Błąd:", response.status_code, response.text)
  sys.exit(0)

currency_map = {}
for currency in resp[0]["rates"]:
  currency_map[currency["code"]] = currency["mid"]

wallets = []

for key in currency_map.keys():
  wallets.append(Wallet(key, currency_map[key], rng.uniform(1, 100)))

print(wallets)

