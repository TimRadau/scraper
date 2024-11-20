import requests
from bs4 import BeautifulSoup
import random
import json
query = input("Suche: ")

userAgents=['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.361675787110',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5412.99 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5361.172 Safari/537.36',
'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5388.177 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5397.215 Safari/537.36']



siteindex = 1
headers={'User-Agent': random.choice(userAgents)}

query = query.replace(" ", "-")

URL = f"https://www.ebay-kleinanzeigen.de/seite:{siteindex}/s-{query}/k0"
print(URL)
resp = requests.get(URL,headers=headers)
soup = BeautifulSoup(resp.text,"html.parser")


elements = soup.find_all("div", class_="aditem-main")
items = []

for element in elements:
    element_soup = BeautifulSoup(str(element), "html.parser")

    # Name finden
    name = element_soup.find('a', class_="ellipsis")
    name_text = name.text.strip() if name else "Kein Name gefunden"

    # Preis finden
    price = element_soup.find('p', class_='aditem-main--middle--price-shipping--price')
    price_text = price.text.strip() if price else "Kein Preis gefunden"

    # Link finden
    link = "https://www.kleinanzeigen.de" + name.get("href") if name else "Kein Link gefunden"

    # Daten in das Dictionary einfügen
    items.append({
        "name": name_text,
        "price": price_text,
        "link": link
    })
print(json.dumps(items, indent=2, ensure_ascii=False))



