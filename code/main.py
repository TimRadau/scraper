import requests
from bs4 import BeautifulSoup
import random
import json



userAgents=['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.361675787110',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5412.99 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5361.172 Safari/537.36',
'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5388.177 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5397.215 Safari/537.36']

headers={'User-Agent': random.choice(userAgents)}
query = input("Suche: ")
query = query.replace(" ", "-")

def check_site_availability(siteindex, query):
    
    URL = f"https://www.ebay-kleinanzeigen.de/seite:{siteindex}/s-{query}/k0"
    print(URL)


    resp = requests.get(URL,headers=headers)
    if not resp:
        return False
    else:
        return resp


def get_one_site(siteindex, query, headers):

    resp = check_site_availability(siteindex, query)
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
    return items

#print(json.dumps(items, indent=2, ensure_ascii=False))
siteindex = 1
item = get_one_site(siteindex, query, headers)
print(json.dumps(item, indent=2, ensure_ascii=False))

#pagination-not-linked pagination-page span für seitenanzahl
